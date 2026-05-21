"""
run_gnfw_fits.py — gNFW backbone-family control fits, parallelized over galaxies

Fits the SPARC T=2-9 sample (102 galaxies) under a generalized NFW (gNFW)
backbone instead of Burkert. Produces a CSV with the same columnar shape as
relaxed/run_relaxed_caps_fits.py and data/einasto_full_sample_results.csv so
that backbone-family comparisons can be performed in §3.3.6.

gNFW profile (Wyithe, Turner & Spergel 2001; Zhao 1996):
    rho(r) = rho_s / [ (r/r_s)^gamma * (1 + r/r_s)^(3 - gamma) ]

Three backbone parameters: rho_s, r_s, gamma. For gamma = 1 this reduces to
the standard NFW profile already in the canonical fitter; gamma is bounded to
[0, 2] for numerical stability. Shells (Gaussian residuals) are identical to
the canonical pipeline; BIC selects between {0, 1, 2} shells under each
backbone.

The mass enclosed M(<r) has no simple closed form for general gamma, so it
is computed by cumulative trapezoidal integration on a fine grid then
interpolated to the requested radii (vectorized; ~500x faster than
per-radius scipy.integrate.quad).

Parallelism: galaxies are independent, so one galaxy per task via
multiprocessing.Pool.imap_unordered. Default n_workers = cpu_count() - 2.

Usage:
  Place this in scripts/ alongside run_canonical_fits.py with sibling dirs:
    - Rotmod_LTG/             (SPARC rotmod .dat files)
    - sparc_sample123.csv     (SPARC catalog)
  Then from the repo root:
    python3 scripts/run_gnfw_fits.py [--n-workers N] [--smoke]

Output:
    data/gnfw_full_sample_fits.csv     (102 rows; same schema shape as relaxed)
    data/run_gnfw_fits.log
"""

import argparse
import os
import sys
import time
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.integrate import cumulative_trapezoid
import multiprocessing as mp
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# Path resolution (matches shell_reality_nulls_parallel.py convention)
# ============================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)

_PACKAGE_ROTMOD = os.path.join(_REPO_ROOT, 'Rotmod_LTG')
_LOCAL_ROTMOD = os.path.join('.', 'Rotmod_LTG')
ROTMOD_DIR = '/Users/ronbibb/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/Rotmod_LTG'

_PACKAGE_SAMPLE = os.path.join(_REPO_ROOT, 'sparc_sample123.csv')
_LOCAL_SAMPLE = './data/sparc_sample123.csv'
SAMPLE_CSV = _PACKAGE_SAMPLE if os.path.exists(_PACKAGE_SAMPLE) else _LOCAL_SAMPLE

_PACKAGE_DATA = os.path.join(_REPO_ROOT, 'data')
OUT_DIR = _PACKAGE_DATA if os.path.isdir(_PACKAGE_DATA) else '.'
OUTPUT_CSV = os.path.join(OUT_DIR, 'gnfw_full_sample_fits.csv')
LOG_FILE = os.path.join(OUT_DIR, 'run_gnfw_fits.log')

# ============================================================
# Configuration  (matches canonical / relaxed conventions)
# ============================================================
G = 4.302e-6            # kpc * (km/s)^2 / M_sun
SIGMA_V_FLOOR = 1.0
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7

T_MIN = 2
T_MAX = 9

# Shell caps — match CANONICAL (not relaxed). gNFW comparison is on the
# canonical analysis convention so the §3.3.6 narrative reads cleanly.
SHELL_R_MAX_GRID = [3.0, 6.0, 12.0]
SHELL_WIDTH_MAX_FRAC = 0.4
SHELL_M_MAX = 5e10

TIME_BUDGET_PER_FIT = 90    # gNFW fits are slower than Burkert; give some room

# gNFW backbone bounds
GAMMA_MIN = 0.0
GAMMA_MAX = 2.0
RHO_S_MIN = 1e3
RHO_S_MAX = 1e10
R_S_MIN = 0.1
R_S_MAX = 500.0

# Mass-integral grid
N_GRID = 500


# ============================================================
# Physics
# ============================================================
def baryon_squared(vg, vd, vb):
    return (vg * np.abs(vg)
            + UPSILON_DISK * vd * np.abs(vd)
            + UPSILON_BULGE * vb * np.abs(vb))


def burkert_v2(r, rho_0, a):
    a = max(a, 1e-6)
    x = r / a
    M_enc = np.pi * rho_0 * a**3 * (
        np.log(1 + x**2) + 2 * np.log(1 + x) - 2 * np.arctan(x))
    return np.maximum(G * M_enc / np.maximum(r, 1e-6), 0)


def gnfw_v2(r, rho_s, r_s, gamma):
    """
    gNFW circular-velocity-squared via cumulative trapezoidal integration.
    Vectorized over r.

    For gamma in [0, 2], the integrand 4*pi*r^2 * rho(r) is integrable at
    r=0 (r^2/r^gamma = r^(2-gamma), integrable for gamma < 3). We set the
    integrand to zero at r=0 explicitly to avoid 0/0 warnings.
    """
    r_s = max(r_s, 1e-6)
    r_arr = np.asarray(r, dtype=float)
    r_max_eval = float(r_arr.max()) * 1.001 + 1e-3

    r_grid = np.linspace(0.0, r_max_eval, N_GRID)
    x = np.maximum(r_grid, 1e-12) / r_s
    # Integrand: 4*pi * r^2 * rho_s / [x^gamma * (1+x)^(3-gamma)]
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        integrand = (4.0 * np.pi * rho_s * r_grid**2
                     / (x**gamma * (1.0 + x)**(3.0 - gamma)))
    integrand[0] = 0.0    # finite limit at r=0 for gamma < 3
    integrand = np.where(np.isfinite(integrand), integrand, 0.0)

    M_cum = cumulative_trapezoid(integrand, r_grid, initial=0.0)
    M_at_r = np.interp(r_arr, r_grid, M_cum)

    return np.maximum(G * M_at_r / np.maximum(r_arr, 1e-6), 0)


def shell_v2(r, M_sh, r_sh, sigma_sh):
    sigma = max(sigma_sh, 1e-6)
    M_enc = 0.5 * M_sh * (1 + erf((r - r_sh) / (np.sqrt(2) * sigma)))
    return np.maximum(G * M_enc / np.maximum(r, 1e-6), 0)


# ============================================================
# Models (closures over V2_bar for curve_fit)
# ============================================================
def model_burkert(V2_bar):
    def vt(r, rho_0, a):
        return np.sqrt(np.maximum(V2_bar + burkert_v2(r, rho_0, a), 0))
    return vt


def model_gnfw(V2_bar):
    def vt(r, rho_s, r_s, gamma):
        return np.sqrt(np.maximum(V2_bar + gnfw_v2(r, rho_s, r_s, gamma), 0))
    return vt


def model_gnfw_fw1(V2_bar):
    def vt(r, rho_s, r_s, gamma, M_sh, r_sh, sigma_frac):
        sigma_sh = sigma_frac * r_sh
        v2 = (V2_bar + gnfw_v2(r, rho_s, r_s, gamma)
              + shell_v2(r, M_sh, r_sh, sigma_sh))
        return np.sqrt(np.maximum(v2, 0))
    return vt


def model_gnfw_fw2(V2_bar):
    def vt(r, rho_s, r_s, gamma, M1, r1, sf1, M2, r2, sf2):
        s1 = sf1 * r1; s2 = sf2 * r2
        v2 = (V2_bar + gnfw_v2(r, rho_s, r_s, gamma)
              + shell_v2(r, M1, r1, s1) + shell_v2(r, M2, r2, s2))
        return np.sqrt(np.maximum(v2, 0))
    return vt


# ============================================================
# Fitters
# ============================================================
def fit_burkert(r, vobs, sig, V2_bar, time_budget=TIME_BUDGET_PER_FIT):
    vt = model_burkert(V2_bar)
    starts = [[3e7, 8.0], [1e7, 15.0], [1e8, 4.0], [3e6, 30.0], [3e8, 2.0],
              [1e6, 50.0], [5e7, 6.0], [1e9, 1.5]]
    bounds = ([1e3, 0.1], [1e10, 200.0])
    best_chi2 = np.inf; best_p = None
    t0 = time.time()
    for p0 in starts:
        try:
            p, _ = curve_fit(vt, r, vobs, p0=p0, bounds=bounds,
                             sigma=sig, maxfev=15000)
            chi2 = float(np.sum(((vobs - vt(r, *p)) / sig)**2))
            if chi2 < best_chi2:
                best_chi2 = chi2; best_p = p
        except Exception:
            continue
        if time.time() - t0 > time_budget:
            break
    return best_p, best_chi2


def fit_gnfw_n_shells(r, vobs, sig, V2_bar, n_shells,
                      time_budget=TIME_BUDGET_PER_FIT):
    """gNFW + n_shells in {0, 1, 2}. Returns (params, chi2)."""
    gamma_starts = [0.5, 1.0, 1.5]
    rho_s_starts = [1e7, 3e7, 1e8]
    r_s_starts = [10.0, 25.0, 60.0]

    if n_shells == 0:
        vt = model_gnfw(V2_bar)
        starts = [(rho, rs, g)
                  for g in gamma_starts
                  for rho in rho_s_starts
                  for rs in r_s_starts]
        lb = [RHO_S_MIN, R_S_MIN, GAMMA_MIN]
        ub = [RHO_S_MAX, R_S_MAX, GAMMA_MAX]
    elif n_shells == 1:
        vt = model_gnfw_fw1(V2_bar)
        starts = []
        for r_max in SHELL_R_MAX_GRID:
            for g in gamma_starts:
                for rho in [1e7, 3e7]:
                    for rs in [10.0, 25.0]:
                        for r_frac in [0.4, 0.7]:
                            r_sh_init = r_frac * r_max
                            M_init = 1e8 * (r_max / 6.0)
                            starts.append(
                                ([rho, rs, g, M_init, r_sh_init, 0.25], r_max))
    else:  # n_shells == 2
        vt = model_gnfw_fw2(V2_bar)
        starts = []
        for r_max in SHELL_R_MAX_GRID:
            for g in gamma_starts:
                for rho in [1e7, 3e7]:
                    for rs in [10.0, 25.0]:
                        r1_init = r_max / 3.0
                        r2_init = 2.0 * r_max / 3.0
                        M_init = 1e8 * (r_max / 6.0)
                        starts.append(
                            ([rho, rs, g,
                              M_init, r1_init, 0.25,
                              M_init, r2_init, 0.25], r_max))

    best_chi2 = np.inf
    best_p_physical = None
    t0 = time.time()

    if n_shells == 0:
        for p0 in starts:
            try:
                p, _ = curve_fit(vt, r, vobs, p0=list(p0), bounds=(lb, ub),
                                 sigma=sig, maxfev=15000)
                chi2 = float(np.sum(((vobs - vt(r, *p)) / sig)**2))
                if chi2 < best_chi2:
                    best_chi2 = chi2; best_p_physical = np.array(p)
            except Exception:
                continue
            if time.time() - t0 > time_budget:
                break
    else:
        for p0, r_max in starts:
            if n_shells == 1:
                lb = [RHO_S_MIN, R_S_MIN, GAMMA_MIN, 1e6, 0.2, 0.01]
                ub = [RHO_S_MAX, R_S_MAX, GAMMA_MAX,
                      SHELL_M_MAX, r_max, SHELL_WIDTH_MAX_FRAC]
            else:
                lb = [RHO_S_MIN, R_S_MIN, GAMMA_MIN,
                      1e6, 0.2, 0.01, 1e6, 0.2, 0.01]
                ub = [RHO_S_MAX, R_S_MAX, GAMMA_MAX,
                      SHELL_M_MAX, r_max, SHELL_WIDTH_MAX_FRAC,
                      SHELL_M_MAX, r_max, SHELL_WIDTH_MAX_FRAC]
            try:
                p, _ = curve_fit(vt, r, vobs, p0=p0, bounds=(lb, ub),
                                 sigma=sig, maxfev=20000)
                chi2 = float(np.sum(((vobs - vt(r, *p)) / sig)**2))
                if chi2 < best_chi2:
                    best_chi2 = chi2
                    if n_shells == 1:
                        rho_s, r_s, gam, M1, r1, sf1 = p
                        best_p_physical = np.array(
                            [rho_s, r_s, gam, M1, r1, sf1 * r1])
                    else:
                        rho_s, r_s, gam, M1, r1, sf1, M2, r2, sf2 = p
                        best_p_physical = np.array(
                            [rho_s, r_s, gam,
                             M1, r1, sf1 * r1,
                             M2, r2, sf2 * r2])
            except Exception:
                continue
            if time.time() - t0 > time_budget:
                break

    return best_p_physical, best_chi2


# ============================================================
# BIC / chi2_red helpers
# ============================================================
def bic_of(chi2, n_pts_used, k):
    return chi2 + k * np.log(n_pts_used)


def chi2_red_of(chi2, n_pts_used, k):
    return chi2 / max(n_pts_used - k, 1)


# ============================================================
# Per-galaxy fit (called by Pool workers)
# ============================================================
def fit_one_galaxy(args):
    """Worker function. args = (galaxy, T, V_flat, logM_star, logM_halo)."""
    galaxy, T, V_flat, logM_star, logM_halo = args
    rotmod_path = os.path.join(ROTMOD_DIR, f'{galaxy}_rotmod.dat')
    if not os.path.exists(rotmod_path):
        return {'Galaxy': galaxy, 'error': f'rotmod not found: {rotmod_path}'}

    try:
        d = np.loadtxt(rotmod_path, comments='#')
    except Exception as e:
        return {'Galaxy': galaxy, 'error': f'rotmod load failed: {e}'}

    r_all, vobs_all, evobs_all = d[:, 0], d[:, 1], d[:, 2]
    vgas, vdisk, vbul = d[:, 3], d[:, 4], d[:, 5]
    Vbar2_all = baryon_squared(vgas, vdisk, vbul)

    n_total = len(r_all)
    mask = vobs_all**2 > Vbar2_all
    n_used = int(mask.sum())
    n_excluded = n_total - n_used

    if n_used < 5:
        return {'Galaxy': galaxy,
                'error': f'only {n_used} usable points',
                'n_pts_total': n_total, 'n_pts_used': n_used}

    r = r_all[mask]; vobs = vobs_all[mask]; evobs = evobs_all[mask]
    Vbar2 = Vbar2_all[mask]
    sig = np.maximum(evobs, SIGMA_V_FLOOR)

    t_galaxy_start = time.time()

    # Burkert sanity-check fit
    p_burk, chi2_burk = fit_burkert(r, vobs, sig, Vbar2)
    if p_burk is None:
        return {'Galaxy': galaxy, 'error': 'Burkert fit failed'}
    chi2r_burk = chi2_red_of(chi2_burk, n_used, 2)
    bic_burk = bic_of(chi2_burk, n_used, 2)

    # gNFW with 0, 1, 2 shells
    p_g0, chi2_g0 = fit_gnfw_n_shells(r, vobs, sig, Vbar2, 0)
    if p_g0 is None:
        return {'Galaxy': galaxy, 'error': 'gNFW 0-shell fit failed'}
    chi2r_g0 = chi2_red_of(chi2_g0, n_used, 3)
    bic_g0 = bic_of(chi2_g0, n_used, 3)

    p_g1, chi2_g1 = fit_gnfw_n_shells(r, vobs, sig, Vbar2, 1)
    chi2r_g1 = chi2_red_of(chi2_g1, n_used, 6) if p_g1 is not None else np.nan
    bic_g1 = bic_of(chi2_g1, n_used, 6) if p_g1 is not None else np.inf

    p_g2, chi2_g2 = fit_gnfw_n_shells(r, vobs, sig, Vbar2, 2)
    chi2r_g2 = chi2_red_of(chi2_g2, n_used, 9) if p_g2 is not None else np.nan
    bic_g2 = bic_of(chi2_g2, n_used, 9) if p_g2 is not None else np.inf

    bics = [bic_g0, bic_g1, bic_g2]
    chi2s = [chi2_g0, chi2_g1, chi2_g2]
    chi2rs = [chi2r_g0, chi2r_g1, chi2r_g2]
    best_n = int(np.argmin(bics))
    best_chi2 = chi2s[best_n]
    best_chi2r = chi2rs[best_n]
    best_bic = bics[best_n]

    elapsed = time.time() - t_galaxy_start

    return {
        'Galaxy': galaxy, 'T': T, 'V_flat': V_flat,
        'logM_star': logM_star, 'logM_halo': logM_halo,
        'n_pts_total': n_total, 'n_pts_used': n_used, 'n_excluded': n_excluded,
        'is_clean': bool(n_excluded == 0),
        'elapsed_sec': elapsed,

        # Burkert (sanity-check / join column)
        'burk_rho0': p_burk[0], 'burk_a_kpc': p_burk[1],
        'burk_chi2': chi2_burk, 'burk_chi2_red': chi2r_burk, 'burk_bic': bic_burk,

        # gNFW backbone-only
        'gnfw0_rho_s': p_g0[0], 'gnfw0_r_s_kpc': p_g0[1], 'gnfw0_gamma': p_g0[2],
        'gnfw0_chi2': chi2_g0, 'gnfw0_chi2_red': chi2r_g0, 'gnfw0_bic': bic_g0,

        # gNFW + 1 shell
        'gnfw1_rho_s': p_g1[0] if p_g1 is not None else np.nan,
        'gnfw1_r_s_kpc': p_g1[1] if p_g1 is not None else np.nan,
        'gnfw1_gamma': p_g1[2] if p_g1 is not None else np.nan,
        'gnfw1_M_sh1': p_g1[3] if p_g1 is not None else np.nan,
        'gnfw1_r_sh1_kpc': p_g1[4] if p_g1 is not None else np.nan,
        'gnfw1_sigma_sh1_kpc': p_g1[5] if p_g1 is not None else np.nan,
        'gnfw1_chi2': chi2_g1, 'gnfw1_chi2_red': chi2r_g1, 'gnfw1_bic': bic_g1,

        # gNFW + 2 shells
        'gnfw2_rho_s': p_g2[0] if p_g2 is not None else np.nan,
        'gnfw2_r_s_kpc': p_g2[1] if p_g2 is not None else np.nan,
        'gnfw2_gamma': p_g2[2] if p_g2 is not None else np.nan,
        'gnfw2_M_sh1': p_g2[3] if p_g2 is not None else np.nan,
        'gnfw2_r_sh1_kpc': p_g2[4] if p_g2 is not None else np.nan,
        'gnfw2_sigma_sh1_kpc': p_g2[5] if p_g2 is not None else np.nan,
        'gnfw2_M_sh2': p_g2[6] if p_g2 is not None else np.nan,
        'gnfw2_r_sh2_kpc': p_g2[7] if p_g2 is not None else np.nan,
        'gnfw2_sigma_sh2_kpc': p_g2[8] if p_g2 is not None else np.nan,
        'gnfw2_chi2': chi2_g2, 'gnfw2_chi2_red': chi2r_g2, 'gnfw2_bic': bic_g2,

        # BIC winner
        'fw_gnfw_best_n_shells': best_n,
        'fw_gnfw_best_chi2': best_chi2,
        'fw_gnfw_best_chi2_red': best_chi2r,
        'fw_gnfw_best_bic': best_bic,
    }


# ============================================================
# Main driver
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='gNFW backbone parallel fitter')
    parser.add_argument('--n-workers', type=int, default=None,
                        help='Worker processes (default: cpu_count - 2)')
    parser.add_argument('--smoke', action='store_true',
                        help='Smoke test: fit only NGC5371 and NGC6946')
    parser.add_argument('--galaxies', type=str, default=None,
                        help='Comma-separated galaxy list to override sample')
    args = parser.parse_args()

    n_cpu = mp.cpu_count()
    n_workers = args.n_workers if args.n_workers else max(1, n_cpu - 2)

    print("=" * 72)
    print("gNFW BACKBONE PARALLEL FITTER")
    print("=" * 72)
    print(f"Rotmod dir:    {ROTMOD_DIR}")
    print(f"Sample CSV:    {SAMPLE_CSV}")
    print(f"Output CSV:    {OUTPUT_CSV}")
    print(f"Log file:      {LOG_FILE}")
    print(f"CPU count:     {n_cpu}")
    print(f"Workers:       {n_workers}")
    print(f"Time budget:   {TIME_BUDGET_PER_FIT}s per fit")
    print(f"Shell caps:    M<={SHELL_M_MAX:.0e}, sigma/r<={SHELL_WIDTH_MAX_FRAC},"
          f" r_grid={SHELL_R_MAX_GRID} (canonical)")
    print(f"gNFW bounds:   gamma in [{GAMMA_MIN}, {GAMMA_MAX}]")
    print("=" * 72)

    if not os.path.isdir(ROTMOD_DIR):
        print(f"\nERROR: Rotmod directory not found at '{ROTMOD_DIR}'")
        sys.exit(1)
    if not os.path.exists(SAMPLE_CSV):
        print(f"\nERROR: Sample CSV not found at '{SAMPLE_CSV}'")
        sys.exit(1)

    sample = pd.read_csv(SAMPLE_CSV)
    target = sample[(sample['T'] >= T_MIN) & (sample['T'] <= T_MAX)].copy()

    if args.smoke:
        target = target[target['Galaxy'].isin(['NGC5371', 'NGC6946'])]
        print(f"\nSMOKE TEST: {target['Galaxy'].tolist()}")
    elif args.galaxies:
        wanted = [g.strip() for g in args.galaxies.split(',')]
        target = target[target['Galaxy'].isin(wanted)]
        print(f"\nFiltered to: {target['Galaxy'].tolist()}")

    print(f"\nTarget sample: {len(target)} galaxies")

    tasks = [(row['Galaxy'], int(row['T']), float(row['Vflat']),
              float(row['logM_star']), float(row['logM_halo']))
             for _, row in target.iterrows()]

    results = []
    errors = []
    t_total_start = time.time()

    with open(LOG_FILE, 'w') as log_fh:
        log_fh.write(f"gNFW fits producer log\n")
        log_fh.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_fh.write(f"Workers: {n_workers}, Time budget: {TIME_BUDGET_PER_FIT}s\n")
        log_fh.write("=" * 72 + "\n")
        log_fh.flush()

        with mp.Pool(processes=n_workers) as pool:
            for i, result in enumerate(
                    pool.imap_unordered(fit_one_galaxy, tasks, chunksize=1)):
                done = i + 1
                gal = result.get('Galaxy', '?')

                if 'error' in result:
                    msg = f"  [{done}/{len(tasks)}] {gal}: ERROR — {result['error']}"
                    print(msg); log_fh.write(msg + '\n')
                    errors.append(result)
                else:
                    results.append(result)
                    n_pts = result.get('n_pts_used', 0)
                    best_n = result.get('fw_gnfw_best_n_shells', -1)
                    chi2r = result.get('fw_gnfw_best_chi2_red', -1)
                    gam = result.get('gnfw0_gamma', -1)
                    elapsed_g = result.get('elapsed_sec', 0)
                    msg = (f"  [{done}/{len(tasks)}] {gal}: "
                           f"best n_shells={best_n}, "
                           f"chi2_r={chi2r:.2f}, "
                           f"gnfw0_gamma={gam:.2f}, "
                           f"n_pts={n_pts}, t={elapsed_g:.1f}s")
                    print(msg); log_fh.write(msg + '\n')

                elapsed = time.time() - t_total_start
                remaining = len(tasks) - done
                avg = elapsed / max(done, 1)
                eta_s = avg * remaining
                if done % 10 == 0 or done == len(tasks):
                    print(f"    --- elapsed: {elapsed/60:.1f}m, "
                          f"ETA: {eta_s/60:.1f}m ---")
                log_fh.flush()

        log_fh.write(f"\nFinished: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_fh.write(f"Total elapsed: {(time.time() - t_total_start)/60:.1f} min\n")
        log_fh.write(f"Successful: {len(results)}/{len(tasks)}\n")
        log_fh.write(f"Errors:     {len(errors)}\n")
        for e in errors:
            log_fh.write(f"  {e.get('Galaxy', '?')}: {e.get('error', '?')}\n")

    if not results:
        print("\nNo successful fits; nothing to write.")
        sys.exit(1)

    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_CSV, index=False)

    print(f"\n{'=' * 72}\nDONE\n{'=' * 72}")
    print(f"Successful: {len(results)}/{len(tasks)}")
    print(f"Errors:     {len(errors)}")
    print(f"Total time: {(time.time() - t_total_start)/60:.1f} minutes")
    print(f"Output:     {OUTPUT_CSV}")
    print(f"Log:        {LOG_FILE}")


if __name__ == '__main__':
    main()

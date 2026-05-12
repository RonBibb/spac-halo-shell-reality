"""
shell_reality_nulls.py — Adversarial null tests for halo_shells v7.0

Two within-galaxy null tests that go beyond the Gaussian-noise null
implemented in null_test.py:

  scramble:  Burkert-only fit subtracted from V^2_DM,obs to obtain residuals;
             residuals shuffled across radii within each galaxy; V_obs
             reconstructed; framework refit. Tests whether localized
             residual structure is spatially coherent in ways the framework
             can detect.

  permute:   V_obs values shuffled across radii (R values held fixed);
             framework refit. Maximally destructive of any radial structure.
             Sanity check that BIC selection responds to spatial coherence
             rather than amplitude alone.

For each null type and each realization, the framework is refit on every
galaxy in the v7.0 canonical sample (102 galaxies, T=2-9) under strict
sigma/r <= 0.4 enforcement. From per-realization shell-bearing fractions
we compute per-T-bin Spearman rho and per-galaxy Spearman rho, and
compare them to the real-data baseline (rho_per_T = -0.833, p = 0.010;
rho_per_galaxy = -0.296, p = 0.003).

Usage:
  python3 shell_reality_nulls.py [N_REALIZATIONS]

  Defaults: N_REALIZATIONS=20. Runtime scales as N * 102 galaxies * 2 null
  types * (8-24 multi-restart fits per n_shells in {0,1,2}). Estimate
  ~30-60 minutes per realization on a modern Apple Silicon Mac, single
  process.

Outputs (in OUTPUT_DIR=./shell_reality_out/):
  per_galaxy.csv              one row per (null_type, realization, galaxy)
  per_realization.csv         per-T fractions and rho per realization
  summary.txt                 real-vs-null comparison and empirical p-values

Path resolution mirrors null_test.py: prefers package layout
(PACKAGE_ROOT/Rotmod_LTG/, PACKAGE_ROOT/data/sparc_T2-T9_canonical_fits.csv),
falls back to ./Rotmod_LTG and ./sparc_T2-T9_canonical_fits.csv when run
from a flat working directory.

Requires: numpy, scipy, pandas. No other dependencies.
"""

import os
import sys
import time
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# Configuration
# ============================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DATA = os.path.join(os.path.dirname(_HERE), 'Rotmod_LTG')
_LOCAL_DATA = '../Rotmod_LTG'
DATA_DIR = _PACKAGE_DATA if os.path.isdir(_PACKAGE_DATA) else _LOCAL_DATA

_PACKAGE_CSV = os.path.join(os.path.dirname(_HERE), 'data', 'sparc_T2-T9_canonical_fits.csv')
_LOCAL_CSV = os.path.join(os.getcwd(), 'sparc_T2-T9_canonical_fits.csv')
CANONICAL_CSV = _PACKAGE_CSV if os.path.isfile(_PACKAGE_CSV) else _LOCAL_CSV

OUTPUT_DIR = os.path.join(os.getcwd(), 'shell_reality_out')

# Real-data baselines (recomputed from canonical CSV at startup; these are
# fallback constants matching the v7.0 manuscript)
REAL_RHO_PER_T_FALLBACK = -0.833
REAL_RHO_PER_GAL_FALLBACK = -0.296

# Null test config
N_REALIZATIONS_DEFAULT = 20
RNG_SEED = 20260507
NULL_TYPES = ['scramble', 'permute']

# Physics constants (same as v7.0 null_test.py)
G = 4.302e-6   # kpc * (km/s)^2 / M_sun
SIGMA_V_FLOOR = 1.0
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7

SHELL_R_MAX_GRID = [3.0, 6.0, 12.0]
SHELL_WIDTH_MAX_FRAC = 0.4


# ============================================================
# Physics (copied from v7.0 null_test.py for portability)
# ============================================================
def baryon_squared(vg, vd, vb):
    return (vg * np.abs(vg)
            + UPSILON_DISK * vd * np.abs(vd)
            + UPSILON_BULGE * vb * np.abs(vb))


def burkert_v(r, rho_0, a):
    a = max(a, 1e-6)
    x = r / a
    M = np.pi * rho_0 * a**3 * (np.log(1+x**2) + 2*np.log(1+x) - 2*np.arctan(x))
    return np.sqrt(np.maximum(G * M / np.maximum(r, 1e-6), 0))


def shell_v2(r, M, r_sh, sigma):
    sigma = max(sigma, 1e-6)
    M_enc = 0.5 * M * (1 + erf((r - r_sh) / (np.sqrt(2) * sigma)))
    return np.maximum(G * M_enc / np.maximum(r, 1e-6), 0)


# ============================================================
# Models (curve_fit compatible) — strict sigma_frac reparameterization
# ============================================================
def model_fw0(V2_bar):
    def vt(r, rho_0, a):
        v2 = V2_bar + burkert_v(r, rho_0, a)**2
        return np.sqrt(np.maximum(v2, 0))
    return vt


def model_fw1(V2_bar):
    def vt(r, rho_0, a, M_sh, r_sh, sigma_frac):
        sigma = sigma_frac * r_sh
        v2 = V2_bar + burkert_v(r, rho_0, a)**2 + shell_v2(r, M_sh, r_sh, sigma)
        return np.sqrt(np.maximum(v2, 0))
    return vt


def model_fw2(V2_bar):
    def vt(r, rho_0, a, M1, r1, sf1, M2, r2, sf2):
        s1 = sf1 * r1
        s2 = sf2 * r2
        v2 = (V2_bar
              + burkert_v(r, rho_0, a)**2
              + shell_v2(r, M1, r1, s1)
              + shell_v2(r, M2, r2, s2))
        return np.sqrt(np.maximum(v2, 0))
    return vt


# ============================================================
# Fitter (matches null_test.py / run_canonical_fits.py conventions)
# ============================================================
def fit_fw_n_shells(rd, vd, ed, V2_bar, n_shells, time_budget=30):
    sig = np.maximum(ed, SIGMA_V_FLOOR)

    if n_shells == 0:
        vt = model_fw0(V2_bar)
        starts = [[3e7, 8.0], [1e7, 15.0], [1e8, 4.0], [3e6, 30.0], [3e8, 2.0]]
        bounds = ([1e3, 0.1], [1e10, 200.0])
        best_chi2, best_p = np.inf, None
        t0 = time.time()
        for p0 in starts:
            try:
                p, _ = curve_fit(vt, rd, vd, p0=p0, bounds=bounds, sigma=sig, maxfev=10000)
                c = float(np.sum(((vd - vt(rd, *p)) / sig)**2))
                if c < best_chi2:
                    best_chi2, best_p = c, p
            except Exception:
                continue
            if time.time() - t0 > time_budget:
                break
        return best_p, best_chi2

    if n_shells == 1:
        vt = model_fw1(V2_bar)
        starts = []
        for r_max in SHELL_R_MAX_GRID:
            for rho0 in [1e7, 3e7, 1e8]:
                for a_init in [5.0, 10.0, 20.0]:
                    for r_frac in [0.3, 0.5, 0.7]:
                        starts.append(([rho0, a_init, 3e9, r_frac*r_max, 0.25], r_max))
    else:
        vt = model_fw2(V2_bar)
        starts = []
        for r_max in SHELL_R_MAX_GRID:
            for rho0 in [1e7, 3e7, 1e8]:
                for a_init in [5.0, 10.0, 20.0]:
                    starts.append(([rho0, a_init, 3e9, r_max/3, 0.25, 3e9, 2*r_max/3, 0.25], r_max))

    best_chi2, best_p_physical = np.inf, None
    t0 = time.time()
    for p0, r_max in starts:
        if n_shells == 1:
            lb = [1e3, 0.1, 1e6, 0.2, 0.01]
            ub = [1e10, 200.0, 5e10, r_max, SHELL_WIDTH_MAX_FRAC]
        else:
            lb = [1e3, 0.1, 1e6, 0.2, 0.01, 1e6, 0.2, 0.01]
            ub = [1e10, 200.0, 5e10, r_max, SHELL_WIDTH_MAX_FRAC,
                  5e10, r_max, SHELL_WIDTH_MAX_FRAC]
        try:
            p, _ = curve_fit(vt, rd, vd, p0=p0, bounds=(lb, ub), sigma=sig, maxfev=15000)
            c = float(np.sum(((vd - vt(rd, *p)) / sig)**2))
            if c < best_chi2:
                best_chi2 = c
                if n_shells == 1:
                    rho0, a, M, rsh, sf = p
                    best_p_physical = np.array([rho0, a, M, rsh, sf*rsh])
                else:
                    rho0, a, M1, r1, sf1, M2, r2, sf2 = p
                    best_p_physical = np.array([rho0, a, M1, r1, sf1*r1, M2, r2, sf2*r2])
        except Exception:
            continue
        if time.time() - t0 > time_budget:
            break
    return best_p_physical, best_chi2


def best_n_via_bic(rd, vd, ed, V2_bar):
    """Best of n_shells in {0,1,2} by BIC. Returns (best_n, chi2, bic)."""
    n_pts = len(rd)
    best_n, best_bic, best_chi2 = 0, np.inf, np.inf
    for ns in [0, 1, 2]:
        p, c = fit_fw_n_shells(rd, vd, ed, V2_bar, ns)
        if p is None:
            continue
        k = 2 + 3*ns
        bic = c + k * np.log(n_pts)
        if bic < best_bic:
            best_n, best_bic, best_chi2 = ns, bic, c
    return best_n, best_chi2, best_bic


# ============================================================
# Null-data generators
# ============================================================
def generate_scramble(rd, V_obs, V2_bar, V_burk_smooth, rng):
    """
    Residual-scrambling null. Operates in V^2 space on the dark-matter residual:
        eps_i = V^2_DM,obs(R_i) - V^2_Burkert(R_i)
    Shuffles eps across radii, reconstructs V_obs:
        V_obs_null = sqrt(V^2_bar + V^2_Burkert + eps_shuffled)

    Preserves: V^2_bar (per-radius), V^2_Burkert (per-radius), eps amplitude
               distribution (multiset), per-radius error bars, R sampling.
    Destroys:  spatial coherence of any localized DM residual structure.
    """
    V2_DM_obs = V_obs**2 - V2_bar
    V2_DM_burk = V_burk_smooth**2
    eps = V2_DM_obs - V2_DM_burk
    perm = rng.permutation(len(eps))
    eps_shuffled = eps[perm]
    V2_DM_null = V2_DM_burk + eps_shuffled
    V2_obs_null = V2_bar + V2_DM_null
    V_obs_null = np.sqrt(np.maximum(V2_obs_null, 0))
    # Floor at 0.1 km/s to avoid pathological zeros downstream
    return np.maximum(V_obs_null, 0.1)


def generate_permute(rd, V_obs, V2_bar, V_burk_smooth, rng):
    """
    Radius-permutation null. Shuffles V_obs values across radii while holding
    R points and error bars fixed. Maximally destructive: breaks the smooth
    backbone too, not just localized structure.
    """
    perm = rng.permutation(len(V_obs))
    return V_obs[perm]


GENERATORS = {
    'scramble': generate_scramble,
    'permute':  generate_permute,
}


# ============================================================
# Per-realization summary statistics
# ============================================================
def compute_realization_stats(per_galaxy_records):
    """
    Given the per-galaxy results from one realization, compute:
      - per-T shell-bearing fractions
      - per-T-bin Spearman rho (T_bin vs fraction)
      - per-galaxy Spearman rho (T_galaxy vs n_shells>0 indicator)
    """
    df = pd.DataFrame(per_galaxy_records)
    out = {}
    if len(df) == 0:
        return out
    # Per-T fractions
    for T in [2, 3, 4, 5, 6, 7, 8, 9]:
        sub = df[df['T'] == T]
        if len(sub) > 0:
            out[f'frac_T{T}'] = float((sub['n_shells'] > 0).mean())
            out[f'n_T{T}'] = int(len(sub))
        else:
            out[f'frac_T{T}'] = np.nan
            out[f'n_T{T}'] = 0
    # Per-T-bin rho
    T_vals = [T for T in [2,3,4,5,6,7,8,9] if not np.isnan(out[f'frac_T{T}'])]
    fracs = [out[f'frac_T{T}'] for T in T_vals]
    if len(T_vals) >= 3:
        rho_T, p_T = spearmanr(T_vals, fracs)
        out['rho_per_T'] = float(rho_T)
        out['p_per_T'] = float(p_T)
    else:
        out['rho_per_T'] = np.nan
        out['p_per_T'] = np.nan
    # Per-galaxy rho
    rho_g, p_g = spearmanr(df['T'].values, (df['n_shells'] > 0).astype(int).values)
    out['rho_per_gal'] = float(rho_g) if not np.isnan(rho_g) else np.nan
    out['p_per_gal'] = float(p_g) if not np.isnan(p_g) else np.nan
    out['n_shellbearing'] = int((df['n_shells'] > 0).sum())
    out['n_total'] = int(len(df))
    return out


# ============================================================
# Galaxy preprocessing — load real data once, cache the bits we need
# ============================================================
def preprocess_galaxies(canon_df):
    """
    For each galaxy in canon_df, load its rotmod data, mask unphysical points,
    compute V2_bar and the smooth Burkert prediction (using burk_rho0/burk_a
    from canonical CSV). Returns a list of dicts ready for null generation.
    """
    galaxies = []
    for _, gal in canon_df.iterrows():
        g = gal['Galaxy']
        path = os.path.join(DATA_DIR, f'{g}_rotmod.dat')
        if not os.path.exists(path):
            continue
        d = np.loadtxt(path, comments='#')
        r, vobs, evobs = d[:, 0], d[:, 1], d[:, 2]
        vgas, vdisk, vbul = d[:, 3], d[:, 4], d[:, 5]
        Vbar2 = baryon_squared(vgas, vdisk, vbul)
        mask = vobs**2 > Vbar2
        if int(mask.sum()) < 5:
            continue
        rd = r[mask]
        vd = vobs[mask]
        ed = evobs[mask]
        V2_bd = Vbar2[mask]
        V_burk_smooth = burkert_v(rd, gal['burk_rho0'], gal['burk_a_kpc'])
        galaxies.append({
            'Galaxy': g,
            'T': int(gal['T']),
            'rd': rd, 'vd': vd, 'ed': ed,
            'V2_bar': V2_bd,
            'V_burk_smooth': V_burk_smooth,
            'n_pts': int(mask.sum()),
        })
    return galaxies


# ============================================================
# Main
# ============================================================
def main():
    n_real = N_REALIZATIONS_DEFAULT
    if len(sys.argv) > 1:
        try:
            n_real = int(sys.argv[1])
        except ValueError:
            pass

    print("=" * 72)
    print("SHELL REALITY NULL TESTS (v7.0 pipeline, strict sigma/r <= 0.4)")
    print(f"N_REALIZATIONS = {n_real}")
    print("=" * 72)

    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: rotmod directory not found: {DATA_DIR}")
        sys.exit(1)
    if not os.path.exists(CANONICAL_CSV):
        print(f"ERROR: canonical CSV not found: {CANONICAL_CSV}")
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    canon = pd.read_csv(CANONICAL_CSV)
    print(f"Loaded canonical CSV: {len(canon)} galaxies")

    # Real baseline (recompute live from CSV)
    T_vals_real = sorted(canon['T'].unique())
    fracs_real = [(canon[canon['T'] == T]['fw_best_n_shells'] > 0).mean()
                  for T in T_vals_real]
    real_rho_per_T, real_p_per_T = spearmanr(T_vals_real, fracs_real)
    real_rho_per_gal, real_p_per_gal = spearmanr(
        canon['T'].values,
        (canon['fw_best_n_shells'] > 0).astype(int).values
    )
    print(f"Real baseline: rho_per_T = {real_rho_per_T:.4f} (p={real_p_per_T:.4f})")
    print(f"Real baseline: rho_per_gal = {real_rho_per_gal:.4f} (p={real_p_per_gal:.4f})")
    print()

    galaxies = preprocess_galaxies(canon)
    print(f"Preprocessed {len(galaxies)} galaxies")
    if len(galaxies) == 0:
        print("ERROR: no galaxies preprocessed; check rotmod files")
        sys.exit(1)

    rng_master = np.random.default_rng(seed=RNG_SEED)
    per_galaxy_records = []
    per_realization_records = []
    t_start = time.time()

    total_units = len(NULL_TYPES) * n_real * len(galaxies)
    unit = 0

    for null_type in NULL_TYPES:
        gen = GENERATORS[null_type]
        for k in range(n_real):
            real_seed = int(rng_master.integers(0, 2**31 - 1))
            rng_real = np.random.default_rng(seed=real_seed)
            this_real_records = []
            for gal in galaxies:
                unit += 1
                v_obs_null = gen(gal['rd'], gal['vd'], gal['V2_bar'],
                                 gal['V_burk_smooth'], rng_real)
                best_n, best_chi2, best_bic = best_n_via_bic(
                    gal['rd'], v_obs_null, gal['ed'], gal['V2_bar']
                )
                rec = {
                    'null_type': null_type,
                    'realization': k,
                    'Galaxy': gal['Galaxy'],
                    'T': gal['T'],
                    'n_pts': gal['n_pts'],
                    'n_shells': best_n,
                    'chi2': best_chi2,
                    'bic': best_bic,
                }
                per_galaxy_records.append(rec)
                this_real_records.append(rec)

                if unit % 25 == 0 or unit == total_units:
                    elapsed = time.time() - t_start
                    eta = elapsed / unit * (total_units - unit)
                    so_far = pd.DataFrame(per_galaxy_records)
                    rate = (so_far['n_shells'] > 0).mean() * 100
                    print(f"  [{unit}/{total_units}] {null_type} real={k} "
                          f"latest={gal['Galaxy']:<12} T={gal['T']} "
                          f"shellrate-so-far={rate:.1f}% "
                          f"({elapsed:.0f}s, ETA {eta:.0f}s)")

            stats = compute_realization_stats(this_real_records)
            stats['null_type'] = null_type
            stats['realization'] = k
            per_realization_records.append(stats)

    # Save per-galaxy results
    df_pg = pd.DataFrame(per_galaxy_records)
    df_pg.to_csv(os.path.join(OUTPUT_DIR, 'per_galaxy.csv'), index=False)
    print(f"\nSaved: {os.path.join(OUTPUT_DIR, 'per_galaxy.csv')}")

    # Save per-realization results
    df_pr = pd.DataFrame(per_realization_records)
    cols_first = ['null_type', 'realization', 'rho_per_T', 'p_per_T',
                  'rho_per_gal', 'p_per_gal', 'n_shellbearing', 'n_total']
    cols_other = [c for c in df_pr.columns if c not in cols_first]
    df_pr = df_pr[cols_first + cols_other]
    df_pr.to_csv(os.path.join(OUTPUT_DIR, 'per_realization.csv'), index=False)
    print(f"Saved: {os.path.join(OUTPUT_DIR, 'per_realization.csv')}")

    # ============================================================
    # Summary
    # ============================================================
    lines = []
    lines.append("=" * 72)
    lines.append("SHELL REALITY NULL TESTS — Summary")
    lines.append("=" * 72)
    lines.append(f"v7.0 pipeline, strict sigma/r <= 0.4 enforcement")
    lines.append(f"N_REALIZATIONS per null type = {n_real}")
    lines.append(f"Galaxies fit per realization = {len(galaxies)}")
    lines.append("")
    lines.append("REAL-DATA BASELINE (v7.0 canonical fits)")
    lines.append(f"  rho_per_T-bin  = {real_rho_per_T:+.4f}  (p = {real_p_per_T:.4f})")
    lines.append(f"  rho_per_galaxy = {real_rho_per_gal:+.4f}  (p = {real_p_per_gal:.4f})")
    lines.append(f"  shell-bearing fraction (real) = {(canon['fw_best_n_shells']>0).sum()}/{len(canon)} "
                 f"= {(canon['fw_best_n_shells']>0).mean():.3f}")
    lines.append("")
    for null_type in NULL_TYPES:
        sub = df_pr[df_pr['null_type'] == null_type]
        lines.append("-" * 72)
        lines.append(f"NULL TYPE: {null_type.upper()}")
        lines.append("-" * 72)
        rhos_T = sub['rho_per_T'].dropna().values
        rhos_g = sub['rho_per_gal'].dropna().values
        if len(rhos_T) > 0:
            lines.append(f"  rho_per_T: mean={rhos_T.mean():+.4f} "
                         f"std={rhos_T.std():.4f} "
                         f"min={rhos_T.min():+.4f} max={rhos_T.max():+.4f}")
            p_emp_T = float((rhos_T <= real_rho_per_T).sum()) / len(rhos_T)
            lines.append(f"  Empirical one-sided p (null rho <= real rho={real_rho_per_T:.4f}): "
                         f"{p_emp_T:.4f} ({(rhos_T <= real_rho_per_T).sum()}/{len(rhos_T)})")
        if len(rhos_g) > 0:
            lines.append(f"  rho_per_gal: mean={rhos_g.mean():+.4f} "
                         f"std={rhos_g.std():.4f} "
                         f"min={rhos_g.min():+.4f} max={rhos_g.max():+.4f}")
            p_emp_g = float((rhos_g <= real_rho_per_gal).sum()) / len(rhos_g)
            lines.append(f"  Empirical one-sided p (null rho <= real rho={real_rho_per_gal:.4f}): "
                         f"{p_emp_g:.4f} ({(rhos_g <= real_rho_per_gal).sum()}/{len(rhos_g)})")
        # Shell-bearing fractions averaged across realizations, per T
        sub_pg = df_pg[df_pg['null_type'] == null_type]
        lines.append("")
        lines.append("  Mean per-T shell-bearing fraction across null realizations:")
        for T in [2, 3, 4, 5, 6, 7, 8, 9]:
            ssub = sub_pg[sub_pg['T'] == T]
            real_sub = canon[canon['T'] == T]
            if len(ssub) > 0 and len(real_sub) > 0:
                null_frac = (ssub['n_shells'] > 0).mean()
                real_frac = (real_sub['fw_best_n_shells'] > 0).mean()
                lines.append(f"    T={T}: null={null_frac:.3f}  real={real_frac:.3f}  "
                             f"ratio={real_frac/max(null_frac,1e-6):.2f}x")
        lines.append("")

    summary_text = "\n".join(lines)
    print()
    print(summary_text)
    with open(os.path.join(OUTPUT_DIR, 'summary.txt'), 'w') as f:
        f.write(summary_text)
    print(f"\nSaved: {os.path.join(OUTPUT_DIR, 'summary.txt')}")
    print(f"\nTotal runtime: {(time.time()-t_start)/60:.1f} min")


if __name__ == '__main__':
    main()

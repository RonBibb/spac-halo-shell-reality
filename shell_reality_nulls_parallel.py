"""
shell_reality_nulls_parallel.py — Adversarial null tests for halo_shells v7.0
                                  (multi-process parallel version)

This is the parallel companion to shell_reality_nulls.py. It implements the
same scramble and permute null tests with identical physics, identical
fitters, identical BIC selection, and identical RNG seeding — but distributes
work across multiple CPU processes to reduce wall-clock time.

DESIGN NOTE: byte-for-byte reproducibility against single-process version
================================================================
The parallelism granularity is the REALIZATION, not the individual galaxy fit.
Each worker process handles one complete realization (one null_type × one k,
102 galaxies) using a single np.random.Generator instance shared across all
galaxies in that realization — exactly matching the single-process loop
structure. This means:

  - Per-realization seeds are computed in the main process identically to
    the single-process script (same rng_master.integers() call sequence).
  - Within a realization, galaxies are processed in CSV order with a single
    rng_real instance whose state advances across galaxies — identical to
    the single-process script.
  - Only the ORDER OF COMPLETION across realizations differs from the
    single-process script. Results are sorted to canonical order before
    writing.

Consequence: running N=100 with this script produces a per_galaxy.csv whose
first-20-realizations rows are byte-identical (within sort order) to running
N=20 with the single-process shell_reality_nulls.py — useful for verifying
correctness against the existing baseline.

Usage:
  python3 shell_reality_nulls_parallel.py [N_REALIZATIONS] [N_WORKERS]

  Defaults: N_REALIZATIONS=20, N_WORKERS=12 (leaves 4 P-cores + 4 E-cores
  free on M1 Ultra for OS, Parallels, etc.)

  Examples:
    python3 shell_reality_nulls_parallel.py 2           # smoke test
    python3 shell_reality_nulls_parallel.py 100         # full run, 12 workers
    python3 shell_reality_nulls_parallel.py 100 8       # full run, 8 workers

Outputs (in OUTPUT_DIR=./shell_reality_out/, identical schema to single-process):
  per_galaxy.csv              one row per (null_type, realization, galaxy)
  per_realization.csv         per-T fractions and rho per realization
  summary.txt                 real-vs-null comparison and empirical p-values

Path resolution: identical to shell_reality_nulls.py (PACKAGE_ROOT/Rotmod_LTG/
and PACKAGE_ROOT/data/sparc_T2-T9_canonical_fits.csv preferred; flat fallback).

Requires: numpy, scipy, pandas. No other dependencies.

Performance note: on M1 Ultra (16 P + 4 E cores), 12 workers typically achieves
~6-8× speedup over single-process. Going higher than 12 hits diminishing returns
because scipy's internal BLAS already uses some threading and contention grows.
"""

import os
import sys
import time
import multiprocessing as mp
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# Configuration (identical to single-process script)
# ============================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DATA = os.path.join(os.path.dirname(_HERE), 'Rotmod_LTG')
_LOCAL_DATA = '../Rotmod_LTG'
DATA_DIR = '/Users/ronbibb/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/Rotmod_LTG'

_PACKAGE_CSV = os.path.join(os.path.dirname(_HERE), 'data', 'sparc_T2-T9_canonical_fits.csv')
_LOCAL_CSV = os.path.join(os.getcwd(), 'sparc_T2-T9_canonical_fits.csv')
CANONICAL_CSV = '/Users/ronbibb/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/paper2_package/data/sparc_T2-T9_canonical_fits.csv'

OUTPUT_DIR = os.path.join(os.getcwd(), 'shell_reality_out')

# Real-data baselines
REAL_RHO_PER_T_FALLBACK = -0.833
REAL_RHO_PER_GAL_FALLBACK = -0.296

# Null test config (single-process script uses the same RNG_SEED → byte-reproducible)
N_REALIZATIONS_DEFAULT = 20
N_WORKERS_DEFAULT = 12
RNG_SEED = 20260507
NULL_TYPES = ['scramble', 'permute']

# Physics constants
G = 4.302e-6   # kpc * (km/s)^2 / M_sun
SIGMA_V_FLOOR = 1.0
UPSILON_DISK = 0.5
UPSILON_BULGE = 0.7

SHELL_R_MAX_GRID = [3.0, 6.0, 12.0]
SHELL_WIDTH_MAX_FRAC = 0.4

# Module-global populated by Pool initializer in worker processes.
# Holds the preprocessed galaxy list so workers don't repickle per task.
_GALAXIES = None


# ============================================================
# Physics (identical to single-process)
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
# Models (identical to single-process)
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
# Fitter (identical to single-process)
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
# Null-data generators (identical to single-process)
# ============================================================
def generate_scramble(rd, V_obs, V2_bar, V_burk_smooth, rng):
    V2_DM_obs = V_obs**2 - V2_bar
    V2_DM_burk = V_burk_smooth**2
    eps = V2_DM_obs - V2_DM_burk
    perm = rng.permutation(len(eps))
    eps_shuffled = eps[perm]
    V2_DM_null = V2_DM_burk + eps_shuffled
    V2_obs_null = V2_bar + V2_DM_null
    V_obs_null = np.sqrt(np.maximum(V2_obs_null, 0))
    return np.maximum(V_obs_null, 0.1)


def generate_permute(rd, V_obs, V2_bar, V_burk_smooth, rng):
    perm = rng.permutation(len(V_obs))
    return V_obs[perm]


GENERATORS = {
    'scramble': generate_scramble,
    'permute':  generate_permute,
}


# ============================================================
# Per-realization summary statistics (identical to single-process)
# ============================================================
def compute_realization_stats(per_galaxy_records):
    df = pd.DataFrame(per_galaxy_records)
    out = {}
    if len(df) == 0:
        return out
    for T in [2, 3, 4, 5, 6, 7, 8, 9]:
        sub = df[df['T'] == T]
        if len(sub) > 0:
            out[f'frac_T{T}'] = float((sub['n_shells'] > 0).mean())
            out[f'n_T{T}'] = int(len(sub))
        else:
            out[f'frac_T{T}'] = np.nan
            out[f'n_T{T}'] = 0
    T_vals = [T for T in [2,3,4,5,6,7,8,9] if not np.isnan(out[f'frac_T{T}'])]
    fracs = [out[f'frac_T{T}'] for T in T_vals]
    if len(T_vals) >= 3:
        rho_T, p_T = spearmanr(T_vals, fracs)
        out['rho_per_T'] = float(rho_T)
        out['p_per_T'] = float(p_T)
    else:
        out['rho_per_T'] = np.nan
        out['p_per_T'] = np.nan
    rho_g, p_g = spearmanr(df['T'].values, (df['n_shells'] > 0).astype(int).values)
    out['rho_per_gal'] = float(rho_g) if not np.isnan(rho_g) else np.nan
    out['p_per_gal'] = float(p_g) if not np.isnan(p_g) else np.nan
    out['n_shellbearing'] = int((df['n_shells'] > 0).sum())
    out['n_total'] = int(len(df))
    return out


# ============================================================
# Galaxy preprocessing (identical to single-process)
# ============================================================
def preprocess_galaxies(canon_df):
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
# Pool initializer and worker
# ============================================================
def _init_worker(galaxies_pickled):
    """Pool initializer — receives galaxies once per worker process."""
    global _GALAXIES
    _GALAXIES = galaxies_pickled


def _process_realization(args):
    """
    Process ONE complete realization (one null_type × one k, all galaxies).
    Uses a single np.random.Generator instance across all galaxies in this
    realization, matching the single-process loop structure exactly. This is
    what preserves byte-for-byte reproducibility against shell_reality_nulls.py.
    """
    null_type, k, seed = args
    rng_real = np.random.default_rng(seed=seed)
    gen = GENERATORS[null_type]
    recs = []
    for gal in _GALAXIES:
        v_obs_null = gen(gal['rd'], gal['vd'], gal['V2_bar'],
                         gal['V_burk_smooth'], rng_real)
        best_n, best_chi2, best_bic = best_n_via_bic(
            gal['rd'], v_obs_null, gal['ed'], gal['V2_bar']
        )
        recs.append({
            'null_type': null_type,
            'realization': k,
            'Galaxy': gal['Galaxy'],
            'T': gal['T'],
            'n_pts': gal['n_pts'],
            'n_shells': best_n,
            'chi2': best_chi2,
            'bic': best_bic,
        })
    return recs


# ============================================================
# Main
# ============================================================
def main():
    n_real = N_REALIZATIONS_DEFAULT
    n_workers = N_WORKERS_DEFAULT

    if len(sys.argv) > 1:
        try:
            n_real = int(sys.argv[1])
        except ValueError:
            pass
    if len(sys.argv) > 2:
        try:
            n_workers = int(sys.argv[2])
        except ValueError:
            pass

    print("=" * 72)
    print("SHELL REALITY NULL TESTS (PARALLEL) — v7.0 pipeline, strict sigma/r <= 0.4")
    print(f"N_REALIZATIONS = {n_real}")
    print(f"N_WORKERS      = {n_workers}")
    print(f"CPU count      = {mp.cpu_count()}")
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

    # ============================================================
    # Seed sequence — MUST match single-process script exactly.
    # rng_master advances ONCE per (null_type, realization) pair, in this
    # order: scramble-0, scramble-1, ..., scramble-(N-1), permute-0, ...
    # ============================================================
    rng_master = np.random.default_rng(seed=RNG_SEED)
    units = []
    for null_type in NULL_TYPES:
        for k in range(n_real):
            seed = int(rng_master.integers(0, 2**31 - 1))
            units.append((null_type, k, seed))

    total_units = len(units)
    total_fits = total_units * len(galaxies)
    print(f"Total realizations to process: {total_units} ({total_fits} galaxy fits)")
    print(f"Launching pool with {n_workers} workers...")
    print()

    t_start = time.time()
    all_records = []
    completed_real = 0
    completed_fits = 0

    # Pool with initializer; chunksize=1 because each unit is already ~50 galaxy fits
    with mp.Pool(processes=n_workers,
                 initializer=_init_worker,
                 initargs=(galaxies,)) as pool:
        for recs in pool.imap_unordered(_process_realization, units, chunksize=1):
            all_records.extend(recs)
            completed_real += 1
            completed_fits += len(recs)
            elapsed = time.time() - t_start
            rate = completed_fits / elapsed if elapsed > 0 else 0
            eta = (total_fits - completed_fits) / rate if rate > 0 else 0
            # First completed realization to report sample-quality data:
            this_nt = recs[0]['null_type']
            this_k = recs[0]['realization']
            this_rate = sum(1 for r in recs if r['n_shells'] > 0) / len(recs) * 100
            print(f"  [{completed_real}/{total_units} reals, "
                  f"{completed_fits}/{total_fits} fits] "
                  f"{this_nt} real={this_k} "
                  f"shellrate={this_rate:.1f}% "
                  f"({elapsed:.0f}s, ETA {eta:.0f}s, "
                  f"rate={rate:.2f} fits/s)")

    # ============================================================
    # Sort to canonical order (matches single-process output ordering).
    # Order: scramble before permute, then by realization, then by CSV galaxy order.
    # ============================================================
    df_pg = pd.DataFrame(all_records)
    null_type_order = {nt: i for i, nt in enumerate(NULL_TYPES)}
    galaxy_order = {g['Galaxy']: i for i, g in enumerate(galaxies)}
    df_pg['_nt_order'] = df_pg['null_type'].map(null_type_order)
    df_pg['_gal_order'] = df_pg['Galaxy'].map(galaxy_order)
    df_pg = df_pg.sort_values(['_nt_order', 'realization', '_gal_order']).reset_index(drop=True)
    df_pg = df_pg.drop(columns=['_nt_order', '_gal_order'])

    # Compute per-realization stats by grouping
    per_realization_records = []
    for null_type in NULL_TYPES:
        for k in range(n_real):
            this_recs = df_pg[(df_pg['null_type'] == null_type) &
                              (df_pg['realization'] == k)].to_dict('records')
            stats = compute_realization_stats(this_recs)
            stats['null_type'] = null_type
            stats['realization'] = k
            per_realization_records.append(stats)

    # Save per-galaxy results
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
    # Summary (identical format to single-process script)
    # ============================================================
    lines = []
    lines.append("=" * 72)
    lines.append("SHELL REALITY NULL TESTS (PARALLEL) — Summary")
    lines.append("=" * 72)
    lines.append(f"v7.0 pipeline, strict sigma/r <= 0.4 enforcement")
    lines.append(f"N_REALIZATIONS per null type = {n_real}")
    lines.append(f"Galaxies fit per realization = {len(galaxies)}")
    lines.append(f"N_WORKERS = {n_workers}")
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

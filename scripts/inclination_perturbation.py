#!/usr/bin/env python3
"""
inclination_perturbation.py
===========================

Inclination systematic perturbation test for shell_reality (Paper 2, §3.3).

For each galaxy in the v7.0 sample, perturb its inclination Inc within the
published SPARC uncertainty (e_Inc), refit the v7.0 framework (Burkert + n
shells, BIC-selected), and record the perturbed shell selections and parameters.

When inclination changes from Inc to Inc':
  - v_los is unchanged (it's the observed line-of-sight velocity)
  - V_obs deprojects as V_obs = v_los / sin(i)
  - So perturbed V_obs = V_obs_nominal * sin(Inc_nominal) / sin(Inc')
  - e_V_obs scales the same way
  - r and V_baryon components are inclination-independent
  - Upsilons unchanged (this test isolates inclination systematics)

If shell selections survive realistic inclination perturbation, shells are not
artifacts of inclination measurement uncertainty.

Per-galaxy perturbations: each galaxy uses its own published e_Inc.

Usage
-----
  python3 inclination_perturbation.py [N_REALIZATIONS] [SEED]
Default: N_REALIZATIONS = 20, SEED = 20260510

Outputs (incremental):
  outputs/inclination_perturbation_per_galaxy.csv
  outputs/inclination_perturbation_log.txt

Resume support: re-running picks up where you left off.
"""

import os
import sys
import time
import csv
import multiprocessing as mp
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd


# ============================================================================
# CONFIGURATION
# ============================================================================

USING_REFERENCE_IMPLEMENTATION = False
V7_FITTER_DIR = "./scripts"
SPARC_CATALOG_PATH = '/Users/ronbibb/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/shell_reality_v2/data/galaxy_classifications.csv'


UPSILON_DISK_NOMINAL  = 0.5
UPSILON_BULGE_NOMINAL = 0.7

# Floor and cap on perturbed inclination to avoid pathological 1/sin(i)
INC_MIN_FLOOR_DEG = 10.0   # SPARC selection effectively excludes < 30° anyway
INC_MAX_CAP_DEG   = 89.0   # avoid singularity at 90°


def resolve_paths():
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    canonical = pkg_root / "data" / "sparc_T2-T9_canonical_fits.csv"
    rotmod    = pkg_root.parent / "Rotmod_LTG"
    outputs   = pkg_root / "outputs"
    if canonical.exists() and rotmod.exists():
        return canonical, rotmod, outputs
    cwd = Path.cwd()
    if (cwd / "sparc_T2-T9_canonical_fits.csv").exists():
        return (cwd / "sparc_T2-T9_canonical_fits.csv",
                cwd / "Rotmod_LTG",
                cwd / "outputs")
    return canonical, rotmod, outputs


def find_v7_fitter_dir():
    if V7_FITTER_DIR is not None:
        d = Path(V7_FITTER_DIR).expanduser().resolve()
        if (d / "run_canonical_fits.py").exists():
            return d
        raise FileNotFoundError(
            f"V7_FITTER_DIR is set to '{V7_FITTER_DIR}' but "
            f"run_canonical_fits.py was not found there."
        )
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    academic = pkg_root.parent
    candidates = [pkg_root, academic, pkg_root / "scripts", Path.cwd()]
    for cand in candidates:
        if (cand / "run_canonical_fits.py").exists():
            return cand
    raise FileNotFoundError(
        "run_canonical_fits.py not found. Set V7_FITTER_DIR.\n"
        f"Searched: {[str(c) for c in candidates]}"
    )


def find_sparc_catalog():
    """Locate sparc_sample123.csv or galaxy_classifications.csv (for Inc, e_Inc)."""
    if SPARC_CATALOG_PATH is not None:
        p = Path(SPARC_CATALOG_PATH).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"SPARC_CATALOG_PATH set to '{SPARC_CATALOG_PATH}' but file not found.")
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    academic = pkg_root.parent
    try:
        v7dir = find_v7_fitter_dir()
    except FileNotFoundError:
        v7dir = None
    # Try sparc_sample123.csv first, then galaxy_classifications.csv
    candidates = []
    for fname in ['sparc_sample123.csv', 'galaxy_classifications.csv']:
        candidates += [
            pkg_root / "data" / fname,
            pkg_root / fname,
            academic / fname,
            Path.cwd() / fname,
        ]
        if v7dir is not None:
            candidates += [v7dir / fname, v7dir.parent / fname,
                           v7dir.parent / "data" / fname]
    for cand in candidates:
        if cand.exists():
            return cand
    raise FileNotFoundError(
        "Neither sparc_sample123.csv nor galaxy_classifications.csv found. "
        "Set SPARC_CATALOG_PATH.\n"
        f"Searched: {[str(c) for c in candidates[:8]]}..."
    )


# ============================================================================
# v7.0 PRODUCTION FITTER WRAPPER (perturbed inclination)
# ============================================================================

def _run_v7(galaxy, rotmod_path, Inc_nominal, Inc_perturbed):
    """Fit one galaxy with perturbed inclination. Returns harness dict."""
    fitter_dir = find_v7_fitter_dir()
    if str(fitter_dir) not in sys.path:
        sys.path.insert(0, str(fitter_dir))
    import run_canonical_fits as rcf

    if not Path(rotmod_path).exists():
        return {'status': 'no_rotmod', 'n_shells': -1}

    d = np.loadtxt(rotmod_path, comments='#')
    r_all, vobs_all, evobs_all = d[:, 0], d[:, 1], d[:, 2]
    vgas, vdisk, vbul = d[:, 3], d[:, 4], d[:, 5]

    # Inclination perturbation: v_los is invariant, V_obs deprojects as 1/sin(i)
    sin_nom = np.sin(np.deg2rad(Inc_nominal))
    sin_new = np.sin(np.deg2rad(Inc_perturbed))
    vobs_factor = sin_nom / sin_new   # >1 if Inc_new < Inc_nominal (more deprojection)

    vobs_pert  = vobs_all  * vobs_factor
    evobs_pert = evobs_all * vobs_factor
    # r, V_gas, V_disk, V_bulge unchanged (computed from photometry, not deprojection)

    # V_bar^2 with NOMINAL Upsilons (unchanged in this test)
    V2_bar_all = (vgas  * np.abs(vgas)
                  + UPSILON_DISK_NOMINAL  * vdisk * np.abs(vdisk)
                  + UPSILON_BULGE_NOMINAL * vbul  * np.abs(vbul))

    # Mask using PERTURBED V_obs
    mask = vobs_pert**2 > V2_bar_all
    n_used = int(mask.sum())
    if n_used < 5:
        return {'status': 'insufficient_DM_points', 'n_shells': -1}

    r      = r_all[mask]
    vobs   = vobs_pert[mask]
    evobs  = evobs_pert[mask]
    V2_bar = V2_bar_all[mask]
    sig    = np.maximum(evobs, rcf.SIGMA_V_FLOOR)

    p_burk, chi2_n0 = rcf.fit_burkert(r, vobs, sig, V2_bar)
    p_fw1,  chi2_n1 = rcf.fit_fw_n_shells(r, vobs, sig, V2_bar, 1)
    p_fw2,  chi2_n2 = rcf.fit_fw_n_shells(r, vobs, sig, V2_bar, 2)

    branches = []
    if p_burk is not None: branches.append((0, p_burk, chi2_n0, 2))
    if p_fw1  is not None: branches.append((1, p_fw1,  chi2_n1, 5))
    if p_fw2  is not None: branches.append((2, p_fw2,  chi2_n2, 8))

    if not branches:
        return {'status': 'all_fits_failed', 'n_shells': -1}

    branches_bic = [
        (n, p, chi2, k,
         rcf.bic_of(chi2, n_used, k),
         rcf.chi2_red_of(chi2, n_used, k))
        for (n, p, chi2, k) in branches
    ]
    n_shells, p_best, chi2_best, k_best, bic_best, chi2_red_best = min(
        branches_bic, key=lambda x: x[4]
    )

    out = {
        'status': 'ok', 'n_shells': int(n_shells), 'n_points': n_used,
        'rho0': float(p_best[0]), 'a_kpc': float(p_best[1]),
        'chi2': float(chi2_best),
        'chi2_red': float(chi2_red_best),
        'bic': float(bic_best),
        'r_sh1': None, 'M_sh1': None, 'sigma_sh1': None,
        'r_sh2': None, 'M_sh2': None, 'sigma_sh2': None,
    }
    if n_shells >= 1:
        out['M_sh1']     = float(p_best[2])
        out['r_sh1']     = float(p_best[3])
        out['sigma_sh1'] = float(p_best[4])
    if n_shells >= 2:
        out['M_sh2']     = float(p_best[5])
        out['r_sh2']     = float(p_best[6])
        out['sigma_sh2'] = float(p_best[7])
    return out


# ============================================================================
# REFERENCE FITTER (for harness testing — NOT v7.0)
# ============================================================================

def _run_reference(galaxy, rotmod_path, Inc_nominal, Inc_perturbed):
    from scipy.optimize import minimize
    from math import erf
    G = 4.302e-6
    SIGMA_OVER_R_MAX = 0.4
    N_RESTARTS = 12
    erf_v = np.vectorize(erf)

    if not Path(rotmod_path).exists():
        return {'status': 'no_rotmod', 'n_shells': -1}
    d = np.loadtxt(rotmod_path, comments='#')
    r = d[:, 0]; V_obs_orig = d[:, 1]; e_V_orig = np.maximum(d[:, 2], 1.0)
    V_gas, V_disk, V_bulge = d[:, 3], d[:, 4], d[:, 5]
    sin_nom = np.sin(np.deg2rad(Inc_nominal))
    sin_new = np.sin(np.deg2rad(Inc_perturbed))
    factor = sin_nom / sin_new
    V_obs = V_obs_orig * factor
    e_V = e_V_orig * factor
    V_bar2 = (V_gas*np.abs(V_gas)
              + UPSILON_DISK_NOMINAL  * V_disk *np.abs(V_disk)
              + UPSILON_BULGE_NOMINAL * V_bulge*np.abs(V_bulge))
    V_DM2 = V_obs**2 - V_bar2
    mask = V_DM2 > 0
    if mask.sum() < 5:
        return {'status': 'insufficient_DM_points', 'n_shells': -1}
    r_use, V_DM2_use = r[mask], V_DM2[mask]
    sigma_V2 = (2 * V_obs[mask] * e_V[mask])**2

    def burkert_v2(rr, rho0, a):
        a = max(a, 1e-6); x = rr / a
        M = np.pi * rho0 * a**3 * (np.log(1+x**2) + 2*np.log(1+x) - 2*np.arctan(x))
        return G * M / np.maximum(rr, 1e-6)
    def shell_v2(rr, r_sh, M_sh, ss):
        M_enc = 0.5 * M_sh * (1 + erf_v((rr - r_sh) / (np.sqrt(2) * ss)))
        return G * M_enc / np.maximum(rr, 1e-6)
    def fit_n(n_shells):
        r_min, r_max = r_use.min(), r_use.max()
        def obj(p):
            log_rho0, log_a = p[0], p[1]
            rho0, a = 10**log_rho0, 10**log_a
            if a < 0.01 or a > 200 or rho0 < 1e4 or rho0 > 1e11: return 1e12
            shells = []
            for i in range(n_shells):
                r_sh = p[2+3*i]; M_sh = 10**p[3+3*i]; sf = 10**p[4+3*i]
                if sf > SIGMA_OVER_R_MAX: return 1e12
                if r_sh < r_min*0.5 or r_sh > r_max*1.2: return 1e12
                if M_sh < 1e6 or M_sh > 1e13: return 1e12
                shells.append((r_sh, M_sh, sf*r_sh))
            V2 = burkert_v2(r_use, rho0, a)
            for rs, Ms, ss in shells:
                V2 = V2 + shell_v2(r_use, rs, Ms, ss)
            return np.sum((V_DM2_use - V2)**2 / sigma_V2)
        best = (None, None, [], np.inf)
        for _ in range(N_RESTARTS):
            x0 = [np.random.uniform(6.5, 9.0), np.random.uniform(0.0, 1.5)]
            for _ in range(n_shells):
                x0.append(np.random.uniform(r_min, r_max*0.8))
                x0.append(np.random.uniform(8.5, 10.5))
                x0.append(np.random.uniform(-1.5, np.log10(SIGMA_OVER_R_MAX*0.99)))
            try:
                res = minimize(obj, x0, method='Nelder-Mead',
                               options={'xatol': 1e-4, 'fatol': 1e-2, 'maxiter': 5000})
                if res.fun < best[3]:
                    rho0, a = 10**res.x[0], 10**res.x[1]
                    shells = []; valid = True
                    for i in range(n_shells):
                        r_sh = res.x[2+3*i]; M_sh = 10**res.x[3+3*i]
                        ss = (10**res.x[4+3*i]) * r_sh
                        if ss/r_sh > SIGMA_OVER_R_MAX: valid = False
                        shells.append((r_sh, M_sh, ss))
                    if valid: best = (rho0, a, shells, res.fun)
            except Exception:
                continue
        return best
    n_pts = len(r_use)
    best_n, best_bic, best_result = 0, np.inf, None
    for n in [0, 1, 2]:
        rho0, a, shells, chi2 = fit_n(n)
        if rho0 is None: continue
        bic = chi2 + (2 + 3*n) * np.log(n_pts)
        if bic < best_bic:
            best_bic = bic; best_n = n; best_result = (rho0, a, shells, chi2)
    if best_result is None:
        return {'status': 'fit_failed', 'n_shells': -1}
    rho0, a, shells, chi2 = best_result
    chi2_red = chi2 / max(n_pts - (2 + 3*best_n), 1)
    out = {
        'status': 'ok', 'n_shells': best_n, 'n_points': n_pts,
        'rho0': rho0, 'a_kpc': a,
        'chi2': chi2, 'chi2_red': chi2_red, 'bic': best_bic,
        'r_sh1': None, 'M_sh1': None, 'sigma_sh1': None,
        'r_sh2': None, 'M_sh2': None, 'sigma_sh2': None,
    }
    if len(shells) >= 1: out['r_sh1'], out['M_sh1'], out['sigma_sh1'] = shells[0]
    if len(shells) >= 2: out['r_sh2'], out['M_sh2'], out['sigma_sh2'] = shells[1]
    return out


def run_v7_framework(galaxy, rotmod_path, Inc_nominal, Inc_perturbed):
    if USING_REFERENCE_IMPLEMENTATION:
        return _run_reference(galaxy, rotmod_path, Inc_nominal, Inc_perturbed)
    return _run_v7(galaxy, rotmod_path, Inc_nominal, Inc_perturbed)


# ============================================================================
# HARNESS
# ============================================================================

CSV_COLUMNS = [
    'Galaxy', 'realization',
    'Inc_nominal_deg', 'Inc_perturbed_deg', 'e_Inc_deg', 'vobs_factor',
    'status', 'n_shells', 'n_points',
    'rho0', 'a_kpc', 'chi2', 'chi2_red', 'bic',
    'r_sh1', 'M_sh1', 'sigma_sh1', 'sigma_over_r1',
    'r_sh2', 'M_sh2', 'sigma_sh2', 'sigma_over_r2',
]


def fit_one_task(args):
    galaxy, rea_idx, Inc_nom, Inc_pert, e_Inc, rotmod_dir = args
    rotmod_path = str(Path(rotmod_dir) / f"{galaxy}_rotmod.dat")
    np.random.seed((rea_idx * 100003 + abs(hash(galaxy))) % (2**31))

    try:
        result = run_v7_framework(galaxy, rotmod_path, Inc_nom, Inc_pert)
    except Exception as e:
        result = {'status': f'exception: {str(e)[:120]}', 'n_shells': -1}

    sin_nom = np.sin(np.deg2rad(Inc_nom))
    sin_new = np.sin(np.deg2rad(Inc_pert))
    vobs_factor = sin_nom / sin_new

    def ratio(num, den):
        if num is None or den is None or den == 0: return None
        return num / den

    return {
        'Galaxy': galaxy,
        'realization': rea_idx,
        'Inc_nominal_deg': Inc_nom,
        'Inc_perturbed_deg': Inc_pert,
        'e_Inc_deg': e_Inc,
        'vobs_factor': vobs_factor,
        'status': result.get('status', 'unknown'),
        'n_shells': result.get('n_shells', -1),
        'n_points': result.get('n_points'),
        'rho0': result.get('rho0'),
        'a_kpc': result.get('a_kpc'),
        'chi2': result.get('chi2'),
        'chi2_red': result.get('chi2_red'),
        'bic': result.get('bic'),
        'r_sh1':         result.get('r_sh1'),
        'M_sh1':         result.get('M_sh1'),
        'sigma_sh1':     result.get('sigma_sh1'),
        'sigma_over_r1': ratio(result.get('sigma_sh1'), result.get('r_sh1')),
        'r_sh2':         result.get('r_sh2'),
        'M_sh2':         result.get('M_sh2'),
        'sigma_sh2':     result.get('sigma_sh2'),
        'sigma_over_r2': ratio(result.get('sigma_sh2'), result.get('r_sh2')),
    }


def append_row(csv_path, row, write_header):
    mode = 'w' if write_header else 'a'
    with open(csv_path, mode, newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction='ignore')
        if write_header: writer.writeheader()
        writer.writerow(row)
        f.flush()
        os.fsync(f.fileno())


def already_done(csv_path):
    if not Path(csv_path).exists():
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(zip(df['Galaxy'], df['realization']))
    except Exception:
        return set()


def log(log_path, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}"
    print(line, flush=True)
    with open(log_path, 'a') as f:
        f.write(line + '\n')


def banner_lines():
    if USING_REFERENCE_IMPLEMENTATION:
        return [
            "******************************************************************",
            "*** WARNING: USING REFERENCE FITTER (NOT v7.0 PRODUCTION CODE) ***",
            "******************************************************************",
        ]
    return [
        "==================================================================",
        "=== INCLINATION PERTURBATION TEST                               ===",
        "=== USING v7.0 PRODUCTION FITTER (run_canonical_fits.py)        ===",
        "=== Per-galaxy Inc draws from N(Inc, e_Inc) using SPARC catalog.===",
        "==================================================================",
    ]


def main():
    n_realizations = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    seed           = int(sys.argv[2]) if len(sys.argv) > 2 else 20260510

    canonical, rotmod_dir, output_dir = resolve_paths()
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / 'inclination_perturbation_per_galaxy.csv'
    log_path = output_dir / 'inclination_perturbation_log.txt'

    log(log_path, "=== Inclination perturbation test starting ===")
    for ln in banner_lines():
        log(log_path, ln)

    if not USING_REFERENCE_IMPLEMENTATION:
        try:
            v7_dir = find_v7_fitter_dir()
            log(log_path, f"  v7.0 fitter dir   = {v7_dir}")
        except FileNotFoundError as e:
            log(log_path, f"ERROR: {e}")
            sys.exit(1)

    try:
        sparc_path = find_sparc_catalog()
        log(log_path, f"  SPARC catalog     = {sparc_path}")
    except FileNotFoundError as e:
        log(log_path, f"ERROR: {e}")
        sys.exit(1)

    log(log_path, f"  N_realizations    = {n_realizations}")
    log(log_path, f"  seed              = {seed}")
    log(log_path, f"  canonical CSV     = {canonical}")
    log(log_path, f"  rotmod dir        = {rotmod_dir}")
    log(log_path, f"  output dir        = {output_dir}")
    log(log_path, f"  Inc floor / cap   = {INC_MIN_FLOOR_DEG}° / {INC_MAX_CAP_DEG}°")

    if not canonical.exists():
        log(log_path, f"ERROR: canonical CSV not found at {canonical}")
        sys.exit(1)
    if not rotmod_dir.exists():
        log(log_path, f"ERROR: rotmod dir not found at {rotmod_dir}")
        sys.exit(1)

    df_canon = pd.read_csv(canonical)
    galaxies = df_canon['Galaxy'].tolist()
    log(log_path, f"  N galaxies        = {len(galaxies)}")

    sparc = pd.read_csv(sparc_path)[['Galaxy', 'Inc', 'e_Inc']].set_index('Galaxy')
    missing = [g for g in galaxies if g not in sparc.index]
    if missing:
        log(log_path, f"WARNING: {len(missing)} galaxies missing from catalog: {missing[:5]}")

    done = already_done(csv_path)
    if done:
        log(log_path, f"  Resuming: {len(done)} (galaxy, realization) pairs already done")
    write_header = not csv_path.exists()

    rng = np.random.default_rng(seed)
    log(log_path, "  Generating per-galaxy inclination perturbations...")
    perturbations = {}  # (galaxy, rea_idx) -> (Inc_nom, Inc_pert, e_Inc)
    e_Inc_values = []
    Inc_values = []
    for rea_idx in range(n_realizations):
        for galaxy in galaxies:
            if galaxy not in sparc.index:
                continue
            Inc_nom = float(sparc.loc[galaxy, 'Inc'])
            e_Inc   = float(sparc.loc[galaxy, 'e_Inc'])
            if not (0 < Inc_nom < 90):
                continue
            # Additive Gaussian perturbation in degrees, floored and capped
            delta = rng.normal(0, max(e_Inc, 1e-6))
            Inc_pert = float(np.clip(Inc_nom + delta, INC_MIN_FLOOR_DEG, INC_MAX_CAP_DEG))
            perturbations[(galaxy, rea_idx)] = (Inc_nom, Inc_pert, e_Inc)
            if rea_idx == 0:
                e_Inc_values.append(e_Inc)
                Inc_values.append(Inc_nom)

    if e_Inc_values:
        e_arr = np.array(e_Inc_values)
        i_arr = np.array(Inc_values)
        log(log_path, f"  Per-galaxy inclination uncertainty (e_Inc):")
        log(log_path, f"    median: {np.median(e_arr):.2f}°, mean: {e_arr.mean():.2f}°, "
                      f"min: {e_arr.min():.2f}°, max: {e_arr.max():.2f}°")
        log(log_path, f"  Per-galaxy inclination (Inc):")
        log(log_path, f"    median: {np.median(i_arr):.1f}°, "
                      f"min: {i_arr.min():.1f}°, max: {i_arr.max():.1f}°")

    all_tasks = []
    for (galaxy, rea_idx), (Inc_nom, Inc_pert, e_Inc) in perturbations.items():
        if (galaxy, rea_idx) in done:
            continue
        all_tasks.append((galaxy, rea_idx, Inc_nom, Inc_pert, e_Inc, str(rotmod_dir)))

    log(log_path, f"  Tasks to run     = {len(all_tasks)}")
    if not all_tasks:
        log(log_path, "Nothing to do; all (galaxy, realization) pairs complete.")
        return

    n_cores = max(1, mp.cpu_count() - 1)
    log(log_path, f"  Parallel workers = {n_cores}")
    log(log_path, "  Beginning fits. Each row written to CSV as it completes.")

    t0 = time.time()
    n_done_session = 0
    n_total = len(all_tasks)

    with mp.Pool(n_cores) as pool:
        for row in pool.imap_unordered(fit_one_task, all_tasks, chunksize=1):
            append_row(csv_path, row, write_header)
            write_header = False
            n_done_session += 1
            if n_done_session % 20 == 0 or n_done_session == n_total:
                elapsed = time.time() - t0
                rate = n_done_session / elapsed if elapsed > 0 else 0
                eta = (n_total - n_done_session) / rate if rate > 0 else float('inf')
                log(log_path, f"  Progress: {n_done_session}/{n_total} "
                              f"({n_done_session/n_total*100:.1f}%)  "
                              f"rate={rate:.2f} fits/sec  ETA={eta/60:.1f} min")

    elapsed = time.time() - t0
    log(log_path, f"=== Done. {n_done_session} fits in this session, "
                  f"{elapsed/60:.1f} min total (avg {elapsed/n_done_session:.1f} sec/fit) ===")

    df_full = pd.read_csv(csv_path)
    log(log_path, f"Total rows in CSV: {len(df_full)}")
    log(log_path, f"Status counts: {df_full['status'].value_counts().to_dict()}")
    ok = df_full[df_full['status'] == 'ok']
    if len(ok):
        log(log_path, "n_shells distribution (all realizations, all galaxies):")
        for n, cnt in ok['n_shells'].value_counts().sort_index().items():
            log(log_path, f"  n_shells={n}: {cnt} ({cnt/len(ok)*100:.1f}%)")


if __name__ == '__main__':
    main()

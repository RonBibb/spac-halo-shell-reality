#!/usr/bin/env python3
"""
covariate_matched_quality.py — Paper II §3.3.7 follow-up

After the initial covariate_model.py result showed T-type non-significant
(β = -0.044, p = 0.93), this script tests whether the T → shell-bearing
relationship is structurally confounded with observational quality covariates,
or merely obscured by their collinearity within SPARC.

Strategy: subsample the 102-galaxy sample into "high-quality" subsets where
the T-quality correlation is weaker than in the full sample, then re-run the
same logistic regression. If T survives in matched-quality subsamples,
the full-sample result reflects T-quality collinearity rather than a true
absence of morphological effect. If T does not survive even in matched
subsamples, the confounding is structural and §3.1 needs reframing.

Four subsamples evaluated:
  (A) Top half by log_N_pts (median split)
  (B) Bottom half by log_mean_V_err (median split, lower err = better)
  (C) Both A and B simultaneously (the strictest quality cut)
  (D) Within-T top half by log_N_pts (preserves T-range while removing
      within-bin quality variation)

For each subsample we report:
  - Sample size and T-distribution
  - Spearman T–quality correlation (should weaken vs full sample)
  - Logistic regression coefficient and p-value for T_z

Inputs (paths relative to repo root):
  ./data/sparc_T2-T9_canonical_fits.csv
  ./data/sparc_sample123.csv
  ./data/galaxy_classifications.csv
  ../Rotmod_LTG/<Galaxy>_rotmod.dat

Outputs (to ./data/):
  covariate_matched_results.csv     — coefficient tables for each subsample
  covariate_matched_summary.txt     — formatted text summary

Sample convention: matches §3.3.5 primary (102-gal, NGC 6674 included).

Author: Ron Bibb
Date: 2026-05-23
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# ---------------------------------------------------------------------------
# Configuration (identical to covariate_model.py)
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
DATA_DIR = PACKAGE_ROOT / "data"
ROTMOD_DIR = Path("../Rotmod_LTG")

CANONICAL_CSV = DATA_DIR / "sparc_T2-T9_canonical_fits.csv"
SAMPLE_CSV    = DATA_DIR / "sparc_sample123.csv"
CLASSIF_CSV   = DATA_DIR / "galaxy_classifications.csv"

OUT_RESULTS = DATA_DIR / "covariate_matched_results.csv"
OUT_SUMMARY = DATA_DIR / "covariate_matched_summary.txt"

EXCLUDE_GALAXIES = ['6674']
T_MIN, T_MAX = 2, 9

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

ROTMOD_COLNAMES = ['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul']
Z_PREDICTORS = ['T_z', 'is_bulge_dom', 'log_N_pts_z', 'log_mean_V_err_z',
                'cos_inc_z', 'log_L36_z']

# ---------------------------------------------------------------------------
# Data loading (mirrors covariate_model.py)
# ---------------------------------------------------------------------------

def load_rotmod(galaxy):
    fp = ROTMOD_DIR / f"{galaxy}_rotmod.dat"
    if not fp.exists():
        return None
    try:
        return pd.read_csv(fp, sep=r'\s+', comment='#', names=ROTMOD_COLNAMES)
    except Exception:
        return None


def rotmod_covariates(galaxy):
    rotmod = load_rotmod(galaxy)
    if rotmod is None or len(rotmod) == 0:
        return {'N_pts': np.nan, 'mean_V_err': np.nan}
    return {'N_pts': len(rotmod), 'mean_V_err': float(rotmod['errV'].mean())}


def build_design_matrix(canonical, sample, classif):
    sample_T = sample[(sample['T'] >= T_MIN) & (sample['T'] <= T_MAX)].copy()
    sample_T = sample_T[~sample_T['Galaxy'].isin(EXCLUDE_GALAXIES)]

    target = canonical[['Galaxy', 'fw_best_n_shells']].copy()
    target['is_SB'] = (target['fw_best_n_shells'] > 0).astype(int)
    df = sample_T.merge(target[['Galaxy', 'is_SB']], on='Galaxy', how='left')
    df = df.dropna(subset=['is_SB'])

    df = df.merge(classif[['Galaxy', 'is_bulge_dom']], on='Galaxy', how='left')
    df['is_bulge_dom'] = df['is_bulge_dom'].fillna(False).astype(int)

    log.info(f"  Reading {len(df)} rotmod files for N_pts / V_err covariates...")
    rotmod_data = [rotmod_covariates(g) for g in df['Galaxy']]
    df['N_pts'] = [d['N_pts'] for d in rotmod_data]
    df['mean_V_err'] = [d['mean_V_err'] for d in rotmod_data]

    df = df.dropna(subset=['N_pts', 'mean_V_err', 'Inc', 'L36']).reset_index(drop=True)

    df['log_N_pts']      = np.log10(df['N_pts'])
    df['log_mean_V_err'] = np.log10(df['mean_V_err'].clip(lower=0.1))
    df['cos_inc']        = np.cos(np.radians(df['Inc']))
    df['log_L36']        = np.log10(df['L36'].clip(lower=1e-4))

    return df


def standardize_on_subsample(df_sub):
    """Z-standardize continuous predictors on the subsample itself."""
    continuous = ['T', 'log_N_pts', 'log_mean_V_err', 'cos_inc', 'log_L36']
    std = df_sub.copy()
    for col in continuous:
        mu, sd = df_sub[col].mean(), df_sub[col].std()
        std[f'{col}_z'] = (df_sub[col] - mu) / sd if sd > 0 else 0.0
    return std


# ---------------------------------------------------------------------------
# Subsample definitions
# ---------------------------------------------------------------------------

def define_subsamples(df):
    """Return dict of {label: boolean_mask} for the four matched subsamples."""
    med_npts = df['log_N_pts'].median()
    med_verr = df['log_mean_V_err'].median()

    sub_A = df['log_N_pts'] >= med_npts
    sub_B = df['log_mean_V_err'] <= med_verr
    sub_C = sub_A & sub_B

    # Within-T top half by log_N_pts
    sub_D = pd.Series(False, index=df.index)
    for T in range(T_MIN, T_MAX + 1):
        T_mask = (df['T'] == T)
        if T_mask.sum() < 2:
            sub_D.loc[T_mask] = True   # keep all if 0-1 galaxies in bin
            continue
        T_median = df.loc[T_mask, 'log_N_pts'].median()
        sub_D.loc[T_mask & (df['log_N_pts'] >= T_median)] = True

    return {
        'FULL':                 pd.Series(True, index=df.index),
        'A_top_Npts':           sub_A,
        'B_bot_Verr':           sub_B,
        'C_both_quality_cuts':  sub_C,
        'D_within_T_top_Npts':  sub_D,
    }


# ---------------------------------------------------------------------------
# Logistic regression
# ---------------------------------------------------------------------------

def fit_logistic_subsample(df_sub):
    """Fit logistic on a standardized subsample. Returns coefficient DataFrame."""
    try:
        import statsmodels.api as sm
    except ImportError:
        log.error("statsmodels missing. pip install statsmodels")
        sys.exit(1)

    std = standardize_on_subsample(df_sub)
    X = std[Z_PREDICTORS].values
    y = df_sub['is_SB'].values.astype(int)

    # Guard against perfect separation or degenerate cases
    if len(np.unique(y)) < 2:
        return None, None, "single-class subsample"
    if len(df_sub) <= len(Z_PREDICTORS) + 1:
        return None, None, f"underdetermined: n={len(df_sub)} <= p+1"

    X_const = sm.add_constant(X, prepend=True)
    try:
        model = sm.Logit(y, X_const)
        result = model.fit(disp=False, method='bfgs', maxiter=500)
    except Exception as e:
        return None, None, f"fit failed: {e}"

    rows = []
    names = ['(intercept)'] + Z_PREDICTORS
    for i, name in enumerate(names):
        rows.append({
            'predictor': name,
            'coef': result.params[i],
            'se': result.bse[i],
            'z': result.tvalues[i],
            'p_value': result.pvalues[i],
        })
    return pd.DataFrame(rows), result, None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_summary(df, subsamples, all_results, fout):
    lines = []
    lines.append("=" * 78)
    lines.append("MATCHED-QUALITY COVARIATE TEST — Paper II §3.3.7 follow-up")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Question: does T-type retain predictive power after partialling out")
    lines.append("observational quality covariates IN SUBSAMPLES WHERE T-quality")
    lines.append("correlation is reduced?")
    lines.append("")
    lines.append("Full-sample T-quality correlations (Spearman):")
    for col in ['log_N_pts', 'log_mean_V_err', 'log_L36', 'cos_inc']:
        rho, p = spearmanr(df['T'], df[col])
        lines.append(f"  T vs {col:<18s}  ρ = {rho:+.3f}  p = {p:.3g}")
    lines.append("")

    # T-distribution and T-quality correlations by subsample
    lines.append("=" * 78)
    lines.append("SUBSAMPLE PROPERTIES")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"  {'Subsample':<25s} {'n':>5s} {'n_SB':>5s} "
                 f"{'T_range':>10s} {'ρ(T,Npts)':>11s} {'ρ(T,Verr)':>11s}")
    lines.append("  " + "-" * 73)
    for label, mask in subsamples.items():
        sub = df[mask]
        n = len(sub)
        n_sb = int(sub['is_SB'].sum())
        T_range = f"{int(sub['T'].min())}-{int(sub['T'].max())}"
        if n >= 4:
            rho_n, _ = spearmanr(sub['T'], sub['log_N_pts'])
            rho_v, _ = spearmanr(sub['T'], sub['log_mean_V_err'])
        else:
            rho_n, rho_v = np.nan, np.nan
        lines.append(f"  {label:<25s} {n:>5d} {n_sb:>5d} "
                     f"{T_range:>10s} {rho_n:>+11.3f} {rho_v:>+11.3f}")
    lines.append("")

    # Logistic results per subsample (T_z coefficient extracted)
    lines.append("=" * 78)
    lines.append("LOGISTIC REGRESSION: T_z COEFFICIENT BY SUBSAMPLE")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"  {'Subsample':<25s} {'n':>5s} "
                 f"{'T_z coef':>10s} {'SE':>8s} {'z':>8s} {'p':>10s} {'sig':>5s}")
    lines.append("  " + "-" * 74)
    for label, mask in subsamples.items():
        sub = df[mask]
        result_df, _, err = all_results[label]
        if err is not None:
            lines.append(f"  {label:<25s} {len(sub):>5d}   [SKIPPED — {err}]")
            continue
        T_row = result_df[result_df['predictor'] == 'T_z'].iloc[0]
        sig = '***' if T_row['p_value'] < 0.001 else ('**' if T_row['p_value'] < 0.01
                  else ('*' if T_row['p_value'] < 0.05 else ''))
        lines.append(
            f"  {label:<25s} {len(sub):>5d} "
            f"{T_row['coef']:>+10.3f} {T_row['se']:>8.3f} {T_row['z']:>+8.2f} "
            f"{T_row['p_value']:>10.4g} {sig:>5s}"
        )
    lines.append("")

    # Interpretation
    lines.append("=" * 78)
    lines.append("INTERPRETATION")
    lines.append("=" * 78)
    lines.append("")
    full_result, _, _ = all_results['FULL']
    full_T = full_result[full_result['predictor'] == 'T_z'].iloc[0]

    survives_any = False
    for label in ['A_top_Npts', 'B_bot_Verr', 'C_both_quality_cuts', 'D_within_T_top_Npts']:
        result_df, _, err = all_results[label]
        if err is not None:
            continue
        T_row = result_df[result_df['predictor'] == 'T_z'].iloc[0]
        if T_row['p_value'] < 0.05:
            survives_any = True
            break

    lines.append(f"  Full sample T_z: β = {full_T['coef']:+.3f}, p = {full_T['p_value']:.3g}")
    lines.append("")
    if survives_any:
        lines.append("  T-type SURVIVES in at least one matched-quality subsample.")
        lines.append("  Interpretation: the full-sample non-significance of T-type reflects")
        lines.append("  T-quality COLLINEARITY in SPARC, not absence of a morphological effect.")
        lines.append("  When the T-quality correlation is reduced via subsampling, the T")
        lines.append("  coefficient becomes detectable. §3.3.7 framing: 'the gradient survives")
        lines.append("  matched-quality control, indicating that T-type and observational")
        lines.append("  quality cannot be cleanly separated in this sample but the morphology")
        lines.append("  effect is consistent with being real.'")
    else:
        lines.append("  T-type DOES NOT SURVIVE in any matched-quality subsample.")
        lines.append("  Interpretation: the confounding between T-type and observational")
        lines.append("  quality is structural in SPARC. The galaxy-level morphology gradient")
        lines.append("  cannot be cleanly separated from data-quality covariates. §3.1's")
        lines.append("  framing should be revised: report the T-correlated shell-bearing rate")
        lines.append("  as a sample-level regularity that is statistically inseparable from")
        lines.append("  observational covariates, not as a clean morphological effect.")
    lines.append("")
    lines.append("  Note: per-shell findings (M-r, σ-r, inner-vs-outer, σ/r) are unaffected.")
    lines.append("  This result concerns galaxy-level shell-bearing classification only.")
    lines.append("")

    Path(fout).write_text("\n".join(lines))
    log.info(f"  Wrote {fout}")
    print("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=" * 70)
    log.info("Paper II §3.3.7 — Matched-quality covariate test")
    log.info("=" * 70)

    log.info("Loading inputs...")
    canonical = pd.read_csv(CANONICAL_CSV)
    sample = pd.read_csv(SAMPLE_CSV)
    classif = pd.read_csv(CLASSIF_CSV)

    log.info("Building design matrix...")
    df = build_design_matrix(canonical, sample, classif)
    log.info(f"  Final sample: n = {len(df)} galaxies, "
             f"{int(df['is_SB'].sum())} shell-bearing")

    log.info("Defining subsamples...")
    subsamples = define_subsamples(df)
    for label, mask in subsamples.items():
        log.info(f"  {label}: n = {int(mask.sum())}")

    log.info("Fitting logistic on each subsample...")
    all_results = {}
    for label, mask in subsamples.items():
        sub = df[mask].reset_index(drop=True)
        result_df, model, err = fit_logistic_subsample(sub)
        all_results[label] = (result_df, model, err)
        if err is None and result_df is not None:
            T_row = result_df[result_df['predictor'] == 'T_z'].iloc[0]
            log.info(f"  {label}: T_z = {T_row['coef']:+.3f} (p = {T_row['p_value']:.4g})")
        else:
            log.info(f"  {label}: {err}")

    # Combine results into one CSV
    long_rows = []
    for label, (result_df, _, err) in all_results.items():
        if err is not None:
            continue
        tmp = result_df.copy()
        tmp.insert(0, 'subsample', label)
        long_rows.append(tmp)
    if long_rows:
        combined = pd.concat(long_rows, ignore_index=True)
        combined.to_csv(OUT_RESULTS, index=False, float_format='%.6f')
        log.info(f"  Wrote {OUT_RESULTS}")

    log.info("Writing summary...")
    write_summary(df, subsamples, all_results, OUT_SUMMARY)
    log.info("Done.")


if __name__ == "__main__":
    main()

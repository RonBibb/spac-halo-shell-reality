#!/usr/bin/env python3
"""
covariate_model.py — Paper II §3.3.7 multivariate covariate control

Pure analysis script (no rotation-curve fitting). Tests whether the morphology
gradient (T-type) retains predictive power for shell-bearing classification
after statistical control for plausibly-confounded covariates:

  - T-type (the headline predictor)
  - Bulge dominance flag
  - log N_RC_points (rotation-curve sampling)
  - log <V_err> (mean rotation-curve uncertainty)
  - cos(inclination)
  - log L_3.6μm (stellar mass proxy)

Two parallel methods for cross-check:
  - Logistic regression (statsmodels.Logit): coefficient table with SE / p / CI
  - Random forest (sklearn): feature-importance ranking

Inputs (paths relative to repo root, scripts run as `python scripts/covariate_model.py`):
  ./data/sparc_T2-T9_canonical_fits.csv   (target: fw_best_n_shells > 0)
  ./data/sparc_sample123.csv              (T, inclination, distance, L36, etc.)
  ./data/galaxy_classifications.csv       (is_bulge_dom, is_bulgeless)
  ../Rotmod_LTG/<Galaxy>_rotmod.dat       (N_pts, <V_err> per galaxy)

Outputs (to ./data/):
  covariate_results.csv     — coefficient table + RF importances (long format)
  covariate_summary.txt     — formatted text summary for §3.3.7 prose

Sample convention: matches manuscript §3.3.5 primary convention
(102-galaxy T=2-9 sample, NGC 6674 included). Set EXCLUDE_GALAXIES = ['NGC6674']
to switch to the NGC 6674-excluded convention.

Author: Ron Bibb
Date: 2026-05-23
"""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
DATA_DIR = PACKAGE_ROOT / "data"
ROTMOD_DIR = PACKAGE_ROOT.parent / "Rotmod_LTG"   # sibling to repo per convention

CANONICAL_CSV = DATA_DIR / "sparc_T2-T9_canonical_fits.csv"
SAMPLE_CSV    = DATA_DIR / "sparc_sample123.csv"
CLASSIF_CSV   = DATA_DIR / "galaxy_classifications.csv"

OUT_RESULTS = DATA_DIR / "covariate_results.csv"
OUT_SUMMARY = DATA_DIR / "covariate_summary.txt"

# Sample convention — empty list = manuscript primary (NGC 6674 included)
EXCLUDE_GALAXIES = []

# T-type range for Paper II
T_MIN, T_MAX = 2, 9

# Random forest hyperparameters (modest tree count; deterministic)
RF_N_ESTIMATORS = 500
RF_RANDOM_STATE = 17

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Per-galaxy covariates from rotmod files
# ---------------------------------------------------------------------------

ROTMOD_COLNAMES = ['Rad', 'Vobs', 'errV', 'Vgas', 'Vdisk', 'Vbul', 'SBdisk', 'SBbul']


def load_rotmod(galaxy):
    """Load a SPARC Rotmod_<galaxy>.dat file, return DataFrame or None."""
    fp = ROTMOD_DIR / f"{galaxy}_rotmod.dat"
    if not fp.exists():
        log.warning(f"  Rotmod file missing for {galaxy}")
        return None
    try:
        df = pd.read_csv(fp, sep=r'\s+', comment='#', names=ROTMOD_COLNAMES)
        return df
    except Exception as e:
        log.warning(f"  Failed to read {fp.name}: {e}")
        return None


def rotmod_covariates(galaxy):
    """Compute N_pts and mean V_err from rotmod file. Returns dict."""
    rotmod = load_rotmod(galaxy)
    if rotmod is None or len(rotmod) == 0:
        return {'N_pts': np.nan, 'mean_V_err': np.nan}
    return {
        'N_pts': len(rotmod),
        'mean_V_err': float(rotmod['errV'].mean()),
    }


# ---------------------------------------------------------------------------
# Build design matrix
# ---------------------------------------------------------------------------

def build_design_matrix(canonical, sample, classif, exclude_galaxies):
    """Construct one row per galaxy with target + 6 standardized predictors."""
    # Restrict to T = 2-9
    sample_T = sample[(sample['T'] >= T_MIN) & (sample['T'] <= T_MAX)].copy()
    sample_T = sample_T[~sample_T['Galaxy'].isin(exclude_galaxies)]

    # Join target (is_shell_bearing) from canonical
    target = canonical[['Galaxy', 'fw_best_n_shells']].copy()
    target['is_SB'] = (target['fw_best_n_shells'] > 0).astype(int)
    df = sample_T.merge(target[['Galaxy', 'is_SB']], on='Galaxy', how='left')

    # Drop galaxies with missing target (not in canonical fits)
    n_before = len(df)
    df = df.dropna(subset=['is_SB'])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        log.info(f"  Dropped {n_dropped} galaxies missing from canonical fits")

    # Join bulge classification
    df = df.merge(classif[['Galaxy', 'is_bulge_dom']], on='Galaxy', how='left')
    df['is_bulge_dom'] = df['is_bulge_dom'].fillna(False).astype(int)

    # Compute per-galaxy rotmod covariates (N_pts, mean V_err)
    log.info(f"  Reading {len(df)} rotmod files for N_pts / V_err covariates...")
    rotmod_data = [rotmod_covariates(g) for g in df['Galaxy']]
    df['N_pts'] = [d['N_pts'] for d in rotmod_data]
    df['mean_V_err'] = [d['mean_V_err'] for d in rotmod_data]

    # Drop any galaxies with missing rotmod data
    n_before = len(df)
    df = df.dropna(subset=['N_pts', 'mean_V_err', 'Inc', 'L36'])
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        log.info(f"  Dropped {n_dropped} galaxies with missing covariates")

    # Derived predictors
    df['log_N_pts']      = np.log10(df['N_pts'])
    df['log_mean_V_err'] = np.log10(df['mean_V_err'].clip(lower=0.1))   # guard against zero
    df['cos_inc']        = np.cos(np.radians(df['Inc']))
    df['log_L36']        = np.log10(df['L36'].clip(lower=1e-4))

    # Predictor list (T-type first; bulge binary; four continuous)
    PREDICTORS = ['T', 'is_bulge_dom', 'log_N_pts', 'log_mean_V_err', 'cos_inc', 'log_L36']

    # Z-score standardize the continuous predictors (NOT the binary one)
    continuous = ['T', 'log_N_pts', 'log_mean_V_err', 'cos_inc', 'log_L36']
    standardized = df[PREDICTORS].copy()
    for col in continuous:
        mu, sd = df[col].mean(), df[col].std()
        standardized[f'{col}_z'] = (df[col] - mu) / sd

    Z_PREDICTORS = ['T_z', 'is_bulge_dom', 'log_N_pts_z', 'log_mean_V_err_z',
                    'cos_inc_z', 'log_L36_z']
    return df, standardized, PREDICTORS, Z_PREDICTORS


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def fit_logistic(standardized, Z_PREDICTORS):
    """Logistic regression via statsmodels. Returns coefficient DataFrame."""
    try:
        import statsmodels.api as sm
    except ImportError:
        log.error("statsmodels not available. Install with: pip install statsmodels")
        sys.exit(1)

    X = standardized[Z_PREDICTORS].values
    X = sm.add_constant(X)
    y = standardized['is_SB'].values.astype(int) if 'is_SB' in standardized.columns else None
    # Note: is_SB lives in df, not standardized — pass separately
    return X


def run_logistic(df, standardized, Z_PREDICTORS):
    import statsmodels.api as sm
    X = standardized[Z_PREDICTORS].values
    X_const = sm.add_constant(X, prepend=True)
    y = df['is_SB'].values.astype(int)

    model = sm.Logit(y, X_const)
    result = model.fit(disp=False, method='bfgs', maxiter=200)

    rows = []
    names = ['(intercept)'] + Z_PREDICTORS
    for i, name in enumerate(names):
        rows.append({
            'method': 'logistic',
            'predictor': name,
            'coef': result.params[i],
            'se': result.bse[i],
            'z': result.tvalues[i],
            'p_value': result.pvalues[i],
            'ci_lower': result.conf_int()[i][0],
            'ci_upper': result.conf_int()[i][1],
            'importance': np.nan,
        })
    return pd.DataFrame(rows), result


def run_random_forest(df, standardized, Z_PREDICTORS):
    try:
        from sklearn.ensemble import RandomForestClassifier
    except ImportError:
        log.error("scikit-learn not available. Install with: pip install scikit-learn")
        sys.exit(1)

    X = standardized[Z_PREDICTORS].values
    y = df['is_SB'].values.astype(int)

    rf = RandomForestClassifier(
        n_estimators=RF_N_ESTIMATORS,
        random_state=RF_RANDOM_STATE,
        n_jobs=-1,
    )
    rf.fit(X, y)

    rows = []
    for i, name in enumerate(Z_PREDICTORS):
        rows.append({
            'method': 'random_forest',
            'predictor': name,
            'coef': np.nan,
            'se': np.nan,
            'z': np.nan,
            'p_value': np.nan,
            'ci_lower': np.nan,
            'ci_upper': np.nan,
            'importance': rf.feature_importances_[i],
        })
    return pd.DataFrame(rows), rf


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_summary(df, log_results, rf_results, log_model, rf_model,
                  Z_PREDICTORS, fout):
    """Formatted summary suitable for §3.3.7 prose."""
    n = len(df)
    n_sb = int(df['is_SB'].sum())

    lines = []
    lines.append("=" * 78)
    lines.append("MULTIVARIATE COVARIATE MODEL — Paper II §3.3.7")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"Sample: {n} galaxies T={T_MIN}-{T_MAX}, NGC 6674 "
                 f"{'INCLUDED' if 'NGC6674' not in EXCLUDE_GALAXIES else 'EXCLUDED'}")
    lines.append(f"Shell-bearing fraction: {n_sb}/{n} = {100*n_sb/n:.1f}%")
    lines.append("")
    lines.append("Predictors (continuous z-standardized; bulge binary 0/1):")
    lines.append("  T_z              : galaxy morphology T-type (headline predictor)")
    lines.append("  is_bulge_dom     : 1 if bulge-dominated, else 0")
    lines.append("  log_N_pts_z      : log10 number of rotation-curve points")
    lines.append("  log_mean_V_err_z : log10 mean V_err (km/s)")
    lines.append("  cos_inc_z        : cos(inclination)")
    lines.append("  log_L36_z        : log10 L_3.6μm stellar mass proxy")
    lines.append("")
    lines.append("=" * 78)
    lines.append("LOGISTIC REGRESSION COEFFICIENTS")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"  Pseudo R²: {log_model.prsquared:.4f}")
    lines.append(f"  LLR p-value (full model vs null): {log_model.llr_pvalue:.4g}")
    lines.append("")
    lines.append(f"  {'Predictor':<22s} {'coef':>10s} {'SE':>8s} {'z':>8s} {'p-value':>10s}")
    lines.append("  " + "-" * 64)
    for _, row in log_results.iterrows():
        sig = '***' if row['p_value'] < 0.001 else ('**' if row['p_value'] < 0.01
                  else ('*' if row['p_value'] < 0.05 else ''))
        lines.append(
            f"  {row['predictor']:<22s} "
            f"{row['coef']:>10.4f} {row['se']:>8.4f} {row['z']:>8.2f} "
            f"{row['p_value']:>10.4g} {sig}"
        )
    lines.append("")
    lines.append("  Headline: does T-type retain a significant coefficient "
                 "after adjustment?")
    T_row = log_results[log_results['predictor'] == 'T_z'].iloc[0]
    survives = T_row['p_value'] < 0.05
    direction = 'negative (early-types more shell-bearing)' if T_row['coef'] < 0 else 'positive'
    lines.append(f"  → T_z coefficient = {T_row['coef']:+.4f} "
                 f"(p = {T_row['p_value']:.4g})")
    lines.append(f"  → Direction: {direction}")
    lines.append(f"  → Survives p < 0.05: {'YES' if survives else 'NO'}")
    lines.append("")
    lines.append("=" * 78)
    lines.append("RANDOM FOREST FEATURE IMPORTANCES")
    lines.append("=" * 78)
    lines.append("")
    rf_sorted = rf_results.sort_values('importance', ascending=False)
    lines.append(f"  {'Predictor':<22s} {'importance':>12s}  rank")
    lines.append("  " + "-" * 44)
    for rank, (_, row) in enumerate(rf_sorted.iterrows(), 1):
        lines.append(f"  {row['predictor']:<22s} {row['importance']:>12.4f}  {rank}")
    lines.append("")
    T_rank = rf_sorted.reset_index(drop=True)
    T_rank_idx = T_rank[T_rank['predictor'] == 'T_z'].index[0] + 1
    lines.append(f"  T_z rank: {T_rank_idx} of {len(Z_PREDICTORS)}")
    lines.append("")
    lines.append("=" * 78)
    lines.append("INTERPRETATION FOR §3.3.7")
    lines.append("=" * 78)
    lines.append("")
    if survives:
        lines.append("  The morphology gradient retains predictive power after statistical")
        lines.append("  control for bulge presence, RC sampling density, RC measurement")
        lines.append("  uncertainty, inclination, and stellar mass proxy. The T-type")
        lines.append(f"  coefficient in the logistic model is {T_row['coef']:+.3f} (p = {T_row['p_value']:.3g}),")
        lines.append("  and T-type ranks #" + str(T_rank_idx) + " of " + str(len(Z_PREDICTORS))
                     + " in random forest feature importance.")
        lines.append("  The headline gradient is consistent with a morphological effect, not")
        lines.append("  a hidden-covariate artifact.")
    else:
        lines.append("  After statistical control, the T-type coefficient is non-significant")
        lines.append(f"  (β = {T_row['coef']:+.3f}, p = {T_row['p_value']:.3g}). The morphology")
        lines.append("  gradient may be mediated by a correlated covariate. Examine which")
        lines.append("  predictor has the dominant coefficient and revise §3.1's interpretation")
        lines.append("  accordingly.")
    lines.append("")

    Path(fout).write_text("\n".join(lines))
    log.info("  Wrote " + str(fout))
    # Echo to stdout
    print("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log.info("=" * 70)
    log.info("Paper II §3.3.7 — Multivariate covariate model")
    log.info("=" * 70)

    # Load inputs
    log.info("Loading inputs...")
    canonical = pd.read_csv(CANONICAL_CSV)
    sample = pd.read_csv(SAMPLE_CSV)
    classif = pd.read_csv(CLASSIF_CSV)
    log.info(f"  canonical fits: {len(canonical)} rows")
    log.info(f"  SPARC catalog:  {len(sample)} rows")
    log.info(f"  classifications:{len(classif)} rows")

    # Build design matrix
    log.info("Building design matrix...")
    df, standardized, PREDICTORS, Z_PREDICTORS = build_design_matrix(
        canonical, sample, classif, EXCLUDE_GALAXIES,
    )
    standardized['is_SB'] = df['is_SB'].values
    log.info(f"  Final sample: n = {len(df)} galaxies, {int(df['is_SB'].sum())} shell-bearing")

    # Fit models
    log.info("Fitting logistic regression...")
    log_results, log_model = run_logistic(df, standardized, Z_PREDICTORS)

    log.info("Fitting random forest...")
    rf_results, rf_model = run_random_forest(df, standardized, Z_PREDICTORS)

    # Write outputs
    log.info("Writing outputs...")
    combined = pd.concat([log_results, rf_results], ignore_index=True)
    combined.to_csv(OUT_RESULTS, index=False, float_format='%.6f')
    log.info("  Wrote " + str(OUT_RESULTS))

    write_summary(df, log_results, rf_results, log_model, rf_model,
                  Z_PREDICTORS, OUT_SUMMARY)

    log.info("Done.")


if __name__ == "__main__":
    main()

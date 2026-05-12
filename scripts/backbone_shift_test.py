"""
backbone_shift_test.py — Phase-1 add-on for the shell_reality program

Tests whether the Burkert backbone absorbs localized residual structure
when the framework is constrained to n=0 shells.

For each galaxy in the v7.0 canonical sample, refits the framework at
n_shells = 0, 1, 2 and captures the Burkert backbone parameters
(rho_0, a) at each level. Then compares (rho_0, a) at the BIC-selected n
against (rho_0, a) at n=0.

The test:
  If shell-bearing galaxies show systematic shifts in (rho_0, a) when
  shells are allowed (e.g., n>=1 has SMALLER rho_0 and LARGER a than
  n=0), that is direct evidence that the smooth backbone absorbs
  structure when shells are not available. Under that interpretation,
  shells are real localized features that the smooth profile would
  otherwise "hide" by adjusting its core parameters.

  If (rho_0, a) is essentially unchanged across n levels in shell-
  bearing galaxies, the shells and backbone are decoupled — the smooth
  backbone is fitting the same broad mass distribution either way, and
  shells are independent additions on top.

Outputs (in OUTPUT_DIR=./shell_reality/results/):
  backbone_shift.csv      one row per galaxy with full backbone params
  backbone_shift_summary.txt   population-level analysis

Runtime: ~5-15 minutes on M1 Ultra (single fit per galaxy at each n).

Imports the shared fitter from shell_reality_nulls.py (must be in same
directory).

Usage:
  cd shell_reality/scripts/
  python3 backbone_shift_test.py
"""

import os
import sys
import time
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wilcoxon
import warnings
warnings.filterwarnings('ignore')

# Reuse the v7.0 fitter from shell_reality_nulls.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell_reality_nulls as sr


# ============================================================
# Configuration — same path resolution as shell_reality_nulls.py
# ============================================================
DATA_DIR = sr.DATA_DIR
CANONICAL_CSV = sr.CANONICAL_CSV

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'backbone_shift.csv')
OUTPUT_SUMMARY = os.path.join(OUTPUT_DIR, 'backbone_shift_summary.txt')


# ============================================================
# Fit at all three n levels and capture Burkert backbone
# ============================================================
def fit_all_n(rd, vd, ed, V2_bar):
    """
    Run framework fit at n_shells = 0, 1, 2. Return a dict with the
    Burkert backbone (rho_0, a), chi2, and BIC at each level, plus
    the BIC-selected n.
    """
    n_pts = len(rd)
    out = {'n_pts': n_pts}
    bics = {}
    for ns in [0, 1, 2]:
        p, c = sr.fit_fw_n_shells(rd, vd, ed, V2_bar, ns)
        if p is None:
            out[f'n{ns}_rho0'] = np.nan
            out[f'n{ns}_a']    = np.nan
            out[f'n{ns}_chi2'] = np.nan
            out[f'n{ns}_bic']  = np.nan
            continue
        # The first two parameters are always (rho_0, a) for the Burkert backbone
        rho0, a = float(p[0]), float(p[1])
        k = 2 + 3*ns
        bic = c + k * np.log(n_pts)
        out[f'n{ns}_rho0'] = rho0
        out[f'n{ns}_a']    = a
        out[f'n{ns}_chi2'] = c
        out[f'n{ns}_bic']  = bic
        bics[ns] = bic
    if bics:
        out['n_selected'] = int(min(bics, key=bics.get))
    else:
        out['n_selected'] = -1
    return out


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 72)
    print("BACKBONE SHIFT TEST (v7.0 pipeline)")
    print("Tests whether Burkert absorbs shell structure when n_shells = 0")
    print("=" * 72)

    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: rotmod directory not found: {DATA_DIR}")
        sys.exit(1)
    if not os.path.exists(CANONICAL_CSV):
        print(f"ERROR: canonical CSV not found: {CANONICAL_CSV}")
        sys.exit(1)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    canon = pd.read_csv(CANONICAL_CSV)
    galaxies = sr.preprocess_galaxies(canon)
    print(f"Preprocessed {len(galaxies)} galaxies")
    print()

    records = []
    t0 = time.time()
    for i, gal in enumerate(galaxies):
        result = fit_all_n(gal['rd'], gal['vd'], gal['ed'], gal['V2_bar'])
        # Lookup canonical CSV row
        v7 = canon[canon['Galaxy'] == gal['Galaxy']].iloc[0]
        rec = {
            'Galaxy': gal['Galaxy'],
            'T': gal['T'],
            'V_flat': float(v7['V_flat']),
            'v7_n_shells': int(v7['fw_best_n_shells']),
            'v7_burk_rho0': float(v7['burk_rho0']),
            'v7_burk_a':    float(v7['burk_a_kpc']),
            **result,
        }
        # Shifts: BIC-selected vs n=0
        ns = rec['n_selected']
        if ns in (1, 2) and not np.isnan(rec[f'n{ns}_rho0']):
            rec['delta_rho0_select'] = rec[f'n{ns}_rho0'] - rec['n0_rho0']
            rec['delta_a_select']    = rec[f'n{ns}_a']    - rec['n0_a']
            rec['log_ratio_rho0']    = np.log10(rec[f'n{ns}_rho0'] / rec['n0_rho0'])
            rec['ratio_a']           = rec[f'n{ns}_a'] / rec['n0_a']
        else:
            rec['delta_rho0_select'] = 0.0
            rec['delta_a_select']    = 0.0
            rec['log_ratio_rho0']    = 0.0
            rec['ratio_a']           = 1.0
        # Maximum-flexibility shift: n=2 vs n=0 (for all galaxies, regardless of selection)
        if not np.isnan(rec['n2_rho0']):
            rec['delta_rho0_n2'] = rec['n2_rho0'] - rec['n0_rho0']
            rec['delta_a_n2']    = rec['n2_a']    - rec['n0_a']
            rec['log_ratio_rho0_n2'] = np.log10(rec['n2_rho0'] / rec['n0_rho0'])
            rec['ratio_a_n2']    = rec['n2_a'] / rec['n0_a']
        else:
            rec['delta_rho0_n2'] = np.nan
            rec['delta_a_n2']    = np.nan
            rec['log_ratio_rho0_n2'] = np.nan
            rec['ratio_a_n2']    = np.nan
        records.append(rec)

        elapsed = time.time() - t0
        eta = elapsed / (i+1) * (len(galaxies) - i - 1)
        print(f"  [{i+1}/{len(galaxies)}] {gal['Galaxy']:<14} T={gal['T']} "
              f"sel_n={ns} "
              f"a:{rec['n0_a']:.2f}->{rec[f'n{ns}_a']:.2f} "
              f"rho0:{rec['n0_rho0']:.2e}->{rec[f'n{ns}_rho0']:.2e} "
              f"({elapsed:.0f}s ETA {eta:.0f}s)")

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved: {OUTPUT_CSV}")

    # ============================================================
    # Population-level analysis
    # ============================================================
    lines = []
    lines.append("=" * 72)
    lines.append("BACKBONE SHIFT TEST — Summary")
    lines.append("=" * 72)
    lines.append("Tests whether Burkert backbone (rho_0, a) shifts systematically")
    lines.append("when the framework is allowed shells (n>=1) vs constrained to n=0.")
    lines.append("")
    lines.append(f"Sample: {len(df)} galaxies from v7.0 canonical sample")
    lines.append("")

    # Sanity: did we recover the v7.0 BIC selection?
    agree = (df['n_selected'] == df['v7_n_shells']).sum()
    lines.append(f"BIC-selection agreement with v7.0 canonical CSV: "
                 f"{agree}/{len(df)} ({agree/len(df)*100:.1f}%)")
    disagree = df[df['n_selected'] != df['v7_n_shells']]
    if len(disagree) > 0:
        lines.append(f"Disagreements ({len(disagree)} galaxies):")
        for _, r in disagree.iterrows():
            lines.append(f"  {r['Galaxy']:<14} T={r['T']} v7_n={r['v7_n_shells']} this_n={r['n_selected']}")
    lines.append("")

    # Split by shell-bearing
    sb = df[df['n_selected'] >= 1].copy()
    nsb = df[df['n_selected'] == 0].copy()
    lines.append(f"Shell-bearing galaxies (this run): {len(sb)}")
    lines.append(f"Non-shell-bearing galaxies:        {len(nsb)}")
    lines.append("")

    # ============================================================
    # Headline test: do (rho_0, a) shift systematically for shell-bearing?
    # ============================================================
    lines.append("-" * 72)
    lines.append("HEADLINE TEST: backbone shift in shell-bearing galaxies")
    lines.append("-" * 72)
    lines.append("Comparison: (rho_0, a) at BIC-selected n vs (rho_0, a) at n=0.")
    lines.append("If the smooth backbone is absorbing shell structure when n=0, then")
    lines.append("allowing shells should systematically:")
    lines.append("  - INCREASE a (less compact core; smooth profile no longer needs")
    lines.append("    to peak as much because shells handle the inner excess)")
    lines.append("  - DECREASE rho_0 (lower central density; same reasoning)")
    lines.append("")

    if len(sb) > 0:
        # Wilcoxon signed-rank test for each direction
        log_ratio_rho0 = sb['log_ratio_rho0'].dropna().values
        log_ratio_a    = np.log10(sb['ratio_a']).dropna().values

        lines.append(f"  log10(rho_0[sel]/rho_0[n=0]) over {len(log_ratio_rho0)} shell-bearing galaxies:")
        lines.append(f"    median: {np.median(log_ratio_rho0):+.3f} dex")
        lines.append(f"    mean:   {np.mean(log_ratio_rho0):+.3f} dex")
        lines.append(f"    std:    {np.std(log_ratio_rho0):.3f} dex")
        if len(log_ratio_rho0) >= 5 and not np.allclose(log_ratio_rho0, 0):
            try:
                w, pw = wilcoxon(log_ratio_rho0, alternative='two-sided', zero_method='wilcox')
                lines.append(f"    Wilcoxon p (two-sided, vs zero): {pw:.4f}")
            except Exception as e:
                lines.append(f"    Wilcoxon failed: {e}")

        lines.append("")
        lines.append(f"  log10(a[sel]/a[n=0]) over {len(log_ratio_a)} shell-bearing galaxies:")
        lines.append(f"    median: {np.median(log_ratio_a):+.3f} dex")
        lines.append(f"    mean:   {np.mean(log_ratio_a):+.3f} dex")
        lines.append(f"    std:    {np.std(log_ratio_a):.3f} dex")
        if len(log_ratio_a) >= 5 and not np.allclose(log_ratio_a, 0):
            try:
                w, pw = wilcoxon(log_ratio_a, alternative='two-sided', zero_method='wilcox')
                lines.append(f"    Wilcoxon p (two-sided, vs zero): {pw:.4f}")
            except Exception as e:
                lines.append(f"    Wilcoxon failed: {e}")

        # Sign test: how many have rho decrease and a increase (the "absorbing" pattern)?
        n_abs_pattern = ((sb['log_ratio_rho0'] < 0) & (sb['ratio_a'] > 1.0)).sum()
        n_opp_pattern = ((sb['log_ratio_rho0'] > 0) & (sb['ratio_a'] < 1.0)).sum()
        lines.append("")
        lines.append(f"  Sign of shift (the 'absorbing' pattern: rho_0 down + a up):")
        lines.append(f"    rho_0 decreases AND a increases: {n_abs_pattern}/{len(sb)} "
                     f"({n_abs_pattern/len(sb)*100:.1f}%) — absorbing pattern")
        lines.append(f"    rho_0 increases AND a decreases: {n_opp_pattern}/{len(sb)} "
                     f"({n_opp_pattern/len(sb)*100:.1f}%) — opposite pattern")
        lines.append(f"    Other (mixed signs):             {len(sb) - n_abs_pattern - n_opp_pattern}/{len(sb)}")

    lines.append("")

    # ============================================================
    # Control: backbone shift in non-shell-bearing galaxies (should be ~0)
    # ============================================================
    lines.append("-" * 72)
    lines.append("CONTROL: backbone shift in non-shell-bearing galaxies (n=2 vs n=0)")
    lines.append("-" * 72)
    lines.append("These galaxies BIC-prefer n=0, so 'allowing shells' shouldn't shift")
    lines.append("the backbone systematically — if it does, it indicates optimizer")
    lines.append("noise in our (rho_0, a) estimates rather than physical signal.")
    lines.append("")

    if len(nsb) > 0:
        log_ratio_rho0_n2 = nsb['log_ratio_rho0_n2'].dropna().values
        log_ratio_a_n2    = np.log10(nsb['ratio_a_n2']).dropna().values
        lines.append(f"  log10(rho_0[n=2]/rho_0[n=0]) over {len(log_ratio_rho0_n2)} non-shell-bearing:")
        lines.append(f"    median: {np.median(log_ratio_rho0_n2):+.3f} dex")
        lines.append(f"    std:    {np.std(log_ratio_rho0_n2):.3f} dex")
        lines.append(f"  log10(a[n=2]/a[n=0]) over {len(log_ratio_a_n2)} non-shell-bearing:")
        lines.append(f"    median: {np.median(log_ratio_a_n2):+.3f} dex")
        lines.append(f"    std:    {np.std(log_ratio_a_n2):.3f} dex")
        lines.append("")
        lines.append("  If the SB and NSB shift distributions look similar, it's optimizer")
        lines.append("  noise. If SB shows a systematic shift that NSB does not, the shift")
        lines.append("  is real and tied to the presence of shells.")

    lines.append("")

    # ============================================================
    # Does shift magnitude correlate with galaxy properties?
    # ============================================================
    lines.append("-" * 72)
    lines.append("SHIFT MAGNITUDE vs galaxy properties (shell-bearing only)")
    lines.append("-" * 72)
    if len(sb) >= 5:
        for col in ['T', 'V_flat', 'n0_rho0', 'n0_a']:
            for shift_col in ['log_ratio_rho0', 'ratio_a']:
                m = sb[[col, shift_col]].dropna()
                if len(m) >= 5:
                    rho_s, p_s = spearmanr(m[col], m[shift_col])
                    lines.append(f"  {shift_col:<18} vs {col:<10}: rho={rho_s:+.3f} p={p_s:.4f}")
    lines.append("")
    lines.append("=" * 72)

    summary_text = "\n".join(lines)
    print()
    print(summary_text)
    with open(OUTPUT_SUMMARY, 'w') as f:
        f.write(summary_text)
    print(f"\nSaved: {OUTPUT_SUMMARY}")
    print(f"Total runtime: {(time.time()-t0)/60:.1f} min")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
ngc6674_exclusion_reanalysis.py — Post-processor for §2.3 exception list retirement.

Re-aggregates the four production-batch CSVs (Υ/D/i perturbations + backbone-shift)
with NGC 6674 excluded from the population, producing 101-galaxy headline stats
parallel to the existing 102-galaxy headlines. No refitting required — all four
production runs already wrote per-galaxy or per-realization data including
NGC 6674; the aggregation is what needs redoing.

This retires the §2.3 exception list ("These analyses ran as coordinated
production batches against the 102-galaxy canonical fits; reconciliation to the
101-galaxy primary sample requires Mac-side reruns") by providing both versions
side-by-side.

Inputs (from data/):
  upsilon_perturbation_per_galaxy.csv      (102 galaxies × 20 realizations)
  distance_perturbation_per_galaxy.csv     (102 galaxies × 20 realizations)
  inclination_perturbation_per_galaxy.csv  (91 galaxies × 20 realizations)
  backbone_shift.csv                       (102 galaxies × 1 row)
  sparc_T2-T9_canonical_fits.csv           (Paper I canonical; needed for canonical n_shells)

Output: prints comparison report. Writes to data/ngc6674_exclusion_summary.txt.

Run from scripts/ or package root.
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, spearmanr


# Path resolution
_HERE = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DATA = os.path.join(os.path.dirname(_HERE), 'data')
_LOCAL_DATA = os.path.join('.', 'data')
DATA_DIR = _PACKAGE_DATA if os.path.isdir(_PACKAGE_DATA) else _LOCAL_DATA
if not os.path.isdir(DATA_DIR):
    print(f"ERROR: data directory not found. Tried: {_PACKAGE_DATA}, {_LOCAL_DATA}")
    sys.exit(1)

EXCLUDE = {'NGC6674'}


# Load canonical
canon_path = os.path.join(DATA_DIR, 'sparc_T2-T9_canonical_fits.csv')
canon = pd.read_csv(canon_path)
canon_n = dict(zip(canon['Galaxy'], canon['fw_best_n_shells']))
print(f"Loaded Paper I canonical: {len(canon)} galaxies")
print(f"Canonical includes NGC6674: {'NGC6674' in canon_n}")
print()


def analyze_perturbation(name, fname, section):
    """Compute per-galaxy and per-fit match rates against canonical, both 102- and 101-galaxy versions."""
    path = os.path.join(DATA_DIR, fname)
    df = pd.read_csv(path)
    if 'status' in df.columns:
        df = df[df['status'] == 'ok'].copy()

    def stats(d, label):
        # Per-fit: each realization × galaxy; n_shells matches canonical?
        d = d.copy()
        d['canon_n'] = d['Galaxy'].map(canon_n)
        d = d.dropna(subset=['canon_n'])
        d['per_fit_match'] = (d['n_shells'] == d['canon_n']).astype(int)
        per_fit = d['per_fit_match'].mean() * 100

        # Per-galaxy: modal n_shells across realizations; matches canonical?
        modes = d.groupby('Galaxy')['n_shells'].agg(lambda s: int(s.mode().iloc[0]))
        canons = d.drop_duplicates('Galaxy').set_index('Galaxy')['canon_n']
        mode_match = (modes == canons.loc[modes.index]).mean() * 100

        return len(modes), per_fit, mode_match

    n_full, pf_full, pg_full = stats(df, 'full')
    df_excl = df[~df['Galaxy'].isin(EXCLUDE)]
    n_excl, pf_excl, pg_excl = stats(df_excl, 'excl')

    return {
        'name': name,
        'section': section,
        'n_full': n_full,
        'n_excl': n_excl,
        'per_fit_102': pf_full,
        'per_fit_101': pf_excl,
        'per_gal_102': pg_full,
        'per_gal_101': pg_excl,
    }


# Run the three perturbation tests
results = []
for name, fname, section in [
    ('Upsilon', 'upsilon_perturbation_per_galaxy.csv', '§3.3.2'),
    ('Distance', 'distance_perturbation_per_galaxy.csv', '§3.3.3'),
    ('Inclination', 'inclination_perturbation_per_galaxy.csv', '§3.3.4'),
]:
    results.append(analyze_perturbation(name, fname, section))


# Backbone-shift analysis (§3.3.7)
bs_path = os.path.join(DATA_DIR, 'backbone_shift.csv')
bs = pd.read_csv(bs_path)


def backbone_stats(d, label):
    """Compute the §3.3.7 headline numbers for a given (possibly filtered) backbone_shift DataFrame."""
    # Shell-bearing under v7 (canonical)
    sb = d[d['v7_n_shells'] > 0].copy()
    n_sb = len(sb)

    # "Absorbing pattern": rho0[BIC] < rho0[n=0] AND a[BIC] > a[n=0]
    # log_ratio_rho0 = log10(rho0[BIC] / rho0[n=0]) so absorbing means log_ratio_rho0 < 0 and ratio_a > 1
    sb['absorbing'] = (sb['log_ratio_rho0'] < 0) & (sb['ratio_a'] > 1)
    n_absorbing = sb['absorbing'].sum()
    pct_absorbing = 100 * n_absorbing / n_sb if n_sb else 0

    # Median shifts
    med_rho0 = sb['log_ratio_rho0'].median()
    med_a_log = np.log10(sb['ratio_a']).median()

    # Wilcoxon (one-sample test that shifts are not zero)
    try:
        w_rho0 = wilcoxon(sb['log_ratio_rho0'])
        w_a = wilcoxon(np.log10(sb['ratio_a']))
        p_rho0 = w_rho0.pvalue
        p_a = w_a.pvalue
    except Exception:
        p_rho0 = p_a = float('nan')

    # Spearman ρ of absorbing-pattern shift with T-type
    sb['shift_signed'] = sb['absorbing'].astype(int)
    rho_T, p_T = spearmanr(sb['T'], sb['log_ratio_rho0'])

    return {
        'n_sb': n_sb,
        'n_absorbing': int(n_absorbing),
        'pct_absorbing': pct_absorbing,
        'med_log_ratio_rho0': med_rho0,
        'med_log_ratio_a': med_a_log,
        'wilcoxon_p_rho0': p_rho0,
        'wilcoxon_p_a': p_a,
        'spearman_rho_T': rho_T,
        'spearman_p_T': p_T,
    }


bs_full = backbone_stats(bs, '102')
bs_excl = backbone_stats(bs[~bs['Galaxy'].isin(EXCLUDE)], '101')


# Format report
lines = []
lines.append("=" * 78)
lines.append("§2.3 EXCEPTION LIST RETIREMENT — NGC 6674 EXCLUSION RE-ANALYSIS")
lines.append("=" * 78)
lines.append("")
lines.append("Production-batch CSVs aggregated under two sample conventions:")
lines.append("  102-galaxy: NGC 6674 INCLUDED (as currently reported in manuscript §3.3)")
lines.append("  101-galaxy: NGC 6674 EXCLUDED (matches §3.1/§3.3.5 primary convention)")
lines.append("")
lines.append("If the 102 vs 101 numbers are qualitatively identical, the §2.3 exception")
lines.append("list can be retired: NGC 6674's inclusion in §3.3.2-4/§3.3.7 is")
lines.append("demonstrably packaging artifact, not a conclusion-affecting choice.")
lines.append("")

lines.append("-" * 78)
lines.append("PERTURBATION TESTS (§3.3.2 / §3.3.3 / §3.3.4)")
lines.append("-" * 78)
lines.append("")
lines.append(f"{'Test':<12} {'Sec':<8} {'N_full':>7} {'N_excl':>7} "
             f"{'Pfit_102':>10} {'Pfit_101':>10} {'Pgal_102':>10} {'Pgal_101':>10}")
lines.append("-" * 78)
for r in results:
    lines.append(f"{r['name']:<12} {r['section']:<8} {r['n_full']:>7} {r['n_excl']:>7} "
                 f"{r['per_fit_102']:>9.2f}% {r['per_fit_101']:>9.2f}% "
                 f"{r['per_gal_102']:>9.2f}% {r['per_gal_101']:>9.2f}%")
lines.append("")
lines.append("Pfit = per-fit match rate (each realization × galaxy)")
lines.append("Pgal = per-galaxy modal-match rate")
lines.append("Shifts of <1 percentage point indicate NGC 6674 has negligible effect.")
lines.append("")

lines.append("-" * 78)
lines.append("BACKBONE-SHIFT TEST (§3.3.7)")
lines.append("-" * 78)
lines.append("")
lines.append(f"{'Statistic':<35} {'102-galaxy':>15} {'101-galaxy':>15} {'Δ':>10}")
lines.append("-" * 78)
for key, label, fmt, kind in [
    ('n_sb', 'Shell-bearing galaxies', 'd', 'int'),
    ('n_absorbing', 'With absorbing pattern', 'd', 'int'),
    ('pct_absorbing', 'Absorbing pattern (%)', '.1f', 'float'),
    ('med_log_ratio_rho0', 'Median Δlog₁₀(ρ₀[BIC]/ρ₀[n=0])', '+.3f', 'float'),
    ('med_log_ratio_a', 'Median Δlog₁₀(a[BIC]/a[n=0])', '+.3f', 'float'),
    ('wilcoxon_p_rho0', 'Wilcoxon p (ρ₀ shift)', '.3e', 'float'),
    ('wilcoxon_p_a', 'Wilcoxon p (a shift)', '.3e', 'float'),
    ('spearman_rho_T', 'Spearman ρ vs T-type', '+.3f', 'float'),
    ('spearman_p_T', 'Spearman p vs T-type', '.3e', 'float'),
]:
    v_full = bs_full[key]
    v_excl = bs_excl[key]
    if kind == 'int':
        s_full = f"{v_full:{fmt}}"
        s_excl = f"{v_excl:{fmt}}"
        s_d = f"{v_excl - v_full:+d}"
    else:
        s_full = f"{v_full:{fmt}}"
        s_excl = f"{v_excl:{fmt}}"
        try:
            s_d = f"{v_excl - v_full:+.3g}"
        except Exception:
            s_d = "—"
    lines.append(f"{label:<35} {s_full:>15} {s_excl:>15} {s_d:>10}")
lines.append("")

# Verdict
lines.append("=" * 78)
lines.append("VERDICT")
lines.append("=" * 78)
lines.append("")
max_pert_delta = max(
    abs(r['per_fit_101'] - r['per_fit_102']) for r in results
) + max(
    abs(r['per_gal_101'] - r['per_gal_102']) for r in results
)
pct_delta = bs_excl['pct_absorbing'] - bs_full['pct_absorbing']
lines.append(f"Maximum perturbation-test headline shift: {max_pert_delta:.2f} percentage points")
lines.append(f"Backbone-shift absorbing-pattern shift: {pct_delta:+.2f} percentage points")
lines.append("")
if abs(max_pert_delta) < 2.0 and abs(pct_delta) < 2.0:
    lines.append("§2.3 exception list IS RETIREABLE: all headline shifts < 2 percentage points.")
    lines.append("Manuscript can quote 101-galaxy convention throughout §3.3 with a single")
    lines.append("methodological note acknowledging that production CSVs included NGC 6674")
    lines.append("but aggregation has been recomputed on the 101-galaxy sample.")
else:
    lines.append("§2.3 exception list NOT YET RETIREABLE: some shifts ≥ 2 percentage points.")
    lines.append("Inspect the table above to identify which channel needs §2.3 to remain.")
lines.append("")

report = "\n".join(lines)
print(report)

# Write to file
out_path = os.path.join(DATA_DIR, 'ngc6674_exclusion_summary.txt')
with open(out_path, 'w') as f:
    f.write(report + "\n")
print(f"\nReport written to: {out_path}")

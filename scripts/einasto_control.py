#!/usr/bin/env python3
"""
einasto_control.py — Backbone-family control analysis for Paper II §3.3.

Compares shell-population organizational signatures under Einasto backbone
vs the Burkert backbone of the canonical analysis. If the morphology gradient,
bulge correlation, scaling slopes, and σ/r distribution survive under Einasto
(which has a free shape parameter and is therefore a strictly more flexible
smooth-halo family than Burkert), that directly addresses the backbone-family
caveat raised in §4.

NGC 6674 excluded throughout for consistency with Paper II primary.
"""
import numpy as np
import pandas as pd
import ast
from scipy.stats import spearmanr, fisher_exact, wilcoxon

# ============================================================
# Path resolution (matches shell_reality_nulls_parallel.py convention)
# ============================================================
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DATA = os.path.join(os.path.dirname(_HERE), 'data')
_LOCAL_DATA = os.path.join('.', 'data')
DATA_DIR = _PACKAGE_DATA if os.path.isdir(_PACKAGE_DATA) else _LOCAL_DATA

EXCLUDE = {'NGC6674'}  # Paper II 101-galaxy convention


def _resolve(filename):
    """Find a CSV in package data/, current dir, or parent dir."""
    candidates = [
        os.path.join(DATA_DIR, filename),
        os.path.join('.', filename),
        os.path.join('..', filename),
        os.path.join('..', 'data', filename),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


EINASTO_PATH = _resolve('einasto_full_sample_results.csv')
if EINASTO_PATH is None:
    print("ERROR: einasto_full_sample_results.csv not found.")
    print("  Expected location: data/einasto_full_sample_results.csv")
    print("  Source: Paper I (sparc-halo-shells) repo §3.7 outputs.")
    print(f"  Searched: {DATA_DIR}, ./, ../, ../data/")
    sys.exit(1)

SAMPLE_PATH = _resolve('sparc_sample123.csv')
CLASSIF_PATH = _resolve('galaxy_classifications.csv')
if SAMPLE_PATH is None or CLASSIF_PATH is None:
    print("ERROR: sparc_sample123.csv or galaxy_classifications.csv not found.")
    sys.exit(1)

einasto = pd.read_csv(EINASTO_PATH)
einasto = einasto[~einasto['galaxy'].isin(EXCLUDE)].reset_index(drop=True)
sample = pd.read_csv(SAMPLE_PATH)
classif = pd.read_csv(CLASSIF_PATH)

# Restrict to canonical T=2-9, Q<=2 sample
canon = set(sample[(sample['T']>=2) & (sample['T']<=9) & (sample['Q']<=2)]['Galaxy']) - EXCLUDE
einasto = einasto[einasto['galaxy'].isin(canon)].reset_index(drop=True)
print(f"Canonical sample (NGC 6674 excluded): {len(einasto)} galaxies")
print()

# --- 1. Shell-bearing comparison ---
ein_sb = einasto[einasto['fw_einasto_n_shells'] > 0]['galaxy'].values
burk_sb = einasto[einasto['fw_burkert_n_shells'] > 0]['galaxy'].values
both = set(ein_sb) & set(burk_sb)
ein_only = set(ein_sb) - set(burk_sb)
burk_only = set(burk_sb) - set(ein_sb)

print(f"Shell-bearing under Burkert: {len(burk_sb)}/{len(einasto)} ({100*len(burk_sb)/len(einasto):.1f}%)")
print(f"Shell-bearing under Einasto: {len(ein_sb)}/{len(einasto)} ({100*len(ein_sb)/len(einasto):.1f}%)")
print(f"Both shell-bearing:    {len(both)}")
print(f"Einasto-only:          {len(ein_only)}")
print(f"Burkert-only:          {len(burk_only)} → galaxies that stop being SB when backbone gets more flexible")
print(f"Classification agreement: {len(both) + (len(einasto) - len(set(ein_sb) | set(burk_sb)))}/{len(einasto)}")
print()

# --- 2. Parse Einasto shells from fw_einasto_popt ---
# Einasto has 3 backbone params (log_rho_s, log_r_s, alpha), then per-shell 3 (log_M, r_shell, sigma_frac)
def parse_popt(popt_str, n):
    """Extract shell parameters: list of (log_M, r_shell, sigma_frac_or_sigma) per shell."""
    arr = np.array(ast.literal_eval(popt_str))
    if n == 0:
        return []
    # 3 backbone + 3*n shell params
    shells = []
    for i in range(n):
        log_M = arr[3 + 3*i]
        r_sh = arr[3 + 3*i + 1]
        sigma_or_frac = arr[3 + 3*i + 2]
        shells.append((log_M, r_sh, sigma_or_frac))
    return shells

ein_shells = []
for _, row in einasto.iterrows():
    n = int(row['fw_einasto_n_shells'])
    if n == 0: continue
    parsed = parse_popt(row['fw_einasto_popt'], n)
    if n == 1:
        log_M, r_sh, s = parsed[0]
        # sigma_frac is the third param; physical σ = sigma_frac × r_shell (under v7.0 convention)
        # But popt is documented as "physical sigma values (sigma_frac resolved)"
        # So `s` is physical sigma directly per the docstring
        ein_shells.append({
            'Galaxy': row['galaxy'], 'T': row['T'], 'n_total': 1, 'position': 'single',
            'log_M': log_M, 'M_sh': 10**log_M, 'r_sh_kpc': r_sh, 'sigma_sh_kpc': s
        })
    elif n == 2:
        (logM1, r1, s1), (logM2, r2, s2) = parsed
        if r1 <= r2:
            (inner_M, inner_r, inner_s), (outer_M, outer_r, outer_s) = (logM1, r1, s1), (logM2, r2, s2)
        else:
            (inner_M, inner_r, inner_s), (outer_M, outer_r, outer_s) = (logM2, r2, s2), (logM1, r1, s1)
        ein_shells.append({
            'Galaxy': row['galaxy'], 'T': row['T'], 'n_total': 2, 'position': 'inner',
            'log_M': inner_M, 'M_sh': 10**inner_M, 'r_sh_kpc': inner_r, 'sigma_sh_kpc': inner_s})
        ein_shells.append({
            'Galaxy': row['galaxy'], 'T': row['T'], 'n_total': 2, 'position': 'outer',
            'log_M': outer_M, 'M_sh': 10**outer_M, 'r_sh_kpc': outer_r, 'sigma_sh_kpc': outer_s})

df = pd.DataFrame(ein_shells)
df['sigma_over_r'] = df['sigma_sh_kpc'] / df['r_sh_kpc']
print(f"Total Einasto shells: {len(df)} across {df['Galaxy'].nunique()} galaxies")
print(f"Two-shell galaxies: {df[df['n_total']==2]['Galaxy'].nunique()}")
print()
print("Sanity check on Einasto shell parameters:")
print(f"  r_shell range: {df['r_sh_kpc'].min():.2f} – {df['r_sh_kpc'].max():.2f} kpc")
print(f"  log M range: {df['log_M'].min():.2f} – {df['log_M'].max():.2f}")
print(f"  σ range: {df['sigma_sh_kpc'].min():.3f} – {df['sigma_sh_kpc'].max():.3f} kpc")
print(f"  σ/r range: {df['sigma_over_r'].min():.3f} – {df['sigma_over_r'].max():.3f}")
print()

# --- 3. Morphology gradient under Einasto ---
print("="*70)
print("MORPHOLOGY GRADIENT (galaxy-level)")
print("="*70)
sb_einasto = set(df['Galaxy'].unique())
for T in range(2, 10):
    T_gals = canon & set(sample[sample['T']==T]['Galaxy'])
    if not T_gals: continue
    rate = len(T_gals & sb_einasto) / len(T_gals)
    print(f"  T={T}: {len(T_gals & sb_einasto):2d}/{len(T_gals):2d} = {rate:.2f}")
T_pairs = [(T, len(canon & set(sample[sample['T']==T]['Galaxy']) & sb_einasto)/len(canon & set(sample[sample['T']==T]['Galaxy']))) 
           for T in range(2, 10) if len(canon & set(sample[sample['T']==T]['Galaxy'])) > 0]
rho_T, p_T = spearmanr([t[0] for t in T_pairs], [t[1] for t in T_pairs])
print(f"  ρ_per_T (Einasto) = {rho_T:+.3f}, p = {p_T:.4f}")
print(f"  ρ_per_T (Burkert) = -0.762, p = 0.028 (for reference)")
print()

# --- 4. Bulge correlation under Einasto ---
print("="*70)
print("BULGE CORRELATION")
print("="*70)
bulged = set(classif[classif['is_bulge_dom']]['Galaxy']) & canon
bulgeless = set(classif[classif['is_bulgeless']]['Galaxy']) & canon
n_b_sb = len(bulged & sb_einasto)
n_b_nsb = len(bulged) - n_b_sb
n_bl_sb = len(bulgeless & sb_einasto)
n_bl_nsb = len(bulgeless) - n_bl_sb
OR, p_OR = fisher_exact([[n_b_sb, n_b_nsb], [n_bl_sb, n_bl_nsb]], alternative='greater')
print(f"  Bulged SB:    {n_b_sb}/{len(bulged)} ({100*n_b_sb/len(bulged):.1f}%)")
print(f"  Bulgeless SB: {n_bl_sb}/{len(bulgeless)} ({100*n_bl_sb/len(bulgeless):.1f}%)")
print(f"  Bulge OR (Einasto) = {OR:.2f}, Fisher p = {p_OR:.4f}")
print(f"  Bulge OR (Burkert) = 3.67, p ≈ 0.01 (for reference)")
print()

# --- 5. Scaling relations under Einasto ---
print("="*70)
print("SCALING RELATIONS")
print("="*70)
log_r = np.log10(df['r_sh_kpc'])
log_s = np.log10(df['sigma_sh_kpc'])
log_M = np.log10(df['M_sh'])
slope_s, int_s = np.polyfit(log_r, log_s, 1)
slope_M, int_M = np.polyfit(log_r, log_M, 1)
rho_s, p_s = spearmanr(log_r, log_s)
rho_M, p_M = spearmanr(log_r, log_M)
print(f"  σ-r slope (Einasto): {slope_s:.2f}, ρ = {rho_s:+.3f}, p = {p_s:.2e}")
print(f"  σ-r slope (Burkert): 1.04, ρ = +0.78  (for reference)")
print()
print(f"  M-r slope (Einasto): {slope_M:.2f}, ρ = {rho_M:+.3f}, p = {p_M:.2e}")
print(f"  M-r slope (Burkert): 0.76, ρ = +0.64  (for reference)")
print()
print(f"  σ/r median (Einasto): {df['sigma_over_r'].median():.3f}, std: {df['sigma_over_r'].std():.3f}")
print(f"  σ/r median (Burkert): 0.275, std: 0.116  (for reference)")
print()

# --- 6. Inner-vs-outer in two-shell galaxies ---
print("="*70)
print("INNER-VS-OUTER (two-shell galaxies)")
print("="*70)
two_shell = df[df['n_total']==2]['Galaxy'].unique()
M_pos = 0
s_pos = 0
M_diffs = []
s_diffs = []
ratios_M = []
for g in two_shell:
    i = df[(df['Galaxy']==g) & (df['position']=='inner')].iloc[0]
    o = df[(df['Galaxy']==g) & (df['position']=='outer')].iloc[0]
    M_diffs.append(o['M_sh'] - i['M_sh'])
    s_diffs.append(o['sigma_sh_kpc'] - i['sigma_sh_kpc'])
    ratios_M.append(o['M_sh'] / i['M_sh'])
    if o['M_sh'] > i['M_sh']: M_pos += 1
    if o['sigma_sh_kpc'] > i['sigma_sh_kpc']: s_pos += 1

wM = wilcoxon(M_diffs, alternative='greater')
ws = wilcoxon(s_diffs, alternative='greater')
print(f"  Two-shell galaxies (Einasto): n = {len(two_shell)}")
print(f"  M outer > inner: {M_pos}/{len(two_shell)} ({100*M_pos/len(two_shell):.1f}%), Wilcoxon p = {wM.pvalue:.4f}")
print(f"  σ outer > inner: {s_pos}/{len(two_shell)} ({100*s_pos/len(two_shell):.1f}%), Wilcoxon p = {ws.pvalue:.4f}")
print(f"  Median M_outer/M_inner: {np.median(ratios_M):.2f}")
print(f"  For Burkert reference: 14/16, p=0.0001 for M; 14/16, p=0.0008 for σ; median ratio 2.06")
print()

# --- 7. Classification agreement matrix ---
print("="*70)
print("CLASSIFICATION AGREEMENT")
print("="*70)
print(f"  Both NOT shell-bearing: {len(einasto) - len(set(burk_sb) | set(ein_sb))}")
print(f"  Both shell-bearing:     {len(both)}")
print(f"  Burkert-only SB:        {len(burk_only)}")
print(f"  Einasto-only SB:        {len(ein_only)}")
total_agreement = (len(einasto) - len(set(burk_sb) | set(ein_sb))) + len(both)
print(f"  Total agreement: {total_agreement}/{len(einasto)} = {100*total_agreement/len(einasto):.1f}%")
print()
print(f"  Burkert-only galaxies (lose SB when backbone gets free α):")
for g in sorted(burk_only):
    T = sample[sample['Galaxy']==g]['T'].values[0] if g in sample['Galaxy'].values else '?'
    print(f"    {g:15s} (T={T})")
print()

# --- 8. Bonus: by-T classification agreement ---
print("="*70)
print("CLASSIFICATION CHANGES BY T-TYPE")
print("="*70)
for T in range(2, 10):
    T_gals = canon & set(sample[sample['T']==T]['Galaxy'])
    if not T_gals: continue
    burk_in_T = T_gals & set(burk_sb)
    ein_in_T = T_gals & set(ein_sb)
    agree_T = (T_gals - (burk_in_T | ein_in_T)) | (burk_in_T & ein_in_T)
    print(f"  T={T}: Burk SB {len(burk_in_T):2d}, Ein SB {len(ein_in_T):2d}, agreement {len(agree_T):2d}/{len(T_gals):2d}")

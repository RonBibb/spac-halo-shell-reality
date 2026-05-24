#!/usr/bin/env python3
"""
antiwarp_subsample.py — Paper II §3.3.5 anti-warp clean subsample analysis

Pure analysis script (no rotation-curve fitting). Reads Paper I's v7.0 canonical
fits CSV, applies four conservative anti-warp cuts, and outputs:
  - data/antiwarp_per_shell.csv     (per-shell catalog with classification flags)
  - data/antiwarp_summary.txt       (formatted statistical comparison)

Anti-warp cuts (all four required for "clean"):
  1. Shell radius well inside the HI gas extent: r_shell / R_HI < 0.3
  2. Disk-dominated at the shell radius: V_disk^2 + V_bulge^2 > V_gas^2
  3. Highest-quality SPARC rotation curve: Q == 1
  4. Inner shell of any two-shell pair: drop outer of n=2

Inputs (must be present in ../data/):
  - sparc_T2-T9_canonical_fits.csv   (FROM PAPER I v7.1.0; not bundled)
  - sparc_sample123.csv              (SPARC catalog)
  - galaxy_classifications.csv       (bulge/dwarf/MW-like flags)
  - Rotmod_LTG/<Galaxy>_rotmod.dat   (per-galaxy rotation curves for V_disk/V_gas/V_bulge)

Outputs (to ../data/):
  - antiwarp_per_shell.csv
  - antiwarp_summary.txt

Sample convention: NGC 6674 inclusion is controlled by the EXCLUDE_GALAXIES
list. Paper I's headline numbers include NGC 6674; the v1.0 release of this
package preserves antiwarp_per_shell.csv with NGC 6674 EXCLUDED (degenerate
fit at r1 = r2 = 3.12 kpc with both masses pegged at the upper bound), and
antiwarp_summary.txt regenerated with NGC 6674 INCLUDED to match the
manuscript. To regenerate antiwarp_per_shell.csv with NGC 6674 included,
set EXCLUDE_GALAXIES = [].

Author: Ron Bibb
Date: 2026-05-10
Version: 1.0 (reconstructed from algorithm specs in manuscript §3.3.5;
              verify against Mac-side reference at
              ~/Library/CloudStorage/OneDrive-Personal(2)/.../shell_reality_v2/scripts/)
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, fisher_exact, pearsonr
from pathlib import Path

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
DATA_DIR = PACKAGE_ROOT / "data"
ROTMOD_DIR = Path("../Rotmod_LTG")

# Paths (with auto-fallback to local layout)
CANONICAL_CSV = DATA_DIR / "sparc_T2-T9_canonical_fits.csv"
SAMPLE_CSV = DATA_DIR / "sparc_sample123.csv"
CLASSIF_CSV = DATA_DIR / "galaxy_classifications.csv"

OUT_PER_SHELL = DATA_DIR / "antiwarp_per_shell.csv"
OUT_SUMMARY = DATA_DIR / "antiwarp_summary.txt"

# Sample convention — set to [] to include NGC 6674 (Paper I convention)
# Set to ['NGC6674'] to exclude (NGC 6674-excluded version preserved as v1.0 catalog)
EXCLUDE_GALAXIES = ['NGC6674']

# Anti-warp cut thresholds
R_OVER_RHI_MAX = 0.3
QUALITY_FLAG = 1

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Rotation curve interpolation
# -----------------------------------------------------------------------------

def load_rotmod(galaxy):
    """Load per-galaxy rotmod file. Returns DataFrame with cols Rad, Vobs, errV,
    Vgas, Vdisk, Vbul."""
    fname = ROTMOD_DIR / f"{galaxy}_rotmod.dat"
    if not fname.exists():
        log.warning(f"Missing rotmod file: {fname}")
        return None
    return pd.read_csv(fname, sep=r'\s+', comment='#',
                       names=['Rad','Vobs','errV','Vgas','Vdisk','Vbul','SBdisk','SBbul'])


def interpolate_at_radius(rotmod, r_target, col):
    """Linear interpolation of rotmod[col] at r_target. Returns nan if out of range."""
    if rotmod is None or len(rotmod) == 0:
        return np.nan
    return np.interp(r_target, rotmod['Rad'].values, rotmod[col].values,
                     left=np.nan, right=np.nan)


# -----------------------------------------------------------------------------
# Anti-warp cut application
# -----------------------------------------------------------------------------

def apply_antiwarp_cuts(df_shells, sample, classif):
    """Apply four anti-warp cuts and return per-shell DataFrame with flag columns.

    df_shells must have one row per shell with columns Galaxy, T, position
    (inner/outer/single), n_total (1 or 2), r_sh_kpc, M_sh, sigma_sh_kpc.
    """
    # Merge in catalog metadata
    df = df_shells.merge(sample[['Galaxy','RHI','Q']], on='Galaxy', how='left')
    df = df.merge(classif[['Galaxy','is_bulge_dom','is_bulgeless']],
                  on='Galaxy', how='left')

    # Compute V_gas, V_disk, V_bulge at each shell radius
    Vgas, Vdisk, Vbul = [], [], []
    for _, row in df.iterrows():
        rotmod = load_rotmod(row['Galaxy'])
        Vgas.append(interpolate_at_radius(rotmod, row['r_sh_kpc'], 'Vgas'))
        Vdisk.append(interpolate_at_radius(rotmod, row['r_sh_kpc'], 'Vdisk'))
        Vbul.append(interpolate_at_radius(rotmod, row['r_sh_kpc'], 'Vbul'))
    df['V_gas_at_kms'] = Vgas
    df['V_disk_at_kms'] = Vdisk
    df['V_bulge_at_kms'] = Vbul

    # Derived quantities
    df['sigma_over_r'] = df['sigma_sh_kpc'] / df['r_sh_kpc']
    df['r_over_RHI'] = df['r_sh_kpc'] / df['RHI']

    # Cut flags
    df['is_disk_dominated'] = (df['V_disk_at_kms']**2 + df['V_bulge_at_kms']**2
                               > df['V_gas_at_kms']**2)
    df['is_inner'] = df['position'].isin(['inner','single'])
    df['is_clean'] = (
        (df['r_over_RHI'] < R_OVER_RHI_MAX) &
        df['is_disk_dominated'] &
        (df['Q'] == QUALITY_FLAG) &
        df['is_inner']
    )

    return df


# -----------------------------------------------------------------------------
# Statistics
# -----------------------------------------------------------------------------

def compute_scaling_stats(df, label=""):
    """Compute M-r and sigma-r slopes (with SE), Spearman ρ, σ/r stats."""
    if len(df) < 3:
        return {}
    log_M = np.log10(df['M_sh'])
    log_r = np.log10(df['r_sh_kpc'])
    log_sig = np.log10(df['sigma_sh_kpc'])
    
    # M-r
    p_M, cov_M = np.polyfit(log_r, log_M, 1, cov=True)
    rho_M, p_M_sp = spearmanr(log_r, log_M)
    
    # σ-r
    p_s, cov_s = np.polyfit(log_r, log_sig, 1, cov=True)
    rho_s, p_s_sp = spearmanr(log_r, log_sig)
    
    return {
        'n': len(df),
        'M_slope': p_M[0], 'M_slope_SE': np.sqrt(cov_M[0,0]),
        'M_rho': rho_M, 'M_rho_p': p_M_sp,
        'sig_slope': p_s[0], 'sig_slope_SE': np.sqrt(cov_s[0,0]),
        'sig_rho': rho_s, 'sig_rho_p': p_s_sp,
        'sigr_median': df['sigma_over_r'].median(),
        'sigr_std': df['sigma_over_r'].std(),
    }


def compute_bulge_OR(df_shells, sample, classif):
    """Bulge correlation odds ratio (galaxy-level), restricted to T=2-9."""
    sample_T = sample[(sample['T'] >= 2) & (sample['T'] <= 9)]
    galaxies_T = set(sample_T['Galaxy'].tolist())
    bulged = [g for g in classif[classif['is_bulge_dom']]['Galaxy'].tolist() if g in galaxies_T]
    bulgeless = [g for g in classif[classif['is_bulgeless']]['Galaxy'].tolist() if g in galaxies_T]
    # ...rest unchanged
    
    sb_galaxies = set(df_shells['Galaxy'].unique())
    n_b_sb = len(set(bulged) & sb_galaxies)
    n_b_nsb = len(bulged) - n_b_sb
    n_bl_sb = len(set(bulgeless) & sb_galaxies)
    n_bl_nsb = len(bulgeless) - n_bl_sb
    
    table = [[n_b_sb, n_b_nsb], [n_bl_sb, n_bl_nsb]]
    or_val, p_val = fisher_exact(table, alternative='greater')
    return {
        'OR': or_val, 'p': p_val,
        'bulged_sb_rate': f"{n_b_sb}/{n_b_sb + n_b_nsb}",
        'bulgeless_sb_rate': f"{n_bl_sb}/{n_bl_sb + n_bl_nsb}",
    }


def compute_morphology_gradient(df_shells, sample):
    """ρ_per_T across T = 2-9 bins."""
    sample_T = sample[(sample['T'] >= 2) & (sample['T'] <= 9)]
    sb_galaxies = set(df_shells['Galaxy'].unique())
    
    rows = []
    for T in range(2, 10):
        T_galaxies = sample_T[sample_T['T'] == T]['Galaxy'].tolist()
        n_total = len(T_galaxies)
        n_sb = len(set(T_galaxies) & sb_galaxies)
        rows.append({'T': T, 'N_gal': n_total, 'SB_rate': n_sb / n_total if n_total else 0})
    
    rho, p = spearmanr([r['T'] for r in rows], [r['SB_rate'] for r in rows])
    return rho, p, rows


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def parse_canonical_to_per_shell(canonical_df, exclude_galaxies):
    """Convert Paper I canonical CSV (one row per galaxy) to per-shell long format.

    Canonical CSV uses branch-specific column names:
      n=1 fits: fw_n1_r_sh1_kpc, fw_n1_M_sh1, fw_n1_sigma_sh1_kpc
      n=2 fits: fw_n2_r_sh{1,2}_kpc, fw_n2_M_sh{1,2}, fw_n2_sigma_sh{1,2}_kpc
    The fw_best_n_shells column selects which branch's columns to read for that galaxy.
    """
    rows = []
    for _, row in canonical_df.iterrows():
        gal = row['Galaxy']
        if gal in exclude_galaxies:
            continue
        n = int(row['fw_best_n_shells'])
        if n == 0:
            continue
        elif n == 1:
            rows.append({
                'Galaxy': gal, 'T': row['T'], 'n_total': 1,
                'position': 'single',
                'r_sh_kpc': row['fw_n1_r_sh1_kpc'],
                'M_sh': row['fw_n1_M_sh1'],
                'sigma_sh_kpc': row['fw_n1_sigma_sh1_kpc'],
            })
        elif n == 2:
            r1, r2 = row['fw_n2_r_sh1_kpc'], row['fw_n2_r_sh2_kpc']
            M1, s1 = row['fw_n2_M_sh1'], row['fw_n2_sigma_sh1_kpc']
            M2, s2 = row['fw_n2_M_sh2'], row['fw_n2_sigma_sh2_kpc']
            # Order inner/outer by radius
            if r1 <= r2:
                inner = (r1, M1, s1); outer = (r2, M2, s2)
            else:
                inner = (r2, M2, s2); outer = (r1, M1, s1)
            rows.append({
                'Galaxy': gal, 'T': row['T'], 'n_total': 2, 'position': 'inner',
                'r_sh_kpc': inner[0], 'M_sh': inner[1], 'sigma_sh_kpc': inner[2],
            })
            rows.append({
                'Galaxy': gal, 'T': row['T'], 'n_total': 2, 'position': 'outer',
                'r_sh_kpc': outer[0], 'M_sh': outer[1], 'sigma_sh_kpc': outer[2],
            })
    return pd.DataFrame(rows)


def write_summary(df_full, df_clean, sample, classif, fout):
    """Write the formatted statistical summary."""
    full_stats = compute_scaling_stats(df_full, "FULL")
    clean_stats = compute_scaling_stats(df_clean, "CLEAN")
    bulge_full = compute_bulge_OR(df_full, sample, classif)
    bulge_clean = compute_bulge_OR(df_clean, sample, classif)
    rho_full, p_full, rows_full = compute_morphology_gradient(df_full, sample)
    rho_clean, p_clean, rows_clean = compute_morphology_gradient(df_clean, sample)
    
    with open(fout, 'w') as f:
        f.write("=" * 76 + "\n")
        f.write("ANTI-WARP SUBSAMPLE ANALYSIS — Paper 2 §3.3\n")
        f.write("=" * 76 + "\n\n")
        f.write("Clean subsample cuts: shells with all of —\n")
        f.write(f"  - r_shell / R_HI < {R_OVER_RHI_MAX}\n")
        f.write("  - disk-dominated at shell radius (V_disk² + V_bulge² > V_gas²)\n")
        f.write(f"  - Q == {QUALITY_FLAG} (highest-quality SPARC galaxy)\n")
        f.write("  - inner shell of any n=2 pair (drop outer)\n\n")
        f.write(f"Total shells: {len(df_full)} across {df_full['Galaxy'].nunique()} galaxies\n")
        f.write(f"Clean shells: {len(df_clean)} across {df_clean['Galaxy'].nunique()} galaxies\n\n")
        
        f.write("=" * 76 + "\n")
        f.write("SCALING RELATIONS\n")
        f.write("=" * 76 + "\n\n")
        f.write(f"{'':<28}{'FULL':<20}{'CLEAN':<20}\n")
        f.write(f"{'n':<28}{full_stats['n']:<20}{clean_stats['n']:<20}\n")
        f.write(f"{'M slope':<28}{full_stats['M_slope']:<20.2f}{clean_stats['M_slope']:<20.2f}\n")
        f.write(f"{'  Spearman ρ':<28}{full_stats['M_rho']:<+20.3f}{clean_stats['M_rho']:<+20.3f}\n")
        f.write(f"{'  p-value':<28}{full_stats['M_rho_p']:<20.4f}{clean_stats['M_rho_p']:<20.4f}\n")
        f.write(f"{'σ slope':<28}{full_stats['sig_slope']:<20.2f}{clean_stats['sig_slope']:<20.2f}\n")
        f.write(f"{'  Spearman ρ':<28}{full_stats['sig_rho']:<+20.3f}{clean_stats['sig_rho']:<+20.3f}\n")
        f.write(f"{'  p-value':<28}{full_stats['sig_rho_p']:<20.4f}{clean_stats['sig_rho_p']:<20.4f}\n")
        f.write(f"{'σ/r median':<28}{full_stats['sigr_median']:<20.3f}{clean_stats['sigr_median']:<20.3f}\n")
        f.write(f"{'σ/r std':<28}{full_stats['sigr_std']:<20.3f}{clean_stats['sigr_std']:<20.3f}\n\n")
        
        f.write("=" * 76 + "\n")
        f.write("BULGE CORRELATION (galaxy-level)\n")
        f.write("=" * 76 + "\n\n")
        f.write(f"{'':<32}{'FULL':<20}{'CLEAN':<20}\n")
        f.write(f"{'Bulged SB rate':<32}{bulge_full['bulged_sb_rate']:<20}{bulge_clean['bulged_sb_rate']:<20}\n")
        f.write(f"{'Bulgeless SB rate':<32}{bulge_full['bulgeless_sb_rate']:<20}{bulge_clean['bulgeless_sb_rate']:<20}\n")
        f.write(f"{'Odds ratio':<32}{bulge_full['OR']:<20.2f}{bulge_clean['OR']:<20.2f}\n\n")
        
        f.write("=" * 76 + "\n")
        f.write("MORPHOLOGY GRADIENT (galaxy-level)\n")
        f.write("=" * 76 + "\n\n")
        f.write(f"  T    N_gal   SB rate (full)      SB rate (clean)\n")
        for rf, rc in zip(rows_full, rows_clean):
            f.write(f"  {rf['T']}    {rf['N_gal']:<7}{rf['SB_rate']*100:>6.1f}%             {rc['SB_rate']*100:>6.1f}%\n")
        f.write(f"\n  ρ_per_T (full):  {rho_full:+.3f}, p = {p_full:.4f}\n")
        f.write(f"  ρ_per_T (clean): {rho_clean:+.3f}, p = {p_clean:.4f}\n\n")


def main():
    log.info(f"Anti-warp subsample analysis — paper2 v1.0")
    log.info(f"Working directory: {HERE}")
    log.info(f"Data directory: {DATA_DIR}")
    
    # Verify inputs
    for f in [CANONICAL_CSV, SAMPLE_CSV, CLASSIF_CSV]:
        if not f.exists():
            log.error(f"REQUIRED INPUT MISSING: {f}")
            if f == CANONICAL_CSV:
                log.error("This file comes from Paper I v7.1.0:")
                log.error("  https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0")
                log.error(f"  Place it at: {f}")
            sys.exit(1)
    
    if not ROTMOD_DIR.exists() or len(list(ROTMOD_DIR.glob('*.dat'))) == 0:
        log.error(f"REQUIRED INPUT MISSING: {ROTMOD_DIR}/*_rotmod.dat")
        sys.exit(1)
    
    # Load inputs
    canonical = pd.read_csv(CANONICAL_CSV)
    sample = pd.read_csv(SAMPLE_CSV)
    classif = pd.read_csv(CLASSIF_CSV)
    
    log.info(f"Canonical CSV: {len(canonical)} rows")
    log.info(f"Sample CSV: {len(sample)} rows")
    log.info(f"Classification CSV: {len(classif)} rows")
    log.info(f"Excluded galaxies: {EXCLUDE_GALAXIES}")
    
    # Parse canonical → per-shell
    df_shells = parse_canonical_to_per_shell(canonical, EXCLUDE_GALAXIES)
    log.info(f"Parsed {len(df_shells)} shells across {df_shells['Galaxy'].nunique()} galaxies")
    
    # Apply cuts
    df_shells = apply_antiwarp_cuts(df_shells, sample, classif)
    df_clean = df_shells[df_shells['is_clean']].copy()
    log.info(f"Clean subsample: {len(df_clean)} shells across {df_clean['Galaxy'].nunique()} galaxies")
    
    # Save per-shell catalog
    cols_out = ['Galaxy','T','Q','n_total','position','r_sh_kpc','M_sh','sigma_sh_kpc',
                'sigma_over_r','r_over_RHI','V_gas_at_kms','V_disk_at_kms',
                'V_bulge_at_kms','is_disk_dominated','is_inner','is_bulge_dom',
                'is_bulgeless','is_clean']
    df_shells[cols_out].to_csv(OUT_PER_SHELL, index=False)
    log.info(f"Wrote {OUT_PER_SHELL}")
    
    # Save summary
    write_summary(df_shells, df_clean, sample, classif, OUT_SUMMARY)
    log.info(f"Wrote {OUT_SUMMARY}")
    
    log.info("Done.")


if __name__ == "__main__":
    main()

"""
make_figures.py — Paper II figure generation.

Generates all manuscript figures from project data CSVs. One function per figure;
runnable individually or all at once. Output: ../figures/ as PDF + PNG.

Usage:
  python3 make_figures.py --all
  python3 make_figures.py --figure 3.1.1
  python3 make_figures.py --figure 3.1.1,3.1.2
  python3 make_figures.py --list

Data sources (resolved automatically from package layout or local fallback):
  ../antiwarp_per_shell.csv         (67 shells, 51 galaxies, 101-galaxy sample)
  ../galaxy_classifications.csv     (123 galaxies, full SPARC + classifications)
  ../shell_reality_out_n100/per_realization.csv  (N=100 null realizations; scramble + permute, 100 each)
  ../upsilon_perturbation_per_galaxy.csv     (2040 rows: 102 galaxies × 20 realizations)
  ../distance_perturbation_per_galaxy.csv    (2040 rows)
  ../inclination_perturbation_per_galaxy.csv (1820 rows)
  ../backbone_shift.csv                      (102 galaxies; §3.3.7 joint refit at n={0,1,2})
  ../einasto_full_sample_results.csv         (102 galaxies; Paper I §3.7 — EXTERNAL, copy from sparc-halo-shells repo)

Coverage:
  Fig 3.1.1   bulge correlation                    ✓ buildable
  Fig 3.1.2   scaling relations (M-r, σ-r, σ/r)    ✓ buildable
  Fig 3.1.3   σ/r quartile gradient                ✓ buildable
  Fig 3.1.4   inner-vs-outer (two-shell paired)    ✓ buildable
  Fig 3.2.1   scramble null distribution           ✓ buildable
  Fig 3.2.2   permute null distribution            ✓ buildable
  Fig 3.3.1   disk dynamical scale coincidence     ✓ partial (3 of 4 panels)
  Fig 3.3.2   Υ perturbation stability             ✓ buildable
  Fig 3.3.3   distance perturbation stability      ✓ buildable
  Fig 3.3.4   inclination perturbation stability   ✓ buildable
  Fig 3.3.5   anti-warp clean subsample            ✓ buildable
  Fig 3.3.6   Einasto backbone comparison          ✓ buildable (requires data/einasto_full_sample_results.csv from Paper I)
  Fig 3.3.7   backbone-shift test                  ✓ buildable (101-galaxy convention; uses data/backbone_shift.csv)
  Fig 3.3.8   covariate forest plot                ✓ buildable (uses data/covariate_results.csv + data/covariate_matched_results.csv)

Tested against project data; numerical outputs match manuscript values.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator
from scipy.stats import spearmanr, wilcoxon, kstest, fisher_exact
import warnings
warnings.filterwarnings('ignore')


# ============================================================
# Path resolution
# ============================================================
_HERE = os.path.dirname(os.path.abspath(__file__))
_PACKAGE = os.path.dirname(_HERE)


def _resolve_data(filename):
    """Find data CSV in package root or local fallback."""
    candidates = [
        os.path.join(_PACKAGE, filename),
        os.path.join(_PACKAGE, 'data', filename),
        os.path.join('.', filename),
        os.path.join('..', filename),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    raise FileNotFoundError(f"Data file not found in any of: {candidates}")


def _output_dir():
    """Resolve figures output directory (../figures/ relative to scripts/)."""
    candidates = [
        os.path.join(_PACKAGE, 'figures'),
        os.path.join('.', 'figures'),
        os.path.join('..', 'figures'),
    ]
    for p in candidates:
        if os.path.isdir(p) or os.path.isdir(os.path.dirname(p)):
            os.makedirs(p, exist_ok=True)
            return p
    # Last resort
    out = os.path.join(_PACKAGE, 'figures')
    os.makedirs(out, exist_ok=True)
    return out


# ============================================================
# Style configuration — applied once at module load
# ============================================================
def _configure_style():
    """Publication-quality matplotlib defaults. AASTeX-compatible."""
    plt.rcParams.update({
        # Fonts — use mathtext for math, no LaTeX dependency required
        'font.family':       'serif',
        'font.serif':        ['DejaVu Serif', 'Times New Roman', 'Times'],
        'mathtext.fontset':  'dejavuserif',
        'font.size':         9,
        'axes.labelsize':    10,
        'axes.titlesize':    10,
        'xtick.labelsize':   8,
        'ytick.labelsize':   8,
        'legend.fontsize':   8,
        # Lines and markers
        'lines.linewidth':   1.2,
        'lines.markersize':  4,
        'axes.linewidth':    0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.minor.width': 0.5,
        'ytick.minor.width': 0.5,
        # Ticks
        'xtick.direction':   'in',
        'ytick.direction':   'in',
        'xtick.top':         True,
        'ytick.right':       True,
        'xtick.minor.visible': True,
        'ytick.minor.visible': True,
        # Layout
        'figure.dpi':        150,
        'savefig.dpi':       300,
        'savefig.bbox':      'tight',
        'savefig.pad_inches': 0.05,
        # Misc
        'axes.grid':         False,
        'legend.frameon':    False,
        'legend.handlelength': 1.5,
    })


# Color palette — distinguishable in grayscale, AAS-friendly
COLORS = {
    'primary':    '#1f77b4',  # dark blue
    'secondary':  '#d62728',  # dark red
    'tertiary':   '#2ca02c',  # dark green
    'highlight':  '#ff7f0e',  # orange (for "highlighted" subsets)
    'neutral':    '#7f7f7f',  # mid-gray
    'reference':  '#bcbcbc',  # light gray (for "real data" or "expected" reference)
    'null_burk':  '#9467bd',  # purple (Burkert-truth null)
    'null_nfw':   '#8c564b',  # brown (NFW-truth null)
    'scramble':   '#1f77b4',  # blue
    'permute':    '#d62728',  # red
    'bulge_dom':  '#d62728',  # red
    'bulgeless':  '#1f77b4',  # blue
}


# AASTeX column widths (inches)
WIDTH_SINGLE = 3.4    # single-column
WIDTH_DOUBLE = 7.0    # double-column / full page-width


# ============================================================
# Output helper
# ============================================================
def _save_figure(fig, name, also_png=True):
    """Save figure as PDF (primary) and PNG (preview) into ../figures/."""
    outdir = _output_dir()
    pdf_path = os.path.join(outdir, f'{name}.pdf')
    fig.savefig(pdf_path, format='pdf')
    if also_png:
        png_path = os.path.join(outdir, f'{name}.png')
        fig.savefig(png_path, format='png')
    plt.close(fig)
    return pdf_path


# ============================================================
# Fig 3.1.1 — Bulge correlation
# ============================================================
def fig_3_1_1():
    """
    Bulge-dominated galaxies preferentially host shells.
    Stacked bar of bulge-dom vs bulgeless, with shell-bearing fraction.
    Reproduces manuscript §3.1.1: OR = 3.67, Fisher p ≈ 0.01.
    """
    gc = pd.read_csv(_resolve_data('galaxy_classifications.csv'))
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))

    # 101-galaxy convention: T=2-9, NGC 6674 excluded
    g101 = gc[(gc['T'] >= 2) & (gc['T'] <= 9) & (gc['Galaxy'] != 'NGC6674')].copy()
    shell_bearing = set(sh['Galaxy'].unique())
    g101['shellbearing'] = g101['Galaxy'].isin(shell_bearing)

    # Counts
    bulge_dom    = g101[g101['is_bulge_dom']]
    bulgeless    = g101[g101['is_bulgeless']]
    n_bd, sb_bd = len(bulge_dom), bulge_dom['shellbearing'].sum()
    n_bl, sb_bl = len(bulgeless), bulgeless['shellbearing'].sum()

    # Stats — manuscript §3.1.1 reports OR = 3.67, Fisher one-sided p = 0.0064.
    # Using alternative='greater': H1 is that bulged galaxies have a higher
    # shell-bearing rate than bulgeless (the directional hypothesis stated in
    # the manuscript). Two-sided would give p ≈ 0.017 and disagree with §3.1.1.
    table = np.array([[sb_bd, n_bd - sb_bd],
                      [sb_bl, n_bl - sb_bl]])
    odds_ratio, fisher_p = fisher_exact(table, alternative='greater')

    # Figure: single column, stacked bars
    fig, ax = plt.subplots(figsize=(WIDTH_SINGLE, 2.8))
    labels = ['Bulge-dominated', 'Bulgeless']
    sb = [sb_bd, sb_bl]
    ns = [n_bd - sb_bd, n_bl - sb_bl]
    x = np.arange(2)
    width = 0.6

    p1 = ax.bar(x, sb, width, color=[COLORS['bulge_dom'], COLORS['bulgeless']],
                label='Shell-bearing', edgecolor='black', linewidth=0.5)
    p2 = ax.bar(x, ns, width, bottom=sb,
                color=[COLORS['bulge_dom'], COLORS['bulgeless']], alpha=0.35,
                label='Non-shell-bearing', edgecolor='black', linewidth=0.5)

    # Annotations
    for i, (s, n_total) in enumerate(zip(sb, [n_bd, n_bl])):
        frac = 100 * s / n_total
        ax.text(i, s/2, f'{s}/{n_total}\n{frac:.1f}%',
                ha='center', va='center', fontsize=9,
                fontweight='bold', color='white')
        ax.text(i, s + (n_total - s)/2, f'{n_total - s}',
                ha='center', va='center', fontsize=9, color='black', alpha=0.6)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Number of galaxies')
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, max(n_bd, n_bl) * 1.15)

    # Stats box
    stat_text = (f'OR = {odds_ratio:.2f}\n'
                 f'Fisher $p = {fisher_p:.4f}$\n'
                 f'(one-sided)')
    ax.text(0.98, 0.97, stat_text, transform=ax.transAxes,
            ha='right', va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.3', alpha=0.9))

    ax.legend(loc='upper left', fontsize=8)
    ax.set_title('Bulge-dominated galaxies preferentially host shells')

    print(f"  bulge-dom: {sb_bd}/{n_bd} = {100*sb_bd/n_bd:.1f}% shell-bearing")
    print(f"  bulgeless: {sb_bl}/{n_bl} = {100*sb_bl/n_bl:.1f}% shell-bearing")
    print(f"  OR={odds_ratio:.2f}, Fisher p={fisher_p:.4f}")
    return _save_figure(fig, 'fig_3_1_1_bulge_correlation')


# ============================================================
# Fig 3.1.2 — Scaling relations (M-r, σ-r, σ/r vs r)
# ============================================================
def fig_3_1_2():
    """
    Three-panel: M-r scaling, σ-r scaling, σ/r vs r.
    Reproduces manuscript §3.1.2-3.1.3:
      M-r: slope 0.76, Spearman ρ=+0.64, p<1e-4
      σ-r: slope 1.04, Spearman ρ=+0.78, p<1e-4
      σ/r: median 0.275, std 0.116
    """
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    r   = sh['r_sh_kpc'].values
    M   = sh['M_sh'].values
    sig = sh['sigma_sh_kpc'].values
    sor = sh['sigma_over_r'].values

    logr = np.log10(r)
    logM = np.log10(M)
    logsig = np.log10(sig)

    # Linear fits in log space
    m_slope, m_intercept = np.polyfit(logr, logM, 1)
    s_slope, s_intercept = np.polyfit(logr, logsig, 1)
    rho_M, p_M     = spearmanr(r, M)
    rho_S, p_S     = spearmanr(r, sig)

    fig, axes = plt.subplots(1, 3, figsize=(WIDTH_DOUBLE, 2.5))

    # --- Panel 1: M-r ---
    ax = axes[0]
    ax.loglog(r, M, 'o', ms=4, mfc=COLORS['primary'], mec='black', mew=0.3, alpha=0.7)
    r_line = np.logspace(np.log10(r.min()*0.9), np.log10(r.max()*1.1), 100)
    M_line = 10**(m_slope * np.log10(r_line) + m_intercept)
    ax.loglog(r_line, M_line, '-', color=COLORS['secondary'], lw=1.2,
              label=f'slope={m_slope:.2f}')
    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$M_{\rm sh}$ ($M_\odot$)')
    ax.text(0.04, 0.96, f'$\\rho = {rho_M:+.2f}$\n$p < 10^{{-4}}$',
            transform=ax.transAxes, va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=8)
    ax.set_title('Mass-radius scaling')

    # --- Panel 2: σ-r ---
    ax = axes[1]
    ax.loglog(r, sig, 'o', ms=4, mfc=COLORS['tertiary'], mec='black', mew=0.3, alpha=0.7)
    sig_line = 10**(s_slope * np.log10(r_line) + s_intercept)
    ax.loglog(r_line, sig_line, '-', color=COLORS['secondary'], lw=1.2,
              label=f'slope={s_slope:.2f}')
    # Hard cap: σ/r = 0.4 line
    ax.loglog(r_line, 0.4 * r_line, '--', color=COLORS['neutral'], lw=0.8,
              label=r'$\sigma/r \leq 0.4$ cap')
    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$\sigma_{\rm sh}$ (kpc)')
    ax.text(0.04, 0.96, f'$\\rho = {rho_S:+.2f}$\n$p < 10^{{-4}}$',
            transform=ax.transAxes, va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=8)
    ax.set_title('Width-radius scaling')

    # --- Panel 3: σ/r vs r ---
    ax = axes[2]
    ax.semilogx(r, sor, 'o', ms=4, mfc=COLORS['highlight'], mec='black', mew=0.3, alpha=0.7)
    median = np.median(sor)
    ax.axhline(median, color=COLORS['secondary'], lw=1.2,
               label=f'median $= {median:.3f}$')
    ax.axhline(0.4, ls='--', color=COLORS['neutral'], lw=0.8,
               label=r'$\sigma/r \leq 0.4$ cap')
    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$\sigma_{\rm sh}/r_{\rm sh}$')
    ax.set_ylim(0, 0.45)
    ax.set_title(r'Fractional width $\sigma/r$')
    ax.text(0.04, 0.96, f'median = {median:.3f}\nstd = {sor.std():.3f}',
            transform=ax.transAxes, va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=8)

    plt.tight_layout()
    print(f"  M-r: slope={m_slope:.2f}, ρ={rho_M:+.2f}, p={p_M:.2e}")
    print(f"  σ-r: slope={s_slope:.2f}, ρ={rho_S:+.2f}, p={p_S:.2e}")
    print(f"  σ/r: median={median:.3f}, std={sor.std():.3f}")
    return _save_figure(fig, 'fig_3_1_2_scaling_relations')


# ============================================================
# Fig 3.1.3 — σ/r vs radius quartile gradient
# ============================================================
def fig_3_1_3():
    """
    σ/r by radius quartile — tests for systematic gradient in fractional width.
    Box-and-whiskers per quartile + per-shell scatter overlay.
    """
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    r   = sh['r_sh_kpc'].values
    sor = sh['sigma_over_r'].values

    # Quartile binning
    quartiles_cat = pd.qcut(r, 4)
    qranges = quartiles_cat.categories
    quartiles = pd.qcut(r, 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    qlabels = [f'Q{i+1}\n[{q.left:.1f}–{q.right:.1f}]\nkpc'
               for i, q in enumerate(qranges)]

    df = pd.DataFrame({'sor': sor, 'q': quartiles, 'r': r})

    fig, ax = plt.subplots(figsize=(WIDTH_SINGLE * 1.2, 2.8))

    # Box plot
    box_data = [df[df['q'].astype(str) == qstr]['sor'].values
                for qstr in df['q'].astype(str).unique()]
    # Get them in order
    box_data = [df[df['q'] == q]['sor'].values for q in quartiles.unique()
                if not pd.isna(q)]

    bp = ax.boxplot(box_data, positions=range(1, 5),
                    widths=0.5, patch_artist=True,
                    boxprops=dict(facecolor=COLORS['primary'], alpha=0.4,
                                   edgecolor=COLORS['primary']),
                    medianprops=dict(color=COLORS['secondary'], linewidth=1.3),
                    whiskerprops=dict(color='black', linewidth=0.7),
                    capprops=dict(color='black', linewidth=0.7),
                    flierprops=dict(marker='o', markersize=2.5,
                                    markerfacecolor=COLORS['neutral'],
                                    markeredgecolor='black', markeredgewidth=0.3))

    # Scatter overlay (small jitter on x)
    rng = np.random.default_rng(seed=42)
    for i, q in enumerate(quartiles.unique()):
        if pd.isna(q):
            continue
        sub = df[df['q'] == q]['sor'].values
        xj = rng.uniform(-0.12, 0.12, size=len(sub)) + (i + 1)
        ax.scatter(xj, sub, s=6, c=COLORS['highlight'], alpha=0.55,
                   edgecolors='black', linewidths=0.2)

    ax.axhline(0.4, ls='--', color=COLORS['neutral'], lw=0.8, alpha=0.7,
               label=r'$\sigma/r = 0.4$ cap')
    overall_median = np.median(sor)
    ax.axhline(overall_median, ls=':', color=COLORS['secondary'], lw=0.8,
               label=f'population median = {overall_median:.3f}')

    ax.set_xticks(range(1, 5))
    ax.set_xticklabels(qlabels, fontsize=7)
    ax.set_xlabel(r'$r_{\rm sh}$ quartile (kpc)')
    ax.set_ylabel(r'$\sigma_{\rm sh}/r_{\rm sh}$')
    ax.set_ylim(0, 0.45)
    ax.legend(loc='lower left', fontsize=7)
    ax.set_title(r'Fractional width by radius quartile')

    # Quartile-level medians, for the test
    q_medians = [np.median(b) for b in box_data]
    rho_q, p_q = spearmanr([1, 2, 3, 4], q_medians)
    ax.text(0.98, 0.97,
            f'quartile medians:\n{q_medians[0]:.3f}, {q_medians[1]:.3f}, '
            f'{q_medians[2]:.3f}, {q_medians[3]:.3f}\n'
            f'Spearman $\\rho = {rho_q:+.2f}$',
            transform=ax.transAxes, va='top', ha='right', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))

    print(f"  quartile medians: {q_medians}")
    print(f"  Spearman ρ across quartiles: {rho_q:+.2f}, p={p_q:.3f}")
    return _save_figure(fig, 'fig_3_1_3_sigma_over_r_quartile')


# ============================================================
# Fig 3.1.4 — Inner-vs-outer paired comparison (two-shell galaxies)
# ============================================================
def fig_3_1_4():
    """
    Two-shell paired comparison: inner vs outer mass and width.
    Reproduces manuscript §3.1.4 inner-vs-outer signature.
    """
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    # Two-shell galaxies (n_total = 2)
    two = sh[sh['n_total'] == 2].copy()
    inner = two[two['position'] == 'inner'].sort_values('Galaxy').reset_index(drop=True)
    outer = two[two['position'] == 'outer'].sort_values('Galaxy').reset_index(drop=True)

    # Wilcoxon paired tests
    M_in, M_out = inner['M_sh'].values, outer['M_sh'].values
    s_in, s_out = inner['sigma_sh_kpc'].values, outer['sigma_sh_kpc'].values
    w_M, p_M = wilcoxon(M_out, M_in, alternative='greater')
    w_s, p_s = wilcoxon(s_out, s_in, alternative='greater')

    n_pairs = len(inner)
    n_out_heavier = int(np.sum(M_out > M_in))
    n_out_wider = int(np.sum(s_out > s_in))

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE * 0.85, 3.0))

    # --- Panel 1: mass ---
    ax = axes[0]
    diag_min = min(M_in.min(), M_out.min()) * 0.6
    diag_max = max(M_in.max(), M_out.max()) * 1.6
    ax.loglog([diag_min, diag_max], [diag_min, diag_max], '--',
              color=COLORS['neutral'], lw=0.8, label='outer = inner')
    ax.loglog(M_in, M_out, 'o', ms=6, mfc=COLORS['primary'],
              mec='black', mew=0.5, alpha=0.8)
    ax.set_xlabel(r'inner shell $M_{\rm sh}$ ($M_\odot$)')
    ax.set_ylabel(r'outer shell $M_{\rm sh}$ ($M_\odot$)')
    ax.set_xlim(diag_min, diag_max)
    ax.set_ylim(diag_min, diag_max)
    ax.set_aspect('equal', adjustable='box')
    ax.text(0.04, 0.96,
            f'$n = {n_pairs}$ pairs\n'
            f'$M_{{\\rm outer}} > M_{{\\rm inner}}$: {n_out_heavier}/{n_pairs}\n'
            f'Wilcoxon $p = {p_M:.4f}$',
            transform=ax.transAxes, va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.set_title('Mass: outer vs inner')
    ax.legend(loc='lower right', fontsize=7)

    # --- Panel 2: width ---
    ax = axes[1]
    diag_min = min(s_in.min(), s_out.min()) * 0.6
    diag_max = max(s_in.max(), s_out.max()) * 1.6
    ax.loglog([diag_min, diag_max], [diag_min, diag_max], '--',
              color=COLORS['neutral'], lw=0.8, label='outer = inner')
    ax.loglog(s_in, s_out, 'o', ms=6, mfc=COLORS['tertiary'],
              mec='black', mew=0.5, alpha=0.8)
    ax.set_xlabel(r'inner shell $\sigma_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'outer shell $\sigma_{\rm sh}$ (kpc)')
    ax.set_xlim(diag_min, diag_max)
    ax.set_ylim(diag_min, diag_max)
    ax.set_aspect('equal', adjustable='box')
    ax.text(0.04, 0.96,
            f'$n = {n_pairs}$ pairs\n'
            f'$\\sigma_{{\\rm outer}} > \\sigma_{{\\rm inner}}$: {n_out_wider}/{n_pairs}\n'
            f'Wilcoxon $p = {p_s:.4f}$',
            transform=ax.transAxes, va='top', fontsize=8,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.set_title('Width: outer vs inner')
    ax.legend(loc='lower right', fontsize=7)

    plt.tight_layout()
    print(f"  Mass: outer heavier in {n_out_heavier}/{n_pairs}, Wilcoxon p={p_M:.4f}")
    print(f"  Width: outer wider in {n_out_wider}/{n_pairs}, Wilcoxon p={p_s:.4f}")
    return _save_figure(fig, 'fig_3_1_4_inner_vs_outer')


# ============================================================
# Helper: null figure
# ============================================================
def _null_figure(null_type, name, title_suffix, color):
    """Generic null-distribution figure for scramble or permute."""
    # Body text §3.2 quotes the N=100 batch (mean=-0.289 std=0.229 for scramble,
    # mean=+0.350 std=0.235 for permute). That data lives in
    # data/shell_reality_out_n100/per_realization.csv. Reading data/per_realization.csv
    # would silently pick up an N=20 leftover and contradict the body.
    pr = pd.read_csv(_resolve_data('shell_reality_out_n100/per_realization.csv'))
    sub = pr[pr['null_type'] == null_type]
    n_real = len(sub)

    # Real-data baseline from per_realization.csv: stored in nulls? No, in summary.
    # Hardcode baseline (computed live from canonical CSV at run time = -0.833 / -0.296):
    real_rho_per_T = -0.833
    real_rho_per_gal = -0.296

    rho_T   = sub['rho_per_T'].dropna().values
    rho_gal = sub['rho_per_gal'].dropna().values

    p_emp_T   = int(np.sum(rho_T   <= real_rho_per_T))   / max(len(rho_T), 1)
    p_emp_gal = int(np.sum(rho_gal <= real_rho_per_gal)) / max(len(rho_gal), 1)
    count_T   = (int(np.sum(rho_T   <= real_rho_per_T)),   len(rho_T))
    count_gal = (int(np.sum(rho_gal <= real_rho_per_gal)), len(rho_gal))

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE * 0.85, 2.8))

    # Format the real-data rho values so the minus sign is forced into the
    # regular-text portion of the label rather than into mathtext, where some
    # backends/fonts drop U+2212. Using `:+.3f` guarantees a literal '-' or '+'
    # character before the digits.
    rho_T_label   = f'real data: $\\rho$ = {real_rho_per_T:+.3f}'
    rho_gal_label = f'real data: $\\rho$ = {real_rho_per_gal:+.3f}'

    # --- Panel 1: per-T-bin Spearman rho ---
    ax = axes[0]
    bins = max(8, int(np.sqrt(len(rho_T))))
    ax.hist(rho_T, bins=bins, color=color, alpha=0.6, edgecolor='black', lw=0.5)
    ax.axvline(real_rho_per_T, color=COLORS['secondary'], lw=1.5,
               label=rho_T_label)
    ax.axvline(0, color=COLORS['neutral'], lw=0.6, ls=':', alpha=0.6)
    ax.set_xlabel(r'$\rho_{\rm per\text{-}T}$ (null realizations)')
    ax.set_ylabel('count')
    ax.legend(loc='upper left', fontsize=7)
    ax.text(0.97, 0.95,
            f'$n = {len(rho_T)}$ real.\n'
            f'mean = {rho_T.mean():+.3f}\n'
            f'std  = {rho_T.std():.3f}\n'
            f'emp. $p = {count_T[0]}/{count_T[1]}$',
            transform=ax.transAxes, va='top', ha='right', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.set_title(r'Per-$T$-bin trend')

    # --- Panel 2: per-galaxy Spearman rho ---
    ax = axes[1]
    bins = max(8, int(np.sqrt(len(rho_gal))))
    ax.hist(rho_gal, bins=bins, color=color, alpha=0.6, edgecolor='black', lw=0.5)
    ax.axvline(real_rho_per_gal, color=COLORS['secondary'], lw=1.5,
               label=rho_gal_label)
    ax.axvline(0, color=COLORS['neutral'], lw=0.6, ls=':', alpha=0.6)
    ax.set_xlabel(r'$\rho_{\rm per\text{-}galaxy}$ (null realizations)')
    ax.set_ylabel('count')
    ax.legend(loc='upper left', fontsize=7)
    ax.text(0.97, 0.95,
            f'$n = {len(rho_gal)}$ real.\n'
            f'mean = {rho_gal.mean():+.3f}\n'
            f'std  = {rho_gal.std():.3f}\n'
            f'emp. $p = {count_gal[0]}/{count_gal[1]}$',
            transform=ax.transAxes, va='top', ha='right', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.set_title(r'Per-galaxy trend')

    fig.suptitle(f'{title_suffix} null distribution (N = {n_real} realizations)',
                 fontsize=10, y=1.02)
    plt.tight_layout()
    print(f"  {null_type} N={n_real}: ρ_T mean={rho_T.mean():+.3f} std={rho_T.std():.3f}, "
          f"emp p={count_T[0]}/{count_T[1]}; "
          f"ρ_gal mean={rho_gal.mean():+.3f} std={rho_gal.std():.3f}, "
          f"emp p={count_gal[0]}/{count_gal[1]}")
    return _save_figure(fig, name)


def fig_3_2_1():
    """Scramble null distribution (within-galaxy DM residual scrambling)."""
    return _null_figure('scramble', 'fig_3_2_1_scramble_null',
                        'Scramble', COLORS['scramble'])


def fig_3_2_2():
    """Permute null distribution (V_obs permutation across radii)."""
    return _null_figure('permute', 'fig_3_2_2_permute_null',
                        'Permute', COLORS['permute'])


# ============================================================
# Fig 3.3.1 — Disk dynamical scale coincidence
# ============================================================
def fig_3_3_1():
    """
    Three-panel CDF: |r_sh - r_scale|/r_scale for Rdisk, 2.15·Rdisk, Reff.
    Compares observed shell-radii distribution against uniform-placement null.
    (V_rot peak panel deferred — requires Rotmod-file parsing for V_rot maximum.)
    """
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    gc = pd.read_csv(_resolve_data('galaxy_classifications.csv'))

    # Join shell catalog with galaxy properties
    merged = sh.merge(gc[['Galaxy', 'Rdisk', 'Reff', 'RHI']], on='Galaxy', how='left')
    merged = merged.dropna(subset=['Rdisk', 'Reff'])

    # Three candidate scales (V_rot peak deferred)
    scales = {
        r'$R_{\rm disk}$': merged['Rdisk'].values,
        r'$2.15\,R_{\rm disk}$': 2.15 * merged['Rdisk'].values,
        r'$R_{\rm eff}$': merged['Reff'].values,
    }
    r_sh = merged['r_sh_kpc'].values

    fig, axes = plt.subplots(1, 3, figsize=(WIDTH_DOUBLE, 2.6))

    for ax, (label, r_scale) in zip(axes, scales.items()):
        dist = np.abs(r_sh - r_scale) / r_scale
        dist_sorted = np.sort(dist)
        cdf = np.arange(1, len(dist_sorted) + 1) / len(dist_sorted)
        ax.plot(dist_sorted, cdf, '-', color=COLORS['primary'], lw=1.4,
                label='observed shells')

        # Uniform-placement null: shells distributed uniformly across [0, max(r_sh)]
        # within each galaxy. Approximate: distribute uniform on [0, observed r_sh max]
        rng = np.random.default_rng(seed=42)
        n_null = 2000
        # For each null shell, sample a galaxy and a uniform radius in that galaxy's range
        gal_groups = merged.groupby('Galaxy').first()
        gal_names = gal_groups.index.values
        gal_rdisk = gal_groups['Rdisk'].values
        gal_reff  = gal_groups['Reff'].values
        scale_by_galaxy = {
            r'$R_{\rm disk}$':       dict(zip(gal_names, gal_rdisk)),
            r'$2.15\,R_{\rm disk}$': dict(zip(gal_names, 2.15 * gal_rdisk)),
            r'$R_{\rm eff}$':        dict(zip(gal_names, gal_reff)),
        }
        # Sample observed r_sh values' galaxies uniformly and r_max from that galaxy
        null_dists = []
        r_max_overall = r_sh.max()
        for _ in range(n_null):
            r_rand = rng.uniform(0, r_max_overall)
            g_rand = rng.choice(merged['Galaxy'].values)
            r_scale_g = scale_by_galaxy[label].get(g_rand, np.nan)
            if r_scale_g and not np.isnan(r_scale_g):
                null_dists.append(np.abs(r_rand - r_scale_g) / r_scale_g)
        null_dists = np.array(null_dists)
        null_sorted = np.sort(null_dists)
        null_cdf = np.arange(1, len(null_sorted) + 1) / len(null_sorted)
        ax.plot(null_sorted, null_cdf, '--', color=COLORS['neutral'], lw=1.0,
                label='uniform null')

        # KS test
        ks_stat, ks_p = kstest(dist, null_dists)

        ax.set_xlabel(rf'$|r_{{\rm sh}} - $ {label}$|\,/\,$ {label}')
        ax.set_ylabel('CDF')
        ax.set_xlim(0, min(np.percentile(np.concatenate([dist, null_dists]), 99), 5))
        ax.set_ylim(0, 1.05)
        ax.set_title(label)
        ax.text(0.96, 0.05, f'KS $p = {ks_p:.3f}$',
                transform=ax.transAxes, ha='right', va='bottom', fontsize=8,
                bbox=dict(facecolor='white', edgecolor='gray',
                          boxstyle='round,pad=0.25', alpha=0.9))
        ax.legend(loc='center right', fontsize=7)

    plt.tight_layout()
    print(f"  3 of 4 disk dynamical scales tested (V_rot peak panel deferred)")
    return _save_figure(fig, 'fig_3_3_1_disk_dynamical_scales')


# ============================================================
# Helper: perturbation stability figure
# ============================================================
def _perturbation_figure(csv_name, label, name, color, n_realizations=20):
    """
    Generic perturbation stability figure:
      Left panel: stacked bar of n_shells stability by canonical class
      Right panel: scatter of perturbed vs canonical r_sh1
    """
    df = pd.read_csv(_resolve_data(csv_name))
    # Strip whitespace from columns
    df.columns = [c.strip() for c in df.columns]

    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    # Canonical n_shells per galaxy: 0 if not in shell catalog, otherwise n_total
    gc = pd.read_csv(_resolve_data('galaxy_classifications.csv'))
    g102 = gc[(gc['T'] >= 2) & (gc['T'] <= 9)]['Galaxy'].values
    canon_n = {}
    for g in g102:
        rows = sh[sh['Galaxy'] == g]
        if len(rows) == 0:
            canon_n[g] = 0
        else:
            canon_n[g] = int(rows['n_total'].iloc[0])

    # Filter only successful fits
    df_ok = df[df['status'].astype(str).str.strip() == 'ok'].copy()

    df_ok['canon_n'] = df_ok['Galaxy'].map(canon_n)
    df_ok['matches'] = (df_ok['n_shells'] == df_ok['canon_n'])

    # Per-canonical-class stability
    classes = [0, 1, 2]
    match_rates = []
    counts = []
    for c in classes:
        sub = df_ok[df_ok['canon_n'] == c]
        if len(sub) > 0:
            rate = sub['matches'].mean() * 100
            match_rates.append(rate)
            counts.append(len(sub))
        else:
            match_rates.append(0.0)
            counts.append(0)

    overall_match = df_ok['matches'].mean() * 100

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE * 0.85, 2.8))

    # --- Panel 1: stability by canonical class ---
    ax = axes[0]
    x = np.arange(3)
    bars = ax.bar(x, match_rates, color=color, alpha=0.7,
                  edgecolor='black', linewidth=0.5)
    for i, (rate, ct) in enumerate(zip(match_rates, counts)):
        ax.text(i, rate + 1.5, f'{rate:.1f}%\n($n={ct}$)',
                ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(['canonical\n$n=0$', 'canonical\n$n=1$', 'canonical\n$n=2$'])
    ax.set_ylabel('per-fit match rate (%)')
    ax.set_ylim(0, 109)
    ax.axhline(overall_match, color=COLORS['secondary'], ls='--', lw=1.0,
               label=f'overall: {overall_match:.1f}%')
    ax.legend(loc='lower left', fontsize=7)
    ax.set_title(f'$n_{{\\rm shells}}$ stability by canonical class')

    # --- Panel 2: r_sh1 perturbed vs canonical (fully-stable shell-bearing only) ---
    ax = axes[1]
    sh_canon = sh[['Galaxy', 'r_sh_kpc', 'position', 'n_total']].copy()
    inner_canon = sh_canon[sh_canon['position'] == 'inner'].rename(
        columns={'r_sh_kpc': 'r_sh_canon'})
    df_fully_stable = df_ok[(df_ok['canon_n'] > 0) & (df_ok['matches'])].copy()
    df_fully_stable = df_fully_stable.merge(
        inner_canon[['Galaxy', 'r_sh_canon']], on='Galaxy', how='left')
    df_fully_stable = df_fully_stable.dropna(subset=['r_sh1', 'r_sh_canon'])

    r_canon = df_fully_stable['r_sh_canon'].values
    r_pert  = df_fully_stable['r_sh1'].values

    rmin = min(r_canon.min(), r_pert.min()) * 0.7
    rmax = max(r_canon.max(), r_pert.max()) * 1.4
    ax.loglog([rmin, rmax], [rmin, rmax], '--', color=COLORS['neutral'], lw=0.8,
              label='perturbed = canonical')
    # ±25% bands
    ax.loglog([rmin, rmax], [1.25*rmin, 1.25*rmax], ':', color=COLORS['neutral'],
              lw=0.6, alpha=0.7)
    ax.loglog([rmin, rmax], [0.75*rmin, 0.75*rmax], ':', color=COLORS['neutral'],
              lw=0.6, alpha=0.7, label=r'$\pm25\%$ band')
    ax.loglog(r_canon, r_pert, '.', ms=2.5, color=color, alpha=0.4)
    ax.set_xlabel(r'canonical $r_{\rm sh,1}$ (kpc)')
    ax.set_ylabel(r'perturbed $r_{\rm sh,1}$ (kpc)')
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(rmin, rmax)
    ax.set_aspect('equal', adjustable='box')

    # Scatter statistic: median |log10(r_pert/r_canon)|
    log_ratio = np.log10(r_pert / r_canon)
    median_scatter = np.median(np.abs(log_ratio))
    ax.text(0.04, 0.96,
            f'$n = {len(r_canon)}$ fits\n'
            f'median $|\\Delta \\log_{{10}} r| = {median_scatter:.3f}$ dex',
            transform=ax.transAxes, va='top', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=7)
    ax.set_title(r'$r_{\rm sh,1}$ stability')

    fig.suptitle(f'{label} perturbation stability (N = {n_realizations} realizations)',
                 fontsize=10, y=1.02)
    plt.tight_layout()
    print(f"  {label}: overall match {overall_match:.1f}%, "
          f"per-class [{match_rates[0]:.1f}%, {match_rates[1]:.1f}%, {match_rates[2]:.1f}%]")
    return _save_figure(fig, name)


def fig_3_3_2():
    """Υ perturbation stability."""
    return _perturbation_figure('upsilon_perturbation_per_galaxy.csv',
                                r'$\Upsilon$',
                                'fig_3_3_2_upsilon_perturbation',
                                COLORS['primary'])


def fig_3_3_3():
    """Distance perturbation stability."""
    return _perturbation_figure('distance_perturbation_per_galaxy.csv',
                                'Distance',
                                'fig_3_3_3_distance_perturbation',
                                COLORS['tertiary'])


def fig_3_3_4():
    """Inclination perturbation stability."""
    return _perturbation_figure('inclination_perturbation_per_galaxy.csv',
                                'Inclination',
                                'fig_3_3_4_inclination_perturbation',
                                COLORS['highlight'])


# ============================================================
# Fig 3.3.5 — Anti-warp clean subsample
# ============================================================
def fig_3_3_5():
    """
    Compare full-sample (67 shells) vs anti-warp clean subsample (25 shells)
    in M-r and σ-r scaling.
    """
    sh = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    clean = sh[sh['is_clean']]

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE * 0.85, 2.8))

    # --- Panel 1: M-r ---
    ax = axes[0]
    ax.loglog(sh['r_sh_kpc'], sh['M_sh'], 'o', ms=4,
              mfc=COLORS['reference'], mec='black', mew=0.3, alpha=0.7,
              label=f'full (n={len(sh)})')
    ax.loglog(clean['r_sh_kpc'], clean['M_sh'], 'o', ms=5,
              mfc=COLORS['highlight'], mec='black', mew=0.4,
              label=f'clean (n={len(clean)})')

    # Fits
    for data, color, lw in [(sh, COLORS['neutral'], 1.0),
                             (clean, COLORS['secondary'], 1.3)]:
        logr, logM = np.log10(data['r_sh_kpc']), np.log10(data['M_sh'])
        slope, intercept = np.polyfit(logr, logM, 1)
        r_line = np.logspace(np.log10(sh['r_sh_kpc'].min()*0.9),
                             np.log10(sh['r_sh_kpc'].max()*1.1), 100)
        ax.loglog(r_line, 10**(slope * np.log10(r_line) + intercept),
                  '-', color=color, lw=lw, alpha=0.8)

    rho_full,  _ = spearmanr(sh['r_sh_kpc'], sh['M_sh'])
    rho_clean, _ = spearmanr(clean['r_sh_kpc'], clean['M_sh'])
    slope_full,  _ = np.polyfit(np.log10(sh['r_sh_kpc']),    np.log10(sh['M_sh']),    1)
    slope_clean, _ = np.polyfit(np.log10(clean['r_sh_kpc']), np.log10(clean['M_sh']), 1)

    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$M_{\rm sh}$ ($M_\odot$)')
    ax.text(0.04, 0.96,
            f'full: slope={slope_full:.2f}, $\\rho={rho_full:+.2f}$\n'
            f'clean: slope={slope_clean:.2f}, $\\rho={rho_clean:+.2f}$',
            transform=ax.transAxes, va='top', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=7)
    ax.set_title(r'Mass-radius scaling')

    # --- Panel 2: σ-r ---
    ax = axes[1]
    ax.loglog(sh['r_sh_kpc'], sh['sigma_sh_kpc'], 'o', ms=4,
              mfc=COLORS['reference'], mec='black', mew=0.3, alpha=0.7,
              label=f'full (n={len(sh)})')
    ax.loglog(clean['r_sh_kpc'], clean['sigma_sh_kpc'], 'o', ms=5,
              mfc=COLORS['highlight'], mec='black', mew=0.4,
              label=f'clean (n={len(clean)})')

    for data, color, lw in [(sh, COLORS['neutral'], 1.0),
                             (clean, COLORS['secondary'], 1.3)]:
        logr, logs = np.log10(data['r_sh_kpc']), np.log10(data['sigma_sh_kpc'])
        slope, intercept = np.polyfit(logr, logs, 1)
        r_line = np.logspace(np.log10(sh['r_sh_kpc'].min()*0.9),
                             np.log10(sh['r_sh_kpc'].max()*1.1), 100)
        ax.loglog(r_line, 10**(slope * np.log10(r_line) + intercept),
                  '-', color=color, lw=lw, alpha=0.8)

    rho_full,  _ = spearmanr(sh['r_sh_kpc'], sh['sigma_sh_kpc'])
    rho_clean, _ = spearmanr(clean['r_sh_kpc'], clean['sigma_sh_kpc'])
    slope_full,  _ = np.polyfit(np.log10(sh['r_sh_kpc']),    np.log10(sh['sigma_sh_kpc']),    1)
    slope_clean, _ = np.polyfit(np.log10(clean['r_sh_kpc']), np.log10(clean['sigma_sh_kpc']), 1)

    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$\sigma_{\rm sh}$ (kpc)')
    ax.text(0.04, 0.96,
            f'full: slope={slope_full:.2f}, $\\rho={rho_full:+.2f}$\n'
            f'clean: slope={slope_clean:.2f}, $\\rho={rho_clean:+.2f}$',
            transform=ax.transAxes, va='top', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=7)
    ax.set_title(r'Width-radius scaling')

    plt.tight_layout()
    # Recompute clean diagnostic prints (don't reuse loop variables)
    Mr_full,  _  = np.polyfit(np.log10(sh['r_sh_kpc']),    np.log10(sh['M_sh']),         1)[:2], None
    Mr_clean, _  = np.polyfit(np.log10(clean['r_sh_kpc']), np.log10(clean['M_sh']),      1)[:2], None
    sr_full,  _  = np.polyfit(np.log10(sh['r_sh_kpc']),    np.log10(sh['sigma_sh_kpc']),  1)[:2], None
    sr_clean, _  = np.polyfit(np.log10(clean['r_sh_kpc']), np.log10(clean['sigma_sh_kpc']),1)[:2], None
    print(f"  full sample: {len(sh)} shells; clean subsample: {len(clean)} shells")
    print(f"  M-r:  full slope {Mr_full[0]:.2f}, clean slope {Mr_clean[0]:.2f}")
    print(f"  σ-r:  full slope {sr_full[0]:.2f}, clean slope {sr_clean[0]:.2f}")
    return _save_figure(fig, 'fig_3_3_5_antiwarp_clean')


# ============================================================
# Stubs for figures requiring external data
# ============================================================
def fig_3_3_6():
    """
    Burkert vs Einasto backbone-family comparison (§3.3.6).

    Three panels:
      (1) M-r scatter under both backbones, with linear fits
      (2) σ-r scatter under both backbones, with linear fits showing attenuation
      (3) σ/r distribution histograms under both backbones, with medians marked

    Reads einasto_full_sample_results.csv (Paper I §3.7 output) and parses
    fw_einasto_popt strings to extract per-shell parameters under the Einasto
    backbone. Burkert shells come from the canonical antiwarp_per_shell.csv.

    NGC 6674 excluded throughout for consistency with Paper II 101-galaxy
    convention.
    """
    import ast

    EXCLUDE = {'NGC6674'}

    try:
        ein_path = _resolve_data('einasto_full_sample_results.csv')
    except FileNotFoundError:
        print("  ⚠  Fig 3.3.6 requires Paper I `einasto_full_sample_results.csv`")
        print("     Place this file in the package root or data/ directory and rerun.")
        print("     Source: run_einasto_full_sample.py in the sparc-halo-shells (Paper I) repo.")
        return None

    einasto_df = pd.read_csv(ein_path)
    einasto_df = einasto_df[~einasto_df['galaxy'].isin(EXCLUDE)].reset_index(drop=True)

    # --- Parse Einasto shells from fw_einasto_popt (Paper I §3.7 schema:
    #     3 backbone params [log_rho_s, log_r_s, alpha] then 3 per shell
    #     [log_M, r_shell, sigma]) ---
    def _parse_popt(popt_str, n):
        arr = np.array(ast.literal_eval(popt_str))
        return [(arr[3 + 3*i], arr[3 + 3*i + 1], arr[3 + 3*i + 2])
                for i in range(n)]

    ein_shells = []
    for _, row in einasto_df.iterrows():
        n = int(row['fw_einasto_n_shells'])
        if n == 0:
            continue
        for log_M, r_sh, sigma in _parse_popt(row['fw_einasto_popt'], n):
            ein_shells.append({
                'Galaxy': row['galaxy'], 'T': row['T'],
                'r_sh_kpc': r_sh, 'M_sh': 10 ** log_M,
                'sigma_sh_kpc': sigma,
                'sigma_over_r': sigma / r_sh,
            })
    ein = pd.DataFrame(ein_shells)
    if len(ein) == 0:
        print("  ⚠  Fig 3.3.6: no Einasto shells parsed — check CSV schema.")
        return None

    # --- Burkert shells from canonical Paper II per-shell catalog ---
    burk = pd.read_csv(_resolve_data('antiwarp_per_shell.csv'))
    burk = burk[~burk['Galaxy'].isin(EXCLUDE)]

    fig, axes = plt.subplots(1, 3, figsize=(WIDTH_DOUBLE, 2.8))

    # --- Panel 1: M-r scatter ---
    ax = axes[0]
    ax.loglog(burk['r_sh_kpc'], burk['M_sh'], 'o', ms=4,
              mfc=COLORS['reference'], mec='black', mew=0.3, alpha=0.7,
              label=f'Burkert (n={len(burk)})')
    ax.loglog(ein['r_sh_kpc'], ein['M_sh'], 's', ms=4,
              mfc=COLORS['highlight'], mec='black', mew=0.4, alpha=0.8,
              label=f'Einasto (n={len(ein)})')

    for data, color, lw in [(burk, COLORS['neutral'], 1.0),
                            (ein, COLORS['secondary'], 1.3)]:
        logr, logM = np.log10(data['r_sh_kpc']), np.log10(data['M_sh'])
        slope, intercept = np.polyfit(logr, logM, 1)
        r_line = np.logspace(np.log10(burk['r_sh_kpc'].min() * 0.9),
                             np.log10(burk['r_sh_kpc'].max() * 1.1), 100)
        ax.loglog(r_line, 10 ** (slope * np.log10(r_line) + intercept),
                  '-', color=color, lw=lw, alpha=0.8)

    slope_burk_M, _ = np.polyfit(np.log10(burk['r_sh_kpc']),
                                  np.log10(burk['M_sh']), 1)
    slope_ein_M, _ = np.polyfit(np.log10(ein['r_sh_kpc']),
                                 np.log10(ein['M_sh']), 1)
    rho_burk_M, _ = spearmanr(burk['r_sh_kpc'], burk['M_sh'])
    rho_ein_M, _ = spearmanr(ein['r_sh_kpc'], ein['M_sh'])

    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$M_{\rm sh}$ ($M_\odot$)')
    ax.text(0.04, 0.96,
            f'Burk: slope={slope_burk_M:.2f}, $\\rho={rho_burk_M:+.2f}$\n'
            f'Ein:  slope={slope_ein_M:.2f}, $\\rho={rho_ein_M:+.2f}$',
            transform=ax.transAxes, va='top', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=7)
    ax.set_title(r'Mass-radius (preserved)')

    # --- Panel 2: σ-r scatter ---
    ax = axes[1]
    ax.loglog(burk['r_sh_kpc'], burk['sigma_sh_kpc'], 'o', ms=4,
              mfc=COLORS['reference'], mec='black', mew=0.3, alpha=0.7,
              label=f'Burkert (n={len(burk)})')
    ax.loglog(ein['r_sh_kpc'], ein['sigma_sh_kpc'], 's', ms=4,
              mfc=COLORS['highlight'], mec='black', mew=0.4, alpha=0.8,
              label=f'Einasto (n={len(ein)})')

    for data, color, lw in [(burk, COLORS['neutral'], 1.0),
                            (ein, COLORS['secondary'], 1.3)]:
        logr = np.log10(data['r_sh_kpc'])
        logs = np.log10(data['sigma_sh_kpc'])
        slope, intercept = np.polyfit(logr, logs, 1)
        r_line = np.logspace(np.log10(burk['r_sh_kpc'].min() * 0.9),
                             np.log10(burk['r_sh_kpc'].max() * 1.1), 100)
        ax.loglog(r_line, 10 ** (slope * np.log10(r_line) + intercept),
                  '-', color=color, lw=lw, alpha=0.8)

    slope_burk_s, _ = np.polyfit(np.log10(burk['r_sh_kpc']),
                                  np.log10(burk['sigma_sh_kpc']), 1)
    slope_ein_s, _ = np.polyfit(np.log10(ein['r_sh_kpc']),
                                 np.log10(ein['sigma_sh_kpc']), 1)
    rho_burk_s, _ = spearmanr(burk['r_sh_kpc'], burk['sigma_sh_kpc'])
    rho_ein_s, _ = spearmanr(ein['r_sh_kpc'], ein['sigma_sh_kpc'])

    ax.set_xlabel(r'$r_{\rm sh}$ (kpc)')
    ax.set_ylabel(r'$\sigma_{\rm sh}$ (kpc)')
    ax.text(0.04, 0.96,
            f'Burk: slope={slope_burk_s:.2f}, $\\rho={rho_burk_s:+.2f}$\n'
            f'Ein:  slope={slope_ein_s:.2f}, $\\rho={rho_ein_s:+.2f}$',
            transform=ax.transAxes, va='top', fontsize=7,
            bbox=dict(facecolor='white', edgecolor='gray',
                      boxstyle='round,pad=0.25', alpha=0.9))
    ax.legend(loc='lower right', fontsize=7)
    ax.set_title(r'Width-radius (attenuated)')

    # --- Panel 3: σ/r distribution histograms ---
    ax = axes[2]
    bins = np.linspace(0, 0.5, 22)
    ax.hist(burk['sigma_over_r'], bins=bins, alpha=0.55,
            color=COLORS['reference'], edgecolor='black', linewidth=0.5,
            label=f'Burkert (n={len(burk)})')
    ax.hist(ein['sigma_over_r'], bins=bins, alpha=0.55,
            color=COLORS['highlight'], edgecolor='black', linewidth=0.5,
            label=f'Einasto (n={len(ein)})')

    med_burk = burk['sigma_over_r'].median()
    med_ein = ein['sigma_over_r'].median()
    ax.axvline(med_burk, color=COLORS['neutral'], lw=1.3, ls='--',
               label=f'Burkert median {med_burk:.3f}')
    ax.axvline(med_ein, color=COLORS['secondary'], lw=1.3, ls='--',
               label=f'Einasto median {med_ein:.3f}')

    ax.set_xlabel(r'$\sigma / r$')
    ax.set_ylabel('Number of shells')
    ax.legend(loc='upper right', fontsize=7)
    ax.set_title(r'$\sigma/r$ distribution (median shifts)')

    fig.tight_layout()
    return _save_figure(fig, 'fig_3_3_6_einasto_comparison')


def fig_3_3_7():
    """
    Backbone-shift test (§3.3.7).

    Two-panel figure: (left) log10(ρ₀[BIC]/ρ₀[n=0]) overlaid histograms for
    shell-bearing vs non-shell-bearing galaxies; (right) log10(a[BIC]/a[n=0])
    overlaid histograms for the same. Vertical lines mark medians and the
    zero-shift reference.

    NGC 6674 excluded for 101-galaxy convention (per §2.3 retirement).
    """
    EXCLUDE = {'NGC6674'}

    df = pd.read_csv(_resolve_data('backbone_shift.csv'))
    df = df[~df['Galaxy'].isin(EXCLUDE)].copy()
    df['log_ratio_a'] = np.log10(df['ratio_a'])

    sb = df[df['v7_n_shells'] > 0]
    nsb = df[df['v7_n_shells'] == 0]

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE * 0.75, 2.8))

    # --- Panel 1: log_ratio_rho0 ---
    ax = axes[0]
    span = max(abs(df['log_ratio_rho0'].min()),
               abs(df['log_ratio_rho0'].max()))
    bins = np.linspace(-span, span, 22)
    ax.hist(nsb['log_ratio_rho0'], bins=bins, alpha=0.55,
            color=COLORS['reference'], edgecolor='black', linewidth=0.5,
            label=f'non-shell-bearing (n={len(nsb)})')
    ax.hist(sb['log_ratio_rho0'], bins=bins, alpha=0.55,
            color=COLORS['highlight'], edgecolor='black', linewidth=0.5,
            label=f'shell-bearing (n={len(sb)})')

    ax.axvline(0, color='black', lw=0.8, ls=':', alpha=0.6)
    ax.axvline(nsb['log_ratio_rho0'].median(), color=COLORS['neutral'],
               lw=1.3, ls='--',
               label=f'NSB median {nsb["log_ratio_rho0"].median():+.2f}')
    ax.axvline(sb['log_ratio_rho0'].median(), color=COLORS['secondary'],
               lw=1.3, ls='--',
               label=f'SB median {sb["log_ratio_rho0"].median():+.2f}')

    ax.set_xlabel(r'$\log_{10}\,\rho_0[\mathrm{BIC}]/\rho_0[n{=}0]$')
    ax.set_ylabel('Number of galaxies')
    ax.legend(loc='upper left', fontsize=7)
    ax.set_title(r'Backbone density shift')

    # --- Panel 2: log_ratio_a ---
    ax = axes[1]
    span_a = max(abs(df['log_ratio_a'].min()),
                 abs(df['log_ratio_a'].max()))
    bins_a = np.linspace(-span_a, span_a, 22)
    ax.hist(nsb['log_ratio_a'], bins=bins_a, alpha=0.55,
            color=COLORS['reference'], edgecolor='black', linewidth=0.5,
            label=f'non-shell-bearing (n={len(nsb)})')
    ax.hist(sb['log_ratio_a'], bins=bins_a, alpha=0.55,
            color=COLORS['highlight'], edgecolor='black', linewidth=0.5,
            label=f'shell-bearing (n={len(sb)})')

    ax.axvline(0, color='black', lw=0.8, ls=':', alpha=0.6)
    ax.axvline(nsb['log_ratio_a'].median(), color=COLORS['neutral'],
               lw=1.3, ls='--',
               label=f'NSB median {nsb["log_ratio_a"].median():+.2f}')
    ax.axvline(sb['log_ratio_a'].median(), color=COLORS['secondary'],
               lw=1.3, ls='--',
               label=f'SB median {sb["log_ratio_a"].median():+.2f}')

    ax.set_xlabel(r'$\log_{10}\,a[\mathrm{BIC}]/a[n{=}0]$')
    ax.set_ylabel('Number of galaxies')
    ax.legend(loc='upper right', fontsize=7)
    ax.set_title(r'Backbone scale-radius shift')

    # Figure-level headline for the absorbing-pattern rate
    absorbing = ((sb['log_ratio_rho0'] < 0) & (sb['ratio_a'] > 1)).sum()
    fig.suptitle(f'Absorbing pattern (ρ₀ ↓ and a ↑): '
                 f'{absorbing}/{len(sb)} = {100 * absorbing / len(sb):.1f}% '
                 f'of shell-bearing galaxies',
                 fontsize=9, y=1.02)

    fig.tight_layout()
    return _save_figure(fig, 'fig_3_3_7_backbone_shift')


def fig_3_3_8():
    """Figure 3.3.8 — Covariate forest plot for §3.3.8 multivariate test.

    Two-panel forest plot:
      (a) Full-sample logistic regression coefficients for six predictors,
          with 95% CIs. Significant predictors (p < 0.05) highlighted.
      (b) T_z coefficient across the five samples reported in §3.3.8
          (FULL plus four matched-quality subsamples), showing the
          consistency of T-type non-significance after covariate adjustment.

    Data sources:
      ../data/covariate_results.csv         (logistic + RF; full sample)
      ../data/covariate_matched_results.csv (logistic; five subsamples, long format)
    """
    cov_full = pd.read_csv(_resolve_data('covariate_results.csv'))
    cov_match = pd.read_csv(_resolve_data('covariate_matched_results.csv'))

    # Panel (a) data: full-sample logistic, drop intercept
    full_log = cov_full[
        (cov_full['method'] == 'logistic')
        & (cov_full['predictor'] != '(intercept)')
    ].copy()
    full_log['ci_lo'] = full_log['coef'] - 1.96 * full_log['se']
    full_log['ci_hi'] = full_log['coef'] + 1.96 * full_log['se']

    label_map = {
        'T_z':              r'$T_z$ (T-type)',
        'is_bulge_dom':     'is_bulge_dom',
        'log_N_pts_z':      r'$\log N_{\rm RC}$',
        'log_mean_V_err_z': r'$\log \langle V_{\rm err} \rangle$',
        'cos_inc_z':        r'$\cos i$',
        'log_L36_z':        r'$\log L_{3.6}$',
    }
    pred_order = ['T_z', 'is_bulge_dom', 'log_N_pts_z',
                  'log_mean_V_err_z', 'cos_inc_z', 'log_L36_z']
    full_log = full_log.set_index('predictor').reindex(pred_order).reset_index()

    # Panel (b) data: T_z across subsamples
    tz_match = cov_match[cov_match['predictor'] == 'T_z'].copy()
    tz_match['ci_lo'] = tz_match['coef'] - 1.96 * tz_match['se']
    tz_match['ci_hi'] = tz_match['coef'] + 1.96 * tz_match['se']
    sub_order = ['FULL', 'A_top_Npts', 'B_bot_Verr',
                 'C_both_quality_cuts', 'D_within_T_top_Npts']
    sub_labels = {
        'FULL':                'Full (n=101)',
        'A_top_Npts':          r'A: top half $N_{\rm pts}$',
        'B_bot_Verr':          r'B: bot half $V_{\rm err}$',
        'C_both_quality_cuts': r'C: A $\cap$ B',
        'D_within_T_top_Npts': r'D: top $N_{\rm pts}$ within T-bin',
    }
    tz_match = tz_match.set_index('subsample').reindex(sub_order).reset_index()

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_DOUBLE, 3.0))

    def _draw_forest(ax, df, label_lookup, xlabel, title):
        y_pos = np.arange(len(df))[::-1]
        for i, (_, row) in enumerate(df.iterrows()):
            y = y_pos[i]
            sig = row['p_value'] < 0.05
            color = COLORS['secondary'] if sig else COLORS['neutral']
            ax.plot([row['ci_lo'], row['ci_hi']], [y, y],
                    color=color, linewidth=1.5, zorder=2)
            ax.plot(row['coef'], y, marker='o', color=color, markersize=5,
                    markeredgecolor='black', markeredgewidth=0.5, zorder=3)
        ax.axvline(0, color='black', linewidth=0.5, linestyle='--', zorder=1)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(label_lookup)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        ax.grid(True, axis='x', alpha=0.3, linewidth=0.4)

    _draw_forest(
        axes[0], full_log,
        [label_map[p] for p in full_log['predictor']],
        r'Logistic coefficient $\beta$ (95% CI)',
        r'(a) Full-sample logistic, $n=101$',
    )
    _draw_forest(
        axes[1], tz_match,
        [sub_labels[s] for s in tz_match['subsample']],
        r'$T_z$ coefficient $\beta$ (95% CI)',
        r'(b) $T_z$ across matched-quality subsamples',
    )

    # Common symmetric x-range across the two panels
    xlim_max = max(abs(axes[0].get_xlim()[0]), abs(axes[0].get_xlim()[1]),
                   abs(axes[1].get_xlim()[0]), abs(axes[1].get_xlim()[1]),
                   2.5)
    for ax in axes:
        ax.set_xlim(-xlim_max, xlim_max)

    plt.tight_layout()
    return _save_figure(fig, 'fig_3_3_8_covariate_forest')


# ============================================================
# Figure registry
# ============================================================
FIGURES = {
    '3.1.1': ('Bulge correlation',                      fig_3_1_1),
    '3.1.2': ('Scaling relations (M-r, σ-r, σ/r)',      fig_3_1_2),
    '3.1.3': ('σ/r quartile gradient',                  fig_3_1_3),
    '3.1.4': ('Inner-vs-outer (two-shell paired)',      fig_3_1_4),
    '3.2.1': ('Scramble null distribution',             fig_3_2_1),
    '3.2.2': ('Permute null distribution',              fig_3_2_2),
    '3.3.1': ('Disk dynamical scale coincidence',       fig_3_3_1),
    '3.3.2': ('Υ perturbation stability',               fig_3_3_2),
    '3.3.3': ('Distance perturbation stability',        fig_3_3_3),
    '3.3.4': ('Inclination perturbation stability',     fig_3_3_4),
    '3.3.5': ('Anti-warp clean subsample',              fig_3_3_5),
    '3.3.6': ('Einasto backbone comparison',            fig_3_3_6),
    '3.3.7': ('Backbone-shift test',                    fig_3_3_7),
    '3.3.8': ('Covariate forest (logistic + matched)',  fig_3_3_8),
}


def main():
    parser = argparse.ArgumentParser(description='Generate Paper II figures.')
    parser.add_argument('--all', action='store_true',
                        help='Generate all figures')
    parser.add_argument('--figure', type=str,
                        help='Comma-separated figure IDs (e.g. 3.1.1,3.1.2)')
    parser.add_argument('--list', action='store_true',
                        help='List available figures')
    args = parser.parse_args()

    if args.list:
        print("Available figures:")
        for fid, (desc, _) in FIGURES.items():
            print(f"  {fid}  — {desc}")
        return

    _configure_style()

    targets = []
    if args.all:
        targets = list(FIGURES.keys())
    elif args.figure:
        targets = [t.strip() for t in args.figure.split(',')]
    else:
        parser.print_help()
        return

    outdir = _output_dir()
    print(f"Output directory: {outdir}")
    print(f"Figures requested: {targets}")
    print()

    for fid in targets:
        if fid not in FIGURES:
            print(f"⚠  Unknown figure: {fid} (use --list)")
            continue
        desc, func = FIGURES[fid]
        print(f"[{fid}] {desc}")
        try:
            result = func()
            if result:
                print(f"  ✓ saved: {os.path.basename(result)}")
        except Exception as e:
            print(f"  ✗ FAILED: {e.__class__.__name__}: {e}")
            import traceback; traceback.print_exc()
        print()


if __name__ == '__main__':
    main()

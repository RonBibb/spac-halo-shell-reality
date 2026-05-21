# halo_shells_paper2

**Statistical Organization of Localized Residual Structure in SPARC Rotation Curves**

Author: Ron Bibb (<ronbibb@gmail.com>)
ORCID: 0009-0004-1153-2464
Version: v1.0-draft (2026-05-21 snapshot)
Target journal: PASP (companion to Paper I)

---

## What is this?

This package contains the manuscript, data, producer scripts, and documentation for Paper II in the SPARC halo-shells program. Paper II is a companion to Paper I (Bibb 2026, PASP manuscript #PASP-102415, awaiting referee reports as of 2026-05-21; repository at https://github.com/RonBibb/sparc-halo-shells, release tag v7.1.0).

**Scope of Paper II.** Paper I established that a Burkert backbone augmented by zero, one, or two BIC-selected Gaussian shells improves rotation curve fits in 91/102 SPARC galaxies and that shell-bearing rate decreases monotonically with morphological lateness (ρ_per_T = -0.833, p = 0.010 on the Paper I-aligned 102-galaxy sample). Paper II asks whether the resulting shell population constitutes a coherent statistical phenomenon — internally organized, robust to artifact channels, and distinguishable from random fitting behavior — or whether it is a constellation of unrelated detections sharing a fitting framework.

Paper II's primary analyses use a **101-galaxy sample (NGC 6674 excluded)** due to a degenerate two-shell fit at r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound; the §2.3 partition disclosure quantifies why qualitative conclusions are unchanged relative to the Paper I 102-galaxy version.

**Findings.**

1. The 67 fitted shells exhibit organized signatures grouped by robustness under multiple-comparisons correction (§3.1.5):

   - **Primary signatures** (Bonferroni-robust; preserved or strengthened under Einasto backbone): mass-radius scaling (M ∝ r^0.76, ρ = +0.64, p < 10⁻⁴), width-radius scaling under Burkert backbone (σ ∝ r^1.04, ρ = +0.78), inner-vs-outer mass ordering in two-shell galaxies (14/16, p = 0.0001).
   - **Secondary signatures** (BH-FDR pass, Bonferroni fail): bulge correlation (OR = 3.67, p ≈ 0.01; near-equivalent to morphology gradient), morphology gradient (ρ_per_T = -0.762, p = 0.028), inner-vs-outer width ordering, two-population separation in r/r_vir.

2. **Width-related signatures are partially backbone-baseline-dependent.** Under an Einasto backbone (one extra free parameter, strictly more flexible than Burkert), the σ-r slope drops from 1.04 to 0.38 and the σ/r median from 0.275 to 0.173; mass-feature signatures and galaxy-level signatures are preserved or strengthened (§3.3.6).

3. **The smooth profile cannot natively absorb the localized structure.** When the Paper I framework is constrained to n_shells = 0, the Burkert backbone systematically deforms (ρ₀ rises by a factor of ≈4.2; scale radius a contracts by a factor of ≈2.1) in 45 of 51 (88.2%) shell-bearing galaxies (101-galaxy convention, via post-aggregation of the 102-galaxy production run). The non-shell-bearing control population does not show this systematic deformation. This disfavors the strong form of the basis-function alternative, in which shells would be decoupled from backbone parameters (§3.3.7).

4. **Two destructive nulls** (within-galaxy residual scrambling, cross-radius velocity permutation; 100 realizations each) fail to reproduce the morphology gradient with asymmetric failure modes: residual scrambling suppresses the gradient (empirical p = 2/100), while cross-radius permutation over-produces detections and reverses the gradient sign (0/100). The asymmetric failure direction is the strongest single piece of evidence against a generic-basis-function origin (§3.2).

5. **Shell selections are stable** under realistic perturbations to mass-to-light ratio (95.1% per-galaxy mode-recovery), distance (94.1%), and inclination (98.9%).

6. **A conservative anti-warp clean subsample** preserves all five headline patterns in direction.

The shell population is not consistent with random fitting behavior, baryonic input mismodeling, disk dynamical coincidence, warp-related velocity-field artifacts, or single-backbone-family flexibility as primary drivers within the channels and amplitudes tested. Whether the structures correspond to genuine localized halo mass features or to other forms of organized galactic dynamics remains an open physical question.

---

## Cap acknowledgment

Paper II treats both the σ/r ≤ 0.4 cap and the mass cap at 5×10¹⁰ M☉ as **definitional constraints** that preserve the "localized" regime distinct from smooth-halo descriptions. §3.1.2 discloses that 8 of 67 shells (11.9%) lie within 0.05 dex of the mass bound, and that the cap-clear subset (n = 59) shows essentially unchanged scaling slopes — the cap is binding for a subset of fits but does not drive the population-level scaling relations. Cap-relaxation effects are deferred to Paper 3, which refines the model by relaxing both caps and re-fitting under hierarchical Υ marginalization in the same pass.

---

## Relationship to Paper I

This package is **not standalone** with respect to Paper I's canonical fits. Paper II uses:

- Paper I's canonical fit catalog (`sparc_T2-T9_canonical_fits.csv`) as the primary input to all per-shell analyses. **Not duplicated here**; lives in the Paper I repository at https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0.
- Paper I's Einasto-backbone fit catalog (`einasto_full_sample_results.csv`) as the input to §3.3.6. **Copied into this repo's `data/` directory** for reproducibility convenience (added 2026-05-19).

Reproducing Paper II's analyses requires:

1. Cloning the Paper I package at tag `v7.1.0`
2. Placing `data/sparc_T2-T9_canonical_fits.csv` from Paper I into this package's `data/` directory
3. Then running the Paper II scripts

The Paper I PDF (`source/paper1_v7.1.0.pdf`) is included for reference.

---

## What this package contains

```
sparc-halo-shell-reality/
├── README.md                          (this file)
├── STATUS.md                          single-source-of-truth for package state (read first)
├── VALIDATION_STATUS.md               version alignment, validation tracking
├── DATA_PROVENANCE.md                 CSV-to-script-to-section traceability
├── ALIGNMENT_AUDIT.md                 audit of Paper I ↔ Paper II numerical alignment
├── PROJECT_README.md                  repo file manifest
├── LICENSE                            MIT License
├── requirements.txt                   Python dependencies
├── shell_reality_nulls_parallel.py    (root-level convenience copy of parallel runner)
│
├── source/
│   ├── paper2.md                      Markdown manuscript source (canonical, ~13,300 words)
│   ├── paper2_consolidated.pdf        Consolidated reading PDF
│   └── paper1_v7.1.0.pdf              Paper I reference PDF
│
├── data/
│   ├── Rotmod_LTG/                    SPARC rotmod files (175 galaxies; 102 in T=2-9 sample)
│   ├── sparc_sample123.csv            SPARC catalog metadata
│   ├── galaxy_classifications.csv     Augmented catalog with bulge/dwarf/MW-like flags
│   ├── nfw_fixedc_fits.csv            NFW fixed-concentration reference fits
│   │
│   ├── antiwarp_per_shell.csv         §3.3.5 per-shell catalog (67 shells; NGC 6674-excluded)
│   ├── antiwarp_summary.txt           §3.3.5 statistical comparison
│   │
│   ├── backbone_shift.csv             §3.3.7 backbone parameters at n=0/1/2 per galaxy
│   ├── backbone_shift_summary.txt     §3.3.7 population-level summary
│   │
│   ├── upsilon_perturbation_per_galaxy.csv    §3.3.2 M*/L perturbation results
│   ├── distance_perturbation_per_galaxy.csv   §3.3.3 distance perturbation
│   ├── inclination_perturbation_per_galaxy.csv §3.3.4 inclination perturbation
│   │
│   ├── nulltest_per_realization.csv   §3.2 N=20 baseline (superseded; see shell_reality_out_n100)
│   ├── nulltest_per_galaxy.csv        §3.2 N=20 baseline
│   ├── nulltest_summary.txt           §3.2 N=20 baseline
│   ├── per_realization.csv            duplicate of nulltest_per_realization.csv (legacy)
│   ├── per_galaxy.csv                 duplicate of nulltest_per_galaxy.csv (legacy)
│   ├── summary.txt                    duplicate of nulltest_summary.txt (legacy)
│   │
│   ├── einasto_full_sample_results.csv     Paper I Einasto fits (for §3.3.6 reproducibility)
│   ├── einasto_robustness_results.csv      Paper I Einasto robustness fits
│   │
│   ├── ngc6674_exclusion_summary.txt  §2.3 retirement: 102-gal vs 101-gal comparison
│   │
│   └── shell_reality_out_n100/        §3.2 N=100 outputs (canonical for §3.2 numerics)
│       ├── per_realization.csv        200 rows (100 scramble + 100 permute)
│       ├── per_galaxy.csv             20,400 rows
│       └── summary.txt                empirical p = 2/100 scramble, 0/100 permute
│
├── scripts/
│   ├── antiwarp_subsample.py            §3.3.5 analysis
│   ├── backbone_shift_test.py           §3.3.7 backbone-shift production runner
│   ├── shell_reality_nulls.py           §3.2 null test runner (serial)
│   ├── shell_reality_nulls_parallel.py  §3.2 null test runner (parallel; byte-identical to serial)
│   ├── upsilon_perturbation.py          §3.3.2 perturbation runner
│   ├── distance_perturbation.py         §3.3.3 perturbation runner
│   ├── inclination_perturbation.py      §3.3.4 perturbation runner
│   ├── run_canonical_fits.py            Paper I production fitter (copied from Paper I)
│   ├── einasto_control.py               §3.3.6 post-hoc analysis on Paper I Einasto fits
│   ├── make_figures.py                  generates all 13 manuscript figures from data/
│   └── ngc6674_exclusion_reanalysis.py  §2.3 retirement: re-aggregates §3.3.2-4 + §3.3.7
│
├── logs/
│   ├── antiwarp_log.txt
│   ├── upsilon_perturbation_log.txt
│   ├── distance_perturbation_log.txt
│   └── inclination_perturbation_log.txt
│
└── figures/                            (13 PDFs, all generated)
    ├── fig_3_1_1_bulge_correlation.pdf
    ├── fig_3_1_2_scaling_relations.pdf
    ├── fig_3_1_3_sigma_over_r_quartile.pdf
    ├── fig_3_1_4_inner_vs_outer.pdf
    ├── fig_3_2_1_scramble_null.pdf
    ├── fig_3_2_2_permute_null.pdf
    ├── fig_3_3_1_disk_dynamical_scales.pdf
    ├── fig_3_3_2_upsilon_perturbation.pdf
    ├── fig_3_3_3_distance_perturbation.pdf
    ├── fig_3_3_4_inclination_perturbation.pdf
    ├── fig_3_3_5_antiwarp_clean.pdf
    ├── fig_3_3_6_einasto_comparison.pdf
    └── fig_3_3_7_backbone_shift.pdf
```

---

## Reproducing the Paper II results

### Prerequisites

- Python 3.10+ with numpy, scipy, pandas, matplotlib (see `requirements.txt`)
- Paper I package at tag v7.1.0 (for the canonical fits CSV)
- Approximately 60–90 minutes of CPU time on a modern Apple Silicon Mac for the full perturbation + null + backbone-shift suite

### Setup

1. Clone Paper I at v7.1.0:
   ```
   git clone https://github.com/RonBibb/sparc-halo-shells.git
   cd sparc-halo-shells
   git checkout v7.1.0
   ```

2. Copy Paper I's canonical catalog into Paper II's data directory:
   ```
   cp sparc-halo-shells/data/sparc_T2-T9_canonical_fits.csv sparc-halo-shell-reality/data/
   ```
   (`einasto_full_sample_results.csv` is already included in this repo for §3.3.6 reproducibility.)

3. Install dependencies:
   ```
   cd sparc-halo-shell-reality
   pip install -r requirements.txt
   ```

### Running the analyses

From `sparc-halo-shell-reality/scripts/`:

```bash
# Pure-analysis scripts (seconds; no fitting)
python3 antiwarp_subsample.py      # data/antiwarp_per_shell.csv, antiwarp_summary.txt
python3 einasto_control.py         # post-hoc analysis on Paper I Einasto fits

# Production runs (with fitting; longer)
python3 shell_reality_nulls.py 100              # serial, ~17 hr; 100 realizations × 2 null types
python3 shell_reality_nulls_parallel.py 100 12  # parallel, ~2 hr; byte-identical to serial
python3 backbone_shift_test.py                  # ~5-15 min; 102 galaxies × 3 n_shells levels
python3 upsilon_perturbation.py                 # ~10-15 min; 102 × 20 realizations
python3 distance_perturbation.py                # ~10-15 min
python3 inclination_perturbation.py             # ~10-15 min

# Figure generation (seconds; no fitting)
python3 make_figures.py --all                   # all 13 figures to ../figures/
python3 make_figures.py --figure 3.1.1,3.2.1    # selective regeneration
python3 make_figures.py --list                  # show all figures
```

### Verifying outputs

Each script prints a summary of the headline statistics on completion. Cross-check against:
- `data/antiwarp_summary.txt` (anti-warp results)
- `data/backbone_shift_summary.txt` (backbone-shift results)
- `data/shell_reality_out_n100/summary.txt` (N=100 null test z-scores)
- The per-galaxy CSVs for perturbation results

---

## Status

This package is **release v1.0-draft**, suitable for internal review and figure generation. PASP submission pending completion of items in `STATUS.md`.

| Component | Status |
| --- | --- |
| Manuscript text | ✅ Drafted; ~13,300 words |
| Markdown source | ✅ Canonical; ongoing edits |
| Acknowledgments | ✅ Drafted (with AI disclosure) |
| Data CSVs (Paper II outputs) | ✅ DONE (15 CSVs in `data/` plus `shell_reality_out_n100/`) |
| SPARC inputs | ✅ DONE (Rotmod_LTG/, classifications, sparc_sample123) |
| Producer scripts | ✅ DONE (11 scripts in `scripts/`) |
| Logs | ✅ Captured for all perturbation/antiwarp runs |
| Figures | ✅ All 13 PDFs in `figures/` |
| §3.1.2 mass-cap acknowledgment | ✅ DONE (commit `a86a0e5`, 2026-05-21) |
| Bibliography | ⏳ Citation hooks; full DOIs pending |
| Tier 2 discrepancy resolution | ⏳ 2 of 4 resolved (Wilcoxon, σ count); 2 remain (KS D, Bulge OR) |
| Cover letter | ⏳ Not started |
| LaTeX conversion | ⏳ Pending (md → AASTeX 7.0.1) |
| Paper I canonical CSV | ❌ EXTERNAL — see "Relationship to Paper I" |
| Paper I citation update | ⏳ Blocked on Paper I PASP decision |
| Zenodo deposit | ⏳ Pending |
| PASP submission | ⏳ Pending |

---

## Citation

> Bibb, R. (2026). *Statistical Organization of Localized Residual Structure in SPARC Rotation Curves.* halo_shells_paper2 v1.0. Code and data: doi:[Zenodo DOI pending]

## Contact

Ron Bibb — <ronbibb@gmail.com> — ORCID 0009-0004-1153-2464

## License

Manuscript: under journal preparation (license per PASP policy upon acceptance).
Data and code: MIT License (see `LICENSE`).

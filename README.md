# halo_shells_paper2 v1.0

**Statistical Organization of Localized Residual Structure in SPARC Rotation Curves**

Author: Ron Bibb (<ronbibb@gmail.com>)
ORCID: 0009-0004-1153-2464
Version: v1.0-draft (2026-05-19 snapshot)
Target journal: PASP (companion to Paper I)

---

## What is this?

This package contains the manuscript, data, producer scripts, and documentation for Paper II in the SPARC halo-shells program. Paper II is a companion to Paper I (Bibb 2026, PASP manuscript #PASP-102415, awaiting referee reports as of 2026-05-19; repository at https://github.com/RonBibb/sparc-halo-shells, release tag v7.1.0).

**Scope of Paper II.** Paper I established that a Burkert backbone augmented by zero, one, or two BIC-selected Gaussian shells improves rotation curve fits in 91/102 SPARC galaxies and that shell-bearing rate decreases monotonically with morphological lateness (ρ_per_T = -0.833, p = 0.010 on the Paper I-aligned 102-galaxy sample). Paper II asks whether the resulting shell population constitutes a coherent statistical phenomenon — internally organized, robust to artifact channels, and distinguishable from random fitting behavior — or whether it is a constellation of unrelated detections sharing a fitting framework.

Paper II's primary analyses use a **101-galaxy sample (NGC 6674 excluded)** due to a degenerate two-shell fit at r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound; the §2.3 partition disclosure quantifies why qualitative conclusions are unchanged relative to the Paper I 102-galaxy version.

**Findings.**

1. The 67 fitted shells exhibit organized signatures grouped by robustness under multiple-comparisons correction (§3.1.5):

   - **Primary signatures** (Bonferroni-robust; preserved or strengthened under Einasto backbone): mass-radius scaling (M ∝ r^0.76, ρ = +0.64, p < 10⁻⁴), width-radius scaling under Burkert backbone (σ ∝ r^1.04, ρ = +0.78), inner-vs-outer mass ordering in two-shell galaxies (14/16, p = 0.0001).
   - **Secondary signatures** (BH-FDR pass, Bonferroni fail): bulge correlation (OR = 3.67, p ≈ 0.01; near-equivalent to morphology gradient), morphology gradient (ρ_per_T = -0.762, p = 0.028), inner-vs-outer width ordering, two-population separation in r/r_vir.

2. **Width-related signatures are partially backbone-baseline-dependent.** Under an Einasto backbone (one extra free parameter, strictly more flexible than Burkert), the σ-r slope drops from 1.04 to 0.38 and the σ/r median from 0.275 to 0.173; mass-feature signatures and galaxy-level signatures are preserved or strengthened (§3.3.6).

3. **The smooth profile cannot natively absorb the localized structure.** When the Paper I framework is constrained to n_shells = 0, the Burkert backbone systematically deforms (ρ₀ rises by a factor of ≈4.2; scale radius a contracts by a factor of ≈2.1) in 45 of 51 (88.2%) shell-bearing galaxies (101-galaxy convention, via post-aggregation of the 102-galaxy production run). The non-shell-bearing control population does not show this systematic deformation. This disfavors the strong form of the basis-function alternative, in which shells would be decoupled from backbone parameters (§3.3.7).

4. **Two destructive nulls** (within-galaxy residual scrambling, cross-radius velocity permutation; 100 realizations each) fail to reproduce the morphology gradient with asymmetric failure modes: residual scrambling suppresses the gradient (the real-data ρ is reached or exceeded in 2/100 realizations, empirical *p* = 0.02), while cross-radius permutation over-produces detections and reverses the gradient sign (0/100 realizations reach the real-data value). The asymmetric failure direction is the strongest single piece of evidence against a generic-basis-function origin (§3.2).

5. **Shell selections are stable** under realistic perturbations to mass-to-light ratio (95.1% per-galaxy mode-recovery), distance (94.1%), and inclination (98.9%).

6. **A conservative anti-warp clean subsample** preserves all five headline patterns in direction.

The shell population is not consistent with random fitting behavior, baryonic input mismodeling, disk dynamical coincidence, warp-related velocity-field artifacts, or single-backbone-family flexibility as primary drivers within the channels and amplitudes tested. Whether the structures correspond to genuine localized halo mass features or to other forms of organized galactic dynamics remains an open physical question.

## Relationship to Paper I

This package is **not standalone** with respect to Paper I's canonical fits or Einasto comparison fits. Paper II uses:

- Paper I's Paper I (v7.1.0) canonical fit catalog (`sparc_T2-T9_canonical_fits.csv`) as the primary input to all per-shell analyses.
- Paper I's Einasto-backbone fit catalog (`einasto_full_sample_results.csv`) as the input to §3.3.6.

Both catalogs live in the Paper I repository (`https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0`, in `data/`) and are not duplicated here to avoid drift between the two papers. Reproducing Paper II's analyses requires:

1. Cloning the Paper I package at tag `v7.1.0`
2. Placing `data/sparc_T2-T9_canonical_fits.csv` and `data/einasto_full_sample_results.csv` from Paper I into this package's `data/` directory (or symlinking)
3. Then running the Paper II scripts

The Paper I PDF (`source/paper1_v7.1.0.pdf`) is included for reference.

## What this package contains

```
halo_shells_paper2_v1.0/
├── README.md                          (this file)
├── STATUS.md                          single-source-of-truth for package state (read first)
├── VALIDATION_STATUS.md               version alignment, validation tracking
├── DATA_PROVENANCE.md                 CSV-to-script-to-section traceability
├── ALIGNMENT_AUDIT.md                 audit of Paper I ↔ Paper II numerical alignment
├── PROJECT_README.md                  project file manifest (preserved)
├── LICENSE                            MIT License
├── requirements.txt                   Python dependencies
│
├── source/
│   ├── paper2.md                      Markdown manuscript source (canonical)
│   ├── paper2_consolidated.pdf        Consolidated reading PDF (manuscript + appendices)
│   └── paper1_v7.1.0.pdf              Paper I reference PDF
│
├── data/
│   ├── Rotmod_LTG/                    SPARC rotmod files (175 galaxies; 102 in T=2-9 sample)
│   ├── sparc_sample123.csv            SPARC catalog metadata
│   ├── galaxy_classifications.csv     Augmented catalog with bulge/dwarf/MW-like flags
│   ├── nfw_fixedc_fits.csv            NFW fixed-concentration reference fits (Paper II §1 context)
│   │
│   ├── antiwarp_per_shell.csv         §3.3.5 per-shell catalog (67 shells; NGC 6674-excluded)
│   ├── antiwarp_summary.txt           §3.3.5 statistical comparison (NGC 6674-excluded)
│   │
│   ├── backbone_shift.csv             §3.3.7 backbone parameters at n=0/1/2 per galaxy
│   ├── backbone_shift_summary.txt     §3.3.7 population-level summary
│   │
│   ├── upsilon_perturbation_per_galaxy.csv    §3.3.2 M*/L perturbation results
│   ├── distance_perturbation_per_galaxy.csv   §3.3.3 distance perturbation
│   ├── inclination_perturbation_per_galaxy.csv §3.3.4 inclination perturbation
│   │
│   ├── nulltest_per_realization.csv   §3.2 N=20 baseline per-realization (40 rows)
│   ├── nulltest_per_galaxy.csv        §3.2 N=20 baseline per-galaxy fits (4080 rows)
│   ├── nulltest_summary.txt           §3.2 N=20 baseline summary
│   ├── per_realization.csv            duplicate of nulltest_per_realization.csv (legacy naming)
│   ├── per_galaxy.csv                 duplicate of nulltest_per_galaxy.csv (legacy naming)
│   ├── summary.txt                    duplicate of nulltest_summary.txt (legacy naming)
│   │
│   └── shell_reality_out_n100/        §3.2 N=100 outputs (canonical for §3.2 numerics)
│       ├── per_realization.csv        200 rows (100 scramble + 100 permute)
│       ├── per_galaxy.csv             20,400 rows
│       └── summary.txt                empirical p = 2/100 scramble, 0/100 permute
│
│   ngc6674_exclusion_summary.txt      §2.3 retirement: 102-galaxy vs 101-galaxy headline comparison for §3.3.2-4 and §3.3.7 (max shift 0.25 pp)
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
│   ├── make_figures.py                  generates all 11 manuscript figures from data/
│   └── ngc6674_exclusion_reanalysis.py  §2.3 retirement: re-aggregates §3.3.2-4 + §3.3.7 with NGC 6674 excluded
│
├── logs/
│   ├── antiwarp_log.txt
│   ├── upsilon_perturbation_log.txt
│   ├── distance_perturbation_log.txt
│   └── inclination_perturbation_log.txt
│
└── figures/                            (11 PDFs: 9 generated, 2 stubs pending Paper I data)
    ├── fig_3_1_*.pdf                   4 figures: §3.1 organized structure
    ├── fig_3_2_*.pdf                   2 figures: §3.2 null distributions (N=100)
    ├── fig_3_3_1..5_*.pdf              5 figures: §3.3 robustness tests
    └── (fig_3_3_6, fig_3_3_7 require Paper I einasto + backbone-shift data; stubs in make_figures.py)
```

## Reproducing the Paper II results

### Prerequisites

- Python 3.10+ with numpy, scipy, pandas, matplotlib (see `requirements.txt`)
- Paper I package at tag v7.1.0 (for the canonical fits CSV and the Einasto fits CSV)
- Approximately 60-90 minutes of CPU time on a modern Apple Silicon Mac for the full perturbation + null + backbone-shift suite

### Setup

1. Clone Paper I at v7.1.0:
   ```
   git clone https://github.com/RonBibb/sparc-halo-shells.git
   cd sparc-halo-shells
   git checkout v7.1.0
   ```

2. Copy Paper I's catalogs into Paper II's data directory:
   ```
   cp sparc-halo-shells/data/sparc_T2-T9_canonical_fits.csv halo_shells_paper2_v1.0/data/
   cp sparc-halo-shells/data/einasto_full_sample_results.csv halo_shells_paper2_v1.0/data/
   ```

3. Install dependencies:
   ```
   cd halo_shells_paper2_v1.0
   pip install -r requirements.txt
   ```

### Running the analyses

From `halo_shells_paper2_v1.0/scripts/`:

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
python3 make_figures.py --all                   # all 11 figures to ../figures/
python3 make_figures.py --figure 3.1.1,3.2.1    # selective regeneration
python3 make_figures.py --list                  # show all figures
```

Outputs are written to `data/` with the canonical filenames listed above.

### Verifying outputs

Each script prints a summary of the headline statistics on completion. Cross-check against:
- `data/antiwarp_summary.txt` (anti-warp results)
- `data/backbone_shift_summary.txt` (backbone-shift results)
- `data/nulltest_summary.txt` (null test z-scores)
- The per-galaxy CSVs for perturbation results

## Status

This package is **release v1.0-draft**, suitable for internal review and figure generation. PASP submission pending completion of items in `STATUS.md`.

| Component | Status |
| --- | --- |
| Manuscript text | ✅ Drafted; ~12,900 words |
| Markdown source | ✅ Canonical; ongoing edits |
| Data CSVs (Paper II outputs) | ✅ DONE (10 CSVs in `data/` plus `shell_reality_out_n100/`) |
| SPARC inputs | ✅ DONE (Rotmod_LTG/, classifications, sparc_sample123) |
| Producer scripts | ✅ DONE (11 scripts in `scripts/`) |
| Logs | ✅ Captured for all perturbation/antiwarp runs |
| Figures | ✅ 9 of 11 PDFs in `figures/` (fig_3_3_6 Einasto and fig_3_3_7 backbone-shift await Paper I data) |
| Bibliography | ⏳ Skeleton entries; full DOIs at submission |
| Paper I canonical CSV | ❌ EXTERNAL — see "Relationship to Paper I" |
| Paper I Einasto CSV | ❌ EXTERNAL — see "Relationship to Paper I" |
| NGC 6674 reruns of §3.3.2-4/§3.3.7 | ✅ DONE 2026-05-19 via aggregation (§2.3 exception list mostly retired; data/ngc6674_exclusion_summary.txt) |
| Tier 2 discrepancy resolution | ⏳ Pending (documented in VALIDATION_STATUS.md) |
| Zenodo deposit | ⏳ Pending |
| PASP submission | ⏳ Pending |

## Citation

> Bibb, R. (2026). *Statistical Organization of Localized Residual Structure in SPARC Rotation Curves.* halo_shells_paper2 v1.0. Code and data: doi:[Zenodo DOI pending]

## Contact

Ron Bibb — <ronbibb@gmail.com> — ORCID 0009-0004-1153-2464

## License

Manuscript: under journal preparation (license per PASP policy upon acceptance).
Data and code: MIT License (see `LICENSE`).

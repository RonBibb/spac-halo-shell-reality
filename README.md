# halo_shells_paper2 v1.0

**Statistical Organization of Localized Residual Structure in SPARC Rotation Curves**

Author: Ron Bibb (<ronbibb@gmail.com>)
ORCID: 0009-0004-1153-2464
Version: v1.0
Release date: 2026-05-10

---

## What is this?

This package contains the manuscript, data, producer scripts, and documentation for Paper II in the SPARC halo-shells program. Paper II is a companion to Paper I (Bibb 2026, AJ submission, repository at https://github.com/RonBibb/sparc-halo-shells, release tag v7.1.0).

**Scope of Paper II.** Paper I established that a Burkert backbone augmented by zero, one, or two BIC-selected Gaussian shells improves rotation curve fits in 91/102 SPARC galaxies and that shell-bearing rate decreases monotonically with morphological lateness (ρ_per_T = -0.833, p = 0.010). Paper II asks whether the resulting shell population constitutes a coherent statistical phenomenon — internally organized, robust to artifact channels, and distinguishable from random fitting behavior — or whether it is a constellation of unrelated detections sharing a fitting framework.

**Findings.**

1. The 69 fitted shells exhibit four largely independent organizational dimensions: bulge correlation (OR = 3.88, p = 0.003), radial scaling (σ ∝ r^1.04, ρ = +0.78), σ/r near-universality (median 0.27 with population gradient 0.35 → 0.19 across radius quartiles), and inner-vs-outer mass ordering in two-shell galaxies (14/17, p = 0.017).
2. Two destructive nulls (within-galaxy residual scrambling, cross-radius velocity permutation) fail to reproduce the morphology gradient with asymmetric failure modes, at z = -3.0 to -8.3 depending on statistic.
3. Shell selections are stable under realistic perturbations to mass-to-light ratio (95.1% per-galaxy mode-recovery), distance (94.1%), and inclination (98.9%).
4. A conservative anti-warp clean subsample preserves all five headline patterns in direction.

The shell population is not consistent with random fitting behavior, baryonic input mismodeling, disk dynamical coincidence, or warp-related velocity-field artifacts as primary drivers within the channels and amplitudes tested. Whether the structures correspond to genuine localized halo mass features or to other forms of organized galactic dynamics remains an open physical question.

## Relationship to Paper I

This package is **not standalone** with respect to Paper I's canonical fits. Paper II uses Paper I's v7.0/v7.1.0 canonical fit catalog (`sparc_T2-T9_canonical_fits.csv`) as the primary input to all per-shell analyses. That catalog lives in the Paper I repository (`https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0`, in `data/`) and is not duplicated here to avoid drift between the two papers. Reproducing Paper II's analyses requires:

1. Cloning the Paper I package at tag `v7.1.0`
2. Placing `data/sparc_T2-T9_canonical_fits.csv` from Paper I into this package's `data/` directory (or symlinking)
3. Then running the Paper II scripts

The Paper I PDF (`source/paper1_v7.1.0.pdf`) is included for reference.

## What this package contains

```
halo_shells_paper2_v1.0/
├── README.md                          (this file)
├── VALIDATION_STATUS.md               version alignment, validation tracking
├── DATA_PROVENANCE.md                 CSV-to-script-to-section traceability
├── ALIGNMENT_AUDIT.md                 audit of Paper I ↔ Paper II numerical alignment
├── PROJECT_README.md                  project file manifest (was the working manifest)
├── LICENSE                            MIT License
├── requirements.txt                   Python dependencies
│
├── source/
│   ├── paper2.md                      Markdown manuscript source (canonical)
│   ├── paper2_consolidated.pdf        Consolidated reading PDF (manuscript + appendices)
│   └── paper1_v7.1.0.pdf              Paper I reference PDF
│
├── data/
│   ├── Rotmod_LTG/                    SPARC rotmod files (175 galaxies; 102 used in T=2-9 sample)
│   ├── sparc_sample123.csv            SPARC catalog metadata
│   ├── galaxy_classifications.csv     Augmented catalog with bulge/dwarf/MW-like flags
│   ├── nfw_fixedc_fits.csv            NFW fixed-concentration reference fits (Paper II §1 context)
│   │
│   ├── antiwarp_per_shell.csv         §3.3.5 per-shell catalog (67 shells; NGC6674 excluded)
│   ├── antiwarp_summary.txt           §3.3.5 statistical comparison
│   │
│   ├── upsilon_perturbation_per_galaxy.csv    §3.3.2 M*/L perturbation results
│   ├── distance_perturbation_per_galaxy.csv   §3.3.3 distance perturbation
│   ├── inclination_perturbation_per_galaxy.csv §3.3.4 inclination perturbation
│   │
│   ├── nulltest_per_realization.csv   §3.2 per-realization summary (40 rows)
│   ├── nulltest_per_galaxy.csv        §3.2 per-galaxy fits (4080 rows)
│   └── nulltest_summary.txt           §3.2 formatted summary
│
├── scripts/
│   ├── antiwarp_subsample.py          §3.3.5 reconstructed analysis script
│   ├── upsilon_perturbation.py        §3.3.2 perturbation runner
│   ├── distance_perturbation.py       §3.3.3 perturbation runner
│   ├── inclination_perturbation.py    §3.3.4 perturbation runner
│   └── shell_reality_nulls.py         §3.2 null test runner
│
├── logs/
│   ├── antiwarp_log.txt
│   ├── upsilon_perturbation_log.txt
│   ├── distance_perturbation_log.txt
│   └── inclination_perturbation_log.txt
│
└── figures/                            (placeholder; figure scripts pending)
```

## Reproducing the Paper II results

### Prerequisites

- Python 3.10+ with numpy, scipy, pandas, matplotlib (see `requirements.txt`)
- Paper I package at tag v7.1.0 (for the canonical fits CSV and the v7.0 production fitter)
- Approximately 30-60 minutes of CPU time on a modern Apple Silicon Mac for the full perturbation + null suite

### Setup

1. Clone Paper I at v7.1.0:
   ```
   git clone https://github.com/RonBibb/sparc-halo-shells.git
   cd sparc-halo-shells
   git checkout v7.1.0
   ```

2. Copy Paper I's canonical fits CSV into Paper II's data directory:
   ```
   cp sparc-halo-shells/data/sparc_T2-T9_canonical_fits.csv halo_shells_paper2_v1.0/data/
   ```

3. Install dependencies:
   ```
   cd halo_shells_paper2_v1.0
   pip install -r requirements.txt
   ```

### Running the analyses

From `halo_shells_paper2_v1.0/scripts/`:

```bash
# Anti-warp clean subsample analysis (~5 seconds; pure analysis, no fitting)
python3 antiwarp_subsample.py

# Spatial-coherence null tests (~30-60 minutes; 20 realizations × 2 null types)
python3 shell_reality_nulls.py

# Baryonic systematic perturbations (~10-15 minutes each)
python3 upsilon_perturbation.py
python3 distance_perturbation.py
python3 inclination_perturbation.py
```

Outputs are written to `data/` with the canonical filenames listed above.

### Verifying outputs

Each script prints a summary of the headline statistics on completion. Cross-check against:
- `data/antiwarp_summary.txt` (anti-warp results)
- `data/nulltest_summary.txt` (null test z-scores)
- The per-galaxy CSVs for perturbation results

## Status

This package is **release v1.0**, draft state, suitable for internal review and figure generation. AJ submission pending Paper I publication.

| Component | Status |
| --- | --- |
| Manuscript text | ✅ Drafted; ~11,400 words |
| LaTeX source | ✅ Compiles; figures pending |
| Markdown source | ✅ Preserved for ongoing edits |
| Data CSVs (Paper II outputs) | ✅ DONE (8 CSVs in `data/`) |
| SPARC inputs | ✅ DONE (Rotmod_LTG/, classifications, sparc_sample123) |
| Producer scripts | ⚠️ Reconstructed from algorithm specs; verify against Mac-side reference |
| Logs | ✅ Captured for all four perturbation/antiwarp runs |
| Figures | ⏳ 10 placeholders; generation scripts to be written |
| Bibliography | ⏳ Skeleton entries; full DOIs at submission |
| Paper I canonical CSV | ❌ NOT INCLUDED — see "Relationship to Paper I" above |
| Validation pass | ⏳ Pending; checklist in `VALIDATION_STATUS.md` |
| Zenodo deposit | ⏳ Pending Paper I publication |
| AJ submission | ⏳ Pending |

## Citation

> Bibb, R. (2026). *Statistical Organization of Localized Residual Structure in SPARC Rotation Curves.* halo_shells_paper2 v1.0. Code and data: doi:[Zenodo DOI pending]

## Contact

Ron Bibb — <ronbibb@gmail.com> — ORCID 0009-0004-1153-2464

## License

Manuscript: under journal preparation (license per AJ policy upon acceptance).
Data and code: MIT License (see `LICENSE`).

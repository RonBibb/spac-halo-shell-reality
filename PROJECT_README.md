# Repository File Manifest — sparc-halo-shell-reality

**Last updated:** 2026-05-21
**Latest commit at snapshot:** `6aba87f`
**Maintainer:** Ron Bibb (<ronbibb@gmail.com>)
**Purpose:** Authoritative manifest of files in this repository, with provenance and version alignment, so future sessions can navigate without re-discovery.

---

## Version alignment — read this first

This repository is aligned with **Paper I v7.1.0** (`https://github.com/RonBibb/sparc-halo-shells`, release tag `v7.1.0`, PASP manuscript #PASP-102415, submitted 2026-05-18, awaiting referee reports as of snapshot). All canonical fits, framework parameters, and headline numbers are consistent with that release.

**This repo's role:** The Paper II working package. Companion manuscript to Paper I; statistical organization of the localized residual structures established in Paper I.

**Not in scope:**

- Paper A, B, C, D framework / k_SMBH coupling / two-component decomposition work (discontinued upstream of v7).
- Paper 3 cap-relaxation and hierarchical Υ marginalization (separate package, in preparation; data and partial code on local Mac, not yet pushed).
- Pre-v7 framework outputs.

If a file or claim references "shells at 10¹¹ M☉," "median r/r_vir ≈ 0.186," or any pre-v7.0 framework, treat as legacy and ignore.

---

## Root-level documentation

| File | Purpose |
| --- | --- |
| `README.md` | Package overview, structure, reproduction guide |
| `STATUS.md` | Single-source-of-truth for package state; submission checklist |
| `VALIDATION_STATUS.md` | Numerical-claims-to-source mapping; Tier 2 discrepancy tracking |
| `DATA_PROVENANCE.md` | Per-CSV producer/inputs/schema/citation trail |
| `ALIGNMENT_AUDIT.md` | Paper I ↔ Paper II numerical alignment audit |
| `PROJECT_README.md` | This file — repository file manifest |
| `LICENSE` | MIT License (data and code) |
| `requirements.txt` | Python dependencies |
| `shell_reality_nulls_parallel.py` | Root-level convenience copy of `scripts/shell_reality_nulls_parallel.py` |

---

## Manuscript (`source/`)

| File | Description |
| --- | --- |
| `source/paper2.md` | Canonical Markdown manuscript source (~13,300 words drafted). Latest edit: 2026-05-21 (§3.1.2 mass-cap acknowledgment paragraph added in commit `a86a0e5`). |
| `source/paper2_consolidated.pdf` | Compiled reading PDF (~221 KB). Reflects current state of `paper2.md`. |
| `source/paper1_v7.1.0.pdf` | Paper I v7.1.0 manuscript PDF (reference). |

LaTeX conversion to AASTeX 7.0.1 for PASP submission is pending.

---

## Data files (`data/`)

### Paper II output CSVs (this repo's analyses)

| File | Rows | Description |
| --- | --- | --- |
| `antiwarp_per_shell.csv` | 67 | §3.3.5 per-shell catalog, NGC 6674-excluded |
| `antiwarp_summary.txt` | — | §3.3.5 formatted summary |
| `backbone_shift.csv` | 102 | §3.3.7 backbone parameters at n=0/1/2 per galaxy |
| `backbone_shift_summary.txt` | — | §3.3.7 population-level summary |
| `upsilon_perturbation_per_galaxy.csv` | 2,040 | §3.3.2 Υ perturbation (102 × 20 realizations) |
| `distance_perturbation_per_galaxy.csv` | 2,040 | §3.3.3 distance perturbation |
| `inclination_perturbation_per_galaxy.csv` | 1,820 | §3.3.4 inclination perturbation (91 × 20; 11 edge-on excluded) |
| `nulltest_per_realization.csv` | 40 | §3.2 N=20 baseline (superseded by N=100) |
| `nulltest_per_galaxy.csv` | 4,080 | §3.2 N=20 baseline per-galaxy |
| `nulltest_summary.txt` | — | §3.2 N=20 baseline summary |
| `per_realization.csv`, `per_galaxy.csv`, `summary.txt` | — | Byte-identical duplicates of `nulltest_*` under legacy naming |
| `shell_reality_out_n100/per_realization.csv` | 200 | **Canonical N=100 for §3.2** |
| `shell_reality_out_n100/per_galaxy.csv` | 20,400 | **Canonical N=100 per-galaxy** |
| `shell_reality_out_n100/summary.txt` | — | **Canonical N=100 summary** |
| `ngc6674_exclusion_summary.txt` | — | §2.3 retirement: 102-gal vs 101-gal headlines for §3.3.2-4 and §3.3.7 |

### SPARC and Paper I inputs (sourced; not produced here)

| File | Description |
| --- | --- |
| `sparc_sample123.csv` | SPARC catalog metadata, 123 rows |
| `galaxy_classifications.csv` | SPARC + bulge/dwarf/MW-like classification flags, 123 rows |
| `nfw_fixedc_fits.csv` | NFW fixed-c reference fits |
| `einasto_full_sample_results.csv` | Paper I Einasto fits (copied for §3.3.6 reproducibility, 2026-05-19) |
| `einasto_robustness_results.csv` | Paper I Einasto robustness fits |
| `fig_3_3_6_einasto_comparison.pdf` (in `data/`) | *Historical placeholder; canonical copy is in `figures/` as of 2026-05-21* |
| `Rotmod_LTG/*_rotmod.dat` | 175 SPARC per-galaxy rotation curve files (Lelli, McGaugh & Schombert 2016) |

### Externally supplied (not in repo)

- `sparc_T2-T9_canonical_fits.csv` — Paper I canonical fits CSV; must be copied from the Paper I repository at v7.1.0 into `data/` before running scripts. See `DATA_PROVENANCE.md` for details.

---

## Scripts (`scripts/`)

All scripts depend on Paper I's `run_canonical_fits.py` or its components for the framework. The Paper I canonical fits CSV must be supplied externally.

| File | Section | Purpose |
| --- | --- | --- |
| `antiwarp_subsample.py` | §3.3.5, §3.1.2-4 | Anti-warp clean subsample analysis; produces `antiwarp_per_shell.csv` |
| `backbone_shift_test.py` | §3.3.7 | Backbone-shift production runner |
| `shell_reality_nulls.py` | §3.2 | Null test runner (serial), 519 lines |
| `shell_reality_nulls_parallel.py` | §3.2 | Null test runner (parallel), byte-identical to serial |
| `upsilon_perturbation.py` | §3.3.2 | M*/L perturbation runner, 514 lines |
| `distance_perturbation.py` | §3.3.3 | Distance perturbation runner, 570 lines |
| `inclination_perturbation.py` | §3.3.4 | Inclination perturbation runner, 570 lines |
| `run_canonical_fits.py` | (framework) | Paper I production fitter, copied from Paper I; 548 lines |
| `einasto_control.py` | §3.3.6 | Post-hoc analysis on Paper I's Einasto fits |
| `make_figures.py` | (all figures) | Generates all 13 manuscript figures from `data/` |
| `ngc6674_exclusion_reanalysis.py` | §2.3 | §2.3 retirement: re-aggregates §3.3.2-4 + §3.3.7 with NGC 6674 excluded |

---

## Logs (`logs/`)

| File | Purpose |
| --- | --- |
| `antiwarp_log.txt` | Run log for `antiwarp_subsample.py` |
| `upsilon_perturbation_log.txt` | Run log for `upsilon_perturbation.py` |
| `distance_perturbation_log.txt` | Run log for `distance_perturbation.py` |
| `inclination_perturbation_log.txt` | Run log for `inclination_perturbation.py` |

---

## Figures (`figures/`)

All 13 manuscript figures generated. Naming convention: `fig_<section>_<title>.pdf`.

| Figure | File | Cited |
| --- | --- | --- |
| 3.1.1 | `fig_3_1_1_bulge_correlation.pdf` | §3.1.1 |
| 3.1.2 | `fig_3_1_2_scaling_relations.pdf` | §3.1.2 |
| 3.1.3 | `fig_3_1_3_sigma_over_r_quartile.pdf` | §3.1.3 |
| 3.1.4 | `fig_3_1_4_inner_vs_outer.pdf` | §3.1.4 |
| 3.2.1 | `fig_3_2_1_scramble_null.pdf` | §3.2.1 |
| 3.2.2 | `fig_3_2_2_permute_null.pdf` | §3.2.2 |
| 3.3.1 | `fig_3_3_1_disk_dynamical_scales.pdf` | §3.3.1 |
| 3.3.2 | `fig_3_3_2_upsilon_perturbation.pdf` | §3.3.2 |
| 3.3.3 | `fig_3_3_3_distance_perturbation.pdf` | §3.3.3 |
| 3.3.4 | `fig_3_3_4_inclination_perturbation.pdf` | §3.3.4 |
| 3.3.5 | `fig_3_3_5_antiwarp_clean.pdf` | §3.3.5 |
| 3.3.6 | `fig_3_3_6_einasto_comparison.pdf` | §3.3.6 (placed 2026-05-21) |
| 3.3.7 | `fig_3_3_7_backbone_shift.pdf` | §3.3.7 |

---

## What's externally referenced but not in repo

- **Paper I canonical fits CSV** (`sparc_T2-T9_canonical_fits.csv`): from `RonBibb/sparc-halo-shells` at v7.1.0. Required by all scripts.
- **Paper 3 cap-relaxation code and outputs:** in preparation on local Mac. Not yet pushed to any repo. Will live in its own repository when ready.
- **LaTeX manuscript source** (`paper2.tex` and `references.bib`): to be generated from `paper2.md` at submission time.

---

## Notes for future-Claude on session start

1. **Read `STATUS.md` first.** It is the single source of truth for package state and current open items.
2. **The 102 vs 101 distinction matters.** §2.3 of the manuscript discloses two conventions; cross-check which one applies when discussing headline numbers.
3. **For numerical claims about the paper itself, check `source/paper2.md` directly** rather than reasoning from earlier values in conversation. The manuscript is canonical; intermediate documents (including these .md files) can lag.
4. **Cap acknowledgment is in §3.1.2.** Mass cap (5×10¹⁰ M☉) is treated as definitional in Paper II; bound-relaxation deferred to Paper 3 (model refinement: cap relaxation paired with hierarchical Υ marginalization).
5. **Excluded work.** Do not invoke Paper A/B/C/D, framework / k_SMBH coupling, or two-component decomposition content. That work is dead-end and shouldn't appear in current analyses or recommendations.

---

*If the file list at the top of a session disagrees with this README, the file list wins for what's loaded — but flag the discrepancy so the README can be updated.*

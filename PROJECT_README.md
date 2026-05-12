# Project Files Manifest

**Last updated:** 2026-05-10
**Maintainer:** Ron Bibb (ronbibb@gmail.com)
**Purpose:** Document the data and code in this project's working set, with version provenance, so future Claude sessions can navigate without re-uploading or re-asking for context.

---

## Version alignment — read this first

This project is aligned with **Paper I v7.1.0** (`https://github.com/RonBibb/sparc-halo-shells`, release tag `v7.1.0`, AJ submission 2026-05-10). All canonical fits, framework parameters, and headline numbers should be consistent with that release.

**Specifically NOT in this project (deliberately pruned):**

- Outputs from v6.5 or earlier framework versions
- The reproduced ceiling-pegging analysis (separate session, separate Claude). Its 36% pegging / 1.25 slope numbers do **not** transfer to actual v7.0 fits — verified in this session as 12% pegging / 0.28 slope on r/r_vir. Treat as out-of-scope unless re-verified.
- Earlier Paper 2 drafts that referenced backbone-invariance from v6.3.6
- Manuscript prose drafts (these live in the working repo, not project files)

If a file or claim references "shells at 10^11 M☉" or "median r/r_vir ≈ 0.186" or any pre-v7.0 framework, treat as legacy and ignore.

---

## File inventory

### Core SPARC inputs (canonical, do not modify)

- **`Rotmod_LTG/*_rotmod.dat`** (140 files) — SPARC per-galaxy rotation curve files from Lelli, McGaugh & Schombert 2016. Columns: r [kpc], V_obs [km/s], e_V_obs, V_gas, V_disk, V_bulge, SB_disk, SB_bulge.
- **`sparc_sample123.csv`** — SPARC sample catalog. 123 rows × 25 cols. Columns: Galaxy, T, D, e_D, f_D, Inc, e_Inc, L36, e_L36, Reff, SBeff, Rdisk, SBdisk, MHI, RHI, Vflat, e_Vflat, Q, Ref, M_star, r_vir, M_halo, plus log-versions.
- **`galaxy_classifications.csv`** — `sparc_sample123.csv` augmented with 7 classification flags (`is_dwarf`, `is_mw_like`, `is_bulge_dom`, `is_bulgeless`, `is_transitional`, `max_bulge_frac`, `has_bulge_col`). 123 rows × 32 cols. **Use this rather than `sparc_sample123.csv`** when bulge or dwarf flags are needed.
- **`PROJECT_README.md`** — this file
- **`sparc_shells.pdf`** — Paper I v7.1.0 manuscript

### Paper I v7.1.0 canonical fit outputs

- **`framework_fits.csv`** — Older two-component fits (cored-iso + Hernquist). Reference only; not used for current Paper II analysis.
- **`nfw_freec_fits.csv`** — NFW free-concentration fits, 123 rows × 14 cols. Reference comparison.
- **`nfw_fixedc_fits.csv`** — NFW fixed-concentration fits (DM14 prior), 123 rows × 12 cols. Reference comparison.
- **`sparc_shells_paper.pdf`** — Paper I v7.1.0 manuscript

(The v7.0 canonical fits CSV `sparc_T2-T9_canonical_fits.csv` is in the parent `sparc-halo-shells` repo, not duplicated here.)

### Paper II §3.3 perturbation tests (this session, v7.0-clean)

All three runs use the v7.0 production fitter (`run_canonical_fits.py`) with strict σ/r ≤ 0.4 enforcement. 20 realizations per channel.

- **`upsilon_perturbation_per_galaxy.csv`** — M*/L systematic test. 2,040 rows (102 galaxies × 20 realizations, 39 fits failed on V_obs² > V_bar² mask after Υ rescaling). Per-galaxy modal n_shells matches canonical in 95.1% of galaxies. Per-fit n_shells matches in 86.2%.
- **`upsilon_perturbation_log.txt`** — Run log: parameters, seed (20260510), per-realization Υ values drawn, progress trace. Documents that the fitter was the v7.0 production code at `sparc-halo-shells/scripts/run_canonical_fits.py`.
- **`distance_perturbation_per_galaxy.csv`** — Distance systematic test. 2,040 rows. Each galaxy draws D' from N(D, e_D) using SPARC catalog uncertainties. Per-galaxy mode-match: 94.1%. Per-fit match: 89.6%.
- **`distance_perturbation_log.txt`** — Run log including per-galaxy fractional uncertainty distribution: median 8.7%, mean 13.8%, max 132% (one dwarf with e_D > D).
- **`inclination_perturbation_per_galaxy.csv`** — Inclination systematic test. 1,820 rows (91 galaxies × 20 realizations; 11 edge-on galaxies at Inc=90° excluded by `0 < Inc < 90` check). Per-galaxy mode-match: 98.9%. Per-fit match: 95.7%.
- **`inclination_perturbation_log.txt`** — Run log including per-galaxy e_Inc distribution (median 3.0°, mean 3.85°, max 10°) and Inc range (30-89°).

### Paper II §3.3.5 anti-warp clean subsample (this session, v7.0-clean)

- **`antiwarp_per_shell.csv`** — Per-shell catalog with all classification flags. 67 shells across 51 galaxies (NGC6674 excluded as degenerate, both shells collapsed to r₁=r₂=3.12 kpc with both masses pegged at the upper bound). Columns: Galaxy, T, Q, n_total, position (inner/outer), r_sh_kpc, M_sh, sigma_sh_kpc, sigma_over_r, r_over_RHI, V_gas_at_kms, V_disk_at_kms, V_bulge_at_kms, is_disk_dominated, is_inner, is_bulge_dom, is_bulgeless.
- **`antiwarp_summary.txt`** — Formatted comparison of full sample (67 shells) vs clean anti-warp subsample (25 shells). Headline patterns survive: M ∝ r^0.66 vs full 0.76; σ ∝ r^0.93 vs 1.04; σ/r 0.316 vs 0.275; ρ_per_T -0.667 vs -0.762; bulge OR 2.49 vs 3.67.
- **`antiwarp_log.txt`** — Run log documenting paths used (canonical CSV, classifications, SPARC catalog, rotmod dir) and successful run completion. Also captures earlier failed runs against wrong rotmod paths — useful as a reminder that the working directory must contain the SPARC rotmod files.

### Paper II §3.2 null tests (this session, v7.0-clean)

Two null channels: scramble (within-galaxy DM-residual permutation, preserves Burkert backbone) and permute (cross-radius V_obs permutation within galaxy, destroys backbone). 20 realizations each.

- **`nulltest_per_realization.csv`** — Per-realization summary. 40 rows (2 null types × 20 realizations). Columns include null_type, real_idx, rho_per_T, rho_per_galaxy, n_shell_bearing, plus per-T shell-bearing fractions.
- **`nulltest_per_galaxy.csv`** — Per-galaxy fits across all realizations. 4,080 rows (2 null types × 20 realizations × 102 galaxies). Columns: null_type, real_idx, Galaxy, T, n_shells, n_shells_BIC, plus chi²/BIC values.
- **`nulltest_summary.txt`** — Formatted summary. Headline: scramble null ρ_per_T = -0.197 ± 0.146 (real = -0.833, z = -4.36); permute null ρ_per_T = +0.375 ± 0.232 (real = -0.833, z = -5.21). Both reject random-structure hypothesis at 0/20 realizations.

### Paper I v7.0/v7.1.0 framework comparison (this session)

- **`backbone_shift.csv`** — Burkert vs Einasto backbone-invariance comparison from Paper I §3.6. 102 galaxies. Used to verify Paper I's claim that morphology gradient survives backbone change (90/102 classification agreement).
- **`backbone_shift_summary.txt`** — Formatted summary of the backbone comparison.

---

## Sample size conventions

These conventions appear in different places and need to be tracked consistently:

- **102 galaxies** = the v7.0 canonical sample (T = 2–9, after SPARC-quality cuts in Paper I)
- **52 galaxies** = shell-bearing fraction in Paper I and §3.2 null tests (NGC6674 included as shell-bearing)
- **51 galaxies / 67 shells** = the per-shell working set in `antiwarp_per_shell.csv` (NGC6674 excluded as degenerate)
- **91 galaxies × 20 reps = 1,820 rows** = inclination perturbation (edge-on Inc=90° galaxies excluded)

If recomputing the morphology gradient ρ_per_T:
- With NGC6674 included (Paper I convention): ρ_per_T = -0.833
- Without NGC6674 (antiwarp convention): ρ_per_T = -0.762

Both are valid v7.0 numbers. **Paper II should use the Paper I convention (include NGC6674) for the morphology gradient** to align headline numbers with the parent paper.

---

## Quick-reference headline numbers

For Paper II writing, these v7.0/v7.1.0-clean numbers are the canonical reference:

| Quantity | Value | Source file |
|---|---|---|
| Total sample | 102 galaxies | `galaxy_classifications.csv` (T=2-9 subset) |
| Shell-bearing rate | 52/102 = 51.0% | `nulltest_summary.txt` |
| 1-shell galaxies | 26 (Paper I) / 35 (antiwarp, NGC6674 excl.) | derived |
| 2-shell galaxies | 26 (Paper I) / 16 (antiwarp, NGC6674 excl.) | derived |
| ρ_per_T (Paper I convention) | -0.833 | `nulltest_summary.txt` |
| ρ_per_galaxy | -0.296 | `nulltest_summary.txt` |
| M slope (vs r/kpc) | 0.76 | `antiwarp_summary.txt` |
| σ slope (vs r/kpc) | 1.04 | `antiwarp_summary.txt` |
| σ/r median | 0.275 | `antiwarp_summary.txt` |
| Bulge OR | 3.67 | `antiwarp_summary.txt` |
| Scramble null z (ρ_per_T) | -4.36 | computed from `nulltest_summary.txt` |
| Permute null z (ρ_per_T) | -5.21 | computed from `nulltest_summary.txt` |
| M*/L perturbation per-galaxy match | 95.1% | `upsilon_perturbation_per_galaxy.csv` |
| Distance perturbation per-galaxy match | 94.1% | `distance_perturbation_per_galaxy.csv` |
| Inclination perturbation per-galaxy match | 98.9% | `inclination_perturbation_per_galaxy.csv` |

---

## Known caveats

1. **Mass ceiling at 5×10¹⁰ M☉ is binding for ~12% of v7.0 shells** (8/67 in the antiwarp set, within 0.05 dex of the upper bound). The kpc M-r slope changes from 0.76 to 0.67 when these are removed. Acknowledge in §2 (methods) or §4 (limitations); do not treat as a major artifact since binary classification and morphology gradient are unaffected.

2. **Inclination perturbation excludes 11 edge-on galaxies** (Inc=90° exactly). Caveat is minor (sin(89°)/sin(90°) ≈ 1.000) but should be mentioned in §3.3.4. To include these, change `< 90` to `<= 90` in `inclination_perturbation.py` and rerun (~9 minutes).

3. **NGC6674 has a degenerate v7.0 fit** (both shells at r=3.12 kpc, both masses pegged at upper bound). Paper I includes it as shell-bearing in the binary classification; Paper II's per-shell analyses (antiwarp, scaling relations) exclude it. Document this convention explicitly in any new analysis script.

4. **Null tests use 20 realizations**, giving an empirical p-floor of 1/20 = 0.05. Effective significance comes from z-scores (-4.36, -5.21), not empirical p-values. If the journal asks for tighter p-values, more realizations would be needed (each takes ~10 min wall clock per realization).

---

## Adding to this manifest

When adding new files to the project, update this manifest with:
- File name
- Source (script/session that produced it, with date)
- Row × column count
- One-sentence description
- Any version/convention caveats

Files added without manifest updates will be hard for future Claude sessions to interpret.

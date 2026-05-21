# Data Provenance — halo_shells_paper2

**Snapshot date:** 2026-05-21
**Latest commit at snapshot:** `6aba87f`

This file documents the provenance of every data file in this package: source script, input dependencies, output schema, and the manuscript section(s) that cite it.

---

## Paper II output CSVs (in `data/`)

### antiwarp_per_shell.csv

- **Producer:** `scripts/antiwarp_subsample.py`
- **Inputs:** Paper I canonical fits CSV, galaxy_classifications.csv, sparc_sample123.csv, Rotmod_LTG/*.dat
- **Schema:** 67 rows × 18 cols. Columns: Galaxy, T, Q, n_total, position (inner/outer), r_sh_kpc, M_sh, sigma_sh_kpc, sigma_over_r, r_over_RHI, V_gas_at_kms, V_disk_at_kms, V_bulge_at_kms, is_disk_dominated, is_inner, is_bulge_dom, is_bulgeless, is_clean
- **Sample convention:** NGC 6674 EXCLUDED (degenerate two-shell fit at r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound 5×10¹⁰ M☉). Matches manuscript §3.3.5 primary table at 67 shells / 25 anti-warp clean shells.
- **Cited in:** §3.3.5 (anti-warp clean subsample), §3.1.2 (scaling relations and mass-bound check including the 8/67 = 11.9% cap acknowledgment added 2026-05-21), §3.1.3 (σ/r quartile gradient), §3.1.4 (inner-vs-outer paired tests)

### antiwarp_summary.txt

- **Producer:** `scripts/antiwarp_subsample.py`
- **Inputs:** Same as antiwarp_per_shell.csv
- **Schema:** Plain text, formatted output
- **Sample convention:** NGC 6674 EXCLUDED — matches the per-shell CSV at 67 shells across 51 galaxies, 25 anti-warp clean shells.
- **Cited in:** §3.3.5 Table 3.3.5

### backbone_shift.csv

- **Producer:** `scripts/backbone_shift_test.py`
- **Inputs:** Paper I canonical fits CSV, Rotmod_LTG/*.dat, Paper I fitter (via `shell_reality_nulls.py` shared module)
- **Test design:** For each of 102 galaxies in the Paper I-aligned sample, refit the Paper I framework at n_shells = 0, 1, 2 and record the Burkert backbone parameters (ρ₀, a) at every level. Compare (ρ₀, a) at the BIC-selected n against (ρ₀, a) at the constrained n=0, separately for shell-bearing and non-shell-bearing galaxies.
- **Schema:** 102 rows × ~25 cols. Columns: Galaxy, T, V_flat, v7_n_shells, v7_burk_rho0, v7_burk_a, n_pts, n0_rho0, n0_a, n0_chi2, n0_bic, n1_rho0, n1_a, n1_chi2, n1_bic, n2_rho0, n2_a, n2_chi2, n2_bic, n_selected, delta_rho0_select, delta_a_select, log_ratio_rho0, ratio_a
- **Sample convention:** NGC 6674 INCLUDED at the raw-fit level (102-galaxy Paper I-aligned). Manuscript reports 101-galaxy aggregations via `ngc6674_exclusion_reanalysis.py`.
- **Cited in:** §3.3.7, §3.3.9 (combined verdict channel)
- **Headline result:** Median log₁₀(ρ₀[BIC]/ρ₀[n=0]) = -0.624 dex; median log₁₀(a[BIC]/a[n=0]) = +0.318 dex; 46/52 (88.5%) shell-bearing galaxies show the "absorbing pattern" of ρ₀ down + a up when shells allowed (102-galaxy raw aggregation; 101-galaxy: 45/51 = 88.2%, see `ngc6674_exclusion_summary.txt`). Wilcoxon p < 10⁻⁴ for both shifts. Shift correlates with T-type (Spearman ρ = +0.44, p = 0.001).

### backbone_shift_summary.txt

- **Producer:** `scripts/backbone_shift_test.py`
- **Inputs:** Same as backbone_shift.csv
- **Schema:** Plain text, formatted population-level summary
- **Sample convention:** Same as backbone_shift.csv (102-galaxy Paper I-aligned, NGC 6674 included)
- **Cited in:** §3.3.7

### upsilon_perturbation_per_galaxy.csv

- **Producer:** `scripts/upsilon_perturbation.py`
- **Inputs:** SPARC Rotmod files, sparc_sample123.csv, Paper I production fitter
- **Test design:** 20 realizations per galaxy. Each draws (log Υ_disk', log Υ_bulge') from independent normal distributions with means (log 0.5, log 0.7) and standard deviation 0.1 dex. Refits the Paper I framework on each perturbed input.
- **Schema:** 2,040 rows × 20 cols (102 galaxies × 20 realizations). Columns: Galaxy, realization, Upsilon_disk, Upsilon_bulge, status, n_shells, n_points, rho0, a_kpc, chi2, chi2_red, bic, r_sh1, M_sh1, sigma_sh1, sigma_over_r1, r_sh2, M_sh2, sigma_sh2, sigma_over_r2
- **Sample convention:** NGC 6674 INCLUDED at the raw-fit level. Manuscript reports 101-galaxy aggregation via `ngc6674_exclusion_reanalysis.py`.
- **Cited in:** §3.3.2; §3.3.9 channel (ii)
- **Run log:** `logs/upsilon_perturbation_log.txt`
- **Headline result:** Per-galaxy modal n_shells matches canonical in 95.1% of galaxies; per-fit match 86.2%.

### distance_perturbation_per_galaxy.csv

- **Producer:** `scripts/distance_perturbation.py`
- **Inputs:** Same as upsilon_perturbation
- **Test design:** 20 realizations. Each draws D' from N(D, e_D) using SPARC catalog uncertainties, refits with perturbed radii (r → r · D'/D) and perturbed baryonic velocities (V_bar → V_bar · √(D'/D)). V_obs unchanged.
- **Schema:** 2,040 rows × 22 cols. Columns: Galaxy, realization, D_nominal_Mpc, D_perturbed_Mpc, distance_factor, e_D_Mpc, status, n_shells, n_points, rho0, a_kpc, chi2, chi2_red, bic, r_sh1, M_sh1, sigma_sh1, sigma_over_r1, r_sh2, M_sh2, sigma_sh2, sigma_over_r2
- **Sample convention:** NGC 6674 INCLUDED at the raw-fit level. 101-gal aggregation via `ngc6674_exclusion_reanalysis.py`.
- **Cited in:** §3.3.3; §3.3.9 channel (iii)
- **Run log:** `logs/distance_perturbation_log.txt`
- **Headline result:** Per-galaxy modal match 94.1%; per-fit 89.6%. Fractional perturbation magnitudes: median 8.7%, mean 13.8%.

### inclination_perturbation_per_galaxy.csv

- **Producer:** `scripts/inclination_perturbation.py`
- **Inputs:** Same as upsilon_perturbation
- **Test design:** 20 realizations. Each draws Inc' from N(Inc, e_Inc) per-galaxy, rescales V_obs and e_V_obs by sin(Inc)/sin(Inc'). All 102 galaxies in the canonical sample are included; 11 edge-on galaxies (Inc = 90°) are handled via a reflection treatment that folds any post-perturbation Inc' > 90° to 180° - Inc' on the observationally-equivalent opposite side of edge-on, preserving a symmetric Gaussian perturbation distribution. Perturbed values are floored at 10° and capped at 89° to avoid pathological behavior near sin(i) = 0. (Pre-2026-05-21: an earlier version of the script used `0 < Inc < 90` and excluded the 11 edge-on galaxies entirely, producing 1,820 rows. See `VALIDATION_STATUS.md` for migration notes.)
- **Schema:** 2,040 rows × 22 cols (102 galaxies × 20 realizations). Columns include Inc_nominal_deg, Inc_perturbed_deg, e_Inc_deg, vobs_factor, plus the same fit columns as the other perturbation CSVs.
- **Sample convention:** NGC 6674 INCLUDED at the raw-fit level. 101-gal aggregation (2,020 fits) via `ngc6674_exclusion_reanalysis.py`.
- **Cited in:** §3.3.4; §3.3.9 channel (iv)
- **Run log:** `logs/inclination_perturbation_log.txt`
- **Headline result:** Per-galaxy modal match 98.0% (99/101 on 101-gal basis; 100/102 on raw); per-fit 95.9%. Edge-on subset matches canonical in 220/220 fits (100%). Tightest position recovery of the three perturbation tests (median |Δ log r₁| = 0.0022 dex).

### nulltest_per_realization.csv

- **Producer:** `scripts/shell_reality_nulls.py` (N=20 baseline run)
- **Status:** N=20 baseline; **superseded for manuscript §3.2 numerics by `shell_reality_out_n100/per_realization.csv` (N=100; documented below)**. Retained for historical reproducibility and for byte-for-byte comparison against the parallel runner's N=2 validation subset.
- **Inputs:** SPARC Rotmod files, Paper I canonical CSV, Paper I production fitter
- **Test design:** Two null types — *scramble* (within-galaxy permutation of dark-matter residuals around the canonical Burkert backbone) and *permute* (within-galaxy permutation of V_obs values across radii). 20 realizations per null type. Each realization fits all 102 galaxies and computes per-T-bin and per-galaxy Spearman ρ.
- **Schema:** 40 rows × 24 cols (2 null types × 20 realizations). Columns: null_type, realization, rho_per_T, p_per_T, rho_per_gal, p_per_gal, n_shellbearing, n_total, plus per-T shell-bearing fractions (frac_T2 through frac_T9 with their counts).
- **Sample convention:** NGC 6674 INCLUDED.
- **Note on duplicate filename:** byte-identical copies also exist at `data/per_realization.csv` under legacy script-output naming.

### nulltest_per_galaxy.csv

- **Producer:** `scripts/shell_reality_nulls.py` (N=20 baseline run)
- **Status:** N=20 baseline; superseded for §3.2 numerics by N=100.
- **Inputs:** Same as nulltest_per_realization.csv
- **Schema:** 4,080 rows × 8 cols (2 null types × 20 realizations × 102 galaxies). Columns: null_type, realization, Galaxy, T, n_pts, n_shells, chi2, bic.
- **Sample convention:** NGC 6674 INCLUDED.
- **Note on duplicate filename:** byte-identical copy at `data/per_galaxy.csv`.

### nulltest_summary.txt

- **Producer:** `scripts/shell_reality_nulls.py` (N=20 baseline run; formatted output)
- **Status:** N=20 baseline summary; superseded for §3.2 numerics by N=100.
- **Schema:** Plain text formatted summary
- **Note on duplicate filename:** byte-identical copy at `data/summary.txt`.

### shell_reality_out_n100/per_realization.csv  *(canonical for §3.2)*

- **Producer:** `scripts/shell_reality_nulls_parallel.py` (100 realizations, 12 workers)
- **Status:** **Canonical N=100 results for §3.2 numerics in the current manuscript.**
- **Inputs:** SPARC Rotmod files, Paper I canonical CSV (sparc_T2-T9_canonical_fits.csv), Paper I production fitter
- **Test design:** Same as nulltest_per_realization.csv but with 100 realizations per null type instead of 20. Parallelism granularity is the realization, with deterministic seeding such that the parallel run is byte-identical to a serial run of the same seed sequence.
- **Schema:** 200 rows × 24 cols (2 null types × 100 realizations). Columns identical to nulltest_per_realization.csv.
- **Sample convention:** NGC 6674 INCLUDED.
- **Cited in:** §3.2, §3.3.8, §3.3.9 channel (viii)
- **Headline results:**
  - Scramble ρ_per_T: mean = -0.289, std = 0.229, z = -2.4σ vs real-data -0.762; empirical p = 2/100.
  - Permute ρ_per_T: mean = +0.350, std = 0.235, z = -5.0σ; empirical p = 0/100.
  - Asymmetric failure direction (scramble under-detects; permute over-detects with reversed sign) preserved relative to N=20 baseline.

### shell_reality_out_n100/per_galaxy.csv  *(canonical for §3.2)*

- **Producer:** `scripts/shell_reality_nulls_parallel.py`
- **Status:** Canonical N=100 per-galaxy fits.
- **Inputs:** Same as shell_reality_out_n100/per_realization.csv.
- **Schema:** 20,400 rows × 8 cols (2 null types × 100 realizations × 102 galaxies). Columns: null_type, realization, Galaxy, T, n_pts, n_shells, chi2, bic.
- **Sample convention:** NGC 6674 INCLUDED.
- **Cited in:** §3.2 (per-galaxy stratifications, when needed).

### shell_reality_out_n100/summary.txt  *(canonical for §3.2)*

- **Producer:** `scripts/shell_reality_nulls_parallel.py` (formatted output)
- **Status:** Canonical N=100 summary. Use this for headline numbers, not `nulltest_summary.txt`.
- **Schema:** Plain text formatted summary.
- **Cited in:** §3.2.1, §3.2.2, §3.2.3, §3.2.4.

---

### ngc6674_exclusion_summary.txt

- **Producer:** `scripts/ngc6674_exclusion_reanalysis.py`
- **Inputs:** `data/upsilon_perturbation_per_galaxy.csv`, `data/distance_perturbation_per_galaxy.csv`, `data/inclination_perturbation_per_galaxy.csv`, `data/backbone_shift.csv`, `data/sparc_T2-T9_canonical_fits.csv` (for canonical n_shells per galaxy)
- **Test design:** Re-aggregate the four §3.3 production-batch CSVs (Υ/D/i perturbations + backbone-shift) with NGC 6674 excluded from the per-galaxy population, producing 101-galaxy headline statistics parallel to the 102-galaxy as-run statistics. No refitting required.
- **Schema:** Plain text formatted report.
- **Headline result:** Maximum shift across all four tests = 0.25 percentage points. §3.3.7 absorbing pattern: 46/52 = 88.5% (102-gal) → 45/51 = 88.2% (101-gal); binomial p = 1.0×10⁻⁸ → 1.8×10⁻⁸.
- **Cited in:** §2.3 (sample-partition retirement note); §3.3.2, §3.3.3, §3.3.4, §3.3.7 (101-galaxy headline numbers).
- **Sample convention:** Reports BOTH 102-galaxy and 101-galaxy versions side-by-side. The manuscript adopts the 101-galaxy numbers throughout §3.3.

---

## Inputs from external sources (in `data/`)

### sparc_sample123.csv

- **Source:** SPARC catalog [Lelli, McGaugh, Schombert 2016, AJ 152, 157]
- **Schema:** 123 rows × 25 cols. Standard SPARC catalog columns plus derived M_star, r_vir, M_halo via abundance matching (procedure described in Paper I §2.1).
- **Cited in:** §2.1 (sample), §2.2 (catalog metadata for fitting)

### galaxy_classifications.csv

- **Source:** Augmented from sparc_sample123.csv with bulge/dwarf/MW-like classifications derived from the SPARC photometric decomposition.
- **Schema:** 123 rows × 32 cols. sparc_sample123 columns plus 7 boolean flags: is_dwarf, is_mw_like, is_bulge_dom, is_bulgeless, is_transitional, max_bulge_frac, has_bulge_col.
- **Cited in:** §3.1.1 (bulge correlation)

### nfw_fixedc_fits.csv

- **Source:** Paper II reference; NFW fixed-concentration fits using the DM14 prior.
- **Schema:** 123 rows × 12 cols.
- **Cited in:** §1 (introduction context); not the primary fitting framework of the paper.

### einasto_full_sample_results.csv

- **Source:** Paper I v7.1.0 (`einasto_full_sample_results.csv`). Copied into this repo's `data/` directory as of 2026-05-19 for reproducibility convenience; canonical version remains in the Paper I repository.
- **Required for:** §3.3.6 backbone-family Einasto comparison via `scripts/einasto_control.py`
- **Cited in:** §3.3.6

### einasto_robustness_results.csv

- **Source:** Paper I v7.1.0 robustness fits. Included for §3.3.6 cross-reference.

### Rotmod_LTG/

- **Source:** SPARC distribution. 175 SPARC galaxies; 102 are used in the T = 2-9 sample after Paper I quality cuts. 101 in primary §3.1/§3.3.5/§3.3.6 analyses (NGC 6674 excluded).
- **Schema:** Tab-separated ASCII files with columns: Rad (kpc), V_obs (km/s), errV (km/s), V_gas, V_disk, V_bulge, SBdisk, SBbul.
- **Cited in:** §2.1; primary input to all fitting analyses.

---

## Inputs that must be supplied externally

### Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`)

- **Source:** Paper I repository at v7.1.0, in `data/`
- **Required for:** All analyses in `scripts/` that reference per-galaxy shell parameters
- **Why not duplicated here:** To prevent drift between Paper I v7.1.0 and a copy embedded in the Paper II repository. The Paper I repo is the canonical source.
- **How to obtain:**
  ```
  git clone https://github.com/RonBibb/sparc-halo-shells.git
  cd sparc-halo-shells && git checkout v7.1.0
  cp data/sparc_T2-T9_canonical_fits.csv ../sparc-halo-shell-reality/data/
  ```

### Paper I production fitter (`run_canonical_fits.py`)

- **Source:** Paper I repository at v7.1.0, in `scripts/`. A copy is included in this package's `scripts/` directory for convenience; the canonical version remains in Paper I.
- **Required for:** All perturbation runner scripts and the null/backbone-shift scripts, which call out to the Paper I fitter on perturbed inputs.

---

## Scripts (full producer details inline with each CSV above)

### scripts/shell_reality_nulls_parallel.py

- **Purpose:** Parallel runner for §3.2 null tests at arbitrary N (default 100). Replaces serial `shell_reality_nulls.py` for production runs at N ≥ 100.
- **Parallelism granularity:** Per realization (not per galaxy). Deterministic seed sequence ensures output is byte-identical to a serial run of the same seed sequence.
- **Default invocation:** `python3 shell_reality_nulls_parallel.py 100 12` (100 realizations × 2 null types, 12 worker processes).
- **Wall time:** ~2 hr on Apple Silicon M1 Ultra at 12 workers.
- **Outputs:** `data/shell_reality_out_n100/{per_realization.csv,per_galaxy.csv,summary.txt}`.

### scripts/einasto_control.py

- **Purpose:** Post-hoc analysis of Paper I's Einasto-backbone fits (§3.3.6). Compares shell-population organizational signatures between Burkert-backbone (Paper I/II canonical) and Einasto-backbone (strictly more flexible, one additional free parameter).
- **External input required:** `data/einasto_full_sample_results.csv` (now included in this repo as of 2026-05-19).
- **Outputs:** Prints comparison statistics to stdout, organized into 8 sections.
- **Sample convention:** NGC 6674 EXCLUDED (101-galaxy convention).
- **Cited in:** §3.3.6.
- **Headline results:** ρ_per_T strengthens to -0.87 (p = 0.005) under Einasto vs -0.762 (p = 0.028) under Burkert; bulge OR strengthens to 4.32 (p = 0.003); M-r slope preserved at 0.82 (Burkert 0.76); σ-r slope attenuates to 0.38 (Burkert 1.04).

### scripts/make_figures.py

- **Purpose:** Generate all 13 manuscript figures from data in `data/`. Function-per-figure architecture; CLI selects individual figures or runs all.
- **Inputs:** Reads from `data/` (paths resolved relative to script location).
- **Outputs:** PDF to `figures/` for each figure. All 13 figures currently generated and present in `figures/`.
- **CLI:**
  ```
  python3 make_figures.py --all                # generate everything
  python3 make_figures.py --figure 3.1.1       # one figure
  python3 make_figures.py --figure 3.1.1,3.2.1 # multiple
  python3 make_figures.py --list               # list available figures
  ```

### scripts/ngc6674_exclusion_reanalysis.py

- **Purpose:** Re-aggregate the four §3.3 production-batch CSVs with NGC 6674 excluded from the per-galaxy population.
- **Inputs:** All four §3.3 per-galaxy CSVs plus the Paper I canonical CSV (for canonical n_shells per galaxy).
- **Outputs:** `data/ngc6674_exclusion_summary.txt` plus stdout.
- **Run time:** ~5 seconds.
- **CLI:** `python3 ngc6674_exclusion_reanalysis.py` (no arguments).
- **Headline result:** Maximum perturbation-test headline shift = 0.16 pp; backbone-shift absorbing-pattern shift = -0.23 pp. All four §3.3 tests retain qualitative direction and significance under the 101-galaxy convention.

---

## Section-to-data quick reference

| Manuscript section | Primary data | Secondary data |
| --- | --- | --- |
| §2.1 Sample | sparc_sample123.csv, galaxy_classifications.csv | Rotmod_LTG/ |
| §2.2 Framework | (Paper I canonical CSV — external) | — |
| §3.1.1 Bulge correlation | galaxy_classifications.csv + Paper I canonical | antiwarp_per_shell.csv |
| §3.1.2 Scaling relations + cap acknowledgment | antiwarp_per_shell.csv | antiwarp_summary.txt |
| §3.1.3 σ/r quartile gradient | antiwarp_per_shell.csv | — |
| §3.1.4 Inner-vs-outer | antiwarp_per_shell.csv + sparc_sample123.csv (r_vir) | — |
| §3.1.5 Multiple-comparisons summary | (recomputed from above) | — |
| §3.2.1 Scramble null | shell_reality_out_n100/per_realization.csv | shell_reality_out_n100/summary.txt |
| §3.2.2 Permute null | shell_reality_out_n100/per_realization.csv | shell_reality_out_n100/summary.txt |
| §3.2.3 Per-T fractions | shell_reality_out_n100/summary.txt | shell_reality_out_n100/per_galaxy.csv |
| §3.3.1 Disk dynamical scales | (analysis on Paper I canonical CSV) | — |
| §3.3.2 Υ perturbation | upsilon_perturbation_per_galaxy.csv | logs/upsilon_perturbation_log.txt |
| §3.3.3 Distance perturbation | distance_perturbation_per_galaxy.csv | logs/distance_perturbation_log.txt |
| §3.3.4 Inclination perturbation | inclination_perturbation_per_galaxy.csv | logs/inclination_perturbation_log.txt |
| §3.3.5 Anti-warp clean subsample | antiwarp_summary.txt | antiwarp_per_shell.csv |
| §3.3.6 Einasto backbone-family control | einasto_full_sample_results.csv | einasto_control.py output |
| §3.3.7 Backbone-shift test | backbone_shift_summary.txt | backbone_shift.csv |
| §3.3.8 Cross-ref to §3.2 | shell_reality_out_n100/summary.txt | — |
| §3.3.9 Combined verdict | (citations above) | — |

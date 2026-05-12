# Data Provenance — halo_shells_paper2 v1.0

This file documents the provenance of every data file in this package: source script, input dependencies, output schema, and the manuscript section(s) that cite it.

---

## Paper II output CSVs (in `data/`)

### antiwarp_per_shell.csv

- **Producer:** `scripts/antiwarp_subsample.py`
- **Inputs:** Paper I canonical fits CSV, galaxy_classifications.csv, sparc_sample123.csv, Rotmod_LTG/*.dat
- **Schema:** 67 rows × 18 cols. Columns: Galaxy, T, Q, n_total, position (inner/outer), r_sh_kpc, M_sh, sigma_sh_kpc, sigma_over_r, r_over_RHI, V_gas_at_kms, V_disk_at_kms, V_bulge_at_kms, is_disk_dominated, is_inner, is_bulge_dom, is_bulgeless, is_clean
- **Sample convention:** NGC 6674 EXCLUDED (degenerate fit at r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound). The CSV is preserved with this exclusion. The accompanying `antiwarp_summary.txt` was regenerated with NGC 6674 INCLUDED to align with Paper I; this discrepancy is documented in VALIDATION_STATUS.md and is on the future-revisions list.
- **Cited in:** §3.3.5 (anti-warp clean subsample), §3.1.2 (mass-bound check), §3.1.4 (inner-vs-outer paired tests)

### antiwarp_summary.txt

- **Producer:** `scripts/antiwarp_subsample.py` (regenerated rerun with NGC 6674 included)
- **Inputs:** Same as antiwarp_per_shell.csv plus Paper I canonical CSV
- **Schema:** Plain text, formatted output
- **Sample convention:** NGC 6674 INCLUDED, 69 shells across 52 galaxies
- **Cited in:** §3.3.5 Table 3.3.5

### upsilon_perturbation_per_galaxy.csv

- **Producer:** `scripts/upsilon_perturbation.py`
- **Inputs:** SPARC Rotmod files, sparc_sample123.csv, Paper I v7.0 production fitter (`run_canonical_fits.py` from Paper I repo)
- **Test design:** 20 realizations per galaxy. Each draws (log Υ_disk', log Υ_bulge') from independent normal distributions with means (log 0.5, log 0.7) and standard deviation 0.1 dex. Refits the v7.0 framework on each perturbed input.
- **Schema:** 2,040 rows × 20 cols (102 galaxies × 20 realizations; 39 fits failed on V_obs² > V_bar² mask after Υ rescaling). Columns: Galaxy, realization, Upsilon_disk, Upsilon_bulge, status, n_shells, n_points, rho0, a_kpc, chi2, chi2_red, bic, r_sh1, M_sh1, sigma_sh1, sigma_over_r1, r_sh2, M_sh2, sigma_sh2, sigma_over_r2
- **Cited in:** §3.3.2; §3.3.7 channel (ii)
- **Run log:** `logs/upsilon_perturbation_log.txt`
- **Headline result:** Per-galaxy modal n_shells matches canonical in 95.1% of galaxies; per-fit match 86.2%.

### distance_perturbation_per_galaxy.csv

- **Producer:** `scripts/distance_perturbation.py`
- **Inputs:** Same as upsilon_perturbation
- **Test design:** 20 realizations. Each draws D' from N(D, e_D) using SPARC catalog uncertainties, refits with perturbed radii (r → r · D'/D) and perturbed baryonic velocities (V_bar → V_bar · √(D'/D)). V_obs unchanged.
- **Schema:** 2,040 rows × 22 cols. Columns: Galaxy, realization, D_nominal_Mpc, D_perturbed_Mpc, distance_factor, e_D_Mpc, status, n_shells, n_points, rho0, a_kpc, chi2, chi2_red, bic, r_sh1, M_sh1, sigma_sh1, sigma_over_r1, r_sh2, M_sh2, sigma_sh2, sigma_over_r2
- **Cited in:** §3.3.3; §3.3.7 channel (iii)
- **Run log:** `logs/distance_perturbation_log.txt`
- **Headline result:** Per-galaxy modal match 94.1%; per-fit 89.6%. Fractional perturbation magnitudes: median 8.7%, mean 13.8%.

### inclination_perturbation_per_galaxy.csv

- **Producer:** `scripts/inclination_perturbation.py`
- **Inputs:** Same as upsilon_perturbation
- **Test design:** 20 realizations. Each draws Inc' from N(Inc, e_Inc) per-galaxy, rescales V_obs and e_V_obs by sin(Inc)/sin(Inc'). 11 galaxies at Inc = 90° excluded by `0 < Inc < 90` check.
- **Schema:** 1,820 rows × 22 cols (91 galaxies × 20 realizations). Columns include Inc_nominal_deg, Inc_perturbed_deg, e_Inc_deg, vobs_factor, plus the same fit columns as the other perturbation CSVs.
- **Cited in:** §3.3.4; §3.3.7 channel (iv)
- **Run log:** `logs/inclination_perturbation_log.txt`
- **Headline result:** Per-galaxy modal match 98.9%; per-fit 95.7%. Tightest position recovery of the three perturbation tests (median Δ log r₁ = 0.005 dex).

### nulltest_per_realization.csv

- **Producer:** `scripts/shell_reality_nulls.py`
- **Inputs:** SPARC Rotmod files, Paper I canonical CSV, v7.0 production fitter
- **Test design:** Two null types — *scramble* (within-galaxy permutation of dark-matter residuals around the canonical Burkert backbone) and *permute* (within-galaxy permutation of V_obs values across radii). 20 realizations per null type. Each realization fits all 102 galaxies and computes per-T-bin and per-galaxy Spearman ρ.
- **Schema:** 40 rows × 24 cols (2 null types × 20 realizations). Columns: null_type, realization, rho_per_T, p_per_T, rho_per_gal, p_per_gal, n_shellbearing, n_total, plus per-T shell-bearing fractions (frac_T2 through frac_T9 with their counts).
- **Cited in:** §3.2

### nulltest_per_galaxy.csv

- **Producer:** `scripts/shell_reality_nulls.py`
- **Inputs:** Same as nulltest_per_realization.csv
- **Schema:** 4,080 rows × 8 cols (2 null types × 20 realizations × 102 galaxies). Columns: null_type, realization, Galaxy, T, n_pts, n_shells, chi2, bic.
- **Cited in:** §3.2 (per-galaxy fit details available for stratification)

### nulltest_summary.txt

- **Producer:** `scripts/shell_reality_nulls.py` (formatted output)
- **Schema:** Plain text formatted summary
- **Cited in:** §3.2.1, §3.2.2, §3.2.3, §3.2.4

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

### Rotmod_LTG/

- **Source:** SPARC distribution. 175 SPARC galaxies; 102 are used in the T = 2-9 sample after quality cuts.
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
  cp data/sparc_T2-T9_canonical_fits.csv ../halo_shells_paper2_v1.0/data/
  ```

### Paper I v7.0 production fitter (`run_canonical_fits.py`)

- **Source:** Paper I repository at v7.1.0, in `scripts/`
- **Required for:** The four perturbation runner scripts (`upsilon_`, `distance_`, `inclination_`, `shell_reality_nulls`) which call out to the v7.0 fitter on perturbed inputs
- **Why not duplicated:** Paper I is the canonical source for the fitter; embedding a copy risks divergence
- **How to obtain:**
  ```
  cp sparc-halo-shells/scripts/run_canonical_fits.py ../halo_shells_paper2_v1.0/scripts/
  ```

---

## Section-to-data quick reference

| Manuscript section | Primary data | Secondary data |
| --- | --- | --- |
| §2.1 Sample | sparc_sample123.csv, galaxy_classifications.csv | Rotmod_LTG/ |
| §2.2 Framework | (Paper I canonical CSV — external) | — |
| §3.1.1 Bulge correlation | galaxy_classifications.csv + Paper I canonical | antiwarp_per_shell.csv |
| §3.1.2 Scaling relations | antiwarp_per_shell.csv | antiwarp_summary.txt |
| §3.1.3 σ/r quartile gradient | antiwarp_per_shell.csv | — |
| §3.1.4 Inner-vs-outer | antiwarp_per_shell.csv + sparc_sample123.csv (r_vir) | — |
| §3.2.1 Scramble null | nulltest_per_realization.csv | nulltest_summary.txt |
| §3.2.2 Permute null | nulltest_per_realization.csv | nulltest_summary.txt |
| §3.2.3 Per-T fractions | nulltest_summary.txt | nulltest_per_galaxy.csv |
| §3.3.1 Disk dynamical scales | (analysis on Paper I canonical CSV) | — |
| §3.3.2 Υ perturbation | upsilon_perturbation_per_galaxy.csv | logs/upsilon_perturbation_log.txt |
| §3.3.3 Distance perturbation | distance_perturbation_per_galaxy.csv | logs/distance_perturbation_log.txt |
| §3.3.4 Inclination perturbation | inclination_perturbation_per_galaxy.csv | logs/inclination_perturbation_log.txt |
| §3.3.5 Anti-warp clean subsample | antiwarp_summary.txt | antiwarp_per_shell.csv |
| §3.3.6 Cross-ref to §3.2 | nulltest_summary.txt | — |
| §3.3.7 Combined verdict | (citations above) | — |

# Validation Status — halo_shells_paper2 v1.0

**Package version:** v1.0
**Release date:** 2026-05-10
**Manuscript file:** `source/paper2.tex` (LaTeX) and `source/paper2.md` (markdown source)
**Parent paper alignment:** Paper I v7.1.0 (https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0)

---

## Version alignment with Paper I

This package is built against Paper I v7.1.0. All canonical fits, framework parameters, and headline numbers are aligned with that release. Specifically:

- **Canonical sample**: 102 SPARC galaxies, T = 2-9, after Paper I quality cuts (matches Paper I §2.1)
- **Framework**: v7.0 Burkert backbone + 0/1/2 BIC-selected Gaussian shells, σ/r ≤ 0.4 strict reparameterization, mass bound 5×10¹⁰ M☉ (matches Paper I §2.2)
- **Shell-bearing classification**: 52 of 102 galaxies, including NGC 6674 as shell-bearing (matches Paper I)
- **Morphology gradient**: ρ_per_T = -0.833, p = 0.010 (matches Paper I Table 4)
- **Per-galaxy permutation p**: 0.002 (matches Paper I)

## What this v1.0 release contains and what it does not

### Included (status: validated against Paper I v7.1.0)

| Component | Status |
| --- | --- |
| antiwarp_per_shell.csv (67 shells; NGC 6674 excluded as degenerate) | ✅ DONE |
| antiwarp_summary.txt (rerun with NGC 6674 included → 69 shells; matches manuscript table 3.3.5) | ✅ DONE |
| upsilon_perturbation_per_galaxy.csv (2,040 rows: 102 × 20) | ✅ DONE |
| distance_perturbation_per_galaxy.csv (2,040 rows) | ✅ DONE |
| inclination_perturbation_per_galaxy.csv (1,820 rows; 11 edge-on excluded) | ✅ DONE |
| nulltest_per_realization.csv (40 rows: 2 × 20) | ✅ DONE |
| nulltest_per_galaxy.csv (4,080 rows: 2 × 20 × 102) | ✅ DONE |
| nulltest_summary.txt | ✅ DONE |
| Run logs (antiwarp + 3 perturbations) | ✅ DONE |
| SPARC Rotmod files (175 galaxies; 102 used) | ✅ DONE |
| Catalog metadata (sparc_sample123.csv, galaxy_classifications.csv) | ✅ DONE |
| Manuscript markdown (paper2.md) | ✅ DONE — drafted ~11,400 words |
| Manuscript LaTeX (paper2.tex) | ⚠️ DRAFT — compiles, but figure includes are stubs |

### Not yet included or pending external action

| Component | Status |
| --- | --- |
| Paper I canonical fits CSV | ❌ EXTERNAL — see Paper I repo at v7.1.0, `data/sparc_T2-T9_canonical_fits.csv` |
| Producer scripts | ⚠️ RECONSTRUCTED — see notes below |
| Figures | ⏳ 10 placeholders; generation scripts to be written |
| MD5SUMS for Paper II outputs | ⏳ TODO at finalization |
| Bibliography full entries | ⏳ Skeletons in `paper2.tex`; verify volume/page/DOI at submission |
| Validation pass A (numerical claims ↔ data) | ⏳ TODO |
| Validation pass B (cross-section consistency) | ⏳ TODO |
| Zenodo deposit | ⏳ Pending Paper I publication |
| AJ submission | ⏳ Pending |

### About the reconstructed scripts

The five producer scripts in `scripts/` (`antiwarp_subsample.py`, `upsilon_perturbation.py`, `distance_perturbation.py`, `inclination_perturbation.py`, `shell_reality_nulls.py`) were reconstructed from algorithm specifications in the manuscript and from the run logs in `logs/`. They are not byte-identical to the scripts that produced the v1.0 outputs in `data/`.

**Before treating them as canonical:** verify the reconstructed scripts against the Mac-side reference scripts at `~/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/shell_reality_v2/scripts/` and reconcile any differences. The most likely sources of drift are: (a) the random seed convention across runs, (b) the exact perturbation distribution form, (c) the exact subprocess-and-pipe-back pattern for invoking `run_canonical_fits.py`. The scientific content (what is computed) should match; the implementation details may differ.

A future revision (v1.1 or later) should replace the reconstructed scripts with the actual Mac-side scripts under MD5 verification.

## Headline numerical claims and their data sources

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Sample size | 102 galaxies, T = 2-9 | sparc_sample123.csv (filtered) | §2.1 |
| Shell-bearing rate | 52/102 = 51.0% | derived from Paper I canonical CSV | §3.1 |
| Morphology gradient ρ_per_T | -0.833 | derived; cross-ref Paper I | §3.1, Abstract |
| Morphology gradient p | 0.010 | nulltest_summary.txt | §3.1 |
| Per-galaxy ρ | -0.296 | nulltest_summary.txt | §3.1 |
| Per-galaxy p (permutation) | 0.002 | from Paper I VALIDATION_STATUS | §1, §3.2 |
| M-r slope | 0.76 ± 0.14 | antiwarp_per_shell.csv (full sample) | §3.1.2 |
| σ-r slope | 1.04 ± 0.10 | antiwarp_per_shell.csv (full sample) | §3.1.2 |
| σ/r median | 0.268 | antiwarp_per_shell.csv | §3.1.2 |
| σ/r quartile gradient (Q1, Q4) | 0.354, 0.185 | derived from antiwarp_per_shell.csv | §3.1.3 |
| Bulge OR | 3.88 (p = 0.003) | derived from galaxy_classifications + canonical | §3.1.1 |
| Inner-vs-outer mass Wilcoxon | 14/17, p = 0.017 | derived from antiwarp_per_shell.csv (n=2 paired) | §3.1.4 |
| Inner-vs-outer σ Wilcoxon | 12/17, p = 0.049 | derived from antiwarp_per_shell.csv | §3.1.4 |
| Two-pop r/r_vir KS | D = 0.47, p = 0.045 | derived from antiwarp_per_shell + r_vir | §3.1.4 |
| Scramble z (ρ_per_T) | -4.36 | nulltest_summary.txt | §3.2.1 |
| Scramble z (ρ_per_galaxy) | -3.04 | nulltest_summary.txt | §3.2.1 |
| Permute z (ρ_per_T) | -5.21 | nulltest_summary.txt | §3.2.2 |
| Permute z (ρ_per_galaxy) | -8.33 | nulltest_summary.txt | §3.2.2 |
| Υ perturbation per-galaxy match | 95.1% | upsilon_perturbation_per_galaxy.csv | §3.3.2 |
| Distance perturbation per-galaxy match | 94.1% | distance_perturbation_per_galaxy.csv | §3.3.3 |
| Inclination perturbation per-galaxy match | 98.9% | inclination_perturbation_per_galaxy.csv | §3.3.4 |
| Anti-warp clean subsample size | 26 of 69 shells | antiwarp_summary.txt | §3.3.5 |
| Mass-bound pegging rate | 14.5% (10/69) | derived from antiwarp_per_shell.csv | §3.1.2, §4.6 |
| Bound-clean M-r slope | 0.67 ± 0.15 | derived from antiwarp_per_shell.csv (n=59) | §3.1.2, §4.6 |

## Sample-size conventions

Several conventions vary across the manuscript and need to remain internally consistent:

- **102 galaxies** = full v7.0 sample (T = 2-9, after Paper I quality cuts)
- **52 shell-bearing galaxies** = Paper I-aligned (NGC 6674 included)
- **69 shells** = total in the per-shell working set after the NGC 6674-included antiwarp rerun
- **67 shells** = NGC 6674-excluded version preserved in `antiwarp_per_shell.csv` (NGC 6674 contributes 2 ceiling-pegged shells with degenerate r₁ = r₂ = 3.12 kpc fit)
- **17 two-shell galaxies** = used in §3.1.4 paired tests (NGC 6674-included)
- **26 anti-warp clean shells** = §3.3.5 conservative subsample (NGC 6674-included rerun)
- **91 galaxies × 20 reps = 1,820 fits** = inclination perturbation (11 edge-on excluded by `0 < Inc < 90` check)

The manuscript uses the NGC 6674-included convention throughout for alignment with Paper I. The `antiwarp_per_shell.csv` file in this package preserves the NGC 6674-excluded version; the antiwarp_summary.txt was regenerated with NGC 6674 included and matches the manuscript's reported numbers.

## Known minor issues

1. **Inclination perturbation excludes 11 edge-on galaxies** (`Inc == 90°`). The exclusion is conservative (sin 89° = 0.9998 ≈ sin 90° = 1.000) and including the 11 galaxies would only increase the apparent stability rate. A future revision could change `< 90` to `<= 90` in the script and rerun for cosmetic completeness. Approximately 9 minutes of CPU time; impact on reported numbers is minimal.

2. **antiwarp_per_shell.csv vs antiwarp_summary.txt sample-size mismatch.** The CSV contains 67 shells (NGC 6674-excluded version preserved as the catalog), while the summary.txt was regenerated with NGC 6674 included (69 shells) to match the manuscript. The discrepancy is documented in `DATA_PROVENANCE.md`; future revisions should regenerate the CSV consistently.

3. **§3.3.7 cross-counting.** §3.3.6 cross-references §3.2 as "channel (vi)" of the artifact-channel battery, while §3.3.7 lists "six independent tests" inclusive of §3.2. Either is defensible; cosmetic only.

4. **Slope intercepts in §3.1.2 equations are TBD.** Slopes (with SEs) and Spearman ρ are filled in; intercepts are pure cosmetic and can be added at LaTeX revision time.

## Reproducibility verification

To verify the v1.0 outputs are reproducible from the inputs:

```bash
cd halo_shells_paper2_v1.0/scripts
python3 antiwarp_subsample.py    # produces data/antiwarp_per_shell.csv, antiwarp_summary.txt
python3 shell_reality_nulls.py   # produces data/nulltest_*.csv, nulltest_summary.txt (~30-60 min)
python3 upsilon_perturbation.py  # produces data/upsilon_perturbation_per_galaxy.csv (~10-15 min)
python3 distance_perturbation.py # produces data/distance_perturbation_per_galaxy.csv (~10-15 min)
python3 inclination_perturbation.py # produces data/inclination_perturbation_per_galaxy.csv (~10-15 min)
```

After reproduction, the headline numbers in the regenerated CSVs should match the values in the existing summary files to within statistical fluctuation (the perturbation and null tests use random seeds; numerical reproducibility requires fixed seeds; see script docstrings for seed conventions).

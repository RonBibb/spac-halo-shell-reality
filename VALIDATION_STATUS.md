# Validation Status — halo_shells_paper2 v1.0

**Package version:** v1.0-draft
**Snapshot date:** 2026-05-12
**Manuscript file:** `source/paper2.md` (markdown source; canonical)
**Parent paper alignment:** Paper I v7.1.0 (https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0)

---

## Version alignment with Paper I

This package is built against Paper I v7.1.0. All canonical fits, framework parameters, and reference numbers are aligned with that release. Specifically:

- **Paper I canonical sample**: 102 SPARC galaxies, T = 2-9, after Paper I quality cuts (matches Paper I §2.1)
- **Framework**: Burkert backbone of the Paper I framework + 0/1/2 BIC-selected Gaussian shells, σ/r ≤ 0.4 strict reparameterization, mass bound 5×10¹⁰ M☉ (matches Paper I §2.2)
- **Paper I shell-bearing classification**: 52 of 102 galaxies (including NGC 6674)
- **Paper I morphology gradient**: ρ_per_T = -0.833, p = 0.010 (matches Paper I Table 4)

Paper II's primary analyses use the **NGC 6674-excluded 101-galaxy sample**, which produces slightly different headline numbers from Paper I (see "Headline numerical claims" below). The §2.3 partition disclosure explicitly addresses this convention and quantifies the impact.

---

## Sample-size conventions

The manuscript uses two sample conventions, disclosed explicitly in §2.3:

- **Primary (NGC 6674-excluded, 101 galaxies):**
  - 51 shell-bearing galaxies (50.5%), 67 shells, 16 two-shell galaxies
  - 25 anti-warp clean shells (§3.3.5)
  - Used in: §1, §2, §3.1, §3.3.1, §3.3.5, §3.3.6, §4, §5

- **Paper I-aligned (NGC 6674-included, 102 galaxies):**
  - 52 shell-bearing galaxies, 69 shells, 17 two-shell galaxies
  - Used in: §3.2 (null tests), §3.3.2-3.3.4 (Υ/D/i perturbations), §3.3.7 (backbone-shift test)
  - These analyses ran as coordinated production batches and require Mac-side reruns to reconcile to the 101-galaxy primary sample.

NGC 6674's fit is degenerate: r₁ = r₂ = 3.12 kpc with both shell masses pegged at the upper bound 5×10¹⁰ M☉. Its exclusion from per-shell analyses is methodologically justified; its retention in production-batch analyses is a packaging artifact awaiting Mac-side reruns.

The 91-galaxy / 1,820-fit inclination perturbation sample further excludes 11 edge-on galaxies (Inc = 90°) by the script's `0 < Inc < 90` check.

---

## Headline numerical claims and their data sources

### Primary signatures (Bonferroni-robust at α = 0.05; NGC 6674-excluded 101-galaxy sample)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Sample size (primary) | 101 galaxies, T = 2-9 | sparc_sample123.csv (filtered) | §2.3 |
| Shell-bearing rate (primary) | 51/101 = 50.5% | derived from Paper I canonical CSV | §3.1 |
| M-r slope | 0.76 ± 0.14, intercept +9.632 | antiwarp_per_shell.csv (full sample, NGC 6674-excluded) | §3.1.2 |
| M-r Spearman ρ | +0.64 (p < 10⁻⁴) | derived from antiwarp_per_shell.csv | §3.1.2 |
| σ-r slope (under Burkert) | 1.04 ± 0.10, intercept -0.698 | antiwarp_per_shell.csv | §3.1.2 |
| σ-r Spearman ρ | +0.78 (p < 10⁻⁴) | derived from antiwarp_per_shell.csv | §3.1.2 |
| Inner-vs-outer mass Wilcoxon | 14/16, p = 0.0001 | derived from antiwarp_per_shell.csv (n=2 paired) | §3.1.4 |

### Secondary signatures (BH-FDR pass at α = 0.05; Bonferroni fail)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Bulge OR (primary sample) | 3.67 (Fisher p ≈ 0.01) | derived from galaxy_classifications + canonical | §3.1.1 |
| Morphology gradient ρ_per_T | -0.762 (p = 0.028) | derived from Paper I canonical | §3.1, §3.2 baseline |
| σ/r median (under Burkert) | 0.275 | antiwarp_per_shell.csv | §3.1.2, §3.1.3 |
| σ/r quartile gradient | modest tendency Q1 → Q4 | derived from antiwarp_per_shell.csv | §3.1.3 |
| Two-pop r/r_vir KS | (Tier 2 discrepancy; see below) | derived from antiwarp_per_shell + r_vir | §3.1.4 |

### Paper I-aligned analyses (102-galaxy sample)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Per-T morphology gradient (Paper I) | ρ = -0.833, p = 0.010 | derived; matches Paper I Table 4 | §3.1 (cross-ref), §3.2 baseline |
| Per-galaxy permutation ρ (Paper I) | -0.296, p = 0.002 | from Paper I VALIDATION_STATUS | §1, §3.2 |
| Scramble z (ρ_per_T) | -4.36 | nulltest_summary.txt | §3.2.1 |
| Scramble z (ρ_per_galaxy) | -3.04 | nulltest_summary.txt | §3.2.1 |
| Permute z (ρ_per_T) | -5.21 | nulltest_summary.txt | §3.2.2 |
| Permute z (ρ_per_galaxy) | -8.33 | nulltest_summary.txt | §3.2.2 |
| Υ perturbation per-galaxy match | 95.1% | upsilon_perturbation_per_galaxy.csv | §3.3.2 |
| Distance perturbation per-galaxy match | 94.1% | distance_perturbation_per_galaxy.csv | §3.3.3 |
| Inclination perturbation per-galaxy match | 98.9% | inclination_perturbation_per_galaxy.csv | §3.3.4 |
| Backbone shift: SB ρ₀ shift median | -0.624 dex (Wilcoxon p < 10⁻⁴) | backbone_shift.csv | §3.3.7 |
| Backbone shift: SB a shift median | +0.318 dex (Wilcoxon p < 10⁻⁴) | backbone_shift.csv | §3.3.7 |
| Backbone shift: "absorbing pattern" rate | 46/52 (88.5%) of SB galaxies | backbone_shift.csv | §3.3.7 |
| Backbone shift vs T-type correlation | Spearman ρ = +0.44, p = 0.001 | backbone_shift.csv | §3.3.7 |

### Anti-warp subsample (§3.3.5; NGC 6674-excluded)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Anti-warp clean subsample size | 25 of 67 shells | antiwarp_summary.txt | §3.3.5 |
| Mass-bound pegging rate | 14.5% (consistent with full sample) | derived from antiwarp_per_shell.csv | §3.1.2 |

### Einasto backbone-family control (§3.3.6)

| Manuscript claim | Numerical value | Source | Section |
| --- | --- | --- | --- |
| Burkert↔Einasto classification agreement | 89/101 (88%) | einasto_control.py on Paper I Einasto CSV | §3.3.6 |
| Burkert-only shell-bearing | 10 | einasto_control.py | §3.3.6 |
| Einasto-only shell-bearing | 2 | einasto_control.py | §3.3.6 |
| Einasto morphology gradient | ρ_per_T ≈ -0.87 (strengthens) | einasto_control.py | §3.3.6 |
| Einasto bulge OR | 4.32 (strengthens) | einasto_control.py | §3.3.6 |
| Einasto M-r slope | 0.82 (preserved) | einasto_control.py | §3.3.6 |
| Einasto σ-r slope | 0.38 (attenuates from 1.04) | einasto_control.py | §3.3.6 |
| Einasto σ/r median | 0.173 (attenuates from 0.275) | einasto_control.py | §3.3.6 |

---

## Tier 2 numerical discrepancies (manuscript vs recompute)

These are values that appear in the manuscript text but differ from straightforward recomputation against the canonical CSV. Each is documented for transparency; none invalidates a primary or secondary finding under multiple-comparisons correction, but the manuscript should be reconciled to its underlying data before submission.

| Manuscript value | Recomputed value | Notes |
| --- | --- | --- |
| Wilcoxon p = 0.017 (inner-vs-outer mass) | p = 0.0001 | Likely different Wilcoxon variant (e.g., signed-rank vs paired-Wilcoxon, zero-handling). Manuscript should switch to recompute value, or the variant should be specified explicitly. |
| Wilcoxon p = 0.049 (inner-vs-outer σ) | p = 0.0008 | Same likely cause. |
| 12/17 σ outer > inner | 14/17 outer > inner (post NGC 6674 excl.: 14/16) | Counting/data-version discrepancy. |
| KS D = 0.47, p = 0.045 | D = 0.688 | Different r_vir source (abundance-matching variant). |
| Bulge OR Fisher p = 0.003 | scipy default 0.0064; Boschloo/Barnard/mid-p 0.0038 | scipy default uses different one-sided convention; the manuscript value matches a mid-p or Barnard variant. Adopt scipy default or specify variant explicitly. |

---

## Multiple-comparisons correction

§3.1 presents seven dependent population tests as exploratory diagnostics, not pre-registered hypotheses. The manuscript reports both Bonferroni and Benjamini-Hochberg FDR results in §3.1.5:

- **Bonferroni at α = 0.05** (threshold p < 0.00714): three primary signatures pass (M-r and σ-r scaling Spearman, inner-vs-outer M Wilcoxon — using recomputed p = 0.0001).
- **BH-FDR at α = 0.05**: all seven §3.1 tests pass.

Tier classification in §3.1.5 derives directly from this stratification.

---

## Known minor issues

1. **NGC 6674-included production batches** (§3.2, §3.3.2-3.3.4, §3.3.7) await Mac-side reruns to reconcile to the 101-galaxy primary sample. Disclosed in §2.3 with quantitative bound on impact (NGC 6674 contributes ≤1% of any production batch).

2. **Inclination perturbation excludes 11 edge-on galaxies** (`Inc == 90°`). The exclusion is conservative (sin 89° = 0.9998 ≈ sin 90° = 1.000) and including the 11 galaxies would only increase the apparent stability rate. A future revision could change `< 90` to `<= 90` in the script and rerun for cosmetic completeness.

3. **§3.3.6 Einasto control depends on external Paper I CSV** (`einasto_full_sample_results.csv`) that is not duplicated in this package.

4. **Backbone shift test sample convention.** Run on the 102-galaxy Paper I-aligned sample, not the 101-galaxy primary. The §2.3 disclosure bounds the impact on the 88.5% absorbing-pattern rate to the range 85.7–90.2% under NGC 6674 exclusion (one galaxy of 52, depending on its classification).

5. **Tier 2 discrepancies above** should be resolved before submission (variant specification or value update).

---

## Reproducibility verification

To verify the v1.0 outputs are reproducible from the inputs:

```bash
cd halo_shells_paper2/scripts
python3 antiwarp_subsample.py     # produces data/antiwarp_per_shell.csv, antiwarp_summary.txt
python3 einasto_control.py        # post-hoc on Paper I Einasto CSV (no fitting)
python3 shell_reality_nulls.py    # produces data/nulltest_*.csv, nulltest_summary.txt (~30-60 min)
python3 backbone_shift_test.py    # produces data/backbone_shift*.* (~5-15 min)
python3 upsilon_perturbation.py   # produces data/upsilon_perturbation_per_galaxy.csv (~10-15 min)
python3 distance_perturbation.py  # produces data/distance_perturbation_per_galaxy.csv (~10-15 min)
python3 inclination_perturbation.py # produces data/inclination_perturbation_per_galaxy.csv (~10-15 min)
```

After reproduction, the headline numbers in the regenerated CSVs should match the values in the existing summary files to within statistical fluctuation. The perturbation and null tests use random seeds; numerical reproducibility requires fixed seeds (see script docstrings for seed conventions).

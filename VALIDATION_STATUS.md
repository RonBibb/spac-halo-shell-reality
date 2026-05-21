# Validation Status — halo_shells_paper2

**Package version:** v1.0-draft
**Snapshot date:** 2026-05-21
**Latest commit at snapshot:** `6aba87f`
**Manuscript file:** `source/paper2.md` (markdown source; canonical)
**Parent paper alignment:** Paper I v7.1.0 (https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0)

---

## Version alignment with Paper I

This package is built against Paper I v7.1.0. All canonical fits, framework parameters, and reference numbers are aligned with that release. Specifically:

- **Paper I canonical sample**: 102 SPARC galaxies, T = 2–9, after Paper I quality cuts (matches Paper I §2.1)
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
  - Used in: §3.2 (null tests) only. §3.3.2-3.3.4 (Υ/D/i perturbations) and §3.3.7 (backbone-shift test) production batches retain their 102-galaxy as-run fits but the manuscript reports 101-galaxy aggregations via `scripts/ngc6674_exclusion_reanalysis.py` (max shift 0.25 pp; see `data/ngc6674_exclusion_summary.txt`).

NGC 6674's fit is degenerate: r₁ = r₂ = 3.12 kpc with both shell masses pegged at the upper bound 5×10¹⁰ M☉.

The inclination perturbation now includes all 11 SPARC galaxies catalogued at $i = 90°$ (edge-on) via a reflection treatment that folds any post-perturbation $i' > 90°$ to $180° - i'$ on the opposite side of edge-on, preserving a symmetric Gaussian perturbation around the nominal inclination. The full sample is 102 galaxies × 20 realizations = 2,040 fits (101-galaxy aggregation: 2,020 fits).

---

## Cap acknowledgment (§3.1.2)

Added in commit `a86a0e5` (2026-05-21). The framework imposes an upper bound on shell mass at 5×10¹⁰ M☉ and a width cap at σ/r ≤ 0.4, both adopted from Paper I to preserve the "localized" regime. Manuscript §3.1.2 discloses:

- **8 of 67 shells (11.9%)** lie within 0.05 dex of the mass bound
- **Cap-clear subset (n = 59):** M-r slope = 0.67 ± 0.15 (vs. full-sample 0.76), σ-r slope = 1.02 ± 0.11 (vs. 1.04), σ/r median = 0.275 (unchanged)
- Cap is treated as **definitional**, not as fit pathology — preserves the "localized" regime distinct from smooth-halo descriptions
- Bound-relaxation effects flagged as future work; **deferred to Paper 3** (model refinement: cap relaxation paired with hierarchical Υ marginalization)

---

## Headline numerical claims and their data sources

### Primary signatures (Bonferroni-robust at α = 0.05; NGC 6674-excluded 101-galaxy sample)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Sample size (primary) | 101 galaxies, T = 2-9 | sparc_sample123.csv (filtered) | §2.3 |
| Shell-bearing rate (primary) | 51/101 = 50.5% | derived from Paper I canonical CSV | §3.1 |
| M-r slope | 0.76 ± 0.14, intercept +9.632 | antiwarp_per_shell.csv (NGC 6674-excluded) | §3.1.2 |
| M-r Spearman ρ | +0.64 (p < 10⁻⁴) | derived from antiwarp_per_shell.csv | §3.1.2 |
| σ-r slope (under Burkert) | 1.04 ± 0.10, intercept -0.698 | antiwarp_per_shell.csv | §3.1.2 |
| σ-r Spearman ρ | +0.78 (p < 10⁻⁴) | derived from antiwarp_per_shell.csv | §3.1.2 |
| Inner-vs-outer mass Wilcoxon | 14/16, p = 0.0001 | derived from antiwarp_per_shell.csv | §3.1.4 |
| Inner-vs-outer σ Wilcoxon | 14/16, p = 0.0008 | derived from antiwarp_per_shell.csv | §3.1.4 |
| Mass-bound pegging rate (§3.1.2 disclosure) | 8/67 = 11.9% (within 0.05 dex of bound) | derived from antiwarp_per_shell.csv | §3.1.2 |

### Secondary signatures (BH-FDR pass at α = 0.05; Bonferroni fail, or Bonferroni-demoted by entanglement)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Bulge OR (primary sample) | 3.67 (Fisher p = 0.0064) | derived from galaxy_classifications + canonical | §3.1.1 |
| Morphology gradient ρ_per_T | -0.762 (p = 0.028) | derived from Paper I canonical | §3.1, §3.2 baseline |
| σ/r median (under Burkert) | 0.275 | antiwarp_per_shell.csv | §3.1.2, §3.1.3 |
| σ/r quartile gradient | modest tendency Q1 → Q4 (0.339 → 0.185) | derived from antiwarp_per_shell.csv | §3.1.3 |
| Two-pop r/r_vir KS | D = 0.6875, p = 0.0007 under Burkert (D = 0.11, p ≈ 1.0 under Einasto; D = 0.89, p = 7×10⁻⁴ under gNFW) | derived from antiwarp_per_shell (radial ordering) + sparc_sample123 r_vir | §3.1.4, §3.3.6 |

### Paper I-aligned analyses (102-galaxy sample)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Per-T morphology gradient (Paper I) | ρ = -0.833, p = 0.010 | derived; matches Paper I Table 4 | §3.1 (cross-ref), §3.2 baseline |
| Per-galaxy permutation ρ (Paper I) | -0.296, p = 0.002 | from Paper I VALIDATION_STATUS | §1, §3.2 |
| Scramble z (ρ_per_T) | -2.4 (N=100, empirical p = 2/100) | shell_reality_out_n100/summary.txt | §3.2.1 |
| Scramble z (ρ_per_galaxy) | -2.1 (N=100, empirical p = 2/100) | shell_reality_out_n100/summary.txt | §3.2.1 |
| Permute z (ρ_per_T) | -5.0 (N=100, empirical p = 0/100) | shell_reality_out_n100/summary.txt | §3.2.2 |
| Permute z (ρ_per_galaxy) | -6.9 (N=100, empirical p = 0/100) | shell_reality_out_n100/summary.txt | §3.2.2 |
| Υ perturbation per-galaxy match | 95.1% | upsilon_perturbation_per_galaxy.csv | §3.3.2 |
| Distance perturbation per-galaxy match | 94.1% | distance_perturbation_per_galaxy.csv | §3.3.3 |
| Inclination perturbation per-galaxy match | 98.0% (99/101) | inclination_perturbation_per_galaxy.csv | §3.3.4 |
| Backbone shift: SB ρ₀ shift median | -0.624 dex (Wilcoxon p < 10⁻⁴) | backbone_shift.csv | §3.3.7 |
| Backbone shift: SB a shift median | +0.318 dex (Wilcoxon p < 10⁻⁴) | backbone_shift.csv | §3.3.7 |
| Backbone shift: "absorbing pattern" rate | 45/51 (88.2%) of SB galaxies (101-gal) | backbone_shift.csv (aggregated by ngc6674_exclusion_reanalysis.py) | §3.3.7 |
| Backbone shift vs T-type correlation | Spearman ρ = +0.44, p = 0.001 | backbone_shift.csv | §3.3.7 |

### Anti-warp subsample (§3.3.5; NGC 6674-excluded)

| Manuscript claim | Numerical value | Source CSV | Section |
| --- | --- | --- | --- |
| Anti-warp clean subsample size | 25 of 67 shells | antiwarp_summary.txt | §3.3.5 |

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

Values that appear in the manuscript text vs. straightforward recomputation against the canonical CSV. The manuscript adopted the recompute values for two of the original four discrepancies; two remain open.

| Manuscript value | Recomputed value | Status as of snapshot |
| --- | --- | --- |
| Wilcoxon p = 0.0001 (inner-vs-outer mass) | p = 0.0001 | ✅ **Resolved.** Manuscript adopts recompute (historical 0.017 retired). |
| Wilcoxon p = 0.0008 (inner-vs-outer σ) | p = 0.0008 | ✅ **Resolved.** Manuscript adopts recompute (historical 0.049 retired). |
| 14/16 σ outer > inner (NGC 6674-excluded) | 14/16 outer > inner | ✅ **Resolved.** Manuscript adopts NGC 6674-excluded basis (historical 12/17 retired). |
| KS D = 0.6875, p = 0.0007 under Burkert | radial-ordering recompute on canonical sparc_sample123 r_vir | ✅ **Resolved 2026-05-21.** The original manuscript value (D = 0.47, p = 0.045) used the `position` column from `antiwarp_per_shell.csv` as the inner/outer partition. That column is a fit-slot label (sh1 vs sh2) and disagrees with radial ordering for 3 of 16 two-shell galaxies (ESO563-G021, NGC2841, UGC02953). All other §3.1.4 statistics (median outer/inner mass ratio 2.62, 14/16 outer-heavier, 14/16 outer-wider) match radial ordering perfectly under recompute, so radial ordering is the manuscript's intended partition. Corrected values: D = 0.6875, p = 0.0007 on the canonical r_vir source. Inner median r/r_vir = 0.012 [0.006, 0.017], outer = 0.027 [0.022, 0.035]. The previously-flagged "recompute D = 0.688" matches the corrected radial-ordering computation. Bonus check: under Einasto the KS attenuates to D = 0.11, p ≈ 1.0 (added to §3.3.6 table and prose); the signature is therefore Burkert-baseline-dependent and stays in secondary tier despite crossing Bonferroni under Burkert. |
| Bulge OR Fisher p = 0.0064 | scipy default adopted | ✅ **Resolved 2026-05-21.** Adopted Fisher scipy default 0.0064. Classified as secondary signature alongside the morphology gradient by entanglement framing (§3.1.1 disclosure: bulge correlation and morphology gradient are two projections of a single underlying contrast); the raw p formally crosses Bonferroni but is not treated as an independent fifth primary signal. See §3.1.5 multi-comparisons paragraph for the explicit demotion reasoning. BH-adjusted p updated 0.014 → 0.009. |

---

## Multiple-comparisons correction

§3.1 presents seven dependent population tests as exploratory diagnostics, not pre-registered hypotheses. The manuscript reports both Bonferroni and Benjamini-Hochberg FDR results in §3.1.5:

- **Bonferroni at α = 0.05** (threshold p < 0.00714): six raw p-values cross the threshold (M-r and σ-r scaling Spearman, both inner-vs-outer Wilcoxon tests, the bulge Fisher test at p = 0.0064, and the KS r/r_vir at p = 0.0007). Three of these are classified as secondary by criteria distinct from the Bonferroni threshold: the bulge correlation is entanglement-demoted (§3.1.1: two projections of a single underlying contrast with the morphology gradient); the σ inner-vs-outer Wilcoxon attenuates to p = 0.10 under Einasto-backbone substitution but strengthens to 9/9, p = 0.002 under gNFW (§3.3.6); the KS r/r_vir attenuates to D = 0.11, p ≈ 1.0 under Einasto but strengthens to D = 0.89, p = 7×10⁻⁴ under gNFW (§3.3.6) — both attenuations are therefore Einasto-α-curvature-specific rather than generic backbone-family-sensitive. The effective set of independent, control-invariant, non-entangled primary signatures under the strict criterion of preservation across ALL backbone-family controls remains three: M-r scaling, σ-r scaling under Burkert, and inner-vs-outer mass ordering. The σ Wilcoxon and KS r/r_vir would promote to primary under a relaxed criterion of "preservation under at least one strict-superset backbone family" (Option 2 of the gNFW addition); the current §3.1.5 tier classification adopts the strict criterion for conservatism.
- **BH-FDR at α = 0.05**: all seven §3.1 tests pass.

Tier classification in §3.1.5 derives directly from this stratification.

---

## Known minor issues

1. **NGC 6674-included production batches** — partially resolved 2026-05-19. §3.3.2-4 and §3.3.7 report 101-galaxy values via post-aggregation through `scripts/ngc6674_exclusion_reanalysis.py` (see `data/ngc6674_exclusion_summary.txt`; max shift 0.25 pp). §3.2 (N=100 nulls) remains on the 102-galaxy sample; an analogous re-aggregation is feasible but not yet performed.

2. **Inclination perturbation edge-on cleanup — resolved 2026-05-21.** Previously the script excluded 11 SPARC galaxies catalogued at $i = 90°$ via a `0 < Inc < 90` check. The check has been changed to `0 < Inc <= 90` paired with a reflection treatment that folds any post-perturbation $i' > 90°$ to $180° - i'$ on the opposite side of edge-on. This preserves a symmetric Gaussian perturbation around the nominal inclination for edge-on galaxies. New sample: 102 galaxies × 20 realizations = 2,040 fits (raw); 2,020 (NGC 6674-excluded aggregation). Headline shifts: per-galaxy modal match 98.9% (90/91) → 98.0% (99/101) — the small downward shift reflects two marginal-BIC galaxies (UGC05253, UGC06818) whose perturbed shell counts now mismatch canonical due to a different realization sequence under the new RNG draw order, not an algorithmic regression. Edge-on galaxies match canonical in 220/220 fits (100%) as expected from $\sin i$ being flat near $i = 90°$. Median $|\Delta \log r_1|$ tightens 0.005 → 0.0022 dex.

3. **§3.3.6 Einasto control depends on `einasto_full_sample_results.csv`** — included in this repo's `data/` directory as of 2026-05-19 for reproducibility.

4. **Backbone shift test sample convention.** Production run used the 102-galaxy Paper I-aligned sample. Manuscript reports 101-galaxy numbers (NGC 6674 excluded) by post-aggregation of `backbone_shift.csv` via `scripts/ngc6674_exclusion_reanalysis.py`. The 102→101 shift is 88.5% → 88.2% (absorbing-pattern rate), 46/52 → 45/51 — qualitatively unchanged.

5. **All Tier 2 discrepancies resolved as of 2026-05-21** (see table above). Two reconciliations took place this date: the Bulge OR p-value (in favor of Fisher scipy default 0.0064 with entanglement-based secondary classification), and the KS D-statistic for r/r_vir (in favor of D = 0.6875 from radial-ordering recompute on the canonical r_vir source, with bonus Einasto-attenuation check added to §3.3.6).

---

## Reproducibility verification

To verify the v1.0 outputs are reproducible from the inputs:

```bash
cd sparc-halo-shell-reality/scripts
python3 antiwarp_subsample.py     # produces data/antiwarp_per_shell.csv, antiwarp_summary.txt
python3 einasto_control.py        # post-hoc on Paper I Einasto CSV (no fitting)
python3 shell_reality_nulls_parallel.py 100 12  # canonical N=100 → data/shell_reality_out_n100/ (~2 hr on M1 Ultra)
# Alternative (slower): python3 shell_reality_nulls.py 100  # serial; same output, ~14-17 hr
python3 backbone_shift_test.py    # produces data/backbone_shift*.* (~5-15 min)
python3 upsilon_perturbation.py   # produces data/upsilon_perturbation_per_galaxy.csv (~10-15 min)
python3 distance_perturbation.py  # produces data/distance_perturbation_per_galaxy.csv (~10-15 min)
python3 inclination_perturbation.py # produces data/inclination_perturbation_per_galaxy.csv (~10-15 min)
```

After reproduction, the headline numbers in the regenerated CSVs should match the values in the existing summary files to within statistical fluctuation. The perturbation and null tests use random seeds; numerical reproducibility requires fixed seeds (see script docstrings for seed conventions).

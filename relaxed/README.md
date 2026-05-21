# Cap-Relaxation Sweep — README

**Directory:** `paper2_package/relaxed/`
**Created:** 2026-05-20
**Status:** Complete; strategic decision pending on home for results.

---

## Purpose

This directory contains a population-wide cap-relaxation sweep of the
102-galaxy SPARC T=2-9 sample, motivated by the discovery that several
canonical-pipeline architectural caps were materially binding on the
shell-fitting optimizer. The sweep was triggered by single-galaxy
investigations on NGC 5371 (σ/r-pegged) and NGC 6674 (M-pegged) showing
that the universal-failure designation was at least partially cap-dependent.

The driving question: **what fraction of Paper 1's empirical results are
artifacts of the canonical cap values vs cap-independent physical findings?**

---

## What was changed

Three architectural caps were relaxed simultaneously in
`run_relaxed_caps_fits.py` (minimal diff from `run_canonical_fits.py`):

| Constraint    | Canonical              | Relaxed                |
|---------------|------------------------|------------------------|
| `SHELL_M_MAX` | 5×10¹⁰ M☉              | 1×10¹² M☉              |
| `SHELL_WIDTH_MAX_FRAC` | 0.4           | 0.8                    |
| `SHELL_R_MAX_GRID`     | [3, 6, 12] kpc | [12, 30, 80] kpc       |

**Everything else is byte-identical** to the canonical pipeline:
Υ_disk = 0.5, Υ_bulge = 0.7, σ_V floor = 1.0 km/s, exclusion rule
V_obs² > V_bar², BIC selection over n_shells ∈ {0, 1, 2}, multi-restart
structure, baryon decomposition, χ² and BIC formulas.

The output CSV has the same schema as the canonical CSV so they can be
joined on `Galaxy` for direct comparison.

---

## Files in this directory

```
relaxed/
├── README.md                              (this file)
├── run_relaxed_caps_fits.py               (the modified pipeline)
├── sparc_T2-T9_relaxed_caps_fits.csv      (102 rows × 43 cols, output)
├── run_relaxed_caps_fits.log              (per-galaxy fit log)
├── cap_comparison_summary.csv             (102 rows, joined comparison)
└── cap_relaxation_overview.png            (4-panel summary figure)
```

---

## Headline results

### Adequacy improvement (χ²_red < 1.5)

- Canonical: 91/102 adequate (89.2%)
- Relaxed:   97/102 adequate (95.1%)
- Net gain:  +6 galaxies (no regressions; adequacy monotonic under relaxation)

### Six rescues — all but one are Paper 1 UF galaxies

| Galaxy   | T | Canonical χ²_red | Relaxed χ²_red | Paper 1 UF? |
|----------|---|------------------|----------------|-------------|
| NGC 6674 | 3 | 13.25            | 0.74           | yes (excluded from 101-sample) |
| NGC 5907 | 5 |  4.21            | 1.17           | yes |
| NGC 5033 | 5 |  2.47            | 1.48           | yes (borderline pass — see caveats) |
| NGC 2841 | 3 |  2.43            | 0.33           | yes |
| NGC 5985 | 3 |  2.26            | 0.38           | yes |
| NGC 0289 | 4 |  1.65            | 0.90           | yes |

### Five still failing under relaxed caps

| Galaxy    | T | Canonical χ²_red | Relaxed χ²_red | NFW χ²_red |
|-----------|---|------------------|----------------|------------|
| NGC 5585  | 7 | 3.68             | 3.67           | 7.08       |
| UGC 06787 | 2 | 6.73             | 2.70           | 28.18      |
| UGC 02953 | 2 | 2.22             | 1.95           | 5.74       |
| UGC 09133 | 2 | 4.82             | 1.85           | 8.51       |
| UGC 00128 | 8 | 2.71             | 1.68           | 2.52       |

All four UF galaxies in this list (UGC 06787, UGC 02953, UGC 09133,
UGC 00128) also have poor NFW fits, consistent with a halo-shape mismatch
that no cap relaxation can paper over. NGC 5585 sits outside the UF list
but arguably should have been on it.

### Universal-failure category, qualified

Of Paper 1 Table 7's 10 universal-failure galaxies:

- **6 are cap-artifacts** (rescued by modest cap relaxation): NGC 6674,
  NGC 5907, NGC 5033, NGC 2841, NGC 5985, NGC 0289.
- **4 are genuine framework limitations** (resist relaxation, NFW also
  poor): UGC 06787, UGC 02953, UGC 09133, UGC 00128.

### Shell-count transition matrix (canonical → relaxed)

```
         relaxed n=0  n=1  n=2
canonical n=0:   48    1    1
canonical n=1:    1   29    5
canonical n=2:    0    5   12
```

- 89 galaxies stable in n_shells (87%)
- 5 cases 2→1 (potential cap-artifact splits — but see caveats below)
- 5 cases 1→2 (relaxed bounds discovered a second feature)
- 4 misc transitions

### Cap-binding fractions

| Cap type    | Canonical fits | Relaxed fits |
|-------------|----------------|--------------|
| M-pegged    | 9/69 (13.0%)   | 2/71 (2.8%)  |
| σ/r-pegged  | 13/69 (18.8%)  | 0/71 (0.0%)  |
| r-pegged    | 4/69 (5.8%)    | 1/71 (1.4%)  |

The σ/r ≤ 0.4 cap was the most disproportionately binding (19% of shells).
The relaxed σ/r ≤ 0.8 cap binds nowhere — the new limit is wide enough that
no shell finds it.

Two galaxies still hit the relaxed M-cap of 10¹² (NGC 5371, UGC 02885),
both with shells near 60-64 kpc. These appear to want even more mass.

### Morphology gradient — Paper 1 headline result is robust

Binary SB classification migrates for only 3/102 galaxies. Per-T-bin
Spearman ρ goes from −0.833 (p = 0.010) canonical to **−0.886 (p = 0.003)
relaxed**. The morphology gradient *strengthens* under relaxation.

---

## Critical methodological caveat

The five 2→1 "collapses" are **NOT** clean mass-preserving consolidations.
In three of five cases the production fitter places the single relaxed
shell at radii beyond the original data range with mass 4-30× the
canonical two-shell sum:

| Galaxy    | Canon (n=2) total M | Relaxed (n=1) | Mass ratio | Center shift |
|-----------|---------------------|---------------|------------|--------------|
| NGC 3198  | r̄=8.2,  M=3.7e10   | r=80, M=6.8e11 | 18×       | +72 kpc      |
| NGC 5371  | r̄=4.5,  M=3.4e10   | r=62.6, M=1e12 [M-cap] | 30× | +58 kpc |
| NGC 6674  | r̄=3.1,  M=1.0e11   | r=58.5, M=4.3e11 | 4×      | +55 kpc      |
| UGC 11455 | r̄=7.8,  M=3.4e10   | r=12.2, M=1.2e11 | 4×      | +4 kpc       |
| UGC 11914 | r̄=7.2,  M=5.8e10   | r=11.3, M=2.9e11 | 5×      | +4 kpc       |

A separate single-galaxy investigation on NGC 5371 (using a different
multi-restart grid) found a different local minimum at r = 4.25 kpc,
M = 3.35×10¹⁰ (mass-preserving), σ/r = 0.789, χ²_red = 1.11. Both are
valid local minima with similar χ² values.

**Implication for the IMBH peri/apo interpretation:** rotation-curve
fitting under wide bounds cannot cleanly distinguish "two real features"
from "one wide feature" from "one off-data-range mass concentration." The
canonical caps were doing real work in keeping the optimization
well-posed. Lifting them does not reveal the true underlying shell
structure — it reveals that the data underdetermines the structure once
the bounds are wide.

The "two-shells-were-really-one" pattern observed in the single-galaxy
session work is one possible reading; the production-fitter "two shells
collapse to a large-r large-M outer feature" pattern is another. Both
deserve treatment in any future paper analyzing this question.

---

## Open questions for follow-up

1. **Which local minimum is physically preferred?** Need a principled
   criterion beyond χ². Options: priors on M_sh from independent estimators
   (M-σ relation if applicable), priors on r_sh from baryon-distribution
   correlation, or requiring shells to lie within the data range.

2. **Are the 4 genuine-failure galaxies (UGC 06787 etc.) telling us about
   limitations of the Burkert backbone family?** All four have poor NFW
   fits too, suggesting the issue is not the framework architecture but
   the smooth halo profile choice. Einasto or DC14 might do better — worth
   testing on this subset specifically.

3. **Does the multi-local-minimum problem affect the 1→2 splits the same
   way?** Particularly NGC 5055 (canonical morphology showcase) went 1→2
   under relaxation with χ²_red 1.46 → 0.53. Worth a single-galaxy
   focused analysis like the NGC 5371 and NGC 6674 work.

4. **For Paper 1 universal-failure framing:** if 6 of 10 UF galaxies are
   cap-artifacts, the §4.1 language ("require architectural complexity
   beyond the framework") needs qualification. Decision on whether to
   volunteer this disclosure before referee review or wait for it to be
   raised.

---

## Pending strategic decision

Three pathways under consideration; decision deferred:

**A. Paper 1 revision-time disclosure (low effort).** One-paragraph
addition to §4.1 noting that 6 of 10 UF galaxies achieve adequacy under
modest cap relaxation. Reframes UF category as "fails-at-canonical-priors"
rather than "architecturally inadequate." Preserves the morphology
gradient finding. ~1-2 hours.

**B. Future paper on cap sensitivity and shell structure (medium effort).**
Use this sweep as the seed for a focused methodological paper. Topics:
what the rotation curve data determines about shell structure, which UF
designations are cap-artifacts vs genuine limitations, the multi-local-
minimum problem under wide bounds. Could be Paper 3 or Paper 4 in the
series. ~1-3 months.

**C. Architectural revision of the framework (high effort).** Replace
hard cap values with physically-motivated priors or information-criterion
penalties. Propagates through all in-flight and future work.

---

## Provenance

- Run executed: 2026-05-20 on Ron Bibb's Mac Studio M1 Ultra
- Software state: identical to canonical pipeline except for three cap
  constants (see `run_relaxed_caps_fits.py` lines marked `>>> CHANGED`)
- Sample: 102 galaxies, SPARC T=2-9, full canonical sample (NGC 6674
  included, in contrast to the 101-galaxy Paper 2 convention)
- Sanity checks passed: Burkert χ²_red identical between canonical and
  relaxed CSVs (confirms only the FW shell fitter changed); NGC 5371 and
  NGC 6674 reproductions from single-galaxy session work match production
  results within ~1%

---

## How to reproduce

```bash
cd paper2_package/relaxed/
# Verify Rotmod_LTG/ symlink or directory exists in ../  or ./
# Verify sparc_sample123.csv exists in ../data/ or ./
python3 run_relaxed_caps_fits.py
```

Output: `sparc_T2-T9_relaxed_caps_fits.csv` + `run_relaxed_caps_fits.log`.
Expected runtime: ~15-20 minutes on Apple Silicon, ~30-90 minutes on Intel.

For the comparison summary, join the canonical CSV from
`paper2_package/` and the relaxed CSV from `paper2_package/relaxed/` on
`Galaxy`. The session script that produced `cap_comparison_summary.csv`
and `cap_relaxation_overview.png` is straightforward to reconstruct from
this README's headline-results section.

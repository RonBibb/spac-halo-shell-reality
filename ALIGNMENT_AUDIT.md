# Paper I (v7.1.0) ↔ Paper II Alignment Audit

**Audit date:** 2026-05-21
**Auditor basis:** Direct review of `source/paper2.md` at commit `6aba87f` against Paper I v7.1.0 (PASP-102415).
**Status:** Current. Supersedes 2026-05-09 audit, which was conducted from web-fetched summary materials only (the original `.tex` was not directly accessible at that time).

---

## Summary

Direct manuscript review finds Paper II aligned with Paper I v7.1.0 across all material claims. Seven specific touchpoints were checked; all are resolved or under explicit management. No critical alignment issues remain.

| Touchpoint | Status |
| --- | --- |
| 1. NGC 6674 inclusion convention | ✅ Resolved (explicit §2.3 partition) |
| 2. Morphology gradient attribution | ✅ Resolved (Paper I cited as established context) |
| 3. Backbone-family robustness | ✅ Aligned (Einasto reused; backbone-shift novel) |
| 4. Null-test framing | ✅ Aligned (distinguished from Paper I's nulls) |
| 5. T=8 wobble comment | ✅ Removed |
| 6. Framework adequacy reference | ✅ Aligned (Paper I cited for 91/102 result) |
| 7. P2-novel content delineation | ✅ Clean (scaling relations, σ/r, bulge correlation, perturbation tests, anti-warp clean, spatial-coherence nulls, backbone-shift) |

---

## Resolved touchpoints

### 1. NGC 6674 inclusion convention

**Paper I (v7.1.0):** Includes NGC 6674. Headline ρ_per_T = -0.833 with NGC 6674 included.

**Paper II resolution:** §2.3 ("Sample partitions used in §3") explicitly discloses two conventions:
- Primary (NGC 6674-excluded, 101 galaxies) for §1, §2, §3.1, §3.3.1, §3.3.5, §3.3.6, §4, §5
- Paper I-aligned (NGC 6674-included, 102 galaxies) for §3.2 only

§3.3.2-4 and §3.3.7 production batches retain 102-galaxy as-run fits but the manuscript reports 101-galaxy aggregations via `scripts/ngc6674_exclusion_reanalysis.py` (max shift 0.25 pp; see `data/ngc6674_exclusion_summary.txt`). NGC 6674's degenerate two-shell fit (r₁ = r₂ = 3.12 kpc, both masses pegged at the upper bound) provides explicit methodological grounds for exclusion from per-shell analyses.

§3.1.5 discloses inline that Paper I's p = 0.010 → Paper II's p = 0.028 on the morphology gradient reflects single-galaxy removal alone. No hidden inconsistency.

### 2. Morphology gradient attribution

**Paper I claim:** Per-T-bin Spearman ρ = -0.83, p = 0.010; per-galaxy permutation p = 0.002; Mann-Kendall p = 0.003.

**Paper II resolution:** §1 introduction explicitly attributes the morphology gradient to Paper I: "...demonstrated a galaxy-level morphology gradient in shell-bearing fraction across T = 2–9 (per-galaxy permutation p = 0.002, per-bin Spearman ρ = -0.83, p = 0.010)" (paper2.md line 32, abstract; line 50, §1).

§3.1.1 in Paper II is the *bulge correlation* section, not the morphology gradient. Paper II's morphology gradient mentions (in §3.1.5 secondary signatures table) explicitly reference Paper I and note the NGC 6674-excluded version (ρ_per_T = -0.762, p = 0.028) as a recomputation under the primary convention, not as a new finding.

### 3. Backbone-family robustness

**Paper I result:** Burkert ↔ Einasto backbone-invariance demonstrated on the full 102-galaxy sample; 90/102 (88%) classification agreement; gradient survives.

**Paper II's relationship to this:**
- §3.3.6 re-uses Paper I's Einasto fits (via `einasto_full_sample_results.csv`) but operates at the **per-shell level**, examining whether the scaling-relation signatures and bulge correlation survive the backbone substitution. This is post-hoc analysis on existing Paper I fits — not a new full-sample backbone run.
- §3.3.7 is novel to Paper II: the backbone-shift test asks whether the smooth Burkert profile can natively absorb the localized structure if shells are disallowed. This is dynamically coupled but distinct from Paper I's backbone-family robustness.

Neither §3.3.6 nor §3.3.7 contradicts or duplicates Paper I; they extend it.

A gNFW backbone test (third profile family) is listed as optional in `STATUS.md` ("not required for submission but strengthens the backbone-family robustness argument"). Discussion in §4 currently mentions backbone-family invariance via Paper I's Einasto comparison and §3.3.7's backbone-shift result; no gNFW claim is made in the present draft.

### 4. Null-test framing

**Paper I's nulls:**
- 346 synthetic mocks: Burkert-truth (FP rate 4.0%) and NFW-truth (FP rate 63.6%)
- Per-galaxy T-label permutation: p = 0.002

**Paper II's nulls (§3.2):**
- Within-galaxy residual scrambling (100 realizations × 102 galaxies)
- Cross-radius V_obs permutation (100 realizations × 102 galaxies)
- Headline: empirical p = 2/100 scramble, 0/100 permute (asymmetric failure modes)

Paper II §3.2.1's opening text explicitly distinguishes its tests from Paper I's: "...complementing the synthetic-mock nulls reported in Paper I §3.5." The spatial-coherence question Paper II addresses (do shells require structured residuals within a galaxy?) is orthogonal to Paper I's FP-rate-and-T-permutation question (does the framework fabricate shells in genuinely smooth data, and does the gradient arise from T-label coincidence?). No redundancy.

### 5. T=8 wobble comment

Paper I v7.0 deleted the T=8 wobble discussion because "T=8 at 33% is on-trend in v7.0."

**Paper II resolution:** No T=8 wobble comment appears in §3.1.1 or §3.1.5 of paper2.md. The only T=8 mention is at §3.2.3 line 317 ("...except T=8 where the real fraction is 0.92× the scramble null due to small-bin statistics"), which is a small-sample-size disclaimer in the context of the per-T null comparison, not a substantive wobble claim. Consistent with Paper I's v7.0 retirement.

### 6. Framework adequacy reference

**Paper I claim:** 91/102 framework adequacy under BIC at χ²_red < 1.5; 65/102 Burkert-only; 52/102 free-c NFW.

**Paper II treatment:** §1 line 50: "It established that Bayesian model selection adequately fits 91/102 SPARC galaxies under the framework versus 65/102 under Burkert-only and 52/102 under free-concentration NFW." Cited as Paper I context, not claimed as a Paper II result. Aligned.

### 7. P2-novel content delineation

Clean differentiator between the two papers. Paper II's novel content over Paper I:

**Per-shell scaling relations (§3.1.2):**
- M ∝ r^0.76 (ρ = +0.64, p < 10⁻⁴)
- σ ∝ r^1.04 under Burkert backbone (ρ = +0.78, p < 10⁻⁴)
- σ/r ≈ 0.275 characteristic fractional width

**Mass-bound cap acknowledgment (§3.1.2, added 2026-05-21):**
- 8/67 shells within 0.05 dex of the 5×10¹⁰ M☉ mass bound
- Cap-clear subset gives essentially unchanged slopes
- Cap framed as definitional; bound-relaxation deferred to Paper 3

**Population organization (§3.1.1, 3.1.3, 3.1.4, 3.1.5):**
- Bulge correlation (OR = 3.67) with explicit morphology-entanglement disclosure
- σ/r quartile gradient (0.339 → 0.185)
- Inner-vs-outer mass and width ordering in two-shell galaxies (14/16, p = 0.0001 and 0.0008)
- Two-population separation in r/r_vir
- Multiple-comparisons-corrected tier classification

**Artifact robustness (§3.3):**
- Coincidence with disk dynamical scales (§3.3.1)
- Υ, distance, inclination perturbation tests (§3.3.2-4)
- Anti-warp clean subsample (§3.3.5)
- Backbone-shift test (§3.3.7) — novel, not in Paper I

**Spatial-coherence nulls (§3.2):**
- Within-galaxy residual scrambling (§3.2.1)
- Cross-radius V_obs permutation (§3.2.2)
- Per-T fractions comparison (§3.2.3)

None of the above appears in Paper I. Paper II's contribution is well-delineated.

---

## What was *not* in this audit

- The Tier 2 numerical discrepancies (two open as of snapshot — KS D and Bulge OR p) are tracked in `VALIDATION_STATUS.md`, not here. Those are manuscript-vs-recompute reconciliations within Paper II, not Paper I ↔ Paper II alignment issues.

- Paper I's PASP-102415 referee response, when it arrives, may necessitate Paper II text changes (citation updates, possibly methodology refinements). Re-audit at that point.

---

## Notes on the 2026-05-09 audit

The earlier version of this document was authored from web-fetched README and VALIDATION_STATUS materials without direct access to Paper I's manuscript .tex or to a complete Paper II draft. It flagged seven issues and recommended including NGC 6674 globally in Paper II. The recommendation was not adopted; Paper II went the other direction (NGC 6674 excluded from primary analyses with explicit §2.3 partition disclosure). The remaining six issues from that audit have all been resolved through manuscript revisions during the 2026-05-19 and 2026-05-21 commit batches.

The 2026-05-09 audit document is superseded by this one.

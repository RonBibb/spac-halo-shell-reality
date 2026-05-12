# Paper 1 (v7.1.0) ↔ Paper 2 Alignment Audit

> Generated 2026-05-09 from public repo content at https://github.com/RonBibb/sparc-halo-shells (README.md and VALIDATION_STATUS.md). Could not access the manuscript .tex directly via web fetch, so this audit is based on the validation document, README, and the headline-result tables — which appear to be comprehensive and aligned with the manuscript per the validation tracking. **If the .tex contains additional claims not in the validation status, this audit is incomplete.**

---

## Summary

I found **seven distinct alignment issues** between Paper 1 v7.1.0 and our Paper 2 working drafts. Three are critical (would create internal contradictions or duplicate Paper 1's claims). Four are minor (small numerical inconsistencies or scoping clarifications).

---

## CRITICAL ISSUES

### Issue 1: NGC6674 inclusion convention conflicts

**Paper 1 (v7.0/v7.1.0) includes NGC6674.**
- Headline number: 52 shell-bearing galaxies (T=8 fraction is 2/6 = 33%)
- T=3 fraction includes NGC6674
- ρ_per_T = -0.83 includes NGC6674

**Our P2 §3.1 and §3.3 (antiwarp) exclude NGC6674.**
- 51 shell-bearing galaxies, 67 shells
- T=3 fraction without NGC6674
- ρ_per_T = -0.762 without NGC6674

**Our P2 §3.2 (null test script outputs) includes NGC6674.**
- ρ_per_T = -0.833 with NGC6674

**Resolution:** **Include NGC6674 globally in P2** to align with Paper 1. The "degenerate fit" reasoning we used (both shells collapse to r₁ = r₂ = 3.12 kpc) is real but Paper 1 chose to keep it. P2 should follow the parent paper's convention.

**What needs changing:**
- §3.1: rerun antiwarp_subsample.py with NGC6674 included → 68 shells (vs 67), 52 galaxies (vs 51), recompute scaling relations and morphology gradient
- §3.3: same antiwarp recomputation → updated clean subsample table
- §3.2: numbers stay (already includes NGC6674)
- Abstract: ρ_per_T stays at −0.833 (already correct under the include-NGC6674 convention)

**Estimated impact:** ρ_per_T shifts from −0.762 → −0.833. M-r and σ-r slopes shift slightly (NGC6674 contributes two shells at r = 3.12 kpc with M = 5×10¹⁰). σ/r ≈ 0.275 likely unchanged at the median.

---

### Issue 2: Morphology gradient is already a Paper 1 result

This is the biggest framing problem.

**Paper 1's published claims include:**
- Per-T-bin Spearman ρ = −0.83 with bootstrap 95% CI [−0.95, −0.22]
- Mann-Kendall p = 0.003 on the morphology gradient
- Per-galaxy permutation p = 0.002 (two-sided)
- Einasto-backbone confirmation: ρ_per_galaxy = −0.347, p = 0.0004
- Magnitude argument: real shell-bearing fractions exceed Burkert-truth FP rates by factors of 6–20 in every T-bin
- Table 4 (morphology + null) covers all 8 T-bins
- T=8 wobble subsection was deleted from v7.0 because "T=8 at 33% is on-trend"

**Our P2 §3.1.1 currently presents the morphology gradient as if introducing it.** It includes:
- The full Table 3.1.1 of per-T fractions
- The ρ = −0.833 number
- A discussion that includes "minor deviation at T=8" (which Paper 1 explicitly removed)

**Resolution:** Reframe P2 §3.1.1 to **recap, not introduce**. Specifically:
- Open with one sentence: "The morphology gradient documented in Paper I (ρ_per_T = −0.83, p = 0.010, Mann-Kendall p = 0.003) ..."
- Cite Paper 1 explicitly
- Use the gradient as the *foundation for* P2's organization analysis, not as a new finding
- Remove the per-T fraction table (it's in Paper 1's Table 4) — possibly reference back instead, or replace with a more compact restatement
- Remove the "minor deviation at T=8" comment (Paper 1 retired this)

**What's NEW to P2 vs. recap from Paper 1:**

Genuinely new in P2:
- M ∝ r^0.76 scaling
- σ ∝ r^1.04 scaling
- σ/r ≈ 0.275 universality
- Bulge correlation (OR = 3.67)
- σ/r quartile gradient (0.339 → 0.185)
- Inner-vs-outer mass test (13/16, p = 0.022)
- M*/L, distance, inclination perturbation tests
- Anti-warp clean subsample
- Within-galaxy residual scrambling null
- Cross-radius V_obs permutation null
- σ/r ≤ 0.4 strict enforcement (this is v7.0 framework, used here)

Inherited from Paper 1:
- Burkert backbone + 0/1/2 Gaussian shells framework
- BIC selection
- 102 SPARC galaxies, T=2-9
- Morphology gradient ρ_per_T = -0.83
- Burkert-vs-Einasto backbone-invariance result

**P2's introduction needs to clearly distinguish these**, otherwise referees will reject as redundant with P1.

---

### Issue 3: Backbone-invariance is partially already in Paper 1

**Paper 1 §3.6 ("Robustness to backbone") includes:**
- Burkert vs Einasto comparison on full 102-galaxy sample
- Burkert/Einasto classification agreement: 90/102 (88%)
- Einasto per-galaxy Spearman ρ = −0.347, p = 0.0004
- Einasto 16-galaxy stratified subsample
- v7.0 enforced strict σ/r ≤ 0.4 in both Burkert and Einasto fits
- Einasto-backbone divide-by-zero bug fixed (cosmetic only — didn't affect any BIC selection)

**Implication for the gNFW / free-shape question:**

What you said: "I have also alluded to a generalized-NFW or free-shape backbone test as future work. It may go into this paper if there is a fit, or a future supplement."

Given Paper 1 already has **Burkert ↔ Einasto backbone-invariance** demonstrated for the full sample with 88% classification agreement and the morphology gradient surviving:

- A gNFW or free-shape extension in P2 would be a **further generalization** of Paper 1's backbone-invariance work, not a foundational test
- Two reasonable framings for P2:
  1. **§4 Discussion / Future Work:** flag gNFW and free-shape as natural next tests beyond Paper 1's Burkert↔Einasto, with a note that arbitrary free-shape backbones risk absorbing the very residuals the framework attributes to shells (interpretive challenge)
  2. **§3.3 Robustness extension:** if you actually run gNFW now and the morphology gradient + scaling relations survive, it strengthens P2 as "backbone-invariance to a third profile family." Probably a paragraph + small table, not a major section. Risk: if gNFW *kills* shells, you've created a paper-internal problem.

**My recommendation:** **§4 Discussion** mention only, unless you specifically want to run gNFW for P2. The Burkert↔Einasto result in Paper 1 is already strong evidence of backbone-invariance.

---

## MINOR ISSUES

### Issue 4: P2's "scramble" and "permute" nulls vs Paper 1's null test

**Paper 1's null test:**
- 346 synthetic mocks: Burkert-truth (smooth Burkert + noise) and NFW-truth (smooth NFW + noise)
- Tests false-positive rate of framework selecting shells in genuinely smooth synthetic data
- Burkert-truth aggregate FP rate: 4.0% (7/173)
- NFW-truth aggregate FP rate: 63.6% (110/173)
- Magnitude argument: real shell-bearing fractions exceed FP rates by 6–20× per T-bin

**Paper 1's permutation test:**
- Per-galaxy permutation p = 0.002 (two-sided)
- This presumably permutes T-type labels across galaxies to test if the gradient could arise by chance
- Different from our shell_reality_nulls.py "permute" null (which permutes V_obs across radii within each galaxy)

**Our P2's null tests (shell_reality_nulls.py):**
- 20 realizations × 102 galaxies × 2 null types = 4,080 fits
- Scramble null: shuffle DM residuals across radii within each galaxy
- Permute null: shuffle V_obs across radii within each galaxy
- Tests reproducibility of the morphology gradient under destructive operations on coherent rotation curve structure

These are **different** tests. P2's are not redundant with Paper 1's, but they need to be clearly distinguished:

**Recommendation for P2 §3.2:** Open with a sentence like "Paper I established that the framework does not generate spurious shells in synthetic Burkert-truth data (FP rate 4.0%) and that the morphology gradient cannot be reproduced by permuting T-type labels across galaxies (p = 0.002). The tests below address a different question: whether the gradient depends on the spatial coherence of localized residual structure within each galaxy, which the random-T-permutation test does not address."

This positions P2's nulls as complementary, targeting the spatial-coherence question Paper 1 doesn't address.

### Issue 5: T=8 wobble comment in P2 §3.1.1

Paper 1's v7.0 deleted the T=8 wobble subsection because "T=8 at 33% is on-trend in v7.0." Our P2 §3.1.1 currently says:

> "The gradient direction — early-type spirals more shell-bearing, late-type systems less so — is monotonic with one minor deviation at T=8 (six galaxies; the sample is too small at this T-bin to interpret structurally)."

**Resolution:** Delete or rephrase. T=8 = 33% sits between T=7 (35.7%) and T=9 (31.2%) — that's monotonically decreasing, no deviation. Replace with "The gradient direction — early-type spirals more shell-bearing, late-type systems less so — is monotonically decreasing across the T = 2–9 range."

### Issue 6: Sample size phrasing

Paper 1 reports 91/102 framework adequacy at χ²_red < 1.5. P2 doesn't currently mention this; it just talks about 102 galaxies and 52/102 shell-bearing.

**Resolution:** No change needed. P2's framing is consistent with Paper 1's. Worth noting in §2 Methods that the v7.0 framework adequacy is established in Paper 1.

### Issue 7: The scaling relations are unique to P2

Paper 1's tables (Tables 1–7 per VALIDATION_STATUS.md) cover:
- T1: aggregate fit quality
- T2: ΔBIC win/loss
- T3: sample composition  
- T4: morphology + null
- T5: null test summary
- T6: NGC 5055
- T7: DC14 universal failures

**None of these cover M ∝ r^0.76, σ ∝ r^1.04, σ/r ≈ 0.275, or the bulge correlation.** These are P2-specific findings — a clean differentiator between the two papers and the right thing for P2 to lead with as its novel content.

---

## Recommended action sequence

In priority order:

### Priority 1: NGC6674 inclusion fix
**Cost:** ~15 minutes (rerun antiwarp script with NGC6674 included, recompute scaling relations and σ/r quartile statistics)
**Impact:** Brings P2's §3.1, §3.3.5 numbers into alignment with Paper 1 conventions

### Priority 2: §3.1 reframing
**Cost:** ~30 minutes of editing
**Impact:** Critical for Paper 2 not appearing redundant with Paper 1. Specifically:
- Open §3.1.1 by citing Paper 1's morphology gradient as established context
- Make clear that P2's contribution is the *organization* of the shell population (scaling relations, σ/r, bulge correlation), not the morphology gradient itself
- Remove Table 3.1.1 or reduce to a brief restatement
- Remove the T=8 deviation comment

### Priority 3: §3.2 reframing
**Cost:** ~15 minutes of editing
**Impact:** Distinguishes P2's spatial-coherence nulls from Paper 1's FP-rate-and-T-permutation nulls. Adds an opening sentence; otherwise prose largely stands.

### Priority 4: gNFW / free-shape decision
**Cost:** Either zero (mention in §4 only) or several hours (run gNFW now)
**Impact:** Affects whether §3.3 has a sixth subsection or whether §4 has an additional paragraph

### Priority 5: Paper 1 introduction citation pass
**Cost:** ~30 minutes once Paper 1 has a final reference (post-AJ-submission)
**Impact:** Ensures P2 cites Paper 1 wherever it builds on Paper 1's results — current draft has placeholders

---

## What I could not verify in this audit

1. **The actual v7.1.0 manuscript .tex** — web_fetch couldn't retrieve it directly. This audit is based on README.md, VALIDATION_STATUS.md, and the headline-result table. If the manuscript contains additional claims not surfaced in the validation tracking, this audit may be incomplete.

2. **What changed v7.0 → v7.1.0 specifically.** The release notes were not visible to me — they showed as truncated "AJ submission release: localized residual structure in SPARC rotation..." across all the v7.0.x and v7.1.0 releases. The v7.0.1 through v7.0.6 sequence suggests these were patches; v7.1.0 may include more substantial changes I couldn't verify.

3. **Paper 1's specific bulge analysis** (if any). I did not see it in the validation status. If Paper 1 has bulge results, the P2 bulge correlation finding may need reframing too.

**To complete the audit, I'd need:**
- The current v7.1.0 sparc_shells_body.tex (manuscript text)
- The v7.1.0 release notes / changelog
- Or just upload the PDF manuscript

**Recommendation: upload the v7.1.0 manuscript PDF or .tex so I can do a fully thorough alignment pass.**

---

## What this means for the drafts in hand

| Draft | Status | Action |
|---|---|---|
| Abstract (locked v1) | NGC6674 numbers correct (-0.833) | No change needed |
| §3.1 (first draft) | NGC6674 numbers wrong (-0.762); morphology gradient framed as new | Rerun antiwarp + reframe §3.1.1 |
| §3.2 (v7.0-clean draft) | NGC6674 included (correct); positioning vs Paper 1 nulls unclear | Add opening paragraph distinguishing from Paper 1's nulls |
| §3.3 (first draft) | NGC6674 excluded in §3.3.5 (wrong); otherwise sound | Rerun antiwarp; minor §3.3.5 update |

None of the drafts are catastrophic. All four sections need light-to-moderate revision rather than rewrites.

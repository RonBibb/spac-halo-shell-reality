# Package Sync Status — halo_shells_paper2

**Snapshot date:** 2026-05-21
**Package version:** v1.0-draft (post-NGC 6674 exclusion + Einasto + backbone-shift + N=100 nulls + framing-softening pass + mass-cap acknowledgment + Bulge OR resolution + inclination edge-on reflection treatment)
**Latest pushed commit at snapshot:** `326f47a` (documentation resync); subsequent uncommitted changes covered by this snapshot include the Bulge OR p-value resolution and the inclination perturbation rerun with edge-on reflection treatment (see Change log).
**Purpose of this file:** Single-source-of-truth for what's in this package at this snapshot, what's complete, and what's pending. Read first.

---

## Manuscript

| Section | State | Notes |
| --- | --- | --- |
| Abstract | Revised 2026-05-19 | ~290 words; NGC 6674-excluded primary sample; backbone-conditional σ/r flagged; bulge-morphology entanglement disclosure added (mirrors §3.1.1) |
| §1 Introduction | First draft | Concession-then-reframe framing for ¶4; literature context preserved |
| §2 Data and methods | Revised 2026-05-19 | 2.1 sample, 2.2 fitting framework, 2.3 partitions (§2.3 exception list retired for §3.3.2-4 and §3.3.7 via post-aggregation; §3.2 remains sole 102-galaxy partition), 2.4 methods (p-floor split 0.01 for §3.2, 0.05 for §3.3 perturbations), 2.5 stats conventions |
| §3.1 Statistical organization | Revised 2026-05-21 | 3.1.1 bulge (with morphology-entanglement quantification; Bulge OR p-value resolved to Fisher 0.0064 with explicit entanglement-based secondary-tier classification, 2026-05-21), 3.1.2 scaling (with slope intercepts, mass-bound rationale, and **mass-cap acknowledgment paragraph added 2026-05-21**), 3.1.3 σ/r quartile gradient (softened), 3.1.4 inner-vs-outer (Wilcoxon and σ counts reconciled to recompute 2026-05-19; KS D resolved to 0.6875 from radial-ordering recompute 2026-05-21, with new Einasto-attenuation caveat), 3.1.5 summary (primary/secondary/soft tiers, multiple-comparisons disclosure; six raw Bonferroni-crossings with three effective primaries after entanglement and Einasto-attenuation demotions; NGC 6674 sensitivity disclosed inline for the morphology gradient) |
| §3.2 Spatial-coherence nulls | Revised 2026-05-19 (N=100) | 3.2.1 scramble (empirical p = 2/100), 3.2.2 permute (0/100), 3.2.3 per-T fractions, 3.2.4 joint. Data in `shell_reality_out_n100/`. |
| §3.3 Robustness against artifacts | Revised 2026-05-21 | 3.3.1 disk scales, 3.3.2-3.3.3 Υ/D perturbations (101-galaxy via post-aggregation), 3.3.4 inclination perturbation (re-run 2026-05-21 with edge-on reflection treatment; now 102-galaxy/2,040 fits raw; 98.0% per-galaxy modal match), 3.3.5 anti-warp clean (NGC 6674-excluded; bulge OR p updated to 0.0064), 3.3.6 Einasto backbone-family control (bulge OR p updated to 0.0064 in table + prose; KS r/r_vir row added 2026-05-21 documenting attenuation from D=0.69 under Burkert to D=0.11 under Einasto; width-and-position attenuation framing in interpretive paragraph), 3.3.7 backbone-shift test (101-galaxy: 45/51 absorbing, 88.2%, p ≈ 1.8×10⁻⁸), 3.3.8 nulls cross-ref, 3.3.9 combined verdict (8 tests; item 7 narrowed 2026-05-19) |
| §4 Discussion | Revised 2026-05-19 | Backbone-family caveat with both Einasto + backbone-shift citations; basis-function-alternative framing softened |
| §5 Conclusions | Revised 2026-05-19 | "Statistical rather than ontological"; Einasto + backbone-shift load-bearing controls cited; null-test wording softened to empirical-p framing |
| Acknowledgments | **Drafted** | Funding statement, software stack (NumPy/SciPy/pandas/Matplotlib), AI assistance disclosure per AAS 2024-25 policy, personal acknowledgment. Zenodo DOI placeholder. |
| Bibliography | Pending | Citation hooks in §1 (Lelli/McGaugh/Schombert, Vegetti, Hezaveh, Gilman, Di Cintio, etc.); full entries with DOIs still needed |
| Figures (13 total) | **All 13 generated** (2026-05-21) | PDFs in `figures/`: 3.1.1–3.1.4, 3.2.1–3.2.2, 3.3.1–3.3.7. |

**Canonical manuscript source:** `source/paper2.md` (~13,300 words drafted). Reading PDF: `source/paper2_consolidated.pdf`.

A previous `source/paper2.tex` file has been removed from this snapshot. LaTeX conversion will be done from `paper2.md` at submission time with AASTeX 7.0.1 scaffolding (PASP requirement).

---

## Sample-size conventions

The manuscript uses two sample conventions, disclosed in §2.3:

- **Primary (NGC 6674-excluded, 101 galaxies):** §1, §2, §3.1, §3.3.1, §3.3.5, §3.3.6, §4, §5. Headline numbers: 51 shell-bearing (50.5%), 67 shells, 16 two-shell galaxies, 25 anti-warp clean shells. Morphology gradient ρ_per_T = -0.762 (p = 0.028). Bulge OR = 3.67. M-r slope 0.76, σ-r slope 1.04, σ/r median 0.275.

- **Paper I-aligned (NGC 6674-included, 102 galaxies):** §3.2 (null tests) only. §3.3.2-3.3.4 (Υ/D/i perturbations) and §3.3.7 (backbone-shift test) production batches were originally run on the 102-galaxy sample but have been re-aggregated on the 101-galaxy sample via `scripts/ngc6674_exclusion_reanalysis.py`; manuscript reports 101-galaxy numbers for those tests.

NGC 6674 has a degenerate two-shell fit (r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound 5×10¹⁰ M☉). Its exclusion from per-shell analyses is methodologically justified.

The inclination perturbation now includes all 11 SPARC galaxies catalogued at $i = 90°$ (edge-on) via a reflection treatment that folds any post-perturbation $i' > 90°$ to $180° - i'$ on the opposite side of edge-on, preserving a symmetric Gaussian perturbation around the nominal inclination. Sample: 102 galaxies × 20 realizations = 2,040 fits (raw); 2,020 fits (101-galaxy aggregation, NGC 6674-excluded).

---

## Mass-bound cap acknowledgment (§3.1.2)

Added in commit `a86a0e5` (2026-05-21). The framework imposes an upper bound on shell mass at 5×10¹⁰ M☉ (adopted from Paper I to preserve the "localized" regime). §3.1.2 now discloses:

- 8 of 67 shells (11.9%) lie within 0.05 dex of the bound
- Among the cap-clear subset (n = 59), M-r slope = 0.67 ± 0.15, σ-r slope = 1.02 ± 0.11, σ/r median = 0.275 (essentially unchanged)
- Cap is treated as **definitional** (preserves "localized" vs. smooth-halo regimes), not as fit pathology
- Bound-relaxation effects flagged as future work; see Paper 3 scope below

---

## Data files

All files in `data/` are present. Status:

| File | State |
| --- | --- |
| `data/antiwarp_per_shell.csv` | Present (67 shells, NGC 6674-excluded, matches §3.3.5 table) |
| `data/antiwarp_summary.txt` | Present (NGC 6674-excluded, 67 shells / 25 clean) |
| `data/backbone_shift.csv` | Present (one row per galaxy with Burkert backbone params at n=0,1,2) |
| `data/backbone_shift_summary.txt` | Present |
| `data/upsilon_perturbation_per_galaxy.csv` | Present (2,040 rows: 102 galaxies × 20 realizations) |
| `data/distance_perturbation_per_galaxy.csv` | Present (2,040 rows) |
| `data/inclination_perturbation_per_galaxy.csv` | Present (2,040 rows: 102 galaxies × 20 realizations; edge-on included via reflection treatment as of 2026-05-21) |
| `data/nulltest_per_realization.csv` | Present (40 rows) — **N=20 baseline; superseded by N=100** |
| `data/nulltest_per_galaxy.csv` | Present (4,080 rows) — N=20 baseline |
| `data/nulltest_summary.txt` | Present — N=20 baseline |
| `data/per_realization.csv`, `data/per_galaxy.csv`, `data/summary.txt` | Byte-identical duplicates of `nulltest_*` files under legacy naming |
| `data/shell_reality_out_n100/per_realization.csv` | **Canonical N=100 for §3.2 (200 rows)** |
| `data/shell_reality_out_n100/per_galaxy.csv` | **Canonical N=100 (20,400 rows)** |
| `data/shell_reality_out_n100/summary.txt` | **Canonical N=100 summary** |
| `data/ngc6674_exclusion_summary.txt` | §2.3 retirement comparison — 102-gal vs 101-gal headlines for §3.3.2-4 and §3.3.7 |
| `data/einasto_full_sample_results.csv` | Paper I Einasto fits (copied in from Paper I repo for §3.3.6 reproducibility) |
| `data/sparc_sample123.csv` | SPARC catalog metadata, 123 rows |
| `data/galaxy_classifications.csv` | With bulge/dwarf/MW-like flags, 123 rows |
| `data/nfw_fixedc_fits.csv` | NFW reference fits |
| `data/Rotmod_LTG/` | 175 SPARC rotmod files; 102 used in T=2-9 sample, 101 in primary analyses |

**Not duplicated here:** Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`). Lives in the Paper I repository at https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0 and is referenced by Paper II scripts.

---

## Logs

All four production-run logs present in `logs/`:

- `logs/antiwarp_log.txt`
- `logs/upsilon_perturbation_log.txt`
- `logs/distance_perturbation_log.txt`
- `logs/inclination_perturbation_log.txt`

---

## Scripts

| Script | State | Notes |
| --- | --- | --- |
| `scripts/antiwarp_subsample.py` | Present | §3.3.5 analysis |
| `scripts/backbone_shift_test.py` | Present | §3.3.7 backbone-shift test |
| `scripts/shell_reality_nulls.py` | Present (519 lines) | §3.2 null tests (serial); shared fitter |
| `scripts/shell_reality_nulls_parallel.py` | Present (added 2026-05-19) | §3.2 parallel runner; byte-identical to serial; ~2 hr at 12 workers for N=100 |
| `scripts/upsilon_perturbation.py` | Present | §3.3.2 producer |
| `scripts/distance_perturbation.py` | Present | §3.3.3 producer |
| `scripts/inclination_perturbation.py` | Present | §3.3.4 producer |
| `scripts/run_canonical_fits.py` | Present (copied from Paper I) | Paper I production fitter underlying all perturbation/null scripts |
| `scripts/einasto_control.py` | Present | §3.3.6 backbone-family Einasto comparison |
| `scripts/make_figures.py` | Present (added 2026-05-19) | Generates 13 manuscript figures from `data/` (all 13 now generated) |
| `scripts/ngc6674_exclusion_reanalysis.py` | Present (added 2026-05-19) | §2.3 retirement; ~5 sec runtime |

---

## Figures

All 13 manuscript figures generated and located in `figures/`:

- `fig_3_1_1_bulge_correlation.pdf`
- `fig_3_1_2_scaling_relations.pdf`
- `fig_3_1_3_sigma_over_r_quartile.pdf`
- `fig_3_1_4_inner_vs_outer.pdf`
- `fig_3_2_1_scramble_null.pdf`
- `fig_3_2_2_permute_null.pdf`
- `fig_3_3_1_disk_dynamical_scales.pdf`
- `fig_3_3_2_upsilon_perturbation.pdf`
- `fig_3_3_3_distance_perturbation.pdf`
- `fig_3_3_4_inclination_perturbation.pdf`
- `fig_3_3_5_antiwarp_clean.pdf`
- `fig_3_3_6_einasto_comparison.pdf` (placed 2026-05-21)
- `fig_3_3_7_backbone_shift.pdf`

---

## Documentation

| File | Purpose |
| --- | --- |
| `STATUS.md` | This file — single-source-of-truth for package state |
| `README.md` | Package overview, structure, reproduction guide |
| `VALIDATION_STATUS.md` | Numerical-claims-to-source mapping; validation tracking |
| `DATA_PROVENANCE.md` | Per-CSV producer/inputs/schema/citation trail |
| `ALIGNMENT_AUDIT.md` | Paper I ↔ Paper II numerical alignment audit (current as of snapshot) |
| `PROJECT_README.md` | Repo file manifest |
| `LICENSE` | MIT |
| `requirements.txt` | Python deps for the scripts |

---

## What's needed before PASP submission

In rough priority order:

1. ~~**Resolve Tier 2 discrepancies** between manuscript-reported and recomputed values~~ — **DONE 2026-05-21.** All four discrepancies reconciled:
   - Wilcoxon p-values §3.1.4 and σ outer>inner count: recompute values adopted 2026-05-19.
   - Bulge OR Fisher p: Fisher scipy default 0.0064 adopted, entanglement-demoted to secondary.
   - KS D-statistic for r/r_vir: radial-ordering recompute on canonical r_vir source gives D = 0.6875, p = 0.0007 under Burkert; Einasto-attenuation check added to §3.3.6.
2. **Finish manuscript text:** full bibliography entries with DOIs.
3. **Cover letter** for PASP submission.
4. **LaTeX conversion:** convert `paper2.md` to AASTeX 7.0.1 source for PASP submission.
5. **Update Paper I citation** once Paper I (PASP-102415, awaiting referee reports as of snapshot) has a decision and final volume/page/DOI.

### Optional, not blocking

- gNFW backbone test as natural follow-on to Einasto (§3.3.6) and backbone-shift (§3.3.7). Strengthens the backbone-family robustness argument but not required.
- Reines dwarf-AGN cross-match (optional strategic addition).

### Deferred to Paper 3 (model refinement)

- **σ/r cap-relaxation paired with hierarchical Υ marginalization.** Paper 2 acknowledges the σ/r ≤ 0.4 cap and the mass cap at 5×10¹⁰ M☉ as definitional constraints (see "Mass-bound cap acknowledgment" above and §3.1.2). Paper 3 refines the model by relaxing both caps and re-fitting under hierarchical Υ marginalization in the same pass. Data and code for the marginalization side already exist in v7.1.1 of the Paper I repo; cap-relaxation Python and outputs are local-side, not yet pushed.

---

## What's deliberately not in this snapshot

- Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`) — external, see Paper I repo
- LaTeX manuscript source — to be generated from markdown at submission
- BibTeX file — to be created at submission
- Paper 3 scripts and outputs (cap relaxation, hierarchical Υ marginalization) — separate package

---

## Change log

### 2026-05-21 revisions

- **§3.1.2 mass-cap acknowledgment paragraph added** (commit `a86a0e5`). Discloses 8 of 67 shells (11.9%) lie within 0.05 dex of the 5×10¹⁰ M☉ upper bound; cap-clear subset (n=59) gives essentially unchanged slopes. Cap framed as definitional. Bound-relaxation deferred to Paper 3.
- **Figure 3.3.6 placed in `figures/`** (commit `6aba87f`). All 13 manuscript figures now in canonical location.
- **Bulge OR p-value resolved.** Adopted Fisher scipy default $p = 0.0064$; abstract, §3.1.1, §3.1.5, §3.3.5 table, and §3.3.6 table/prose updated. Although the raw p formally crosses the Bonferroni threshold for seven tests ($p < 0.0071$), the bulge correlation is classified as a secondary signature alongside the morphology gradient under the §3.1.1 entanglement framing (two projections of a single underlying contrast). The §3.1.5 multiple-comparisons paragraph reflects this with explicit demotion reasoning; BH-adjusted p for bulge updated from 0.014 to 0.009.
- **Inclination perturbation edge-on cleanup.** Script updated from `0 < Inc < 90` to `0 < Inc <= 90` with reflection treatment (post-perturbation $i' > 90°$ folds to $180° - i'$). The 11 edge-on SPARC galaxies are now included symmetrically. New sample: 102 galaxies × 20 realizations = 2,040 fits (raw); 2,020 (101-galaxy aggregation). Headline shifts: per-galaxy modal match 98.9% (90/91) → 98.0% (99/101); per-fit 95.7% → 95.9%; median $|\Delta \log r_1|$ tightens 0.005 → 0.0022 dex. Edge-on subset matches canonical in 220/220 fits. §3.3.4 prose, §2.3 partition table (i: 98.04% → 98.02%), and Figure 3.3.4 caption updated.
- **KS D r/r_vir resolved.** The original manuscript value ($D = 0.47$, $p = 0.045$) used the `position` column from `antiwarp_per_shell.csv` as the inner/outer partition; that column is a fit-slot label and disagrees with radial ordering for 3 of 16 two-shell galaxies. All other §3.1.4 statistics (median outer/inner mass ratio 2.62, 14/16 outer-heavier, 14/16 outer-wider) match radial ordering, so radial ordering is the manuscript's intended partition. Corrected values on the canonical r_vir source: $D = 0.6875$, $p = 0.0007$. The raw p now crosses Bonferroni. Bonus Einasto check: under Einasto the KS attenuates dramatically ($D = 0.11$, $p \approx 1.0$); inner/outer median r/r_vir shift from 0.012/0.027 (Burkert) to 0.050/0.052 (Einasto). KS is therefore Burkert-baseline-dependent and stays in secondary tier despite crossing Bonferroni under Burkert — same demotion logic as σ inner-vs-outer Wilcoxon. Updates: §3.1.4 prose (D, p, medians, IQRs, removal of "marginal" framing, new backbone-dependence caveat), §3.1.5 KS secondary entry, §3.1.5 multiple-comparisons paragraph (six raw Bonferroni-crossings; three effective primary signatures), §3.3.6 Einasto comparison table (new KS row), §3.3.6 width-and-position attenuation paragraph (KS added to attenuated group), §3.3.6 interpretive paragraph (shell-position parameters added to "partially degenerate with backbone shape" framing).

### 2026-05-19 revisions

- **§2.3 exception list retired for §3.3.2-4 and §3.3.7** via post-aggregation through `scripts/ngc6674_exclusion_reanalysis.py`. Re-running per-galaxy aggregation on the 101-galaxy sample produces shifts ≤ 0.25 pp on every §3.3 headline number. Detailed comparison in `data/ngc6674_exclusion_summary.txt`. Manuscript updated:
  - §2.3: exception list narrowed to §3.2 only
  - §3.3.7 body: 46/52 (88.5%) → 45/51 (88.2%); binomial p shifts from 1.0×10⁻⁸ to 1.8×10⁻⁸ (still vanishing)
  - §3.3.9 item 7, §4 backbone paragraph, §4 nulls paragraph, §5 Conclusions: four sibling 88.5% references updated to 88.2%

- **§3.2 N=100 null test rerun** completed via new `shell_reality_nulls_parallel.py` (12-worker parallel, byte-identical to serial). Headline numbers:
  - Scramble: ρ_per_T mean = -0.289 ± 0.229, z = -2.4σ, empirical p = 2/100
  - Permute: ρ_per_T mean = +0.350 ± 0.235, z = -5.0σ, empirical p = 0/100
  - Asymmetric failure direction preserved.
- **Abstract revised** to disclose bulge-morphology entanglement.
- **§3.1.5 morphology gradient bullet** now discloses NGC 6674 sensitivity inline (Paper I's p = 0.010 → Paper II's p = 0.028 reflects single-galaxy removal alone).
- **§3.3.9 item 7** narrowed to "The smooth profile cannot natively absorb the structure without measurable parameter shift" — same evidence, narrower defensible claim.
- **§4 and §5 framing** softened to align with N=100 data and §3.3.9 item 7 narrowing.
- **Figures:** 9 of 11 PDFs generated and committed to `figures/`. (3.3.6 added 2026-05-19 in `data/`; 3.3.7 added in `figures/`. Both later resolved into `figures/` on 2026-05-21.)
- **`scripts/einasto_control.py`** added with portable path resolution.
- **Wilcoxon p-values §3.1.4 reconciled** to recompute values (0.0001 mass, 0.0008 σ) — manuscript-historical values 0.017/0.049 retired.
- **σ outer-vs-inner count reconciled** to 14/16 (NGC 6674-excluded 16 two-shell galaxies basis).
- **Target journal change:** AJ → PASP, following Paper I's PASP submission as #PASP-102415 (awaiting referee reports as of snapshot).

### Earlier (v1.0-draft initial)

- Initial package scaffolding, 2026-05-09 to 2026-05-12.
- Manuscript first drafts of §1–§5 completed.
- Paper I v7.1.0 alignment established.
- Initial figure pass (subset).

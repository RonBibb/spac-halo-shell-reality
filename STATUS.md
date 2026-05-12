# Package Sync Status — halo_shells_paper2

**Snapshot date:** 2026-05-12
**Package version:** v1.0-draft (post-NGC 6674 exclusion + Einasto + backbone-shift additions)
**Purpose of this file:** Single-source-of-truth for what's in this package at this snapshot, what's complete, and what's pending. Read first.

---

## Manuscript

| Section | State | Notes |
| --- | --- | --- |
| Abstract | First draft, revised | ~250 words; NGC 6674-excluded primary sample; backbone-conditional σ/r flagged |
| §1 Introduction | First draft | Concession-then-reframe framing for ¶4; literature context preserved |
| §2 Data and methods | First draft | 2.1 sample, 2.2 fitting framework, 2.3 partitions (101-galaxy primary + §3.2/§3.3.2-4/§3.3.7 exception list), 2.4 methods, 2.5 stats conventions |
| §3.1 Statistical organization | First draft | 3.1.1 bulge (with morphology-entanglement quantification), 3.1.2 scaling (with slope intercepts + mass-bound rationale), 3.1.3 σ/r quartile gradient (softened), 3.1.4 inner-vs-outer, 3.1.5 summary (primary/secondary/soft tiers, multiple-comparisons disclosure) |
| §3.2 Spatial-coherence nulls | First draft (uses 102-galaxy production run; §2.3 exception) | 3.2.1 scramble, 3.2.2 permute, 3.2.3 per-T fractions, 3.2.4 joint |
| §3.3 Robustness against artifacts | First draft | 3.3.1 disk scales, 3.3.2-3.3.4 Υ/D/i perturbations (102-galaxy; §2.3 exception), 3.3.5 anti-warp clean (NGC 6674-excluded), 3.3.6 Einasto backbone-family control, 3.3.7 backbone-shift test (102-galaxy; §2.3 exception), 3.3.8 nulls cross-ref, 3.3.9 combined verdict (8 tests) |
| §4 Discussion | First draft | Backbone-family caveat with both Einasto + backbone-shift citations; basis-function defense via destructive-nulls + backbone-shift |
| §5 Conclusions | First draft | "Statistical rather than ontological"; Einasto + backbone-shift load-bearing controls cited |
| Acknowledgments | Pending | Stub only |
| Bibliography | Pending | Citation hooks in place; full entries needed |
| Figures (11 total) | Pending | Placeholders annotated in §3 with data sources |

**Canonical manuscript source:** `source/paper2.md`

A previous `source/paper2.tex` file has been removed from this snapshot. It contained content generated during package scaffolding that did not match the markdown source. LaTeX conversion will be done from `paper2.md` at submission time with appropriate AASTeX 6.3+ scaffolding.

---

## Sample-size conventions

The manuscript uses two sample conventions, disclosed in §2.3:

- **Primary (NGC 6674-excluded, 101 galaxies):** §1, §2, §3.1, §3.3.1, §3.3.5, §3.3.6, §4, §5. Headline numbers: 51 shell-bearing (50.5%), 67 shells, 16 two-shell galaxies, 25 anti-warp clean shells. Morphology gradient ρ_per_T = -0.762 (p = 0.028). Bulge OR = 3.67. M-r slope 0.76, σ-r slope 1.04, σ/r median 0.275.

- **Paper I-aligned (NGC 6674-included, 102 galaxies):** §3.2 (null tests), §3.3.2-3.3.4 (Υ/D/i perturbations), §3.3.7 (backbone-shift test). These analyses ran as coordinated production batches against the 102-galaxy canonical fits; reconciliation to the 101-galaxy primary sample requires Mac-side reruns. The §2.3 disclosure quantifies why qualitative conclusions hold (NGC 6674 contributes ≤1% of any batch, ≤1/9 to any per-T bin, etc.).

NGC 6674 has a degenerate two-shell fit (r₁ = r₂ = 3.12 kpc with both masses pegged at the upper bound 5×10¹⁰ M☉). Its exclusion from per-shell analyses is methodologically justified; its retention in the production-batch analyses is a packaging artifact awaiting future rerun.

---

## Data files

All files in `data/` are present. Status:

| File | State |
| --- | --- |
| `data/antiwarp_per_shell.csv` | Present (67 shells, NGC 6674-excluded, matches §3.3.5 table) |
| `data/antiwarp_summary.txt` | Present (NGC 6674-excluded, 67 shells / 25 clean, matches §3.3.5 table) |
| `data/backbone_shift.csv` | Present (one row per galaxy with Burkert backbone params at n=0,1,2) |
| `data/backbone_shift_summary.txt` | Present (population-level summary of §3.3.7 results) |
| `data/upsilon_perturbation_per_galaxy.csv` | Present (2,040 rows: 102 galaxies × 20 realizations) |
| `data/distance_perturbation_per_galaxy.csv` | Present (2,040 rows) |
| `data/inclination_perturbation_per_galaxy.csv` | Present (1,820 rows; 11 edge-on excluded by `0 < Inc < 90`) |
| `data/nulltest_per_realization.csv` | Present (40 rows: 2 null types × 20 reps) |
| `data/nulltest_per_galaxy.csv` | Present (4,080 rows: 2 × 20 × 102) |
| `data/nulltest_summary.txt` | Present |
| `data/sparc_sample123.csv` | Present (SPARC catalog metadata, 123 rows) |
| `data/galaxy_classifications.csv` | Present (with bulge/dwarf/MW-like flags, 123 rows) |
| `data/nfw_fixedc_fits.csv` | Present (NFW reference fits) |
| `data/Rotmod_LTG/` | Present (175 SPARC rotmod files; 102 used in T=2-9 sample, 101 in primary analyses) |

**Not duplicated here:** Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`) and Paper I Einasto results CSV (`einasto_full_sample_results.csv`). Both live in the Paper I repository at https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0 and are referenced by Paper II scripts.

---

## Logs

All four production-run logs are present in `logs/`:

- `logs/antiwarp_log.txt`
- `logs/upsilon_perturbation_log.txt`
- `logs/distance_perturbation_log.txt`
- `logs/inclination_perturbation_log.txt`

---

## Scripts

| Script | State | Notes |
| --- | --- | --- |
| `scripts/antiwarp_subsample.py` | Present (canonical Mac-side version) | §3.3.5 analysis |
| `scripts/backbone_shift_test.py` | Present | §3.3.7 backbone-shift test; depends on shell_reality_nulls.py for shared fitter |
| `scripts/shell_reality_nulls.py` | Present (519 lines) | §3.2 null tests; implements scramble/permute nulls; shared fitter used by backbone_shift_test.py |
| `scripts/upsilon_perturbation.py` | Present (514 lines) | §3.3.2 producer |
| `scripts/distance_perturbation.py` | Present (570 lines) | §3.3.3 producer |
| `scripts/inclination_perturbation.py` | Present (570 lines) | §3.3.4 producer |
| `scripts/run_canonical_fits.py` | Present (548 lines, copied from Paper I) | Paper I production fitter underlying all perturbation/null scripts |
| `scripts/einasto_control.py` | Present | §3.3.6 backbone-family Einasto comparison (post-hoc analysis on Paper I's Einasto fits) |

All scripts depend on Paper I's `run_canonical_fits.py` or its components for the Paper I fitting framework. The Paper I canonical fits CSV must be supplied externally (see "Data files" note above).

---

## Documentation

| File | Purpose |
| --- | --- |
| `STATUS.md` | This file — single-source-of-truth for package state |
| `README.md` | Package overview, structure, reproduction guide |
| `VALIDATION_STATUS.md` | Numerical-claims-to-source mapping; validation tracking |
| `DATA_PROVENANCE.md` | Per-CSV producer/inputs/schema/citation trail |
| `ALIGNMENT_AUDIT.md` | Paper I ↔ Paper II numerical alignment audit |
| `PROJECT_README.md` | Original working manifest (preserved) |
| `LICENSE` | MIT |
| `requirements.txt` | Python deps for the scripts |

---

## What's needed before AJ submission

In rough priority order:

1. **Mac-side NGC 6674 reruns** of §3.2 null tests and §3.3.2-3.3.4 perturbation tests (and §3.3.7 backbone-shift if time permits) to reconcile to 101-galaxy primary sample. The §2.3 disclosure currently bounds the impact but does not close the asymmetry.
2. **Resolve Tier 2 discrepancies** between manuscript-reported and recomputed values:
   - Wilcoxon p-values in §3.1.4 (manuscript 0.017/0.049 historical vs recompute 0.0001/0.0008)
   - σ outer>inner count (manuscript 12/17 historical vs recompute 14/17)
   - KS D-statistic for r/r_vir (manuscript 0.47 vs recompute 0.688 — likely r_vir source difference)
   - Bulge OR Fisher p (manuscript 0.003 vs scipy default 0.0064; matches Boschloo/Barnard/mid-p at 0.0038)
3. **Finish manuscript text:** acknowledgments paragraph, full bibliography entries with DOIs.
4. **Generate the 11 figures** from the annotated placeholders in §3. Data is present in `data/` or in Paper I repo (Einasto).
5. **Optional gNFW backbone test** as natural follow-on to Einasto (§3.3.6) and backbone-shift (§3.3.7). Not required for submission but strengthens the backbone-family robustness argument.
6. **Citation hooks → entries:** the §1 references (Lelli/McGaugh/Schombert, Vegetti, Hezaveh, Gilman, Di Cintio, etc.) need to resolve to actual bibliography entries.
7. **LaTeX conversion:** convert `paper2.md` to AASTeX 6.3+ source for submission.
8. **Update Paper I citation** from "in press" to final volume/page/DOI once Paper I is published.

---

## What's deliberately not in this snapshot

- Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`) — external, see Paper I repo
- Paper I Einasto fits CSV (`einasto_full_sample_results.csv`) — external, see Paper I repo
- Generated figure files (PDFs/PNGs) — to be produced from data + scripts
- LaTeX manuscript source — to be generated from markdown at submission
- BibTeX file — to be created at submission

---

## Change log since v1.0-draft initial

- **NGC 6674 systematic exclusion** from primary analysis (§1, §2.3, §3.1, §3.3.5, §3.3.6, §4, §5, sample-conventions appendix). Exception list disclosed in §2.3.
- **§3.3.6 Einasto backbone-family control** added with Paper I Einasto fits as input. Headline: 88% classification agreement, morphology + bulge + mass-feature signatures strengthen under Einasto; width-related signatures attenuate (backbone-baseline-dependent).
- **§3.3.7 backbone-shift test** added (NEW Mac-side production run). Headline: 46/52 (88.5%) of SB galaxies show systematic backbone deformation when shells are removed; rules out decoupled-basis-function interpretation.
- **§3.1.5 restructured** into primary (Bonferroni-robust) / secondary (BH-FDR pass, Bonferroni fail) / soft tiers with explicit multiple-comparisons disclosure.
- **§3.1 introduction** acknowledges exploratory-population-diagnostic nature; not corrected for multiple comparisons; not pre-registered.
- **§3.1.1 bulge/morphology entanglement** quantified — 19/24 bulged at T=2,3; bulge correlation and morphology gradient are "two projections of one underlying contrast" rather than independent dimensions.
- **§3.1.3 σ/r quartile gradient** softened ("modest population-level tendency" instead of "factor-of-two range").
- **§3.1.4 sample size** updated to 16 two-shell pairs; Wilcoxon p-values recomputed (with Tier 2 discrepancy disclosed).
- **Abstract** flags σ-r and σ/r as Burkert-backbone-conditional with reference to §3.3.6.
- **§4 backbone-family paragraph** rewritten to cite both Einasto (§3.3.6) and backbone-shift (§3.3.7) as the two backbone-related controls.
- **§4 basis-function defense** strengthened with backbone-shift evidence.
- **§5** mentions Einasto and backbone-shift alongside other robustness tests.
- **§3.3.9 combined verdict** updated from seven to eight complementary tests with "backbone-deformation under shell absorption" added as a channel.
- **Slope intercepts** filled in §3.1.2 equations.
- **Mass-bound rationale** added to §3.1.2.
- **Sample-conventions appendix** updated to reflect 101-galaxy primary.

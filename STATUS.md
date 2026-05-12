# Package Sync Status — halo_shells_paper2

**Snapshot date:** 2026-05-11
**Package version:** v1.0-draft
**Purpose of this file:** Single-source-of-truth for what's in this package at this snapshot, what's complete, and what's pending. Read first.

---

## Manuscript

| Section | State | Notes |
| --- | --- | --- |
| Abstract | First draft, revised | ~250 words, tightened |
| §1 Introduction | First draft | Field framing, SPARC context, Paper I bridge, scope deferrals, outline |
| §2 Data and methods | First draft | 2.1 sample, 2.2 v7.0 framework, 2.3 partitions, 2.4 methods, 2.5 stats conventions |
| §3.1 Statistical organization | First draft | 3.1.1 bulge, 3.1.2 scaling, 3.1.3 σ/r gradient, 3.1.4 inner-vs-outer, 3.1.5 summary |
| §3.2 Spatial-coherence nulls | First draft | 3.2.1 scramble, 3.2.2 permute, 3.2.3 per-T fractions, 3.2.4 joint |
| §3.3 Robustness against artifacts | First draft | 3.3.1 disk scales, 3.3.2-3.3.4 Υ/D/i perturbations, 3.3.5 anti-warp clean, 3.3.6 nulls x-ref, 3.3.7 combined |
| §4 Discussion | First draft | Constrains classes; flags backbone-shape robustness as future work |
| §5 Conclusions | First draft | "Statistical rather than ontological" framing |
| Acknowledgments | Pending | Stub only |
| Bibliography | Pending | Citation hooks in place; full entries needed |
| Figures (10 total) | Pending | Placeholders annotated in §3 with data sources |

**Canonical manuscript source:** `source/paper2.md`

A previous `source/paper2.tex` file has been removed from this snapshot. It contained content generated during package scaffolding that did not match the markdown source. LaTeX conversion will be done from `paper2.md` at submission time with appropriate AASTeX 6.3+ scaffolding.

---

## Data files

All files in `data/` are present and aligned with v7.0/v7.1.0 of Paper I. Status:

| File | State |
| --- | --- |
| `data/antiwarp_per_shell.csv` | Present (67 shells, NGC 6674 excluded; see note below) |
| `data/antiwarp_summary.txt` | Present (regenerated with NGC 6674 included, 69 shells, matches manuscript) |
| `data/upsilon_perturbation_per_galaxy.csv` | Present (2,040 rows) |
| `data/distance_perturbation_per_galaxy.csv` | Present (2,040 rows) |
| `data/inclination_perturbation_per_galaxy.csv` | Present (1,820 rows; 11 edge-on excluded) |
| `data/nulltest_per_realization.csv` | Present (40 rows: 2 nulls × 20 reps) |
| `data/nulltest_per_galaxy.csv` | Present (4,080 rows) |
| `data/nulltest_summary.txt` | Present |
| `data/sparc_sample123.csv` | Present (SPARC catalog metadata) |
| `data/galaxy_classifications.csv` | Present (with bulge/dwarf/MW-like flags) |
| `data/nfw_fixedc_fits.csv` | Present (NFW reference fits) |
| `data/Rotmod_LTG/` | Present (175 SPARC rotmod files) |

**Note on antiwarp CSV/summary sample-size mismatch:** The per-shell CSV currently preserves the NGC 6674-excluded version (67 shells), while the summary text was regenerated with NGC 6674 included (69 shells) to match Paper I conventions and the manuscript's numbers. Regenerating the CSV with NGC 6674 included is on the small-fixes list.

**Not included in this package:** Paper I canonical fits CSV (`sparc_T2-T9_canonical_fits.csv`). This file lives in the Paper I repository at https://github.com/RonBibb/sparc-halo-shells/releases/tag/v7.1.0 and is referenced by Paper II scripts. It is not duplicated here to prevent drift between Paper I v7.1.0 and a copy embedded in this package.

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
| `scripts/antiwarp_subsample.py` | Reconstructed from manuscript §3.3.5 spec | Pure-analysis script (no fitting); verify against Mac-side reference at `~/Library/CloudStorage/OneDrive-Personal(2)/.../shell_reality_v2/scripts/` |
| `scripts/upsilon_perturbation.py` | NOT WRITTEN | Wrapper for Paper I v7.0 fitter; pending |
| `scripts/distance_perturbation.py` | NOT WRITTEN | Wrapper for Paper I v7.0 fitter; pending |
| `scripts/inclination_perturbation.py` | NOT WRITTEN | Wrapper for Paper I v7.0 fitter; pending |
| `scripts/shell_reality_nulls.py` | NOT WRITTEN | Implements scramble/permute nulls; pending |

The four wrapper scripts depend on Paper I's `run_canonical_fits.py` as the underlying fitter. For reproduction purposes, the canonical version of each producer script lives on the Mac-side working repository. These scripts can be either ported from the Mac side or reconstructed here as a future task.

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

1. **Finish the manuscript text:** acknowledgments paragraph, full bibliography entries with DOIs.
2. **Generate the 10 figures** from the annotated placeholders in §3. Data is present in `data/`.
3. **Port or rewrite the four missing producer scripts** so the package is reproducible from inputs.
4. **Regenerate `antiwarp_per_shell.csv`** with NGC 6674 included, so the CSV matches the summary and manuscript.
5. **Citation hooks → entries:** the §1 references (Lelli/McGaugh/Schombert, Vegetti, Hezaveh, Gilman, Di Cintio, etc.) need to resolve to actual bibliography entries.
6. **LaTeX conversion:** convert `paper2.md` to AASTeX 6.3+ source for submission.
7. **Update Paper I citation** from "in press" to final volume/page/DOI once Paper I is published.

---

## What's deliberately not in this snapshot

- Paper I canonical fits CSV — external, see Paper I repo
- Paper I production fitter (`run_canonical_fits.py`) — external
- Generated figure files (PDFs/PNGs) — to be produced from data + scripts
- LaTeX manuscript source — to be generated from markdown at submission
- BibTeX file — to be created at submission

---

## Sync verification

If you (Ron) want to verify what's in this package matches what we discussed in conversation, the manuscript content in `source/paper2.md` should match the markdown you've been editing in this session, including:

- Revised abstract (~250 words, scaling claim toned down, perturbation/null numerics in §3.3/§3.2 only)
- §1 with 7 paragraphs ending in the section outline
- §3.1.3 with the "fractional radial extent" phrasing (no sphere/ring interpretation)
- §4 with 7 paragraphs ending in the four-direction future-work list
- §5 with 5 paragraphs ending in "statistical rather than ontological"
- All 10 figure placeholders in §3 with data-source annotations

If any of those don't match, the package is out of sync and we should rebuild.

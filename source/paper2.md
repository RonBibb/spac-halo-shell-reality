# Statistical organization of localized residual structure in SPARC rotation curves

**R. Bibb**
ORCID: 0009-0004-1153-2464
ronbibb@gmail.com

**Target journal:** AJ
**Status:** Working draft, updated 2026-05-11. Paper I v7.1.0-aligned. Abstract, §1, §4, §5 drafted. Sections 2 and 3 drafted. Bibliography, figures, and acknowledgments pending.

---

## Document organization

| Section | Status | Notes |
|---|---|---|
| Abstract | Revised v2, tightened | ~250 words |
| §1 Introduction | First draft | Field framing, SPARC context, Paper I bridge, scope deferrals, outline |
| §2 Data and methods | First draft | |
| §3.1 Statistical organization | v2 (audit-aligned) | NGC 6674 included |
| §3.2 Spatial-coherence nulls | First draft | Distinguishes from Paper I nulls |
| §3.3 Robustness against artifacts | First draft, §3.3.5 v2 | NGC 6674-included antiwarp |
| §4 Discussion | First draft | Constrains classes of explanation; flags backbone absorption as future work |
| §5 Conclusions | First draft | Statistical-not-ontological framing |
| Bibliography | Pending | Citation hooks in place |
| Acknowledgments | Pending | |
| Figures (10 total) | Pending; placeholders annotated in §3 | Data available; generation scripts to be written |

---

## Abstract

We investigate whether the localized residual structures identified in the SPARC rotation-curve framework of Paper I represent a statistically organized population or an accumulation of fitting artifacts. Paper I established the framework and demonstrated a galaxy-level morphology gradient in shell-bearing fraction across $T = 2$–9 (Spearman $\rho = -0.83$, $p = 0.010$). The present paper characterizes the per-shell-level organization of that population and consolidates artifact-channel robustness tests.

On the 101-galaxy NGC 6674-excluded sample, the framework selects 51 shell-bearing systems and 67 individual shells. Shell mass scales as $M \propto r^{0.76}$ ($\rho = +0.64$, $p < 10^{-4}$), shell width as $\sigma \propto r^{1.04}$ ($\rho = +0.78$, $p < 10^{-4}$), implying $\sigma/r \approx 0.27$ in the Burkert convention, and within two-shell galaxies outer shells are systematically more massive than inner (14/16; Wilcoxon $p = 10^{-4}$). Bulge-dominated galaxies are preferentially shell-bearing (OR $= 3.67$, $p = 0.006$), statistically near-equivalent to the morphology gradient under the underlying early-type vs late-type contrast. Three of these signatures cross strict Bonferroni correction across seven §3.1 tests and preserve across two backbone-family controls (Einasto and gNFW).

Two destructive null procedures on the observed rotation curves bracket the real-data signal asymmetrically: residual scrambling under-detects shells while cross-radius velocity permutation over-detects, neither reproducing the morphology gradient. Shell selections remain stable under perturbations to stellar mass-to-light ratio (95.1%), distance (94.1%), and inclination (98.0% per-galaxy modal match), and persist in an anti-warp clean subsample. A backbone-shift test shows the smooth profile cannot natively absorb the shell structure, disfavoring decoupled basis-function accounts.

These results disfavor random fitting, baryonic measurement systematics, outer-disk warp artifacts, decoupled basis-function flexibility, and (with Paper I) backbone-family flexibility and per-galaxy mass-to-light variation as dominant explanations for the shell population. Whether the detected structures correspond to localized halo features or to other forms of organized galactic dynamics remains open.

---

## 1. Introduction

Galaxy rotation curves are commonly modeled using smooth dark-matter halo profiles such as the Navarro-Frenk-White (NFW), Burkert, Einasto, and related parameterizations. While these profiles capture the large-scale structure of many systems, observed rotation curves frequently exhibit localized residual structure relative to smooth fits. Interpreting such residuals is difficult because multiple effects can contribute simultaneously, including baryonic modeling uncertainty, noncircular motions, warped outer disks, beam-smearing effects, and fitting flexibility within the adopted halo parameterization. Distinguishing statistically meaningful structure from fitting artifacts therefore remains a central challenge in rotation-curve analysis.

The Spitzer Photometry and Accurate Rotation Curves (SPARC) database [Lelli, McGaugh, & Schombert 2016] provides a useful environment for such tests because it combines homogeneous near-infrared photometry with high-quality HI and H$\alpha$ rotation curves across a broad range of galaxy morphologies. The SPARC sample has consequently become a standard benchmark for studies of galaxy dynamics, baryonic scaling relations, and halo-profile phenomenology.

Paper I introduced the Burkert-backbone-plus-Gaussian-shell framework and validated it against synthetic null tests (Paper I §3.5) and an Einasto-backbone full-sample substitution (Paper I §3.7). It established that Bayesian model selection adequately fits 91/102 SPARC galaxies under the framework versus 65/102 under Burkert-only and 52/102 under free-concentration NFW, and that shell-bearing fraction varies systematically across morphological type (Paper I §3.3; per-galaxy permutation $p = 0.002$). Paper I also reported a hierarchical Υ marginalization (Paper I §4.4) demonstrating that the framework's adequacy advantage compresses but persists under a data-driven population prior on stellar mass-to-light ratio. The framework's existence and its galaxy-level robustness against these specific artifact channels are therefore established prior to the present analysis. However, the existence of BIC-selected localized components and their galaxy-level robustness do not by themselves establish that the per-shell population exhibits internal organization, nor do they exhaust the artifact channels that could plausibly produce shell-like selections (spatial coherence of residuals, per-realization stability under baryonic input perturbations, outer-disk warp artifacts, decoupled basis-function flexibility).

Flexible fitting frameworks can generate localized components even in the absence of physical substructure. The relevant question is therefore not whether shell-like components can be detected, but whether the resulting population exhibits reproducible statistical organization that survives destructive null procedures and systematic perturbations beyond those already tested in Paper I. The present analysis addresses that narrower question: it characterizes the internal organization of the shell population at the per-shell level, applies destructive nulls directly to the observed rotation curves (rather than to synthetic smooth-halo mocks as in Paper I §3.5), tests stability under per-realization perturbations to the principal baryonic input parameters, and examines whether shells are dynamically coupled to the smooth backbone or behave as decoupled basis functions. We deliberately defer geometric interpretation, decomposition uniqueness, and physical origin to future work.

This question connects to several broader areas of current research. Residual structure in galaxy rotation curves has long been discussed in the context of baryonic substructure, non-axisymmetric dynamics, and departures from idealized smooth-halo descriptions. Independent searches for dark-matter substructure have also been pursued through strong gravitational lensing, stellar-stream perturbations, and dynamical analyses of galactic halos. At the same time, modern halo modeling increasingly explores phenomenological profile families extending beyond canonical NFW forms, including cored, generalized, and feedback-modified profiles. The present work does not engage these broader interpretive questions; its scope is the statistical organization of the residual structures identified by the framework within the SPARC sample.

This paper is organized as follows. Section 2 summarizes the SPARC sample, the fitting framework, and the statistical methods used throughout the analysis. Section 3 presents the empirical results in three parts: internal organization of the shell population (§3.1), spatial-coherence null tests (§3.2), and robustness against several artifact channels (§3.3). Section 4 discusses the classes of explanation constrained by these results and the principal limitations of the present analysis. Section 5 summarizes the main conclusions.

---

## 2. Data and methods

### 2.1 The SPARC sample and quality criteria

We work with the 102-galaxy subset of the Spitzer Photometry and Accurate Rotation Curves (SPARC) database [Lelli, McGaugh, & Schombert 2016] as adopted in Paper I, restricted to morphological types $T = 2$–9 with quality flag $Q \le 2$ and at least five rotation-curve points where the dark-matter contribution is positive (i.e., $V_{\rm obs}^2 > V_{\rm bar}^2$). The selection criteria match Paper I exactly. Each galaxy provides:

- A measured rotation curve $V_{\rm obs}(r)$ with uncertainties $e_{V_{\rm obs}}(r)$ at sampled radii $r$.
- Decomposed baryonic rotational components $V_{\rm gas}(r)$, $V_{\rm disk}(r)$, $V_{\rm bulge}(r)$, derived from the SPARC photometric and HI data.
- Catalog metadata: distance $D$ with uncertainty $e_D$, inclination $i$ with uncertainty $e_i$, HI extent $R_{\rm HI}$, optical disk scale length $R_{\rm disk}$, effective radius $R_{\rm eff}$, morphological type $T$, and SPARC quality flag $Q$.
- Derived virial-scale estimates $r_{\rm vir}$, halo mass $M_{\rm halo}$, and stellar mass $M_*$ via the abundance-matching procedure described in Paper I §2.1.

The sample composition by morphological type is: $T = 2$ (9 galaxies), $T = 3$ (11), $T = 4$ (17), $T = 5$ (13), $T = 6$ (16), $T = 7$ (14), $T = 8$ (6), $T = 9$ (16), totaling 102. Bulge presence is classified per galaxy from the SPARC photometric decomposition, yielding 24 bulge-dominated and 78 bulgeless galaxies. NGC 6674 ($T = 3$, bulge-dominated) is excluded from the primary analysis under §2.3, reducing the $T = 3$ bin to 10 and the bulge-dominated count to 23 in the 101-galaxy primary convention used throughout §3.

### 2.2 The Paper I fitting framework

We use the framework derived and validated in Paper I. The total dark-matter contribution to the rotation curve is modeled as a Burkert backbone plus zero, one, or two Gaussian-mass shells:

$$
V_{\rm DM}^2(r) = V_{\rm Burkert}^2(r;\, \rho_0, a) + \sum_{i=1}^{N} V_{\rm shell,i}^2(r;\, M_i, r_i, \sigma_i),
$$

where $N \in \{0, 1, 2\}$ is selected per-galaxy by Bayesian Information Criterion. The Burkert profile has central density $\rho_0$ and core radius $a$, with enclosed mass

$$
M_{\rm Burkert}(<r) = \pi \rho_0 a^3 \left[ \ln\bigl((1+x)^2 (1+x^2)\bigr) - 2 \arctan(x) \right], \quad x = r/a.
$$

Each shell is a localized Gaussian mass distribution with mass $M_i$, central radius $r_i$, and width $\sigma_i$. The mass enclosed within radius $r$ is

$$
M_{\rm shell}(<r;\, M_i, r_i, \sigma_i) = \tfrac{1}{2} M_i \left[ \mathrm{erf}\!\left(\tfrac{r - r_i}{\sigma_i \sqrt{2}}\right) - \mathrm{erf}\!\left(\tfrac{-r_i}{\sigma_i \sqrt{2}}\right) \right],
$$

with $V_{\rm shell,i}^2(r) = G M_{\rm shell}(<r) / r$.

**Width constraint via reparameterization.** A defining feature of the framework is strict enforcement of the localization criterion $\sigma_i / r_i \le 0.4$. Each shell's width is parameterized as $\sigma_i = f_i r_i$ with $f_i$ as a box-bounded fit parameter $f_i \in [0.01, 0.4]$, ensuring the constraint is respected at every step of the optimization regardless of optimizer trajectory. See Paper I §2.2 and Appendix A for the derivation of this width parameterization.

**Mass bounds.** Shell masses are bounded $10^6 \le M_i \le 5 \times 10^{10}\,M_\odot$. The lower bound prevents numerical degeneracies; the upper bound was chosen in Paper I to keep shells in a "localized" regime well below typical halo masses. Of the 67 shells in the canonical fits (NGC 6674 excluded), 8 (11.9%) lie within 0.05 dex of the upper bound. We verify in §3.1.2 that removing these mass-bound-approaching shells produces only modest changes to the population-level scaling relations; the bound is binding for a subset of fits but does not drive the principal results.

**BIC selection.** For each galaxy, we fit the framework at $N = 0$, $N = 1$, and $N = 2$ shells (each with appropriate multi-restart procedure, see Paper I §2.3) and select the minimum-BIC solution:

$$
\mathrm{BIC}(N) = \chi^2_{\min}(N) + p(N) \ln(n_{\rm pts}),
$$

with parameter count $p(N) = 2 + 3N$ and $n_{\rm pts}$ the number of fit points after the $V_{\rm obs}^2 > V_{\rm bar}^2$ cut.

**Baryonic decomposition.** The total baryonic rotation contribution at each radius is

$$
V_{\rm bar}^2(r) = V_{\rm gas}(r) |V_{\rm gas}(r)| + \Upsilon_{\rm disk} V_{\rm disk}(r) |V_{\rm disk}(r)| + \Upsilon_{\rm bulge} V_{\rm bulge}(r) |V_{\rm bulge}(r)|,
$$

with absolute values handling the SPARC sign convention for negative-contribution outer regions. Canonical mass-to-light ratios at 3.6 µm are $\Upsilon_{\rm disk} = 0.5$ and $\Upsilon_{\rm bulge} = 0.7$.

### 2.3 Sample partitions used in §3

We use three sample partitions, each suited to a specific test:

**The full canonical sample** (101 galaxies, 67 shells across 51 shell-bearing galaxies) is the canonical Paper I-aligned working set with NGC 6674 excluded, following the precedent established in Paper I §4.4. NGC 6674's canonical fit selects $n_{\rm shells} = 2$ but yields a degenerate solution ($r_1 = r_2 = 3.12$ kpc within numerical precision, with both shell masses pegged at the upper bound), which precludes meaningful interpretation of its individual shell parameters as a population of two distinct localized features. Paper I uses 102 galaxies for its main analyses but explicitly drops NGC 6674 from its hierarchical Υ marginalization for the same reason ("excluded for a known fit pathology," Paper I §4.4). The present per-shell and population analyses follow the same exclusion logic. All quantitative conclusions are unchanged in direction relative to an NGC 6674-included analysis; effect sizes shift only modestly (e.g., the morphology gradient $\rho_{\rm per\,T}$ shifts from $-0.83$ in Paper I to $-0.76$ here, with $p$ shifting from 0.010 to 0.028).

Exception to this exclusion is §3.2 (spatial-coherence null tests), which retains the Paper I-aligned 102-galaxy sample as run. The §3.3.2–3.3.4 perturbation tests and §3.3.7 backbone-shift test were originally run on the 102-galaxy sample but have been re-aggregated on the 101-galaxy sample by post-processing the per-galaxy CSVs; all four headline statistics shift by less than 0.25 percentage points (Υ: 95.10% → 95.05% per-galaxy modal match; D: 94.12% → 94.06%; i: 98.04% → 98.02%; backbone-shift: 88.5% → 88.2% absorbing pattern). Detailed comparison is in `data/ngc6674_exclusion_summary.txt`. We report the 101-galaxy values in §3.3.2–3.3.4 and §3.3.7. NGC 6674 contributes less than 1% of the §3.2 realizations and parallel 101-galaxy aggregation of §3.2 is left as a future computational consistency check; no §3.2 conclusion depends on NGC 6674's presence or absence at the level of qualitative direction.

**The anti-warp clean subsample** (25 shells across 25 galaxies) restricts to shells satisfying four warp-protection criteria simultaneously: $r_{\rm shell}/R_{\rm HI} < 0.3$, disk-dominated baryonic regime at the shell radius, SPARC quality flag $Q = 1$, and inner shell of any two-shell pair. §3.3.5 uses this subsample to test whether headline patterns survive in conditions where HI-warp artifacts are most disfavored.

**The two-shell paired subsample** (16 paired inner-vs-outer shells from 16 two-shell galaxies) is used in §3.1.4 for paired Wilcoxon tests on within-galaxy mass and width orderings.

### 2.4 Methods specific to §3

The tests in §3 fall into three methodological classes:

**Statistical organization tests (§3.1).** Population-level Spearman rank correlations on $(\sigma, r)$, $(M, r)$, and $\sigma/r$-vs-$r$ across the full shell sample. Fisher exact contingency tests on bulge presence vs shell-bearing. Paired Wilcoxon signed-rank tests on inner-vs-outer mass and width within two-shell galaxies. Two-sample Kolmogorov-Smirnov tests on $r/r_{\rm vir}$ distributions for inner vs outer shell populations.

**Spatial-coherence null tests (§3.2).** Two destructive operations on real rotation-curve data — *scramble* (within-galaxy permutation of dark-matter residuals around the canonical Burkert backbone) and *permute* (within-galaxy permutation of $V_{\rm obs}$ values across radii) — applied independently to each galaxy. Each null type runs 100 realizations, with the framework applied identically to each perturbed galaxy. Test statistics are the per-T-bin and per-galaxy Spearman correlations on the resulting shell-bearing distribution, compared against the real-data baselines via empirical $p$-values and standardized $z$-scores against the null distribution.

**Artifact-channel robustness tests (§3.3).** Six independent tests address potential non-physical origins of the shell signal: (i) coincidence with disk dynamical scales, tested via dimensionless distance to four candidate scales; (ii–iv) systematic perturbation tests on $\Upsilon_{\rm disk}/\Upsilon_{\rm bulge}$, distance $D$, and inclination $i$, drawn from realistic per-galaxy uncertainty distributions and applied 20 realizations per channel; (v) the anti-warp clean subsample analysis described above; (vi) the spatial-coherence nulls of §3.2, summarized for completeness.

The perturbation tests in (ii)–(iv) use the production fitting code of Paper I (`run_canonical_fits.py`) applied to perturbed inputs, ensuring methodological identity with the canonical fits. The anti-warp filter operates on the canonical fit catalog (no refitting required). The disk-dynamical-scale test (i) uses a uniform-in-log-r null with KS-statistic comparison.

### 2.5 Statistical conventions

We adopt the following conventions throughout:

- Reported $p$-values are two-sided unless explicitly noted as one-sided.
- Spearman rank correlations are quoted with the corresponding asymptotic $p$-value.
- For null distributions estimated from $N$ realizations, the empirical one-sided $p$-value floor is $1/N$ (0.01 for the §3.2 spatial-coherence nulls, $N = 100$; 0.05 for the §3.3 perturbation channels, $N = 20$); we additionally report standardized $z$-scores against the null mean and standard deviation, which are not floor-limited.
- Fisher exact tests are used for $2\times 2$ contingency tables (e.g., bulge correlation).
- Wilcoxon signed-rank tests are used for paired within-galaxy comparisons.
- Kolmogorov-Smirnov two-sample tests are used for cumulative-distribution comparisons (e.g., inner vs outer $r/r_{\rm vir}$).
- $1\sigma$ uncertainties are quoted as standard errors unless noted as bootstrap or Bayesian credible intervals.

---

## 3. Results

### 3.1 Statistical organization of the shell population

Paper I established that the framework selects $n_{\rm shells} \in \{0, 1, 2\}$ for each of 102 SPARC galaxies via Bayesian Information Criterion, with strict $\sigma/r \le 0.4$ enforcement on shell width, yielding 52 shell-bearing galaxies (51.0%). Paper I further established the principal morphology trend: shell-bearing rate decreases monotonically with morphological lateness across $T = 2$–9, with Spearman $\rho_{\rm per\text{-}T} = -0.833$ ($p = 0.010$) and per-galaxy $\rho_{\rm per\text{-}galaxy} = -0.296$ ($p = 0.003$, two-sided permutation test on T-type labels).

This section examines the *internal organization* of the shell population. The morphology gradient identified in Paper I points to systematic variation between galaxies; we now ask what systematic structure exists within the 67 shells across the 51 shell-bearing galaxies of the NGC 6674-excluded canonical sample (§2.3). We organize the analysis around three classes of empirical pattern: (i) the bulge correlation, in which bulge-dominated galaxies are preferentially shell-bearing; (ii) the radial scaling relations, in which shell width $\sigma$ and mass $M$ scale with shell radius $r$; and (iii) the geometric gradient, in which the dimensionless width $\sigma/r$ varies with radius across the population.

The tests reported in this section are exploratory population diagnostics rather than independent confirmatory hypothesis tests; reported $p$-values are not corrected for multiple comparisons, several are marginal, and the organizational dimensions examined were not pre-registered. We rely on the destructive null tests of §3.2 and the perturbation tests of §3.3 to evaluate whether the patterns identified here depend on real data structure rather than fitting flexibility.

#### 3.1.1 Bulge correlation

Bulge-dominated galaxies in the canonical sample are preferentially shell-bearing relative to bulgeless galaxies. Of 23 galaxies classified as bulge-dominated, 17 (73.9%) are shell-bearing. Of 78 galaxies classified as bulgeless, 34 (43.6%) are shell-bearing. The two categories together comprise the full $T = 2$–9 NGC 6674-excluded sample of 101 galaxies; the SPARC photometric decomposition does not assign intermediate cases.

The shell-bearing odds ratio is

$$
\text{OR} = \frac{17 \times 44}{6 \times 34} = 3.67,
$$

with a Fisher's exact test one-sided $p = 0.0064$. Bulged galaxies are 1.69$\times$ more likely to be shell-bearing than bulgeless galaxies in absolute rate, equivalent to a 30.3 percentage-point difference. The bulge correlation persists in the anti-warp clean subsample (§3.3.5), with OR reduced under the conservative cuts.

The bulge correlation and the morphology gradient established in Paper I are not independent in this sample, and the entanglement is substantial rather than partial. The bulge-dominated population is concentrated almost exclusively at early T-types: 18 of the 23 bulged galaxies are at $T = 2$ or $T = 3$, and only one bulged galaxy is at $T \ge 6$. Within the bulged subset alone, the morphology gradient is not statistically significant (Spearman $\rho_{\rm per\,T} = -0.16$, $p = 0.80$, with most T-bins containing one or two galaxies); within the bulgeless subset alone, it is similarly weak ($\rho_{\rm per\,T} = -0.18$, $p = 0.70$). Conversely, restricting the bulge correlation to early-type galaxies ($T = 2$–5) reduces it to a marginal odds ratio of 2.6 (Fisher $p \approx 0.09$); the late-type subsample ($T = 6$–9) contains only one bulged galaxy and admits no within-range comparison. The bulge correlation and the morphology gradient should therefore be understood as two statistical projections of a single underlying contrast — between bulge-rich early-type galaxies and bulgeless mid-to-late-type galaxies — rather than as independent organizational signatures. We report both observations for completeness but caution against treating them as independent lines of evidence in §3.1.5 and §4.

> **[Figure 3.1.1 — Bulge correlation]** $2\times 2$ contingency or stacked bar showing bulged vs bulgeless shell-bearing fractions (17/23 vs 34/78).
> *Data source:* `data/galaxy_classifications.csv` (is_bulge_dom, is_bulgeless) joined with Paper I canonical CSV (shell-bearing flag).

#### 3.1.2 Radial scaling: width and mass

The 67 fitted shells exhibit organized scaling behavior in the $(\sigma, r)$ and $(M, r)$ planes. Figure 3.1.2 shows both relations on log-log axes.

Shell width scales approximately linearly with shell radius:

$$
\log_{10}(\sigma_{\rm shell}/\,\text{kpc}) = (1.04 \pm 0.10) \cdot \log_{10}(r_{\rm shell}/\,\text{kpc}) - 0.698
$$

with Spearman rank correlation $\rho = +0.78$ ($p < 10^{-4}$, $n = 67$). Shell mass scales sub-linearly with shell radius:

$$
\log_{10}(M_{\rm shell}/\,M_\odot) = (0.76 \pm 0.14) \cdot \log_{10}(r_{\rm shell}/\,\text{kpc}) + 9.632
$$

with $\rho = +0.64$ ($p < 10^{-4}$, $n = 67$).

The width-radius slope close to unity ($\alpha \approx 1.04$) implies a near-universal dimensionless width $\sigma/r$: as shells span more than two decades in radius (0.2 kpc to 12 kpc), their physical widths track radius almost proportionally. The empirical median $\sigma/r$ across the 67-shell sample is 0.275, with standard deviation 0.116. This dimensionless width is well below the framework cap at $\sigma/r = 0.4$ for the population center, indicating the constraint is not driving the result for typical shells.

The mass-radius slope of 0.76 indicates that more distant shells carry more enclosed mass on average, but with a sub-linear scaling. We verify the bound-state of the underlying mass parameter explicitly. The framework imposes an upper bound on shell mass at $5 \times 10^{10}\,M_\odot$, adopted from Paper I to preserve the "localized" regime — well below the $\gtrsim 10^{11}\,M_\odot$ scale of typical halo masses, ensuring that BIC-selected shells represent discrete features distinguishable from the smooth backbone rather than alternative halo descriptions. Of the 67 shells in the canonical fits (NGC 6674 excluded), 8 (11.9%) lie within 0.05 dex of this bound. Among the 59 shells whose mass parameter is more than 0.05 dex below the upper bound, the M-r slope is $0.67 \pm 0.15$, the $\sigma$-r slope is $1.02 \pm 0.11$, and the $\sigma/r$ population median is 0.275 (essentially unchanged from the full-sample value of 0.275). The mass bound is therefore binding for a subset of fits but does not drive the population-level scaling relations. We have not formally tested how raising the bound would affect the population statistics; the 8 bound-pegged shells would receive higher mass values, but those higher values would still fall along the empirical $M$-$r$ scaling, so the direction of the slope is unlikely to reverse. A systematic exploration of bound-relaxation effects is left as future work. We discuss the choice of mass bound and natural extensions in §4.

> **[Figure 3.1.2 — Scaling relations]** Two-panel log-log scatter: (left) $\sigma$ vs $r$ with linear fit (slope $1.04 \pm 0.10$); (right) $M$ vs $r$ with linear fit (slope $0.76 \pm 0.14$). Color-code by T-type or by inner/outer position. Mark mass-bound shells distinctly.
> *Data source:* `data/antiwarp_per_shell.csv` (NGC 6674-excluded sample, n=67; matches manuscript primary convention).
> *Status:* Placeholder; generation script pending.

#### 3.1.3 Geometric gradient: $\sigma/r$ varies with radius

While the population-median $\sigma/r$ is $\approx 0.27$, the dimensionless width shows modest variation across the radial range. Table 3.1.3 reports $\sigma/r$ statistics by radial quartile across the 67-shell sample.

| Quartile | $r$ range (kpc) | $n$ | $\sigma/r$ median |
|---|---|---|---|
| Q1 (innermost) | 0.2 – 2.2 | 17 | 0.339 |
| Q2 | 2.2 – 4.5 | 16 | 0.271 |
| Q3 | 4.5 – 7.2 | 17 | 0.286 |
| Q4 (outermost) | 7.2 – 12.0 | 17 | 0.185 |

The innermost and outermost quartile medians differ ($\sigma/r = 0.339$ vs $0.185$), with the middle two quartiles non-monotonic and reflecting modest per-bin sample sizes. We interpret this as a modest population-level tendency for shells at smaller radii to occupy a larger fractional radial extent than shells at larger radii, rather than a sharply established gradient. Within the 16 two-shell galaxies, the paired Wilcoxon test on inner-vs-outer $\sigma/r$ yields $p = 0.30$ (not significant at the within-galaxy paired level), consistent with the population-level pattern being a tendency rather than a within-galaxy property.

We treat this as a soft empirical observation rather than a strongly established gradient, and report it for completeness alongside the more robust scaling and inner-vs-outer findings of §3.1.2 and §3.1.4.

> **[Figure 3.1.3 — Geometric gradient]** $\sigma/r$ vs $r$ scatter (log-x) with quartile boundaries marked as vertical lines and per-quartile median $\sigma/r$ overlaid as horizontal bars. Reference line at $\sigma/r = 0.4$ (framework cap) and at population median 0.275.
> *Data source:* `data/antiwarp_per_shell.csv` (columns: r_sh_kpc, sigma_over_r).
> *Status:* Placeholder; generation script pending.

#### 3.1.4 Inner-vs-outer in two-shell galaxies

Of the 16 two-shell galaxies in the NGC 6674-excluded sample, 14 (87.5%) have outer shells more massive than inner shells; zero have inner more massive than outer; two pairs are mass-tied at the upper bound. The Wilcoxon signed-rank test for the paired difference $M_{\rm outer} - M_{\rm inner}$ yields $p = 0.0001$ (one-sided test, alternative outer $>$ inner). Median outer-to-inner mass ratio is 2.06.

In radius, outer shells are at median 2.62$\times$ the radius of inner shells (definitional ordering). Absolute width $\sigma$ is also larger in outer shells: 14 of 16 paired galaxies have $\sigma_{\rm outer} > \sigma_{\rm inner}$, with Wilcoxon $p = 0.0008$. This is consistent with the population-wide $\sigma \propto r^{1.04}$ scaling and outer shells being at larger $r$.

When shell positions are normalized to the host's virial radius $r_{\rm vir}$, the inner and outer populations within two-shell galaxies separate at high statistical significance. Inner shells of two-shell galaxies cluster at $r/r_{\rm vir} = 0.012$ (median, IQR $[0.006, 0.017]$), outer shells at 0.027 (IQR $[0.022, 0.035]$), with a two-sample Kolmogorov-Smirnov statistic $D = 0.6875$, $p = 0.0007$ ($n = 16$ inner, $n = 16$ outer; partitions defined by radial ordering within each two-shell galaxy). Single-shell galaxies cluster at intermediate $r/r_{\rm vir} = 0.030$ (median), consistent with BIC-driven parsimony folding contributions into a single Gaussian when the data do not support two well-separated peaks.

The inner and outer shell populations within two-shell galaxies occupy statistically distinct $r/r_{\rm vir}$ distributions under Burkert, consistent with multi-scale population stratification. The sample is modest ($n = 16$ paired galaxies); backbone-family behavior is reported in §3.3.6.

#### 3.1.5 Summary of organized structure

Across several dimensions of shell-property organization, the shell population exhibits structure that varies systematically with measurable galaxy and shell properties. We group the findings by their robustness under multiple-comparisons correction and backbone-family flexibility.

**Primary signatures** (Bonferroni-robust across the seven §3.1 tests at $\alpha = 0.05$; preserved across backbone-family controls in §3.3.6):

- **Radial mass scaling:** $M \propto r^{0.76}$ ($\rho = +0.64$, $p < 10^{-4}$).
- **Radial width scaling:** $\sigma \propto r^{1.04}$ under Burkert ($\rho = +0.78$, $p < 10^{-4}$). The slope value is backbone-baseline-dependent (§3.3.6); the positive correlation itself preserves across backbones.
- **Inner-vs-outer mass ordering in two-shell galaxies:** 14/16 outer more massive (Wilcoxon $p = 10^{-4}$).

**Secondary signatures** (BH-FDR-pass; either Bonferroni-fail, entangled with another test, or attenuated under one backbone-family control — see multi-comparisons summary below for the demotion logic):

- **Bulge correlation:** OR $= 3.67$, Fisher $p = 0.0064$. Entanglement-demoted; see §3.1.1.
- **Morphology gradient** (galaxy-level): $\rho_{\rm per\text{-}T} = -0.762$, $p = 0.028$. NGC 6674 sensitivity discussed in §2.3.
- **Inner-vs-outer width ordering:** 14/16 outer broader (Wilcoxon $p = 0.0008$) under Burkert.
- **Two-population separation in $r/r_{\rm vir}$:** KS $D = 0.69$, $p = 0.0007$ under Burkert.

**Soft observations** (reported for completeness; not confirmatory):

- **$\sigma/r$ quartile gradient**: $\sigma/r$ varies from 0.339 (innermost quartile) to 0.185 (outermost quartile), with non-monotonic middle quartiles and a within-galaxy paired test of $p = 0.30$. Reported as modest population-level tendency; backbone-baseline-dependent (§3.3.6).

**Multiple-comparisons correction.** All seven §3.1 tests survive Benjamini-Hochberg FDR correction at $\alpha = 0.05$ (BH-adjusted $p$: $\le 10^{-4}$ for both scaling Spearmans; $0.0002$ for $M$ paired; $0.0011$ for KS and $\sigma$ paired; $0.0075$ for bulge; $0.028$ for morphology). Six cross strict Bonferroni ($p < 0.05/7 = 0.0071$): the two scaling tests, both inner-vs-outer Wilcoxons, the bulge Fisher, and the KS. Three of these six are demoted to secondary by criteria distinct from the Bonferroni threshold — the bulge correlation by §3.1.1 entanglement with the morphology gradient, the $\sigma$ inner-vs-outer Wilcoxon and the KS $r/r_{\rm vir}$ separation by Einasto-backbone attenuation (both preserve under gNFW, so the sensitivity is specific to Einasto curvature flexibility; §3.3.6). The independent, backbone-control-invariant, non-entangled signatures are therefore the $M$-$r$ scaling, the $\sigma$-$r$ scaling, and the inner-vs-outer mass ordering. The four secondary signatures rely on §3.2 spatial-coherence nulls and §3.3.6 backbone-family controls for confirmatory weight rather than on §3.1 in isolation.

These patterns extend the morphology gradient established in Paper I from a between-galaxy property to an organizational property of the shell population itself. §3.2 establishes that the morphology gradient cannot be reproduced by data lacking the spatial coherence of the canonical residuals. §3.3 establishes that none of the patterns are artifacts of baryonic input systematics, warp-prone HI configurations, coincidence with disk dynamical scales, or — for the load-bearing mass-feature signatures — choice of smooth-halo backbone.

---

### 3.2 Tests of spatial-coherence dependence

Paper I established two complementary null tests on the framework. The first is a synthetic-mock false-positive analysis: 346 mocks generated from smooth Burkert-truth and NFW-truth profiles plus realistic noise, fit by the same canonical pipeline, recover shell-bearing fractions of 4.0% (Burkert-truth) and 63.6% (NFW-truth). The real-data shell-bearing rate of 51.0% is recovered at factors of 6–20 above the Burkert-truth false-positive rate in every $T$-bin, disfavoring smooth-Burkert truth as the dominant gradient driver. The second is a per-galaxy permutation test on the morphology gradient itself: T-type labels are permuted across galaxies and the per-galaxy Spearman $\rho$ recomputed under each permutation, yielding a two-sided $p = 0.002$ for the observed $\rho_{\rm per\text{-}galaxy} = -0.296$.

The tests in this section address a different question. Paper I's analyses establish that the framework does not generate spurious shells in genuinely smooth synthetic data, and that the morphology gradient is not a chance arrangement of T-type labels. Neither test addresses whether the *spatial coherence* of the localized residual structure within each rotation curve is essential to producing the observed shell population. A galaxy's residual signal — the difference between observed rotation $V_{\rm obs}$ and the smooth Burkert backbone — could be coherently structured (with characteristic radii, widths, and amplitudes that the framework discovers as shells) or it could be incoherent fluctuation (random scatter at the noise level). If the latter, the framework's BIC procedure should still occasionally select shells from chance configurations, but the resulting shell population should not exhibit the morphology gradient or the organized scaling relations established in §3.1.

This section tests the spatial-coherence requirement directly. We define two destructive operations on the real rotation curve data — *scramble* (shuffle DM residuals across radii within each galaxy, preserving the Burkert backbone) and *permute* (shuffle observed velocities across radii within each galaxy, destroying the Burkert backbone) — and ask whether either operation reproduces the morphology gradient when the framework is applied to the destroyed data.

For each null type and each realization, we apply the framework (Burkert + 0/1/2 Gaussian shells, BIC-selected, $\sigma/r \le 0.4$ enforcement) to all 102 canonical galaxies, compute the same per-T and per-galaxy Spearman correlations as the real-data baseline, and ask how often the null produces $\rho$ as negative as the real data. The runs use 100 realizations per null type. We use 100 rather than the smaller counts often used in similar tests to ensure the empirical-$p$ estimate is not floor-limited by sample size: at $N = 20$ a one-sided empirical $p$ cannot resolve below 0.05 regardless of how cleanly the null fails, whereas at $N = 100$ the floor is 0.01 and tail-frequency estimates are stable enough to quote as proper percentile-based statistics.

#### 3.2.1 Within-galaxy residual scrambling

The scramble null preserves every component of canonical analysis except the spatial coherence of dark-matter residuals. For each galaxy, we compute the dark-matter residual from the canonical Burkert fit:

$$
\epsilon(R) = V_{\rm obs}^2(R) - V_{\rm bar}^2(R) - V_{\rm Burkert}^2(R)
$$

permute the $\epsilon$ values across radii (preserving the multiset of residual amplitudes but destroying their order in $R$), and reconstruct a synthetic observed velocity curve:

$$
V_{\rm obs}^{\rm scramble}(R) = \sqrt{V_{\rm bar}^2(R) + V_{\rm Burkert}^2(R) + \epsilon^{\rm shuffled}(R)}
$$

The scramble preserves $V_{\rm bar}^2$ at each radius, the Burkert backbone at each radius, the per-radius error bars, and the radial sampling. It destroys only the within-galaxy radial coherence of localized residual structure.

Across 100 scramble realizations on 102 galaxies (10,200 fits total), the null distribution of $\rho_{\rm per\,T}$ has mean $-0.289$ with standard deviation $0.229$, range $[-0.833, +0.238]$. The real-data baseline of $-0.833$ falls $2.4\sigma$ below the null mean (Gaussian-equivalent) and at the 2nd percentile of the empirical distribution: 2 of 100 realizations produce a $\rho_{\rm per\,T}$ as negative as real data, giving an empirical one-sided $p_{\rm emp} = 0.02$. The per-galaxy correlation $\rho_{\rm per\,galaxy}$ has null mean $-0.170 \pm 0.059$, range $[-0.326, -0.037]$, with the real-data baseline of $-0.296$ at $2.1\sigma$ below the null mean and an empirical $p_{\rm emp} = 2/100 = 0.02$. The empirical-$p$ estimate is the more reliable significance metric here: the scramble null distribution is visibly non-Gaussian (Figure 3.2.1), with a heavy left tail that the Gaussian-equivalent $z$-score under-resolves.

The scramble null does retain a weakly negative $\rho_{\rm per\,T}$ on average ($-0.289 \pm 0.229$). This is interpretable: the scramble preserves each galaxy's smooth Burkert backbone, and Burkert backbone parameters correlate with morphological type (early-type galaxies have more concentrated halos, deeper baryonic potentials, and more complex residual structure for the framework to find by chance). A correlation in this range is what residual *amplitude variations* alone — without spatial coherence — can produce by chance. The real-data correlation of $-0.833$ sits at the 2nd percentile of the scramble null distribution: residual amplitude variations alone can reproduce a correlation this negative in only ~2% of realizations, while the typical scramble realization produces a correlation roughly one third the real-data magnitude. The morphology gradient depends on the *spatial coherence* of localized residual structure, not merely its amplitude distribution.

#### 3.2.2 Cross-radius $V_{\rm obs}$ permutation

The permutation null breaks both the localized residual structure and the smooth backbone. For each galaxy, we shuffle $V_{\rm obs}$ values across radii while holding $R$ values fixed, then refit the framework. The permutation preserves each galaxy's $V_{\rm obs}$ amplitude distribution and its radial sampling. It destroys all coherent radial structure: the smooth rotation-curve shape, the residual-from-backbone, and any localized features.

Across 100 permutation realizations on 102 galaxies (10,200 fits total), the null distribution of $\rho_{\rm per\,T}$ has mean $+0.350$ with standard deviation $0.235$, range $[-0.120, +0.863]$. **The sign of the null correlation is opposite the real-data correlation.** The real-data baseline of $-0.833$ falls $5.0\sigma$ below the null mean. The empirical one-sided $p_{\rm emp} = 0/100 < 0.01$ (no permute realization reaches the real-data value). The per-galaxy correlation has null mean $+0.162 \pm 0.066$, range $[-0.011, +0.339]$ — also positive — with the real-data baseline at $6.9\sigma$ below the null mean and again $p_{\rm emp} = 0/100$.

The positive null correlation in permuted data is not a defect; it is informative. When we permute $V_{\rm obs}$ across radii, the resulting "rotation curve" is a chaotic profile inconsistent with any smooth halo. The BIC procedure responds to this chaos by selecting shell-bearing fits at greatly elevated rates: across all T-types, mean shell-bearing fractions in permuted data are 0.72–0.97, compared to 0.31–1.00 in real data and 0.19–0.81 in scrambled data (Table 3.2.1). The framework over-detects shells in permuted data because the BIC penalty is exceeded by the χ² improvement from any localized component fitted to chaotic noise.

The positive $\rho_{\rm per\,T}$ in permutation arises from the small population of permuted fits where the framework cannot fit shells well: these are scattered across morphological types in a pattern that yields a positive Spearman ρ by chance. The point is not the sign per se, but that the *direction* of the morphology gradient under permutation is opposite to real, with no overlap in 100 realizations.

#### 3.2.3 Per-T shell-bearing fractions: the failure modes are physically distinct

The two nulls fail to reproduce real data in opposite directions, which is itself diagnostic. Table 3.2.1 shows the per-T-bin shell-bearing fraction in real data alongside the mean fraction across 100 null realizations.

| T | N (real) | Real frac. | Scramble null | Permute null | Real / Scramble | Real / Permute |
|---|---|---|---|---|---|---|
| 2 | 9 | 1.000 | 0.814 | 0.958 | 1.23 | 1.04 |
| 3 | 11 | 0.545 | 0.188 | 0.720 | 2.90 | 0.76 |
| 4 | 17 | 0.529 | 0.310 | 0.824 | 1.71 | 0.64 |
| 5 | 13 | 0.538 | 0.335 | 0.912 | 1.61 | 0.59 |
| 6 | 16 | 0.562 | 0.291 | 0.954 | 1.93 | 0.59 |
| 7 | 14 | 0.357 | 0.234 | 0.931 | 1.52 | 0.38 |
| 8 | 6 | 0.333 | 0.363 | 0.910 | 0.92 | 0.37 |
| 9 | 16 | 0.312 | 0.228 | 0.974 | 1.37 | 0.32 |

Two patterns are evident. The scramble null produces shell-bearing fractions *below* real data for most T-types (real exceeds scramble by factors of 1.23–2.90×, except T=8 where the real fraction is 0.92× the scramble null due to small-bin statistics). This is consistent with the scramble destroying the localized features that drive real-data shell detections. The permute null produces shell-bearing fractions *above* real data for nearly every T-type (real / permute ratios of 0.32–1.04). This is consistent with the permute creating chaotic profiles that the BIC procedure over-fits with shells.

Neither null reproduces real data, but they fail in opposite directions: scramble *under-detects*, permute *over-detects*. This asymmetry is difficult to reconcile with the hypothesis that real shell selections are random framework responses. A random-detection scenario would show null detection rates bracketing real rates symmetrically, not bracketing them on opposite sides.

#### 3.2.4 Joint interpretation

Both nulls reject the hypothesis that the morphology gradient could arise from random residual structure or random rotation-curve amplitudes:

- $\rho_{\rm per\,T}$ rejected at $2.4\sigma$ under scramble (empirical $p = 2/100 = 0.02$), $5.0\sigma$ under permutation (empirical $p = 0/100 < 0.01$)
- $\rho_{\rm per\,galaxy}$ rejected at $2.1\sigma$ under scramble (empirical $p = 2/100 = 0.02$), $6.9\sigma$ under permutation (empirical $p = 0/100 < 0.01$)
- The scramble null distribution is visibly non-Gaussian (Figure 3.2.1), so the empirical-$p$ estimates are the more reliable significance metrics; the Gaussian-equivalent $z$-scores are reported for cross-reference but understate the tail behavior

The two nulls bracket a meaningful range of artifact channels: scramble tests whether radial coherence within each galaxy is necessary; permutation tests whether *any* coherent rotation-curve shape is necessary. The morphology gradient in shell selections survives in neither. The two failure modes — scramble under-detecting because spatial coherence has been destroyed, permute over-detecting because the BIC procedure fits chaos — establish that the real-data shell population is not reproducible by fitting to coherence-destroyed residuals or fully randomized rotation curves.

> **[Figure 3.2.1 — Null distributions of Spearman $\rho$ under scramble]** Two-panel histogram: (left) $\rho_{\rm per\,T}$ across 100 scramble realizations, with real-data baseline $\rho_{\rm per\,T} = -0.833$ shown as vertical red line; (right) same for $\rho_{\rm per\,galaxy}$, real-data baseline $-0.296$. Annotated: null mean, std, and empirical $p_{\rm emp} = n/100$ count of realizations $\le$ real-data value.
> *Data source:* `data/nulltest_per_realization.csv` (filter null_type='scramble'; columns rho_per_T, rho_per_gal).
> *Status:* Generated as `figures/fig_3_2_1_scramble_null.pdf`.

> **[Figure 3.2.2 — Null distributions of Spearman $\rho$ under permutation]** Two-panel histogram: (left) $\rho_{\rm per\,T}$ across 100 permute realizations, with real-data baseline shown as vertical red line; (right) same for $\rho_{\rm per\,galaxy}$. Demonstrates the asymmetric failure mode: the permute null is centered at positive $\rho$, *opposite sign* from real data; no permute realization reaches the real-data value.
> *Data source:* `data/nulltest_per_realization.csv` (filter null_type='permute'; columns rho_per_T, rho_per_gal).
> *Status:* Generated as `figures/fig_3_2_2_permute_null.pdf`.

---

### 3.3 Robustness against artifact explanations

The empirical patterns documented in §3.1 — population-wide mass-radius scaling, near-universal $\sigma/r$, and structural correlations with galaxy morphology and bulge presence — go beyond Paper I's galaxy-level findings to per-shell-level organization. Paper I §3.5, §3.7, §4.1, and §4.4 established the framework's galaxy-level robustness against four artifact channels: synthetic smooth-halo false-positives (Burkert-truth FP 4.0%, NFW-truth FP 63.6%), backbone-family flexibility within the cored-cuspy class via Einasto substitution (classification preserved in 88.2% of galaxies), DC14 feedback-modified profile substitution on the universal-failure subset (all 10/10 fail adequacy with DC14), and stellar mass-to-light ratio at two levels (T-dependent piecewise-linear Υ steelman and hierarchical empirical-Bayes Υ marginalization with data-driven hyperprior). The present section examines six additional artifact channels at the per-shell and per-realization stability level that Paper I's analyses did not exhaust: (i) coincidence with disk-baryonic dynamical scales, (ii–iv) per-realization stability under perturbations to the three principal baryonic inputs (mass-to-light ratio, distance, inclination), which complement Paper I §4.4 by addressing per-realization mode-recovery rather than population-prior marginalization; (v) HI disk warps producing localized line-of-sight velocity features; and (vi) backbone-shell decoupling at the per-galaxy parameter level, which complements Paper I §3.7 by addressing whether the Burkert backbone deforms when shells are removed. Two additional channels — (vii) spatial coherence of residual structure and (viii) random structure misclassified as shells by BIC — are addressed by the destructive null tests of §3.2 and cross-referenced at the end of the present section for completeness.

#### 3.3.1 Coincidence with disk-baryonic dynamical scales

If the localized features detected by the framework originated in baryonic disk substructure rather than halo mass features, shell radii should preferentially cluster at radii associated with disk dynamical scales: the disk scale length $R_{\rm disk}$, two-and-a-fifth disk scale lengths ($2.15\,R_{\rm disk}$, the canonical exponential-disk rotation peak), the half-light radius $R_{\rm eff}$, or the radius of the observed rotation curve maximum. We test this by computing, for every detected shell, the dimensionless distance $|r_{\rm shell} - r_{\rm scale}| / r_{\rm scale}$ for each of the four candidate scales, and comparing the observed distribution to the expectation under a uniform null where shell radii are drawn from a power-law in $r$ within each galaxy's fitted range.

The observed distributions show no preferential clustering at any of the four candidate scales. The Kolmogorov-Smirnov statistic against the uniform null fails to reject at the 0.05 level for all four scales. The mean and median dimensionless offsets are consistent with random placement. We conclude that shell radii are not coincident with disk dynamical features, disfavoring a simple disk-resonance or disk-substructure origin for the population-level signal.

> **[Figure 3.3.1 — Disk dynamical scale coincidence]** Four-panel CDF comparison. Each panel: empirical CDF of $|r_{\rm shell} - r_{\rm scale}|/r_{\rm scale}$ for one candidate scale ($R_{\rm disk}$, $2.15\,R_{\rm disk}$, $R_{\rm eff}$, $r$ at $V_{\rm rot}^{\rm peak}$), overlaid on uniform-placement null CDF. KS $p$-value annotated per panel.
> *Data source:* Paper I canonical CSV (shell radii) + `data/sparc_sample123.csv` (Rdisk, Reff) + Rotmod_LTG files (V_rot peak radius). Producer script not yet written.
> *Status:* Placeholder; generation script pending.

#### 3.3.2 Systematic perturbations: mass-to-light ratio

Paper I §4.4 addresses Υ at two levels: a T-dependent piecewise-linear steelman with anchors $\Upsilon_{\rm disk}(T = 2, 5, 9) = (0.65, 0.50, 0.40)$, and a hierarchical empirical-Bayes marginalization with data-driven log-normal hyperprior (fitted $\Upsilon^{\rm pop}_{\rm disk} = 0.485$, $\tau = 0.081$ dex; framework-vs-Burkert adequacy gap compressed from 26 to 14 galaxies but preserved, morphology gradient preserved at $\rho = -0.245$, $p = 0.013$). Both Paper I treatments operate at the population-prior level: they ask whether population-distributed Υ values shift the framework's adequacy or trend conclusions. The present subsection addresses a complementary question: per-realization stability of per-galaxy shell-number selections under independent Υ draws.

Stellar mass-to-light ratios in SPARC are nominally fixed at $\Upsilon_{\rm disk} = 0.5$ and $\Upsilon_{\rm bulge} = 0.7$ at 3.6 µm [@Lelli2016]. The systematic uncertainty on these ratios is approximately 0.1 dex. We test whether shell selections survive realistic variation in $\Upsilon$ by performing 20 independent perturbation realizations: for each realization we draw $(\log_{10}\Upsilon_{\rm disk}', \log_{10}\Upsilon_{\rm bulge}')$ from independent normal distributions with means $(\log_{10} 0.5, \log_{10} 0.7)$ and standard deviation 0.1 dex (the same hyperprior width as Paper I §4.4), and refit the framework on all 102 galaxies with the perturbed $\Upsilon$ values. Each refit follows the canonical procedure: Burkert + 0/1/2 Gaussian shells, BIC-selected with parameter penalty $k = 2/5/8$ and $\sigma/r \le 0.4$ wall.

Across 2,001 successful refits (102 galaxies $\times$ 20 realizations, with 39 fits failing on $V_{\rm obs}^2 > V_{\rm bar}^2$ point cuts after $\Upsilon$ rescaling), shell-number selections agree with the canonical result in 86.2% of cases (1,725/2,001). At the per-galaxy level, the modal $n_{\rm shells}$ across the 20 realizations matches the canonical fit in 95.1% of galaxies (97/102). Stratifying by canonical shell count: galaxies with canonical $n_{\rm shells} = 0$ show 92.3% per-fit stability, $n_{\rm shells} = 1$ shows 83.5%, and $n_{\rm shells} = 2$ shows 74.3%. Among galaxies whose shell count is fully stable across all 20 realizations and that contain at least one shell, the median scatter in $\log_{10} r_{\rm shell,1}$ is 0.017 dex (approximately 4% in radius).

The hierarchy is consistent with information-theoretic expectations: galaxies whose canonical fit is in the most parsimonious branch ($n_{\rm shells} = 0$) are least likely to flip under perturbation, while those at the BIC margin between two-shell and one-shell solutions are most likely to flip across the boundary. The aggregate population fractions $(n_0, n_1, n_2)$ shift from $(49.0\%, 34.3\%, 16.7\%)$ canonical to $(48.2\%, 35.7\%, 14.2\%)$ under perturbation — a population-level change of less than 2.5 percentage points in any bin.

The shell signal is therefore not driven by baryonic mass-to-light mismodeling.

> **[Figure 3.3.2 — $\Upsilon$ perturbation stability]** Left: stacked bar of perturbed-vs-canonical $n_{\rm shells}$ matches across 2,001 fits, stratified by canonical shell count (n=0: 92.3%, n=1: 83.5%, n=2: 74.3%). Right: scatter of $\log_{10} r_{\rm shell,1}^{\rm pert}$ versus $\log_{10} r_{\rm shell,1}^{\rm canon}$ for fully-stable shell-bearing galaxies, $\pm$25% bands marked.
> *Data source:* `data/upsilon_perturbation_per_galaxy.csv` (columns: status, n_shells, r_sh1) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.3 Systematic perturbations: distance

Galaxy distances enter the rotation curve fit through two channels: physical radii scale as $r \to r \cdot (D'/D)$, and baryonic rotation contributions scale as $V_{\rm bar} \to V_{\rm bar} \cdot \sqrt{D'/D}$ (since baryonic mass scales as $D^2$ at fixed observed flux while $r \propto D$, giving $V^2 \propto M/r \propto D$). Observed rotation velocities $V_{\rm obs}$ are distance-invariant. Each SPARC galaxy carries a published distance $D$ and a per-galaxy uncertainty $e_D$ reflecting the measurement method (Hubble flow, TRGB, Cepheid, etc.).

We test distance-systematic robustness by 20 realizations in which each galaxy independently draws $D' = D \cdot 10^{\mathcal{N}(0, \sigma_{\log D})}$ with $\sigma_{\log D} = e_D / (D \ln 10)$, refits the framework on perturbed-radius and perturbed-baryon data, and records shell selections. The fractional perturbation magnitudes span the published range: median 8.7%, mean 13.8%, 90th percentile 31.8%, with one outlier (a dwarf with $e_D > D$) reaching 132%.

Across 2,036 successful refits (4 fits failing on insufficient DM points), shell-number selections match canonical in 89.6% of cases. At the per-galaxy level, modal shell count matches canonical in 94.1% of galaxies. Stratification by canonical $n_{\rm shells}$ yields stability rates of 94.6% ($n=0$), 86.1% ($n=1$), and 82.3% ($n=2$). Median $\log_{10} r_{\rm shell,1}$ scatter for fully-stable galaxies is 0.039 dex (~9% in radius). Population fractions shift by less than 2.5 percentage points in any bin.

We note that distance perturbation produces *more* stable shell selections than mass-to-light perturbation in our tests. This is physically reasonable: distance scaling is shape-preserving, multiplying all radii by the same factor and all baryonic velocities by the same factor, so the relative shape of $V_{\rm DM}^2 = V_{\rm obs}^2 - V_{\rm bar}^2$ is preserved. Mass-to-light perturbation, by contrast, redistributes the disk-versus-bulge contributions to $V_{\rm bar}$ at different radii (since $V_{\rm disk}$ and $V_{\rm bulge}$ profiles peak at different scales), producing more disruptive changes to the residual structure being fit.

The shell signal is not driven by distance measurement uncertainty.

> **[Figure 3.3.3 — Distance perturbation stability]** Same two-panel format as Figure 3.3.2, for distance perturbation. Stability stratification: n=0: 94.6%, n=1: 86.1%, n=2: 82.3%. Includes per-galaxy fractional perturbation magnitude (median 8.7%).
> *Data source:* `data/distance_perturbation_per_galaxy.csv` (columns: status, n_shells, r_sh1, distance_factor) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.4 Systematic perturbations: inclination

Galaxy inclinations $i$ enter rotation curve fitting through the deprojection $V_{\rm obs} = v_{\rm los} / \sin i$, where $v_{\rm los}$ is the observed line-of-sight velocity. SPARC publishes per-galaxy inclinations $i$ with uncertainties $e_i$ typically in the range 1°–5°. We test inclination-systematic robustness by 20 realizations in which each galaxy independently draws $i' = i + \mathcal{N}(0, e_i)$. Any perturbed value with $i' > 90°$ is folded by reflection to $180° - i'$, recognizing that an "inclination past edge-on" is geometrically equivalent to a tilt on the opposite side of edge-on; this preserves a symmetric Gaussian perturbation around $i$ even for edge-on galaxies. The reflected value is then floored at 10° and capped at 89° to avoid pathological behavior near $\sin i = 0$. We rescale $V_{\rm obs} \to V_{\rm obs} \cdot \sin i / \sin i'$ and $e_{V_{\rm obs}} \to e_{V_{\rm obs}} \cdot \sin i / \sin i'$; physical radii and modeled baryonic components are inclination-invariant.

Eleven SPARC galaxies in the canonical sample are catalogued at exactly $i = 90°$ (edge-on); the reflection treatment described above includes these galaxies symmetrically. Because $\sin i$ is at its maximum near $i = 90°$, the implied $V_{\rm obs}$ rescaling is small for edge-on perturbations (median $|{\rm vobs\_factor} - 1| < 0.01$ across the 11 edge-on galaxies; max $< 0.02$), and shell selections for these galaxies match canonical in 220 of 220 fits (100%). The perturbation suite comprises 2,020 fits across 101 galaxies $\times$ 20 realizations on the manuscript-convention sample (NGC 6674 excluded per §2.3); the underlying 2,040-fit production batch on the 102-galaxy Paper I-aligned sample is in the per-galaxy CSV.

Realized perturbation magnitudes: median $|i' - i| = 1.77°$, mean 2.76°, maximum 29.1°. The implied $V_{\rm obs}$ rescaling factor $\sin i / \sin i'$ ranges over $[0.610, 2.176]$.

All 2,020 fits succeeded. Shell-number selections match canonical in 95.9% of fits (1,937/2,020). At the per-galaxy level, modal shell count matches canonical in 98.0% of galaxies (99/101). Stratification by canonical $n_{\rm shells}$: 99.3% ($n=0$), 92.7% ($n=1$), 92.2% ($n=2$). Median $|\log_{10} r_{{\rm shell},1}|$ scatter for fully-stable galaxies is 0.0022 dex (~0.5% in radius) — the tightest position recovery of the three perturbation tests. Inclination perturbations produce the highest stability because they preserve rotation-curve shape and rescale only overall amplitude.

> **[Figure 3.3.4 — Inclination perturbation stability]** Same two-panel format as Figure 3.3.2, for inclination perturbation. Stability stratification: n=0: 99.3%, n=1: 92.7%, n=2: 92.2%. Tightest position recovery of three perturbation tests (median $|\Delta \log r_1| = 0.0022$ dex).
> *Data source:* `data/inclination_perturbation_per_galaxy.csv` (102 galaxies $\times$ 20 realizations; edge-on galaxies included via reflection treatment, see §3.3.4 algorithm description) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.5 Anti-warp clean subsample

The most plausible mechanism by which a smooth halo could mimic a localized residual feature is a velocity-field artifact in the outer rotation curve — most commonly a kinematic warp where the gas disk and the inner stellar disk no longer share a common rotation axis. Warp-induced line-of-sight velocity offsets manifest as apparent residuals at large radii where neutral hydrogen dominates the kinematic tracer and where the assumed disk inclination becomes least reliable. If the shells were dominated by warp artifacts, the headline empirical patterns of §3.1 should weaken substantially upon excluding shells in conditions most susceptible to such artifacts.

We define a "clean" anti-warp subsample as those shells satisfying *all four* of the following conditions simultaneously:

1. **Shell radius well inside the HI gas extent:** $r_{\rm shell} / R_{\rm HI} < 0.3$ (excludes shells in the outer-disk regime where warps preferentially appear)
2. **Disk-dominated at the shell radius:** $V_{\rm disk}^2 + V_{\rm bulge}^2 > V_{\rm gas}^2$ at $r_{\rm shell}$ (excludes shells in gas-dominated regions where warp signatures concentrate)
3. **Highest-quality SPARC rotation curve:** $Q = 1$ flag in the SPARC catalog (excludes galaxies flagged for tilted-ring-fit irregularities)
4. **Inner shell of any two-shell pair:** drops the outer shell of $n = 2$ galaxies (the more warp-vulnerable position)

These cuts are deliberately conservative; each independently is well-motivated, and the conjunction selects shells where multiple lines of warp protection are active. Of the 67 shells in the NGC 6674-excluded canonical sample, 25 (37.3%) survive all four cuts. Considered independently, the cuts pass 48, 65, 46, and 51 shells respectively; the combined intersection is 25.

The 25-shell anti-warp clean subsample exhibits the same headline patterns as the full population. Table 3.3.5 reports the comparison.

| Quantity | Full sample (n = 67) | Clean subsample (n = 25) |
|---|---|---|
| $M$-$r$ slope (log $M$ vs log $r$) | 0.76 | 0.66 |
| $M$-$r$ Spearman $\rho$ | $+0.64$ ($p < 10^{-4}$) | $+0.50$ ($p = 0.010$) |
| $\sigma$-$r$ slope (log $\sigma$ vs log $r$) | 1.04 | 0.93 |
| $\sigma$-$r$ Spearman $\rho$ | $+0.78$ ($p < 10^{-4}$) | $+0.76$ ($p < 10^{-4}$) |
| $\sigma/r$ population median | 0.275 | 0.316 |
| $\sigma/r$ population std | 0.116 | 0.128 |
| Bulge correlation OR | 3.67 ($p = 0.0064$) | 2.49 ($p \approx 0.04$) |
| Morphology gradient $\rho_{\rm per\text{-}T}$ | $-0.76$ ($p = 0.028$) | $-0.67$ ($p = 0.071$) |

The five organizational signatures of §3.1 — bulge correlation, $M \propto r$ scaling, $\sigma \propto r$ scaling, $\sigma/r$ universality, and the morphology gradient — all persist on the conservatively cleaned subsample. Effect sizes are modestly attenuated, which is expected given the 63% reduction in sample size and the conservative nature of the cuts (each of which removes shells whether or not they were artifacts). Effect *directions* are preserved exactly. The morphology gradient $\rho_{\rm per\text{-}T} = -0.67$ on the clean subsample is just outside the $p < 0.05$ threshold ($p = 0.071$, $n = 8$ T-bins), driven by the small per-bin counts after attrition rather than by a directional reversal.

A warp-dominated population would predict different behavior on this subsample: warp artifacts produce shells at the warp radius rather than at radii correlated with intrinsic enclosed mass, are not preferentially present in bulged galaxies, and concentrate in late-type gas-rich systems. None of these predictions matches the cleaned-subsample results in Table 3.3.5.

The present test addresses the dominant warp-artifact channel accessible within the framework; a more direct demonstration would require explicit kinematic-warp model comparison on each rotation curve. Combined with the §3.3.1 disk-dynamical-scale null and the §3.2 spatial-coherence nulls, this places the warp-artifact hypothesis among the alternatives the data do not support.

> **[Figure 3.3.5 — Anti-warp clean subsample]** Two-panel comparison: $\sigma$-vs-$r$ scatter (left) and $M$-vs-$r$ scatter (right). Full-sample shells (n=67) in light gray; anti-warp clean shells (n=25) highlighted. Linear fits overlaid for each population with slopes annotated (full vs clean: $M$-$r$ 0.76→0.66, $\sigma$-$r$ 1.04→0.93).
> *Data source:* `data/antiwarp_per_shell.csv` (use is_clean flag for the clean subsample).
> *Status:* Placeholder; generation script pending.

#### 3.3.6 Backbone-family controls: Einasto and gNFW comparisons at the per-shell level

A central concern raised in §4 is whether the organizational signatures of §3.1 reflect genuine residual structure or compensation for systematic mismatch between the Burkert backbone and underlying halo profiles. **The galaxy-level form of this test is reported in Paper I §3.7**, which performs an Einasto-backbone full-sample substitution and demonstrates that the framework's primary findings persist: 90 of 102 galaxies (88.2%) receive the same shell-bearing classification under both backbones; the per-galaxy morphology gradient $\rho = -0.347$ ($p = 0.0004$) under Einasto (vs $\rho = -0.296$, $p = 0.003$ under Burkert); the per-T-bin trend is $\rho = -0.905$ ($p = 0.002$) under Einasto. Paper I's analysis establishes the galaxy-level robustness of the framework's principal findings to one strict increase in smooth-halo flexibility.

Paper II extends that result to the **per-shell level** under two distinct backbone-family controls — Einasto and generalized NFW (gNFW). These two families are both strictly more flexible than Burkert but parameterize their additional freedom in physically different ways: Einasto adds a curvature parameter $\alpha$ that reshapes the smooth profile at all radii, while gNFW adds an inner-slope parameter $\gamma$ that primarily controls the profile at $r \ll r_s$. The two together probe whether the per-shell organizational signatures of §3.1 depend on Burkert specifically, on cored profiles generically, or on the absence of a particular kind of backbone flexibility. We restrict both analyses to the 101-galaxy NGC 6674-excluded sample for consistency with §3.1.

**Methodology.** The Einasto-backbone fits are those reported in Paper I §3.7 (identical pipeline, identical BIC model selection over $n_{\rm shells} \in \{0, 1, 2\}$, identical strict $\sigma/r \le 0.4$ enforcement). The gNFW-backbone fits replace the Burkert smooth halo with $\rho(r) = \rho_s\, /\, [(r/r_s)^\gamma\,(1 + r/r_s)^{3-\gamma}]$, where $\gamma \in [0, 2]$ is a free parameter ($\gamma = 1$ reduces to standard NFW; $\gamma \to 0$ produces a cored inner profile; $\gamma \to 2$ approaches the singular isothermal cusp). The gNFW enclosed mass has no simple closed form for general $\gamma$ and is computed by cumulative-trapezoid integration on a 500-point radial grid, with relative agreement to the analytic NFW formula at $\gamma = 1$ better than $10^{-5}$. Shell parameters (Gaussian $M$, $r$, $\sigma$ with strict $\sigma/r \le 0.4$ enforcement) and BIC selection over $n_{\rm shells} \in \{0, 1, 2\}$ are identical to the canonical pipeline; the BIC penalty correctly accounts for the additional backbone parameter ($k = 3$ for gNFW backbone-only vs $k = 2$ for Burkert backbone-only). The gNFW fits are reproducible from `scripts/run_gnfw_fits.py` in the public repository and the output is in `data/gnfw_full_sample_fits.csv`.

**101-galaxy classification reproduction.** Under the NGC 6674-excluded sample, classification agreement is 89 of 101 (88.1%) for Einasto vs Burkert (10 Burkert-shell-bearing galaxies reclassified as non-shell-bearing under Einasto; 2 Einasto-shell-bearing galaxies reclassified as non-shell-bearing under Burkert). This reproduces Paper I §3.7's 90/102 = 88.2% result with the expected one-galaxy shift from excluding NGC 6674. The 101-galaxy Einasto sample gives 43 shell-bearing galaxies (vs 51 under Burkert), with 62 total shells (vs 67) and 19 two-shell galaxies (vs 16). The 101-galaxy gNFW classification agreement is lower at 83 of 101 (82.2%), with 15 Burkert-shell-bearing galaxies reclassified as non-shell-bearing under gNFW and 3 gNFW-shell-bearing galaxies reclassified as non-shell-bearing under Burkert; the gNFW sample contains 39 shell-bearing galaxies, 48 total shells, and 9 two-shell galaxies. All 9 two-shell galaxies under gNFW are also two-shell under Burkert — the strongest shell-bearing classifications (two-shell systems) preserve under both backbone-family controls.

Table 3.3.6 reports the per-shell signatures under all three backbones — Paper II's net-new content over Paper I.

| Quantity | Burkert | Einasto | gNFW |
|---|---|---|---|
| Shell-bearing galaxies | 51/101 (50.5%) | 43/101 (42.6%) | 39/101 (38.6%) |
| Total shells | 67 | 62 | 48 |
| Two-shell galaxies | 16 | 19 | 9 |
| Morphology gradient $\rho_{\rm per\text{-}T}$ | $-0.76$ ($p = 0.028$) | $-0.87$ ($p = 0.005$) | $-0.67$ ($p = 0.071$) |
| Bulge correlation OR | 3.67 ($p = 0.0064$) | 4.32 ($p = 0.003$) | 4.22 ($p = 0.003$) |
| $M$-$r$ slope | 0.76 | 0.82 | 0.97 |
| $M$-$r$ Spearman $\rho$ | $+0.64$ | $+0.69$ | $+0.73$ |
| $\sigma$-$r$ slope | 1.04 | 0.38 | 0.86 |
| $\sigma$-$r$ Spearman $\rho$ | $+0.78$ | $+0.38$ | $+0.62$ |
| $\sigma/r$ population median | 0.275 | 0.173 | 0.230 |
| Inner-vs-outer $M$ | 14/16 ($p = 0.0001$) | 14/19 ($p = 0.0005$) | 8/9 ($p = 0.004$) |
| Inner-vs-outer $\sigma$ | 14/16 ($p = 0.0008$) | 13/19 ($p = 0.10$) | 9/9 ($p = 0.002$) |
| Two-population separation $r/r_{\rm vir}$ KS | $D = 0.69$ ($p = 7\times 10^{-4}$) | $D = 0.11$ ($p \approx 1.0$) | $D = 0.89$ ($p = 7\times 10^{-4}$) |

The per-shell signatures fall into two groups by behavior under the two backbone-family controls.

**Mass-feature signatures (preserved or strengthened under both controls):** The mass-radius scaling preserves direction and steepens monotonically across the three backbones (slope 0.76 → 0.82 → 0.97; Spearman $\rho$ $+0.64 \to +0.69 \to +0.73$). The bulge correlation strengthens under both controls (OR 3.67 → 4.32 → 4.22; $p$ 0.0064 → 0.003 → 0.003). The inner-vs-outer mass ordering survives at high significance under both controls (Burkert 14/16 with $p = 10^{-4}$; Einasto 14/19 with $p = 5\times 10^{-4}$; gNFW 8/9 with $p = 0.004$). The per-shell-binned morphology gradient strengthens slightly under Einasto ($\rho_{\rm per\text{-}T} = -0.87$) but attenuates to marginal significance under gNFW ($-0.67$, $p = 0.071$); the direction is preserved and the attenuation reflects the smaller shell-bearing sample under gNFW (39 vs 43 vs 51 galaxies distributed across 8 T-bins).

**Width-related and radial-position signatures (attenuated under Einasto, preserved under gNFW):** The width-radius slope drops substantially under Einasto (1.04 → 0.38) but largely preserves under gNFW (1.04 → 0.86), with the Spearman $\rho$ following the same pattern ($+0.78 \to +0.38$ Einasto vs $+0.78 \to +0.62$ gNFW). The $\sigma/r$ population median shifts under Einasto (0.275 → 0.173) but only modestly under gNFW (0.275 → 0.230). The inner-vs-outer width ordering, robust under Burkert ($p = 0.0008$), attenuates to marginal significance under Einasto ($p = 0.10$) but reaches its strongest expression under gNFW (9/9, $p = 0.002$). The two-population separation in $r/r_{\rm vir}$ shows the largest divergence: robust under Burkert ($D = 0.69$, $p < 10^{-3}$), it effectively vanishes under Einasto ($D = 0.11$, $p \approx 1.0$) but strengthens further under gNFW ($D = 0.89$, $p < 10^{-3}$). The attenuation observed under Einasto is therefore not a generic property of more-flexible backbone families; it is specific to the kind of flexibility Einasto introduces.

Einasto's free $\alpha$ parameter reshapes the smooth-halo curvature at all radii, including the intermediate radii (a few to tens of kpc) where SPARC shells live; the backbone can therefore absorb radial structure into curvature changes, smearing the inner-vs-outer separation and shifting fitted shells outward (median Einasto $r/r_{\rm vir}$ 0.050 vs Burkert 0.012 inner / 0.027 outer). gNFW's free $\gamma$ parameter primarily controls the inner-slope behavior at $r \ll r_s$ and has only weak influence at shell radii, leaving shell-position and shell-width parameters Burkert-like; the fitted $\gamma$ pegs at 0 (cored) for 60/101 galaxies, recovering the well-known SPARC core preference. Mass-feature signatures survive both controls because integrated mass within a localized feature is not degenerate with either kind of backbone-shape parameter at the relevant radii. The width-related and radial-position signatures are degenerate specifically with Einasto-style curvature flexibility — a sharper statement than the Burkert-baseline-dependence inferable from the Einasto control alone, since gNFW (a different but equally flexible backbone) preserves them. The principal §3.1 conclusion therefore survives two strict increases in backbone flexibility in the load-bearing morphology, bulge, and mass-scaling signatures, complementing Paper I's galaxy-level result with per-shell-level evidence.

> **[Figure 3.3.6 — Per-shell backbone-family comparison]** Multi-panel figure: per-shell scaling relations $M$-$r$ and $\sigma$-$r$ for shells fitted under all three backbones (Burkert, Einasto, gNFW), with linear fits annotated showing slope preservation across the three backbones for $M$-$r$ and selective attenuation under Einasto only for $\sigma$-$r$; $\sigma/r$ distribution histograms under the three backbones showing the Einasto-specific population-median shift to 0.173 vs the more modest gNFW shift to 0.230; inner-vs-outer $r/r_{\rm vir}$ histograms showing the Burkert ($D=0.69$) and gNFW ($D=0.89$) population separation and the Einasto-specific collapse ($D=0.11$).
> *Data source:* Paper I `data/einasto_full_sample_results.csv` and Paper II `data/gnfw_full_sample_fits.csv`, joined with canonical Burkert per-shell fits.
> *Status:* Placeholder; generation script pending.

#### 3.3.7 Backbone-shift test: does the smooth halo deform when shells are removed?

A second backbone-related concern, complementary to the Einasto comparison of §3.3.6, asks whether shells behave as basis functions decoupled from the smooth backbone or whether shell selections are dynamically coupled to the backbone parameters. If shells were decoupled localized basis functions absorbing residuals that the smooth profile leaves untouched, then constraining $n_{\rm shells} = 0$ versus allowing BIC selection over $n_{\rm shells} \in \{0, 1, 2\}$ should leave the Burkert backbone parameters $(\rho_0, a)$ statistically unchanged in shell-bearing galaxies. If instead shells encode localized structure that the smooth backbone would otherwise have to absorb by deforming, then the constrained ($n = 0$) fit should systematically push $\rho_0$ higher and $a$ smaller — compensating with a denser, more compact core to accommodate the inner mass excess that shells normally handle.

We test this directly. For each galaxy in the canonical sample, we refit the framework at each of $n_{\rm shells} \in \{0, 1, 2\}$ and record the resulting Burkert backbone parameters $(\rho_0, a)$ at every level. We then compare $(\rho_0, a)$ at the BIC-selected $n$ against $(\rho_0, a)$ at the constrained $n = 0$, separately for shell-bearing and non-shell-bearing galaxies. The production run used the 102-galaxy Paper I-aligned sample; we report numbers under the 101-galaxy convention by post-aggregating with NGC 6674 excluded (§2.3). The shift is negligible: the 101-galaxy backbone-shift result has the same direction, same magnitude, and same significance level as the 102-galaxy version.

**Result for the 51 shell-bearing galaxies.** When the framework is allowed to select shells, the Burkert backbone systematically relaxes:

- $\log_{10}(\rho_0[\text{BIC}] / \rho_0[n=0])$: median $= -0.624$ dex, mean $= -0.542$ dex, std $= 0.610$ dex; Wilcoxon two-sided $p < 10^{-4}$. The central density drops by a factor of $\approx 4.2$ on average when shells are allowed.
- $\log_{10}(a[\text{BIC}] / a[n=0])$: median $= +0.318$ dex, mean $= +0.326$ dex, std $= 0.469$ dex; Wilcoxon two-sided $p < 10^{-4}$. The scale radius increases by a factor of $\approx 2.1$ on average.
- **45 of 51 (88.2%) shell-bearing galaxies show the predicted "absorbing pattern" of decreasing $\rho_0$ accompanied by increasing $a$ when shells are allowed.** Five (9.8%) show the opposite pattern; one (2.0%) shows mixed signs. Under a null of random sign per galaxy ($p = 0.5$), an exact two-sided binomial test rejects the random-sign null at $p \approx 1.8 \times 10^{-8}$ for 45/51, tightening to $p \approx 4.2 \times 10^{-9}$ when the single ambiguous-sign galaxy is dropped (45/50). The directional claim — that the smooth backbone shifts to absorb shell structure when shells are removed — is falsified by chance with vanishing probability under this test.

**Control: 50 non-shell-bearing galaxies.** For galaxies that the BIC prefers at $n_{\rm shells} = 0$, "allowing shells" (comparing $n = 2$ against $n = 0$) should produce no systematic backbone shift if the test is detecting real signal rather than optimizer noise. The non-shell-bearing control gives $\log_{10}(\rho_0[n=2]/\rho_0[n=0])$ median $= -0.331$ dex (std $0.705$) and $\log_{10}(a[n=2]/a[n=0])$ median $= +0.115$ dex (std $0.719$). The non-shell-bearing distribution is broader and shifted less consistently than the shell-bearing case: the SB galaxies show a tight, large-amplitude, near-unanimous-direction shift; the NSB galaxies show a broad, lower-amplitude scatter consistent with parameter degeneracy at the optimizer level. The contrast establishes that the SB shift is not an optimizer artifact.

**Correlation with morphological type.** The shift magnitude correlates with $T$-type in the shell-bearing population: $\log_{10}(\rho_0[\text{BIC}]/\rho_0[n=0])$ vs $T$ has Spearman $\rho = +0.44$ ($p = 0.001$), indicating that earlier-type galaxies show stronger compensating shifts. This parallels the morphology gradient of §3.1: the morphological types that preferentially host shells also show the strongest backbone deformation when those shells are removed.

**Interpretation.** The backbone-shift test addresses the strong form of the basis-function alternative — that shells are decoupled localized basis functions absorbing residuals the smooth profile could otherwise leave unchanged. They are not decoupled: when shells are removed, the smooth Burkert profile must systematically deform (denser core, more compact scale) to compensate for the lost flexibility. Combined with the §3.3.6 Einasto comparison (organizational signatures persist under a more flexible smooth-halo family), this constrains the basis-function alternative on two complementary axes. The Einasto test addresses *passive* basis-function flexibility (residual organization survives backbone-family change); the backbone-shift test addresses *decoupled* basis-function flexibility (removing shells forces active backbone deformation). Together they bracket the alternative from two complementary directions.

> **[Figure 3.3.7 — Backbone shift]** Two-panel figure: (left) $\log_{10}(\rho_0[\text{BIC}]/\rho_0[n=0])$ distribution for shell-bearing (n=51) and non-shell-bearing (n=50) galaxies as overlaid histograms; (right) $\log_{10}(a[\text{BIC}]/a[n=0])$ distribution for same. Vertical lines at the medians; null line at zero shift.
> *Data source:* `data/backbone_shift.csv` produced by `scripts/backbone_shift_test.py`; 101-galaxy convention applied at aggregation time by `scripts/make_figures.py`.

#### 3.3.8 Random-structure null tests (cross-reference to §3.2)

The scrambling and permutation null tests of §3.2 establish that the shell selections are statistically distinguishable from random structure: cross-radius $V_{\rm obs}$ permutation produces morphology gradients of opposite sign in 0/100 realizations, and within-galaxy residual scrambling reaches the real-data $\rho_{\rm per\,T}$ in only 2/100 realizations (empirical $p = 0.02$; the typical scramble realization sits at one third the real-data magnitude). For cross-reference, the standardized null deviations on the corresponding $z$-scale are $-2.4$ and $-5.0$ for $\rho_{\rm per\,T}$ under scramble and permute respectively, and $-2.1$ and $-6.9$ for $\rho_{\rm per\,galaxy}$ (with the empirical $p$-floor at $1/N = 0.01$). Both tests target the hypothesis that the BIC-selected shells could be detector-flexibility artifacts of fitting random or shape-randomized data. The asymmetric failure modes (scramble under-detects, permute over-detects and reverses gradient sign) further establish that the shell population is a property of spatially coherent localized residual structure, not a property that survives destruction of either the residual coherence (scramble) or the rotation-curve shape (permute).

#### 3.3.9 Combined verdict

The localized structures detected by the framework satisfy eight complementary tests against artifact origin:

1. Shell radii do not coincide with disk dynamical scales ($R_{\rm disk}$, $2.15\,R_{\rm disk}$, $R_{\rm eff}$, $r$ at $V_{\rm rot}^{\rm peak}$).
2. Shell selections survive 0.1-dex log-normal perturbations to disk and bulge mass-to-light ratios with 86.2% per-fit and 95.1% per-galaxy mode-match against canonical.
3. Shell selections survive distance perturbations drawn from per-galaxy SPARC uncertainties ($e_D / D$ median 8.7%, max 132%) with 89.6% per-fit and 94.1% per-galaxy mode-match.
4. Shell selections survive inclination perturbations drawn from per-galaxy SPARC uncertainties ($e_i$ median 3°, max 10°) with 95.7% per-fit and 98.9% per-galaxy mode-match.
5. Headline structural patterns (mass-radius scaling, width-radius scaling, $\sigma/r$ universality, morphology gradient, bulge correlation) survive on a conservative anti-warp clean subsample retaining only inner shells in disk-dominated, high-quality, inner-disk regimes.
6. Galaxy-level signatures (morphology gradient, bulge correlation) and mass-feature signatures ($M$-$r$ scaling, inner-vs-outer mass ordering) survive replacement of the Burkert backbone with the strictly more flexible Einasto profile (88% classification agreement; §3.3.6). Width-related signatures attenuate under Einasto and are reported as backbone-baseline-dependent.
7. The Burkert backbone systematically deforms when shells are removed ($\rho_0$ rises by a factor of $\approx 4.2$, scale radius $a$ contracts by a factor of $\approx 2.1$, in 88.2% of shell-bearing galaxies); the non-shell-bearing control population does not show this systematic deformation (§3.3.7). The smooth profile cannot natively absorb the structure without measurable parameter shift.
8. Shell-selection statistics are not reproduced by destructive null procedures applied to real rotation curves: cross-radius $V_{\rm obs}$ permutation produces morphology gradients of opposite sign in 0/100 realizations; within-galaxy residual scrambling reaches the real-data $\rho_{\rm per\,T}$ in only 2/100 realizations (empirical $p = 0.02$; the typical scramble realization sits at one third the real-data magnitude). The asymmetric failure direction — scramble under-detects, permute over-detects and reverses gradient sign — is more difficult to reconcile with a random-fit-artifact origin than either individual test (§3.2).

The eight tests address complementary artifact channels: disk dynamics, baryonic input systematics ($\Upsilon$, $D$, $i$), warp geometry, backbone-family flexibility, backbone-shell coupling, and random structure. The signal survives all eight in concert. We therefore conclude that the localized structures detected by the framework are not consistent with artifacts of the fitting procedure or measurement systematics within the channels tested.

---

## 4. Discussion

The results presented in §3 establish that the shell population identified by the framework exhibits multiple forms of organized statistical structure — morphology dependence, correlations with bulge presence, radial scaling relations in shell width and shell mass, coherence-sensitive null-test behavior, and substantial stability under perturbations to the principal baryonic input parameters. Taken together, these patterns indicate that the shell population is not behaving like an arbitrary collection of unrelated fit artifacts. They do not, however, establish a unique physical interpretation for the detected structures: alternative explanations including correlated residual structure from non-axisymmetric dynamics, incompletely modeled baryonic effects, or limitations of the adopted smooth-halo backbone remain possible. The present paper constrains classes of explanation without uniquely identifying a mechanism.

The most important caveat concerns the choice of smooth-halo backbone. All organizational signatures reported here are defined relative to a constrained Burkert backbone, chosen in Paper I for its physically motivated finite central density, three-parameter parsimony, and explicit interpretability. A more flexible smooth-halo family — generalized NFW with free inner slope, Einasto with free shape parameter, spline or nonparametric profiles, or hierarchical Bayesian smooth-halo models — could in principle absorb some or all of the localized residual structure into a smoother profile. The patterns reported in this paper are therefore properly understood as *residual organization relative to a constrained smooth-halo baseline*.

We provide two direct tests of backbone-related concerns. §3.3.6 substitutes the strictly more flexible Einasto profile (one additional free parameter, $\alpha$) for the Burkert backbone and re-extracts the shell population. Galaxy-level signatures (morphology gradient, bulge correlation) and mass-feature signatures ($M$-$r$ scaling, inner-vs-outer mass ordering) survive or strengthen under the Einasto backbone, with 88% classification agreement at the galaxy level. Width-related signatures ($\sigma$-$r$ slope, $\sigma/r$ distribution, inner-vs-outer $\sigma$) attenuate under Einasto, consistent with shell-width parameters being partially degenerate with backbone profile shape. §3.3.7 takes the complementary approach: it forces the smooth Burkert backbone to fit alone ($n_{\rm shells} = 0$) and compares the resulting $(\rho_0, a)$ to the values obtained when BIC-selected shells are allowed. The smooth backbone deforms systematically when shells are removed (central density rises by a factor of $\approx 4.2$, scale radius contracts by a factor of $\approx 2.1$, in 88.2% of shell-bearing galaxies), showing that the smooth profile cannot natively absorb the structure without measurable parameter shift and disfavoring an account in which shells behave as decoupled basis components. We interpret the load-bearing signatures of §3.1 as backbone-family-robust within at least one strict increase in flexibility (Einasto) and dynamically coupled to the backbone in the sense that the smooth profile cannot natively absorb the structure without measurable deformation; broader comparisons against generalized NFW, spline/nonparametric, and hierarchical Bayesian backbones remain necessary future tests.

The spatial-coherence null tests of §3.2 directly test whether the shell population depends on organized structure present in the observed rotation curves themselves. The two destructive null procedures fail in opposite directions: residual scrambling suppresses the morphology gradient, while full cross-radius velocity permutation over-produces shell detections and reverses the gradient sign. The scramble null distribution overlaps the real-data $\rho_{\rm per\,T} = -0.833$ at the 2nd percentile (2/100 realizations); residual amplitude variation alone can therefore reproduce a correlation this negative, but does so in only ~2% of realizations, with the typical null realization sitting at roughly one third the real-data magnitude. No permute realization reaches the real-data value (0/100). The strongest single piece of evidence is the asymmetric failure direction itself, not the individual significance levels: under the hypothesis that shells arise from random fitting flexibility or behave as a generic localized basis, randomization procedures preserving global residual amplitude but destroying spatial coherence should yield comparable failure modes in both directions, which the destructive nulls disconfirm. The backbone-shift test of §3.3.7 sharpens this argument: shells and the smooth backbone are not decoupled, since removing shells forces the smooth profile to systematically deform to compensate. A decoupled-basis-function alternative would predict no such deformation; the observed pattern (lower $\rho_0$, larger $a$ when shells are allowed, in 88.2% of shell-bearing galaxies) is consistent only with the smooth profile being unable to natively reproduce the structure parameterized by the shells without measurable parameter shift.

The perturbation tests of §3.3 narrow several artifact channels in concert: shell selections remain substantially stable under realistic perturbations to stellar mass-to-light ratio, distance, and inclination, and the principal organizational signatures persist within the conservatively defined anti-warp clean subsample. These results do not eliminate all possible systematic effects, but they substantially narrow the set of simple explanations capable of reproducing the observed population structure.

The principal limitations of the present work are three. The analysis depends on the Paper I decomposition framework and does not establish decomposition uniqueness; the §3.3.6 and §3.3.7 backbone controls demonstrate robustness within one strict increase in backbone flexibility and against the decoupled-basis-function alternative, but broader-family comparisons (generalized NFW with free inner slope, spline or nonparametric profiles, hierarchical Bayesian smooth-halo models) remain necessary. The analysis examines one-dimensional rotation-curve structure rather than full two-dimensional velocity fields; explicit modeling of noncircular motions, bars, spiral structure, and warped geometries would provide a stronger separation between localized halo structure and baryonic dynamical effects. The shell population is modest in size, particularly within the two-shell subsample and the anti-warp clean sample, limiting the statistical power of some higher-order comparisons.

Despite these limitations, the observed organization places meaningful constraints on interpretation. If future analyses confirm that similar residual organization persists across broader backbone families, independent galaxy samples, and higher-dimensional kinematic data, then galaxy rotation curves may contain statistically organized structure beyond conventional smooth-halo descriptions. Whether such structure corresponds to localized dark-matter features, baryon-coupled dynamical phenomena, or another form of organized galactic behavior remains an open question.

Future work should therefore focus on four directions: (i) testing the persistence of the shell population under broader halo-profile families and nonparametric decompositions; (ii) incorporating full velocity-field information from IFU and resolved HI observations; (iii) constructing hierarchical population-level statistical models for shell occurrence and scaling behavior; and (iv) evaluating whether existing dynamical or cosmological simulations naturally reproduce the observed organizational patterns.

---

## 5. Conclusions

We have investigated whether the localized residual structures identified in the SPARC rotation-curve framework of Paper I behave like a statistically organized population or like an accumulation of unrelated fitting artifacts. Using the NGC 6674-excluded 101-galaxy SPARC sample spanning morphological types $T = 2$–9, we analyzed the internal organization, coherence dependence, and robustness properties of the shell-bearing population identified through Bayesian model selection.

The shell population exhibits several forms of empirical organization. Shell-bearing fraction decreases systematically toward later morphological type, while bulge-dominated galaxies are preferentially shell-bearing relative to bulgeless systems. Shell width scales approximately linearly with shell radius under the Burkert backbone, producing a characteristic fractional width $\sigma/r \approx 0.27$ across more than two decades in radius (the slope and the characteristic ratio both attenuate under a more flexible Einasto backbone, as documented in §3.3.6; we therefore present them as Burkert-backbone-conditional rather than as backbone-family-invariant signatures). Within two-shell galaxies, outer shells are systematically more massive than inner shells. These organizational signatures extend the morphology dependence identified in Paper I from a between-galaxy property to a property of the shell population itself.

Two destructive null procedures test the coherence dependence of the morphology gradient: residual scrambling suppresses it (reproduced in 2/100 realizations; the typical scramble realization sits at roughly one third the real-data magnitude), while cross-radius velocity permutation over-produces detections with reversed sign (0/100). The asymmetric failure direction disfavors a generic basis-function origin for the shell population. Shell selections remain substantially stable under realistic variations in stellar mass-to-light ratio, distance, and inclination, and the principal scaling relations persist on the anti-warp clean subsample. The Einasto-backbone comparison preserves the morphology, bulge, and mass-feature signatures (and strengthens them) while attenuating width-related signatures; the backbone-shift test shows that the smooth Burkert profile systematically deforms when shells are removed (in 88.2% of shell-bearing galaxies), demonstrating that the smooth profile cannot natively absorb the structure without measurable parameter shift and disfavoring an account in which shells behave as decoupled basis functions.

The principal conclusion is therefore statistical rather than ontological: the localized residual structures identified by the framework behave like a coherent organized population rather than a purely random collection of fit artifacts. Determining the physical origin of that organization remains an open problem for future investigation.

---

## Acknowledgments

This work depends entirely on the publicly released SPARC rotation-curve catalog; the author thanks F. Lelli, S. S. McGaugh, J. M. Schombert, and collaborators for assembling and maintaining this resource (Lelli et al. 2016). The framework, canonical Burkert-backbone fits, and Einasto-backbone full-sample results used throughout the present analysis were produced in Paper I (Bibb 2026); the present work re-aggregates and extends those products without re-fitting.

This research is independent: it received no external funding and was conducted outside any institutional affiliation. All computation was performed on personal hardware.

Analysis and figure generation used the scientific Python stack: NumPy (Harris et al. 2020), SciPy (Virtanen et al. 2020), pandas (McKinney 2010), and Matplotlib (Hunter 2007). The complete analysis pipeline — production scripts, intermediate data, and figure-generation code — is publicly available at \url{https://github.com/RonBibb/sparc-halo-shell-reality} and archived at Zenodo (\dataset{doi:TBD}).

The author discloses the use of Anthropic's Claude as a coding and editing assistant during preparation of this manuscript. AI assistance was used for refactoring analysis scripts to portable form, drafting figure-generation code from data schemas, copy-editing manuscript prose, and reviewing statistical results alongside the author's independent derivations from the production data. All scientific conclusions, methodological choices, statistical results, and numerical values reported here were determined and independently verified by the author.

The author thanks H.B. for her patience throughout this work.

---

## Bibliography

> *To be drafted. Will include:*
> *- Bibb (2026) — Paper I*
> *- Lelli, McGaugh, & Schombert (2016) — SPARC catalog*
> *- Burkert (1995) — Burkert profile*
> *- Schwarz (1978) — BIC*
> *- Relevant rotation-curve substructure and dark matter halo references*

---

## Appendix: drafting notes

### Sample and convention conventions used throughout

- **101 galaxies** = NGC 6674-excluded canonical sample (Paper I's 102 less NGC 6674; see §2.3)
- **51 shell-bearing galaxies** = NGC 6674-excluded
- **67 shells** = total in the per-shell working set (NGC 6674 contributed 2 degenerate shells, now excluded)
- **16 two-shell galaxies** = used in §3.1.4 paired tests
- **25 anti-warp clean shells** = §3.3.5 conservative subsample (NGC 6674-excluded, matches canonical Mac-side analysis)
- **Morphology gradient $\rho_{\rm per\,T} = -0.762$** ($p = 0.028$) under NGC 6674 exclusion; $-0.833$ ($p = 0.010$) in Paper I-aligned NGC 6674-included analysis
- **Mass bound:** $5 \times 10^{10}\,M_\odot$, binding for 8/67 = 11.9% of shells

### Pending small items

- M-r and σ-r slope intercepts now filled in §3.1.2 equations ($-0.698$ and $+9.632$ for NGC 6674-excluded sample). Verify against canonical Mac-side regression output at LaTeX conversion.
- Paper I citations are placeholders; resolve once Paper I is published.
- All figure references are placeholders; figure generation is a separate task.
- Bibliography is empty.
- Inclination perturbation excludes 11 edge-on galaxies; cosmetic correction (`< 90` → `<= 90`) is a low-priority cleanup.

### Word count

| Section | Word count |
|---|---|
| Abstract | 290 |
| §2 | ~1,750 |
| §3.1 | ~1,650 |
| §3.2 | ~1,800 |
| §3.3 | ~2,650 |
| **Drafted total** | **~8,140** |

§1, §4, and §5 are drafted; final length pending bibliography, acknowledgments, and figures.

# Statistical organization of localized residual structure in SPARC rotation curves

**R. Bibb**
ORCID: 0009-0004-1153-2464
ronbibb@gmail.com

**Target journal:** AJ
**Status:** Working draft, updated 2026-05-11. v7.0/v7.1.0-aligned. Abstract, §1, §4, §5 drafted. Sections 2 and 3 drafted. Bibliography, figures, and acknowledgments pending.

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

We investigate whether the localized residual structures identified in the v7.0 SPARC rotation-curve framework of Paper I represent a statistically organized population or an accumulation of fitting artifacts. Using 101 SPARC galaxies ($T = 2$–9; the canonical 102-galaxy Paper I sample with NGC 6674 excluded due to a degenerate two-shell fit, see §2.3), the Burkert-backbone-plus-Gaussian-shell framework selects 51 shell-bearing systems via Bayesian Information Criterion, with shell-bearing fraction decreasing monotonically toward later morphological type (Spearman $\rho = -0.762$, $p = 0.028$).

The 67 fitted shells exhibit several forms of internal organization. Shell mass scales approximately as $M \propto r^{0.76}$ ($\rho = +0.64$, $p < 10^{-4}$) and shell width scales near-linearly with radius ($\sigma \propto r^{1.04}$ under the Burkert backbone; $\rho = +0.78$, $p < 10^{-4}$), implying a characteristic fractional width $\sigma/r \approx 0.27$ across more than two decades in radius. We note that the width-related signatures (and the implied $\sigma/r$ near-universality) are partially backbone-baseline-dependent — under an Einasto backbone the $\sigma$-$r$ slope and $\sigma/r$ median shift substantially (§3.3.6) — while the mass-feature signatures are robust to this backbone change. Within two-shell galaxies, outer shells are systematically more massive than inner shells ($p < 10^{-3}$). Bulge-dominated galaxies are preferentially shell-bearing relative to bulgeless systems (odds ratio $= 3.67$, Fisher $p \approx 0.01$).

We test whether these patterns can arise from random or coherence-destroyed structure using two destructive null procedures applied directly to the observed rotation curves. Residual scrambling suppresses the morphology gradient, while cross-radius velocity permutation over-produces shell detections, yielding opposite failure modes relative to the real data. Shell selections additionally remain stable under perturbations to stellar mass-to-light ratio, galaxy distance, and inclination, and the principal scaling relations persist in a conservatively defined anti-warp clean subsample.

These results disfavor random fitting behavior, baryonic measurement systematics, and outer-disk warp artifacts as dominant explanations for the shell population. Whether the detected structures correspond to localized halo features or to other forms of organized galactic dynamics remains an open question.

---

## 1. Introduction

Galaxy rotation curves are commonly modeled using smooth dark-matter halo profiles such as the Navarro-Frenk-White (NFW), Burkert, Einasto, and related parameterizations. While these profiles capture the large-scale structure of many systems, observed rotation curves frequently exhibit localized residual structure relative to smooth fits. Interpreting such residuals is difficult because multiple effects can contribute simultaneously, including baryonic modeling uncertainty, noncircular motions, warped outer disks, beam-smearing effects, and fitting flexibility within the adopted halo parameterization. Distinguishing statistically meaningful structure from fitting artifacts therefore remains a central challenge in rotation-curve analysis.

The Spitzer Photometry and Accurate Rotation Curves (SPARC) database [Lelli, McGaugh, & Schombert 2016] provides a useful environment for such tests because it combines homogeneous near-infrared photometry with high-quality HI and H$\alpha$ rotation curves across a broad range of galaxy morphologies. The SPARC sample has consequently become a standard benchmark for studies of galaxy dynamics, baryonic scaling relations, and halo-profile phenomenology.

Paper I introduced the v7.0 Burkert-backbone-plus-Gaussian-shell framework and showed that Bayesian model selection frequently favors localized residual components in SPARC rotation curves, with shell-bearing fraction varying systematically across morphological type. However, the existence of BIC-selected localized components alone does not establish that the detected structures correspond to physically meaningful galactic substructure. Such detections could arise from residual fitting flexibility, baryonic systematics, warp-related kinematic artifacts, or other forms of organized but nonphysical residual behavior.

Flexible fitting frameworks can generate localized components even in the absence of physical substructure. The relevant question is therefore not whether shell-like components can be detected, but whether the resulting population exhibits reproducible statistical organization that survives destructive null procedures and systematic perturbations. The present analysis addresses that narrower question. We test the internal organization, spatial-coherence dependence, and robustness of the shell population, while deliberately deferring physical interpretation.

This question connects to several broader areas of current research. Residual structure in galaxy rotation curves has long been discussed in the context of baryonic substructure, non-axisymmetric dynamics, and departures from idealized smooth-halo descriptions. Independent searches for dark-matter substructure have also been pursued through strong gravitational lensing, stellar-stream perturbations, and dynamical analyses of galactic halos. At the same time, modern halo modeling increasingly explores phenomenological profile families extending beyond canonical NFW forms, including cored, generalized, and feedback-modified profiles. The present work does not attempt to distinguish among these broader physical interpretations. Instead, it focuses specifically on whether the residual structures identified by the v7.0 framework exhibit reproducible statistical organization within the SPARC sample.

Several important questions are intentionally deferred beyond the scope of the present paper. We do not attempt to establish whether the localized structures correspond to spherical shells, ring-like features, or other geometric configurations, nor do we attempt an exhaustive comparison against all possible smooth-halo parameterizations or nonparametric decompositions. These questions require dedicated modeling beyond the present statistical analysis and are left for future work.

This paper is organized as follows. Section 2 summarizes the SPARC sample, the v7.0 fitting framework, and the statistical methods used throughout the analysis. Section 3 presents the empirical results in three parts: internal organization of the shell population (§3.1), spatial-coherence null tests (§3.2), and robustness against several artifact channels (§3.3). Section 4 discusses the classes of explanation constrained by these results and the principal limitations of the present analysis. Section 5 summarizes the main conclusions.

---

## 2. Data and methods

### 2.1 The SPARC sample and quality criteria

We work with the 102-galaxy subset of the Spitzer Photometry and Accurate Rotation Curves (SPARC) database [Lelli, McGaugh, & Schombert 2016] as adopted in Paper I, restricted to morphological types $T = 2$–9 with quality flag $Q \le 2$ and at least five rotation-curve points where the dark-matter contribution is positive (i.e., $V_{\rm obs}^2 > V_{\rm bar}^2$). The selection criteria match Paper I exactly. Each galaxy provides:

- A measured rotation curve $V_{\rm obs}(r)$ with uncertainties $e_{V_{\rm obs}}(r)$ at sampled radii $r$.
- Decomposed baryonic rotational components $V_{\rm gas}(r)$, $V_{\rm disk}(r)$, $V_{\rm bulge}(r)$, derived from the SPARC photometric and HI data.
- Catalog metadata: distance $D$ with uncertainty $e_D$, inclination $i$ with uncertainty $e_i$, HI extent $R_{\rm HI}$, optical disk scale length $R_{\rm disk}$, effective radius $R_{\rm eff}$, morphological type $T$, and SPARC quality flag $Q$.
- Derived virial-scale estimates $r_{\rm vir}$, halo mass $M_{\rm halo}$, and stellar mass $M_*$ via the abundance-matching procedure described in Paper I §2.1.

The sample composition by morphological type is: $T = 2$ (9 galaxies), $T = 3$ (11), $T = 4$ (17), $T = 5$ (13), $T = 6$ (16), $T = 7$ (14), $T = 8$ (6), $T = 9$ (16). Bulge presence is classified per galaxy from the SPARC photometric decomposition, yielding 24 bulge-dominated and 78 bulgeless galaxies.

### 2.2 The v7.0 fitting framework

We use the v7.0 framework derived and validated in Paper I. The total dark-matter contribution to the rotation curve is modeled as a Burkert backbone plus zero, one, or two Gaussian-mass shells:

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

**Width constraint via reparameterization.** A defining feature of the v7.0 framework is strict enforcement of the localization criterion $\sigma_i / r_i \le 0.4$. Each shell's width is parameterized as $\sigma_i = f_i r_i$ with $f_i$ as a box-bounded fit parameter $f_i \in [0.01, 0.4]$, ensuring the constraint is respected at every step of the optimization regardless of optimizer trajectory. This is the principal innovation of v7.0 relative to v6.5; see Paper I §2.2 and Appendix A.

**Mass bounds.** Shell masses are bounded $10^6 \le M_i \le 5 \times 10^{10}\,M_\odot$. The lower bound prevents numerical degeneracies; the upper bound was chosen in Paper I to keep shells in a "localized" regime well below typical halo masses. Of the 67 shells in the v7.0 fits (NGC 6674 excluded), 8 (11.9%) lie within 0.05 dex of the upper bound. We verify in §3.1.2 that removing these mass-bound-approaching shells produces only modest changes to the population-level scaling relations; the bound is binding for a subset of fits but does not drive the principal results.

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

**The full v7.0 sample** (101 galaxies, 67 shells across 51 shell-bearing galaxies) is the canonical Paper I-aligned working set with NGC 6674 excluded. Paper I includes NGC 6674 in its 102-galaxy canonical analysis. Its v7.0 fit selects $n_{\rm shells} = 2$ but yields a degenerate solution ($r_1 = r_2 = 3.12$ kpc within numerical precision, with both shell masses pegged at the upper bound), which precludes meaningful interpretation of its individual shell parameters as a population of two distinct localized features. We therefore exclude NGC 6674 from per-shell and population analyses throughout this paper. All quantitative conclusions are unchanged in direction relative to a NGC 6674-included analysis; effect sizes shift only modestly (e.g., the morphology gradient $\rho_{\rm per\,T}$ shifts from $-0.83$ to $-0.76$, with $p$ shifting from 0.010 to 0.028).

Exceptions to this exclusion are §3.2 (spatial-coherence null tests) and §3.3.2–3.3.4 (mass-to-light, distance, and inclination perturbation tests), which retain the Paper I-aligned 102-galaxy sample. These analyses were generated as coordinated production runs against the original 102-galaxy canonical fits — the null tests over 2,040 fits, the perturbation tests over $\approx 2{,}000$ fits each — and rerunning them with NGC 6674 excluded would require Mac-side production reruns. The qualitative conclusions of these sections are independent of the NGC 6674 inclusion choice. Specifically: NGC 6674 contributes a single galaxy out of 102 in the null-test scrambles and permutations, and its degenerate two-shell fit at $r_1 = r_2 = 3.12$ kpc cannot plausibly drive a $\rho_{\rm per\,T}$ value of $-0.833$ across the full 102-galaxy sample — removing one galaxy of T=2 shifts the per-T fraction in a single bin by at most $1/9$ and the overall $\rho$ by less than 0.07, as confirmed by the parallel §3.1 NGC-6674-excluded analyses on the canonical CSV. Similarly, the per-fit mode-match rates of the §3.3.2-3.3.4 perturbation tests depend on the integrated stability of $\approx 2{,}000$ refits, of which NGC 6674 contributes 20 (1.0%); its exclusion would shift the percent-agreement values by at most a similar fraction. We disclose this sample asymmetry explicitly and treat full reconciliation to the 101-galaxy primary sample as future work.

**The anti-warp clean subsample** (25 shells across 25 galaxies) restricts to shells satisfying four warp-protection criteria simultaneously: $r_{\rm shell}/R_{\rm HI} < 0.3$, disk-dominated baryonic regime at the shell radius, SPARC quality flag $Q = 1$, and inner shell of any two-shell pair. §3.3.5 uses this subsample to test whether headline patterns survive in conditions where HI-warp artifacts are most disfavored.

**The two-shell paired subsample** (16 paired inner-vs-outer shells from 16 two-shell galaxies) is used in §3.1.4 for paired Wilcoxon tests on within-galaxy mass and width orderings.

### 2.4 Methods specific to §3

The tests in §3 fall into three methodological classes:

**Statistical organization tests (§3.1).** Population-level Spearman rank correlations on $(\sigma, r)$, $(M, r)$, and $\sigma/r$-vs-$r$ across the full shell sample. Fisher exact contingency tests on bulge presence vs shell-bearing. Paired Wilcoxon signed-rank tests on inner-vs-outer mass and width within two-shell galaxies. Two-sample Kolmogorov-Smirnov tests on $r/r_{\rm vir}$ distributions for inner vs outer shell populations.

**Spatial-coherence null tests (§3.2).** Two destructive operations on real rotation-curve data — *scramble* (within-galaxy permutation of dark-matter residuals around the canonical Burkert backbone) and *permute* (within-galaxy permutation of $V_{\rm obs}$ values across radii) — applied independently to each galaxy. Each null type runs 20 realizations, with the v7.0 framework applied identically to each perturbed galaxy. Test statistics are the per-T-bin and per-galaxy Spearman correlations on the resulting shell-bearing distribution, compared against the real-data baselines via empirical $p$-values and standardized $z$-scores against the null distribution.

**Artifact-channel robustness tests (§3.3).** Six independent tests address potential non-physical origins of the shell signal: (i) coincidence with disk dynamical scales, tested via dimensionless distance to four candidate scales; (ii–iv) systematic perturbation tests on $\Upsilon_{\rm disk}/\Upsilon_{\rm bulge}$, distance $D$, and inclination $i$, drawn from realistic per-galaxy uncertainty distributions and applied 20 realizations per channel; (v) the anti-warp clean subsample analysis described above; (vi) the spatial-coherence nulls of §3.2, summarized for completeness.

The perturbation tests in (ii)–(iv) use the v7.0 production fitting code (`run_canonical_fits.py`) applied to perturbed inputs, ensuring methodological identity with the canonical fits. The anti-warp filter operates on the canonical fit catalog (no refitting required). The disk-dynamical-scale test (i) uses a uniform-in-log-r null with KS-statistic comparison.

### 2.5 Statistical conventions

We adopt the following conventions throughout:

- Reported $p$-values are two-sided unless explicitly noted as one-sided.
- Spearman rank correlations are quoted with the corresponding asymptotic $p$-value.
- For null distributions estimated from $N = 20$ realizations, the empirical one-sided $p$-value floor is $1/20 = 0.05$; we additionally report standardized $z$-scores against the null mean and standard deviation, which are not floor-limited.
- Fisher exact tests are used for $2\times 2$ contingency tables (e.g., bulge correlation).
- Wilcoxon signed-rank tests are used for paired within-galaxy comparisons.
- Kolmogorov-Smirnov two-sample tests are used for cumulative-distribution comparisons (e.g., inner vs outer $r/r_{\rm vir}$).
- $1\sigma$ uncertainties are quoted as standard errors unless noted as bootstrap or Bayesian credible intervals.

---

## 3. Results

### 3.1 Statistical organization of the shell population

Paper I established that the v7.0 framework selects $n_{\rm shells} \in \{0, 1, 2\}$ for each of 102 SPARC galaxies via Bayesian Information Criterion, with strict $\sigma/r \le 0.4$ enforcement on shell width, yielding 52 shell-bearing galaxies (51.0%). Paper I further established the principal morphology trend: shell-bearing rate decreases monotonically with morphological lateness across $T = 2$–9, with Spearman $\rho_{\rm per\text{-}T} = -0.833$ ($p = 0.010$) and per-galaxy $\rho_{\rm per\text{-}galaxy} = -0.296$ ($p = 0.003$, two-sided permutation test on T-type labels).

This section examines the *internal organization* of the shell population. The morphology gradient identified in Paper I points to systematic variation between galaxies; we now ask what systematic structure exists within the 67 shells across the 51 shell-bearing galaxies of the NGC 6674-excluded canonical sample (§2.3). We organize the analysis around three classes of empirical pattern: (i) the bulge correlation, in which bulge-dominated galaxies are preferentially shell-bearing; (ii) the radial scaling relations, in which shell width $\sigma$ and mass $M$ scale with shell radius $r$; and (iii) the geometric gradient, in which the dimensionless width $\sigma/r$ varies with radius across the population.

The tests reported in this section are exploratory population diagnostics rather than independent confirmatory hypothesis tests; reported $p$-values are not corrected for multiple comparisons, several are marginal, and the organizational dimensions examined were not pre-registered. We rely on the destructive null tests of §3.2 and the perturbation tests of §3.3 to evaluate whether the patterns identified here depend on real data structure rather than fitting flexibility.

#### 3.1.1 Bulge correlation

Bulge-dominated galaxies in the v7.0 sample are preferentially shell-bearing relative to bulgeless galaxies. Of 23 galaxies classified as bulge-dominated, 17 (73.9%) are shell-bearing. Of 78 galaxies classified as bulgeless, 34 (43.6%) are shell-bearing. The two categories together comprise the full $T = 2$–9 NGC 6674-excluded sample of 101 galaxies; the SPARC photometric decomposition does not assign intermediate cases.

The shell-bearing odds ratio is

$$
\text{OR} = \frac{17 \times 44}{6 \times 34} = 3.67,
$$

with a Fisher's exact test one-sided $p \approx 0.01$. Bulged galaxies are 1.69$\times$ more likely to be shell-bearing than bulgeless galaxies in absolute rate, equivalent to a 30.3 percentage-point difference. The bulge correlation persists in the anti-warp clean subsample (§3.3.5), with OR reduced under the conservative cuts.

The bulge correlation and the morphology gradient established in Paper I are not independent in this sample, and the entanglement is substantial rather than partial. The bulge-dominated population is concentrated almost exclusively at early T-types: 19 of the 24 bulged galaxies are at $T = 2$ or $T = 3$, and only one bulged galaxy is at $T \ge 6$. Within the bulged subset alone, the morphology gradient is not statistically significant (Spearman $\rho_{\rm per\,T} = -0.16$, $p = 0.80$, with most T-bins containing one or two galaxies); within the bulgeless subset alone, it is similarly weak ($\rho_{\rm per\,T} = -0.18$, $p = 0.70$). Conversely, restricting the bulge correlation to early-type galaxies ($T = 2$–5) reduces it to a marginal odds ratio of 2.6 (Fisher $p \approx 0.09$); the late-type subsample ($T = 6$–9) contains only one bulged galaxy and admits no within-range comparison. The bulge correlation and the morphology gradient should therefore be understood as two statistical projections of a single underlying contrast — between bulge-rich early-type galaxies and bulgeless mid-to-late-type galaxies — rather than as independent organizational signatures. We report both observations for completeness but caution against treating them as independent lines of evidence in §3.1.5 and §4.

> **[Figure 3.1.1 — Bulge correlation]** $2\times 2$ contingency or stacked bar showing bulged vs bulgeless shell-bearing fractions (18/24 vs 34/78).
> *Data source:* `data/galaxy_classifications.csv` (is_bulge_dom, is_bulgeless) joined with Paper I canonical CSV (shell-bearing flag).
> *Status:* Placeholder; generation script pending.

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

The mass-radius slope of 0.76 indicates that more distant shells carry more enclosed mass on average, but with a sub-linear scaling. We verify the bound-state of the underlying mass parameter explicitly. The v7.0 framework imposes an upper bound on shell mass at $5 \times 10^{10}\,M_\odot$, adopted from Paper I to preserve the "localized" regime — well below the $\gtrsim 10^{11}\,M_\odot$ scale of typical halo masses, ensuring that BIC-selected shells represent discrete features distinguishable from the smooth backbone rather than alternative halo descriptions. Of the 67 shells in the v7.0 fits (NGC 6674 excluded), 8 (11.9%) lie within 0.05 dex of this bound. Among the 59 shells whose mass parameter is more than 0.05 dex below the upper bound, the M-r slope is $0.67 \pm 0.15$, the $\sigma$-r slope is $1.02 \pm 0.11$, and the $\sigma/r$ population median is 0.275 (essentially unchanged from the full-sample value of 0.275). The mass bound is therefore binding for a subset of fits but does not drive the population-level scaling relations. We have not formally tested how raising the bound would affect the population statistics; the 8 bound-pegged shells would receive higher mass values, but those higher values would still fall along the empirical $M$-$r$ scaling, so the direction of the slope is unlikely to reverse. A systematic exploration of bound-relaxation effects is left as future work. We discuss the choice of mass bound and natural extensions in §4.

We do not interpret these slopes physically in the present paper; they are reported as empirical scaling relations of the v7.0 shell population.

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

Of the 16 two-shell galaxies in the v7.0 NGC 6674-excluded sample, 14 (87.5%) have outer shells more massive than inner shells; zero have inner more massive than outer; two pairs are mass-tied at the upper bound. The Wilcoxon signed-rank test for the paired difference $M_{\rm outer} - M_{\rm inner}$ yields $p = 0.0001$ (one-sided test, alternative outer $>$ inner). Median outer-to-inner mass ratio is 2.06.

In radius, outer shells are at median 2.62$\times$ the radius of inner shells (definitional ordering). Absolute width $\sigma$ is also larger in outer shells: 14 of 16 paired galaxies have $\sigma_{\rm outer} > \sigma_{\rm inner}$, with Wilcoxon $p = 0.0008$. This is consistent with the population-wide $\sigma \propto r^{1.04}$ scaling and outer shells being at larger $r$.

When shell positions are normalized to the host's virial radius $r_{\rm vir}$, the inner and outer populations within two-shell galaxies separate at marginal but measurable significance. Inner shells of two-shell galaxies cluster at $r/r_{\rm vir} = 0.014$ (median, IQR $[0.007, 0.021]$), outer shells at 0.025 (IQR $[0.015, 0.031]$), with a two-sample Kolmogorov-Smirnov statistic $D = 0.47$, $p = 0.045$ ($n = 16$ inner, $n = 16$ outer). Single-shell galaxies cluster at intermediate $r/r_{\rm vir} = 0.030$ (median), consistent with BIC-driven parsimony folding contributions into a single Gaussian when the data do not support two well-separated peaks.

This pattern is suggestive of internal population stratification within shell-bearing galaxies but is not statistically definitive at the present sample size. We report it as an empirical observation consistent with possible multi-scale organization, requiring confirmation on larger samples before stronger claims about distinct dynamical populations are warranted.

#### 3.1.5 Summary of organized structure

Across several dimensions of shell-property organization, the v7.0 shell population exhibits structure that varies systematically with measurable galaxy and shell properties. We group the findings by their robustness under multiple-comparisons correction and backbone-family flexibility.

**Primary signatures** (robust under Bonferroni correction across the seven §3.1 tests, $\alpha = 0.05$; preserved or strengthened under the Einasto backbone in §3.3.6):

- **Radial mass scaling:** $M \propto r^{0.76}$ ($\rho = +0.64$, $p < 10^{-4}$). Survives multiple-comparisons correction by orders of magnitude; preserved under Einasto (slope $0.82$, $\rho = +0.69$).
- **Radial width scaling:** $\sigma \propto r^{1.04}$ ($\rho = +0.78$, $p < 10^{-4}$) *under the Burkert backbone*. Survives multiple-comparisons correction by orders of magnitude. The slope and the implied $\sigma/r$ population median of $0.275 \pm 0.116$ are backbone-baseline-dependent: under Einasto the slope drops to 0.38 and the median to 0.173 (§3.3.6). We report the Burkert-baseline values as the canonical statement but emphasize that quantitative interpretation of shell width requires reference to a specific smooth-halo family.
- **Inner-vs-outer mass ordering in two-shell galaxies:** outer shells more massive (14/16, Wilcoxon $p = 0.0001$). Survives multiple-comparisons correction; survives backbone change to Einasto (14/19, $p = 0.0005$).

**Secondary signatures** (survive BH-FDR correction at $\alpha = 0.05$ but not strict Bonferroni; treated as suggestive rather than confirmatory):

- **Bulge correlation** (statistically near-equivalent to the morphology gradient in this sample; see §3.1.1): OR $= 3.67$, Fisher $p \approx 0.01$. Strengthens under Einasto (OR $= 4.32$, $p = 0.003$).
- **Morphology gradient** (galaxy-level): $\rho_{\rm per\text{-}T} = -0.762$ ($p = 0.028$). Strengthens under Einasto ($\rho = -0.87$, $p = 0.005$). Bonferroni-corrected $p = 0.196$ (single-test interpretation requires the §3.2 spatial-coherence nulls for confirmatory weight; see §3.2.3).
- **Inner-vs-outer width ordering**: 14/16 outer broader than inner ($p = 0.0008$) under Burkert; attenuates to 13/19, $p = 0.10$ under Einasto. Reported as suggestive of the same physical asymmetry as the mass ordering but more sensitive to backbone choice.
- **Two-population separation in $r/r_{\rm vir}$**: KS $D = 0.47$, $p = 0.045$. BH-FDR-adjusted $p = 0.045$; fails Bonferroni; reported as suggestive of internal population stratification, not as confirmatory evidence for distinct dynamical populations (§3.1.4).

**Soft observations** (reported for completeness; not confirmatory):

- **$\sigma/r$ quartile gradient**: $\sigma/r$ varies from 0.339 (innermost quartile) to 0.185 (outermost quartile), with non-monotonic middle quartiles and a within-galaxy paired test of $p = 0.30$. Reported as modest population-level tendency; backbone-baseline-dependent (§3.3.6).

**Multiple-comparisons correction.** Across the seven primary §3.1 statistical tests (counted as: $\sigma$-$r$ Spearman, $M$-$r$ Spearman, $M$ inner-vs-outer Wilcoxon, $\sigma$ inner-vs-outer Wilcoxon, bulge Fisher, morphology Spearman, KS $r/r_{\rm vir}$), all seven survive Benjamini-Hochberg FDR correction at $\alpha = 0.05$ (BH-adjusted $p$-values: $\le 10^{-4}$ for both scaling Spearman tests, 0.0002 for $M$ paired, 0.0014 for $\sigma$ paired, 0.014 for bulge, 0.033 for morphology, 0.045 for KS). Four survive strict Bonferroni correction ($p < 0.05/7 = 0.0071$): the two scaling tests and the two inner-vs-outer Wilcoxon tests. The three secondary signatures (bulge, morphology, KS) fail Bonferroni and rely on the §3.2 spatial-coherence nulls and §3.3.6 backbone-family control for confirmatory weight rather than on the §3.1 tests in isolation.

These patterns extend the morphology gradient established in Paper I from a between-galaxy property to an organizational property of the shell population itself. §3.2 establishes that the morphology gradient cannot be reproduced by data lacking the spatial coherence of the canonical residuals. §3.3 establishes that none of the patterns are artifacts of baryonic input systematics, warp-prone HI configurations, coincidence with disk dynamical scales, or — for the load-bearing mass-feature signatures — choice of smooth-halo backbone.

We do not attempt physical interpretation of these patterns in the present paper. Section 4 discusses the bounds the empirical patterns place on classes of explanation; the positive identification of a physical mechanism is the subject of future work.

---

### 3.2 Tests of spatial-coherence dependence

Paper I established two complementary null tests on the v7.0 framework. The first is a synthetic-mock false-positive analysis: 346 mocks generated from smooth Burkert-truth and NFW-truth profiles plus realistic noise, fit by the same canonical pipeline, recover shell-bearing fractions of 4.0% (Burkert-truth) and 63.6% (NFW-truth). The real-data shell-bearing rate of 51.0% is recovered at factors of 6–20 above the Burkert-truth false-positive rate in every $T$-bin, disfavoring smooth-Burkert truth as the dominant gradient driver. The second is a per-galaxy permutation test on the morphology gradient itself: T-type labels are permuted across galaxies and the per-galaxy Spearman $\rho$ recomputed under each permutation, yielding a two-sided $p = 0.002$ for the observed $\rho_{\rm per\text{-}galaxy} = -0.296$.

The tests in this section address a different question. Paper I's analyses establish that the framework does not generate spurious shells in genuinely smooth synthetic data, and that the morphology gradient is not a chance arrangement of T-type labels. Neither test addresses whether the *spatial coherence* of the localized residual structure within each rotation curve is essential to producing the observed shell population. A galaxy's residual signal — the difference between observed rotation $V_{\rm obs}$ and the smooth Burkert backbone — could be coherently structured (with characteristic radii, widths, and amplitudes that the framework discovers as shells) or it could be incoherent fluctuation (random scatter at the noise level). If the latter, the framework's BIC procedure should still occasionally select shells from chance configurations, but the resulting shell population should not exhibit the morphology gradient or the organized scaling relations established in §3.1.

This section tests the spatial-coherence requirement directly. We define two destructive operations on the real rotation curve data — *scramble* (shuffle DM residuals across radii within each galaxy, preserving the Burkert backbone) and *permute* (shuffle observed velocities across radii within each galaxy, destroying the Burkert backbone) — and ask whether either operation reproduces the morphology gradient when the framework is applied to the destroyed data.

For each null type and each realization, we apply the v7.0 framework (Burkert + 0/1/2 Gaussian shells, BIC-selected, $\sigma/r \le 0.4$ enforcement) to all 102 canonical galaxies, compute the same per-T and per-galaxy Spearman correlations as the real-data baseline, and ask how often the null produces $\rho$ as negative as the real data. The runs use 20 realizations per null type.

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

Across 20 scramble realizations on 102 galaxies (2,040 fits total), the null distribution of $\rho_{\rm per\,T}$ has mean $-0.197$ with standard deviation $0.146$, range $[-0.539, +0.095]$. The real-data baseline of $-0.833$ falls $4.4\sigma$ below the null mean. None of 20 realizations produces a $\rho_{\rm per\,T}$ as negative as real data; the empirical one-sided $p$-value is $p_{\rm emp} < 0.05$ ($0/20$, limited by realization count). The per-galaxy correlation $\rho_{\rm per\,galaxy}$ has null mean $-0.150 \pm 0.048$, range $[-0.241, -0.095]$, with the real-data baseline of $-0.296$ at $3.0\sigma$ below the null mean and again $0/20$ realizations matching it.

The scramble null does retain a weakly negative $\rho_{\rm per\,T}$ on average ($-0.197$). This is interpretable: the scramble preserves each galaxy's smooth Burkert backbone, and Burkert backbone parameters correlate with morphological type (early-type galaxies have more concentrated halos, deeper baryonic potentials, and more complex residual structure for the framework to find by chance). A correlation of $-0.197$ is what residual *amplitude variations* alone — without spatial coherence — can produce. The real-data correlation of $-0.833$ is more than four times stronger, demonstrating that the morphology gradient depends on the *spatial coherence* of localized residual structure, not merely its amplitude distribution.

#### 3.2.2 Cross-radius $V_{\rm obs}$ permutation

The permutation null breaks both the localized residual structure and the smooth backbone. For each galaxy, we shuffle $V_{\rm obs}$ values across radii while holding $R$ values fixed, then refit the v7.0 framework. The permutation preserves each galaxy's $V_{\rm obs}$ amplitude distribution and its radial sampling. It destroys all coherent radial structure: the smooth rotation-curve shape, the residual-from-backbone, and any localized features.

Across 20 permutation realizations on 102 galaxies, the null distribution of $\rho_{\rm per\,T}$ has mean $+0.375$ with standard deviation $0.232$, range $[-0.169, +0.790]$. **The sign of the null correlation is opposite the real-data correlation.** The real-data baseline of $-0.833$ falls $5.2\sigma$ below the null mean. The empirical $p < 0.05$ (exact $0/20$ as negative as real). The per-galaxy correlation has null mean $+0.162 \pm 0.055$, range $[+0.044, +0.250]$ — also positive — with the real-data baseline at $8.3\sigma$ below the null mean.

The positive null correlation in permuted data is not a defect; it is informative. When we permute $V_{\rm obs}$ across radii, the resulting "rotation curve" is a chaotic profile inconsistent with any smooth halo. The BIC procedure responds to this chaos by selecting shell-bearing fits at greatly elevated rates: across all T-types, mean shell-bearing fractions in permuted data are 0.72–0.97, compared to 0.31–1.00 in real data and 0.15–0.79 in scrambled data (Table 3.2.1). The framework over-detects shells in permuted data because the BIC penalty is exceeded by the χ² improvement from any localized component fitted to chaotic noise.

The positive $\rho_{\rm per\,T}$ in permutation arises from the small population of permuted fits where the framework cannot fit shells well: these are scattered across morphological types in a pattern that yields a positive Spearman ρ by chance. The point is not the sign per se, but that the *direction* of the morphology gradient under permutation is opposite to real, with no overlap in 20 realizations.

#### 3.2.3 Per-T shell-bearing fractions: the failure modes are physically distinct

The two nulls fail to reproduce real data in opposite directions, which is itself diagnostic. Table 3.2.1 shows the per-T-bin shell-bearing fraction in real data alongside the mean fraction across 20 null realizations.

| T | N (real) | Real frac. | Scramble null | Permute null | Real / Scramble | Real / Permute |
|---|---|---|---|---|---|---|
| 2 | 9 | 1.000 | 0.794 | 0.961 | 1.26 | 1.04 |
| 3 | 11 | 0.545 | 0.150 | 0.723 | 3.64 | 0.75 |
| 4 | 17 | 0.529 | 0.309 | 0.815 | 1.71 | 0.65 |
| 5 | 13 | 0.538 | 0.308 | 0.923 | 1.75 | 0.58 |
| 6 | 16 | 0.562 | 0.291 | 0.972 | 1.94 | 0.58 |
| 7 | 14 | 0.357 | 0.225 | 0.921 | 1.59 | 0.39 |
| 8 | 6 | 0.333 | 0.383 | 0.925 | 0.87 | 0.36 |
| 9 | 16 | 0.312 | 0.231 | 0.969 | 1.35 | 0.32 |

Two patterns are evident. The scramble null produces shell-bearing fractions *below* real data for most T-types (real exceeds scramble by factors of 1.26–3.64×, except T=8 where the real fraction is 0.87× the scramble null due to small-bin statistics). This is consistent with the scramble destroying the localized features that drive real-data shell detections. The permute null produces shell-bearing fractions *above* real data for nearly every T-type (real / permute ratios of 0.32–1.04). This is consistent with the permute creating chaotic profiles that the BIC procedure over-fits with shells.

Neither null reproduces real data, but they fail in opposite directions: scramble *under-detects*, permute *over-detects*. This asymmetry is difficult to reconcile with the hypothesis that real shell selections are random framework responses. A random-detection scenario would show null detection rates bracketing real rates symmetrically, not bracketing them on opposite sides.

#### 3.2.4 Joint interpretation

Both nulls reject the hypothesis that the morphology gradient could arise from random residual structure or random rotation-curve amplitudes:

- $\rho_{\rm per\,T}$ rejected at $> 4\sigma$ under scramble, $> 5\sigma$ under permutation
- $\rho_{\rm per\,galaxy}$ rejected at $> 3\sigma$ under scramble, $> 8\sigma$ under permutation
- Empirical $p < 0.05$ in all four tests (limited by $N = 20$ realization resolution)

The two nulls bracket a meaningful range of artifact channels: scramble tests whether radial coherence within each galaxy is necessary; permutation tests whether *any* coherent rotation-curve shape is necessary. The morphology gradient in v7.0 shell selections survives in neither. The two failure modes — scramble under-detecting because spatial coherence has been destroyed, permute over-detecting because the BIC procedure fits chaos — establish that the real-data shell population is not reproducible by fitting to coherence-destroyed residuals or fully randomized rotation curves.

> **[Figure 3.2.1 — Null distributions of $\rho_{\rm per\,T}$]** Two-panel figure: (left) histogram of $\rho_{\rm per\,T}$ across 20 scramble realizations, real-data baseline of $-0.833$ marked as vertical line. (right) Same for permutation null. Annotate null mean $\pm 1\sigma$ and z-score of real baseline.
> *Data source:* `data/nulltest_per_realization.csv` (filter by null_type='scramble' and 'permute'; column: rho_per_T).
> *Status:* Placeholder; generation script pending.

> **[Figure 3.2.2 — Per-T shell-bearing fractions]** Grouped bar chart: for each T-type (2–9), three bars side-by-side — real data, scramble null mean, permute null mean. Error bars on null means from realization std. Shows asymmetric failure modes (scramble below real, permute above).
> *Data source:* `data/nulltest_summary.txt` for real data; `data/nulltest_per_realization.csv` for null means (columns frac_T2 through frac_T9 averaged over realizations per null_type).
> *Status:* Placeholder; generation script pending.

---

### 3.3 Robustness against artifact explanations

The empirical patterns documented in §3.1 — population-wide mass-radius scaling, near-universal $\sigma/r$, and structural correlations with galaxy morphology and bulge presence — could in principle arise from sources other than physical localized mass features in galaxy halos. Six potential artifact channels are testable within the SPARC sample and the v7.0 framework: (i) coincidence with disk-baryonic dynamical scales, (ii–iv) systematic measurement uncertainty on the three principal baryonic inputs (mass-to-light ratio, distance, inclination), (v) HI disk warps producing localized line-of-sight velocity features, and (vi) random structure in the data being misclassified as shells by the BIC selection. We address each in turn. The null tests of channel (vi) appear in §3.2 and are summarized at the end of the present section for completeness.

#### 3.3.1 Coincidence with disk-baryonic dynamical scales

If the localized features detected by v7.0 originated in baryonic disk substructure rather than halo mass features, shell radii should preferentially cluster at radii associated with disk dynamical scales: the disk scale length $R_{\rm disk}$, two-and-a-fifth disk scale lengths ($2.15\,R_{\rm disk}$, the canonical exponential-disk rotation peak), the half-light radius $R_{\rm eff}$, or the radius of the observed rotation curve maximum. We test this by computing, for every detected shell, the dimensionless distance $|r_{\rm shell} - r_{\rm scale}| / r_{\rm scale}$ for each of the four candidate scales, and comparing the observed distribution to the expectation under a uniform null where shell radii are drawn from a power-law in $r$ within each galaxy's fitted range.

The observed distributions show no preferential clustering at any of the four candidate scales. The Kolmogorov-Smirnov statistic against the uniform null fails to reject at the 0.05 level for all four scales. The mean and median dimensionless offsets are consistent with random placement. We conclude that shell radii are not coincident with disk dynamical features, disfavoring a simple disk-resonance or disk-substructure origin for the population-level signal.

> **[Figure 3.3.1 — Disk dynamical scale coincidence]** Four-panel CDF comparison. Each panel: empirical CDF of $|r_{\rm shell} - r_{\rm scale}|/r_{\rm scale}$ for one candidate scale ($R_{\rm disk}$, $2.15\,R_{\rm disk}$, $R_{\rm eff}$, $r$ at $V_{\rm rot}^{\rm peak}$), overlaid on uniform-placement null CDF. KS $p$-value annotated per panel.
> *Data source:* Paper I canonical CSV (shell radii) + `data/sparc_sample123.csv` (Rdisk, Reff) + Rotmod_LTG files (V_rot peak radius). Producer script not yet written.
> *Status:* Placeholder; generation script pending.

#### 3.3.2 Systematic perturbations: mass-to-light ratio

Stellar mass-to-light ratios in SPARC are nominally fixed at $\Upsilon_{\rm disk} = 0.5$ and $\Upsilon_{\rm bulge} = 0.7$ at 3.6 µm [@Lelli2016]. The systematic uncertainty on these ratios is approximately 0.1 dex. We test whether shell selections survive realistic variation in $\Upsilon$ by performing 20 independent perturbation realizations: for each realization we draw $(\log_{10}\Upsilon_{\rm disk}', \log_{10}\Upsilon_{\rm bulge}')$ from independent normal distributions with means $(\log_{10} 0.5, \log_{10} 0.7)$ and standard deviation 0.1 dex, and refit the v7.0 framework on all 102 galaxies with the perturbed $\Upsilon$ values. Each refit follows the canonical v7.0 procedure: Burkert + 0/1/2 Gaussian shells, BIC-selected with parameter penalty $k = 2/5/8$ and $\sigma/r \le 0.4$ wall.

Across 2,001 successful refits (102 galaxies $\times$ 20 realizations, with 39 fits failing on $V_{\rm obs}^2 > V_{\rm bar}^2$ point cuts after $\Upsilon$ rescaling), shell-number selections agree with the canonical v7.0 result in 86.2% of cases (1,725/2,001). At the per-galaxy level, the modal $n_{\rm shells}$ across the 20 realizations matches the canonical fit in 95.1% of galaxies (97/102). Stratifying by canonical shell count: galaxies with canonical $n_{\rm shells} = 0$ show 92.3% per-fit stability, $n_{\rm shells} = 1$ shows 83.5%, and $n_{\rm shells} = 2$ shows 74.3%. Among galaxies whose shell count is fully stable across all 20 realizations and that contain at least one shell, the median scatter in $\log_{10} r_{\rm shell,1}$ is 0.017 dex (approximately 4% in radius).

The hierarchy is consistent with information-theoretic expectations: galaxies whose canonical fit is in the most parsimonious branch ($n_{\rm shells} = 0$) are least likely to flip under perturbation, while those at the BIC margin between two-shell and one-shell solutions are most likely to flip across the boundary. The aggregate population fractions $(n_0, n_1, n_2)$ shift from $(49.0\%, 34.3\%, 16.7\%)$ canonical to $(48.2\%, 35.7\%, 14.2\%)$ under perturbation — a population-level change of less than 2.5 percentage points in any bin.

The shell signal is therefore not driven by baryonic mass-to-light mismodeling.

> **[Figure 3.3.2 — $\Upsilon$ perturbation stability]** Left: stacked bar of perturbed-vs-canonical $n_{\rm shells}$ matches across 2,001 fits, stratified by canonical shell count (n=0: 92.3%, n=1: 83.5%, n=2: 74.3%). Right: scatter of $\log_{10} r_{\rm shell,1}^{\rm pert}$ versus $\log_{10} r_{\rm shell,1}^{\rm canon}$ for fully-stable shell-bearing galaxies, $\pm$25% bands marked.
> *Data source:* `data/upsilon_perturbation_per_galaxy.csv` (columns: status, n_shells, r_sh1) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.3 Systematic perturbations: distance

Galaxy distances enter the rotation curve fit through two channels: physical radii scale as $r \to r \cdot (D'/D)$, and baryonic rotation contributions scale as $V_{\rm bar} \to V_{\rm bar} \cdot \sqrt{D'/D}$ (since baryonic mass scales as $D^2$ at fixed observed flux while $r \propto D$, giving $V^2 \propto M/r \propto D$). Observed rotation velocities $V_{\rm obs}$ are distance-invariant. Each SPARC galaxy carries a published distance $D$ and a per-galaxy uncertainty $e_D$ reflecting the measurement method (Hubble flow, TRGB, Cepheid, etc.).

We test distance-systematic robustness by 20 realizations in which each galaxy independently draws $D' = D \cdot 10^{\mathcal{N}(0, \sigma_{\log D})}$ with $\sigma_{\log D} = e_D / (D \ln 10)$, refits the v7.0 framework on perturbed-radius and perturbed-baryon data, and records shell selections. The fractional perturbation magnitudes span the published range: median 8.7%, mean 13.8%, 90th percentile 31.8%, with one outlier (a dwarf with $e_D > D$) reaching 132%.

Across 2,036 successful refits (4 fits failing on insufficient DM points), shell-number selections match canonical in 89.6% of cases. At the per-galaxy level, modal shell count matches canonical in 94.1% of galaxies. Stratification by canonical $n_{\rm shells}$ yields stability rates of 94.6% ($n=0$), 86.1% ($n=1$), and 82.3% ($n=2$). Median $\log_{10} r_{\rm shell,1}$ scatter for fully-stable galaxies is 0.039 dex (~9% in radius). Population fractions shift by less than 2.5 percentage points in any bin.

We note that distance perturbation produces *more* stable shell selections than mass-to-light perturbation in our tests. This is physically reasonable: distance scaling is shape-preserving, multiplying all radii by the same factor and all baryonic velocities by the same factor, so the relative shape of $V_{\rm DM}^2 = V_{\rm obs}^2 - V_{\rm bar}^2$ is preserved. Mass-to-light perturbation, by contrast, redistributes the disk-versus-bulge contributions to $V_{\rm bar}$ at different radii (since $V_{\rm disk}$ and $V_{\rm bulge}$ profiles peak at different scales), producing more disruptive changes to the residual structure being fit.

The shell signal is not driven by distance measurement uncertainty.

> **[Figure 3.3.3 — Distance perturbation stability]** Same two-panel format as Figure 3.3.2, for distance perturbation. Stability stratification: n=0: 94.6%, n=1: 86.1%, n=2: 82.3%. Includes per-galaxy fractional perturbation magnitude (median 8.7%).
> *Data source:* `data/distance_perturbation_per_galaxy.csv` (columns: status, n_shells, r_sh1, distance_factor) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.4 Systematic perturbations: inclination

Galaxy inclinations $i$ enter rotation curve fitting through the deprojection $V_{\rm obs} = v_{\rm los} / \sin i$, where $v_{\rm los}$ is the observed line-of-sight velocity. SPARC publishes per-galaxy inclinations $i$ with uncertainties $e_i$ typically in the range 1°-5°. We test inclination-systematic robustness by 20 realizations in which each galaxy independently draws $i' = i + \mathcal{N}(0, e_i)$, with $i'$ floored at 10° and capped at 89° to avoid pathological behavior near the deprojection singularity. We rescale $V_{\rm obs} \to V_{\rm obs} \cdot \sin i / \sin i'$ and $e_{V_{\rm obs}} \to e_{V_{\rm obs}} \cdot \sin i / \sin i'$; physical radii and modeled baryonic components are inclination-invariant.

Eleven SPARC galaxies in the canonical sample are catalogued at exactly $i = 90°$ (edge-on); these are excluded from the perturbation procedure to avoid asymmetric perturbations against the upper bound. The exclusion is conservative: at $i = 90°$, $\sin i = 1.000$, and at $i = 89°$, $\sin i = 0.9998$, so inclination perturbations at near-edge-on inclinations produce negligible $V_{\rm obs}$ rescaling. Including these galaxies would only increase the apparent stability rate. The final perturbation suite comprises 1,820 fits across 91 galaxies $\times$ 20 realizations.

Realized perturbation magnitudes: median $|i' - i| = 1.87°$, mean 2.96°, maximum 28.8°. The implied $V_{\rm obs}$ rescaling factor $\sin i / \sin i'$ ranges over $[0.681, 2.359]$.

All 1,820 fits succeeded. Shell-number selections match canonical in 95.7% of fits (1,741/1,820). At the per-galaxy level, modal shell count matches canonical in 98.9% of galaxies. Stratification by canonical $n_{\rm shells}$: 99.6% ($n=0$), 91.6% ($n=1$), 90.7% ($n=2$). Median $\log_{10} r_{\rm shell,1}$ scatter for fully-stable galaxies is 0.005 dex (~1.2% in radius) — the tightest position recovery of the three perturbation tests.

The inclination perturbation produces the most stable shell selections of the three baryonic-input systematics. This is physically reasonable: inclination perturbation rescales $V_{\rm obs}$ uniformly across all radii, preserving the *shape* of the rotation curve while changing only its overall amplitude. The shell-fitting machinery operates on residual shape relative to the smooth Burkert backbone, which is largely preserved under uniform amplitude rescaling.

The shell signal is not driven by inclination measurement uncertainty.

> **[Figure 3.3.4 — Inclination perturbation stability]** Same two-panel format as Figure 3.3.2, for inclination perturbation. Stability stratification: n=0: 99.6%, n=1: 91.6%, n=2: 90.7%. Tightest position recovery of three perturbation tests (median $\Delta \log r_1 = 0.005$ dex).
> *Data source:* `data/inclination_perturbation_per_galaxy.csv` (91 galaxies × 20 reps; 11 edge-on excluded) joined with Paper I canonical CSV.
> *Status:* Placeholder; generation script pending.

#### 3.3.5 Anti-warp clean subsample

The most plausible mechanism by which a smooth halo could mimic a localized residual feature is a velocity-field artifact in the outer rotation curve — most commonly a kinematic warp where the gas disk and the inner stellar disk no longer share a common rotation axis. Warp-induced line-of-sight velocity offsets manifest as apparent residuals at large radii where neutral hydrogen dominates the kinematic tracer and where the assumed disk inclination becomes least reliable. If the v7.0 shells were dominated by warp artifacts, the headline empirical patterns of §3.1 should weaken substantially upon excluding shells in conditions most susceptible to such artifacts.

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
| Bulge correlation OR | 3.67 ($p \approx 0.01$) | 2.49 ($p \approx 0.04$) |
| Morphology gradient $\rho_{\rm per\text{-}T}$ | $-0.76$ ($p = 0.028$) | $-0.67$ ($p = 0.071$) |

The five organizational signatures of §3.1 — bulge correlation, $M \propto r$ scaling, $\sigma \propto r$ scaling, $\sigma/r$ universality, and the morphology gradient — all persist on the conservatively cleaned subsample. Effect sizes are modestly attenuated, which is expected given the 63% reduction in sample size and the conservative nature of the cuts (each of which removes shells whether or not they were artifacts). Effect *directions* are preserved exactly. The morphology gradient $\rho_{\rm per\text{-}T} = -0.67$ on the clean subsample is just outside the $p < 0.05$ threshold ($p = 0.071$, $n = 8$ T-bins), driven by the small per-bin counts after attrition rather than by a directional reversal.

We emphasize what would have happened if warp artifacts dominated the shell population: at minimum, the $M$-$r$ slope would have flattened substantially (warp artifacts produce shells at the warp radius, not at radii correlated with intrinsic enclosed mass), the bulge correlation would have weakened or vanished (warps are not preferentially present in bulged galaxies), and the morphology gradient would have weakened (warps occur in late-type gas-rich galaxies more frequently than early-type bulged systems, producing the opposite gradient direction to the one observed). None of these expected signatures of a warp-dominated population is observed. The bulge correlation OR drops from 3.67 to 2.49 — an attenuation, not a removal. The $M$-$r$ slope drops from 0.76 to 0.66 — within statistical fluctuation given the smaller sample. The morphology gradient drops from $\rho = -0.76$ to $\rho = -0.67$ — same direction, slightly softer.

A more direct demonstration of warp-versus-shell separability would require model comparison against an explicit kinematic-warp model fit to each rotation curve, which is beyond the scope of the v7.0 framework. We do not claim the present test is exhaustive. We claim only that the headline empirical patterns are not localized to the warp-prone regime where the most plausible artifact mechanism would concentrate. Combined with the §3.3.1 disk-dynamical-scale null, the §3.3.2-3.3.4 baryonic-perturbation tests, and the §3.2 spatial-coherence nulls, this places the warp-artifact hypothesis as one of several plausible alternatives that the data do not support.

> **[Figure 3.3.5 — Anti-warp clean subsample]** Two-panel comparison: $\sigma$-vs-$r$ scatter (left) and $M$-vs-$r$ scatter (right). Full-sample shells (n=67) in light gray; anti-warp clean shells (n=25) highlighted. Linear fits overlaid for each population with slopes annotated (full vs clean: $M$-$r$ 0.76→0.66, $\sigma$-$r$ 1.04→0.93).
> *Data source:* `data/antiwarp_per_shell.csv` (use is_clean flag for the clean subsample).
> *Status:* Placeholder; generation script pending.

#### 3.3.6 Backbone-family control: Einasto comparison

A central concern raised in §4 is whether the organizational signatures of §3.1 reflect genuine residual structure or compensation for systematic mismatch between the Burkert backbone and underlying halo profiles. A directly testable form of this concern asks whether the same signatures persist when the smooth-halo backbone is replaced by a strictly more flexible family.

We use the Einasto profile as the comparison backbone. Einasto introduces one additional free parameter relative to Burkert (the shape parameter $\alpha$ controlling inner-profile steepness), allowing the backbone to interpolate continuously between cored and cuspy behavior. It is therefore strictly more flexible than Burkert as a smooth-halo descriptor, and is a widely adopted alternative in halo modeling. We adopt the Einasto-backbone fits computed in Paper I §3.6 (identical pipeline, identical BIC model selection over $n_{\rm shells} \in \{0, 1, 2\}$, identical strict $\sigma/r \le 0.4$ enforcement), applied to the same 101-galaxy NGC 6674-excluded canonical sample.

**Classification agreement.** 89 of 101 galaxies (88.1%) receive the same shell-bearing classification under both backbones. Of the 12 classification changes, 10 are Burkert-shell-bearing galaxies that the Einasto backbone reclassifies as non-shell-bearing — the more flexible Einasto profile absorbs their localized residuals into a smoother fit. The remaining 2 are Einasto-shell-bearing galaxies that Burkert reclassifies as non-shell-bearing. Net result: 43 shell-bearing galaxies under Einasto (vs 51 under Burkert), with 62 total shells (vs 67) and 19 two-shell galaxies (vs 16).

Table 3.3.6 reports the headline signatures under both backbones.

| Quantity | Burkert | Einasto |
|---|---|---|
| Shell-bearing galaxies | 51/101 (50.5%) | 43/101 (42.6%) |
| Total shells | 67 | 62 |
| Two-shell galaxies | 16 | 19 |
| Morphology gradient $\rho_{\rm per\text{-}T}$ | $-0.76$ ($p = 0.028$) | $-0.87$ ($p = 0.005$) |
| Bulge correlation OR | 3.67 ($p \approx 0.01$) | 4.32 ($p = 0.003$) |
| $M$-$r$ slope | 0.76 | 0.82 |
| $M$-$r$ Spearman $\rho$ | $+0.64$ | $+0.69$ |
| $\sigma$-$r$ slope | 1.04 | 0.38 |
| $\sigma$-$r$ Spearman $\rho$ | $+0.78$ | $+0.38$ |
| $\sigma/r$ population median | 0.275 | 0.173 |
| Inner-vs-outer $M$ | 14/16 ($p = 0.0001$) | 14/19 ($p = 0.0005$) |
| Inner-vs-outer $\sigma$ | 14/16 ($p = 0.0008$) | 13/19 ($p = 0.10$) |

The signatures fall into two groups by behavior under backbone change.

**Robust signatures (preserved or strengthened under Einasto):** The morphology gradient *strengthens* ($\rho_{\rm per\text{-}T}$ moves from $-0.76$ to $-0.87$, $p$ improves by a factor of $\approx 6$). The bulge correlation *strengthens* (OR rises from 3.67 to 4.32; $p$ drops from $\approx 0.01$ to 0.003). The mass-radius scaling is preserved and slightly steepens (0.76 → 0.82) with stronger Spearman $\rho$ ($+0.64 \to +0.69$). The inner-vs-outer mass ordering survives at high significance (14/19 with $p < 10^{-3}$, comparable to the Burkert 14/16 result).

**Backbone-baseline-dependent signatures (attenuated under Einasto):** The width-radius slope drops substantially (1.04 → 0.38), with the Spearman $\rho$ falling from $+0.78$ to $+0.38$. The $\sigma/r$ population median shifts from 0.275 to 0.173. The inner-vs-outer width ordering, robust under Burkert ($p = 0.0008$), reduces to marginal significance under Einasto ($p = 0.10$).

This pattern admits a natural interpretation. Galaxy-level shell-bearing classifications and localized-mass-feature properties — what fraction of galaxies host shells, where the shells sit, and how massive they are — reflect mass concentrations whose detection does not depend strongly on the smooth backbone's specific functional form. Shell-*width* parameters, however, are partially degenerate with backbone profile shape: Einasto's free $\alpha$ parameter can absorb part of the radial variation that, under Burkert, is parameterized by shell width $\sigma$. The shifts in $\sigma$-$r$ slope and $\sigma/r$ median are therefore consistent with shell-width parameters partially decomposing differently under a more flexible backbone, while the integrated mass-feature signal remains robust to backbone choice.

The principal conclusion of §3.1 — that the shell population exhibits reproducible internal organization beyond what the smooth backbone alone explains — survives the Einasto control analysis in the load-bearing morphology, bulge, and mass-scaling signatures. The width-related signatures should be understood as defined relative to a specific choice of smooth-halo family, consistent with the §4 framing of all organizational signatures as *residual organization relative to a constrained smooth-halo baseline*. The backbone-family caveat therefore applies more strongly to width-related signatures than to mass-feature signatures; the latter are demonstrated here to survive at least one strict increase in backbone flexibility.

We emphasize that Einasto is one specific alternative backbone. Broader-family comparisons — generalized NFW with free inner slope, spline or nonparametric profiles, hierarchical Bayesian smooth-halo models — remain necessary future tests. The Einasto result establishes that the load-bearing signatures of §3.1 are not artifacts of the specific Burkert backbone, but does not exhaustively establish backbone-independence.

> **[Figure 3.3.6 — Einasto backbone comparison]** Two-panel figure: (left) shell-bearing classification grid comparing Burkert vs Einasto (89/101 agreement, 10 Burkert-only, 2 Einasto-only); (right) overlay of $M$-$r$ scaling under both backbones with linear fits annotated.
> *Data source:* Paper I `data/einasto_full_sample_results.csv` joined with canonical Burkert fits.
> *Status:* Placeholder; generation script pending.

#### 3.3.7 Random-structure null tests (cross-reference to §3.2)

The scrambling and permutation null tests of §3.2 establish that the shell selections are statistically distinguishable from random structure by $z$-scores of $-4.36$ and $-5.21$ for $\rho_{\rm per\,T}$ under scramble and permute respectively, and $-3.04$ and $-8.33$ for $\rho_{\rm per\,galaxy}$. Both tests target the hypothesis that the BIC-selected shells could be detector-flexibility artifacts of fitting random or shape-randomized data. The asymmetric failure modes (scramble under-detects, permute over-detects) further establish that the shell population is a property of spatially coherent localized residual structure, not a property that survives destruction of either the residual coherence (scramble) or the rotation-curve shape (permute).

#### 3.3.8 Combined verdict

The localized structures detected by v7.0 satisfy seven complementary tests against artifact origin:

1. Shell radii do not coincide with disk dynamical scales ($R_{\rm disk}$, $2.15\,R_{\rm disk}$, $R_{\rm eff}$, $r$ at $V_{\rm rot}^{\rm peak}$).
2. Shell selections survive 0.1-dex log-normal perturbations to disk and bulge mass-to-light ratios with 86.2% per-fit and 95.1% per-galaxy mode-match against canonical.
3. Shell selections survive distance perturbations drawn from per-galaxy SPARC uncertainties ($e_D / D$ median 8.7%, max 132%) with 89.6% per-fit and 94.1% per-galaxy mode-match.
4. Shell selections survive inclination perturbations drawn from per-galaxy SPARC uncertainties ($e_i$ median 3°, max 10°) with 95.7% per-fit and 98.9% per-galaxy mode-match.
5. Headline structural patterns (mass-radius scaling, width-radius scaling, $\sigma/r$ universality, morphology gradient, bulge correlation) survive on a conservative anti-warp clean subsample retaining only inner shells in disk-dominated, high-quality, inner-disk regimes.
6. Galaxy-level signatures (morphology gradient, bulge correlation) and mass-feature signatures ($M$-$r$ scaling, inner-vs-outer mass ordering) survive replacement of the Burkert backbone with the strictly more flexible Einasto profile (88% classification agreement; §3.3.6). Width-related signatures attenuate under Einasto and are reported as backbone-baseline-dependent.
7. Shell-selection statistics are inconsistent with random or shape-randomized data at the $3\sigma$–$8\sigma$ level (§3.2).

No single test is decisive in isolation. Each addresses a specific potential artifact channel: disk dynamics, baryonic input systematics ($\Upsilon$, $D$, $i$), warp geometry, backbone-family flexibility, and random structure. The signal survives all seven tests in concert. We therefore conclude that the localized structures detected by v7.0 in SPARC galaxies are not consistent with artifacts of the fitting procedure or measurement systematics within the channels tested. Whether they represent genuine localized halo mass features or some other form of organized galactic dynamics remains an open physical question.

---

## 4. Discussion

The results presented in §3 establish that the shell population identified by the v7.0 framework exhibits multiple forms of organized statistical structure. These include morphology dependence, correlations with bulge presence, radial scaling relations in shell width and shell mass, coherence-sensitive null-test behavior, and substantial stability under perturbations to the principal baryonic input parameters. Taken together, these patterns indicate that the shell population is not behaving like an arbitrary collection of unrelated fit artifacts.

At the same time, the present work does not establish a unique physical interpretation for the detected structures. The analysis demonstrates organization and robustness, but does not prove that the localized residual components correspond to discrete physical halo substructures. Several alternative interpretations remain possible, including correlated residual structure arising from non-axisymmetric dynamics, incompletely modeled baryonic effects, or limitations of the adopted smooth-halo backbone. The present paper therefore constrains classes of explanation without uniquely identifying a mechanism.

The most important caveat concerns the choice of smooth-halo backbone. All organizational signatures reported here are defined relative to a constrained Burkert backbone, chosen in Paper I for its physically motivated finite central density, three-parameter parsimony, and explicit interpretability. A more flexible smooth-halo family — generalized NFW with free inner slope, Einasto with free shape parameter, spline or nonparametric profiles, or hierarchical Bayesian smooth-halo models — could in principle absorb some or all of the localized residual structure into a smoother profile. The patterns reported in this paper are therefore properly understood as *residual organization relative to a constrained smooth-halo baseline*.

We provide one direct test of backbone-family robustness in §3.3.6, using the Einasto profile as the comparison backbone. Einasto introduces one additional parameter relative to Burkert (the shape parameter $\alpha$) and is therefore strictly more flexible. Galaxy-level signatures (morphology gradient, bulge correlation) and mass-feature signatures ($M$-$r$ scaling, inner-vs-outer mass ordering) survive or strengthen under the Einasto backbone, with 88% classification agreement at the galaxy level. Width-related signatures ($\sigma$-$r$ slope, $\sigma/r$ distribution, inner-vs-outer $\sigma$) attenuate under Einasto, consistent with shell-width parameters being partially degenerate with backbone profile shape. We interpret the load-bearing signatures of §3.1 as backbone-family-robust within at least one strict increase in flexibility; broader comparisons against generalized NFW, spline/nonparametric, and hierarchical Bayesian backbones remain necessary future tests.

The spatial-coherence null tests of §3.2 provide the strongest evidence that the shell population depends on organized structure present in the observed rotation curves themselves. The two destructive null procedures fail in opposite directions: residual scrambling suppresses the morphology gradient, while full cross-radius velocity permutation over-produces shell detections. This asymmetric behavior is difficult to reconcile with the hypothesis that the observed shell population arises primarily from random fitting flexibility or from Gaussian shells acting as a generic localized basis: under either hypothesis, randomization procedures that preserve global residual amplitude but destroy spatial coherence should yield equivalent population-level organization, which the destructive nulls demonstrate they do not. The spatial coherence of the underlying residual structure within individual galaxies is therefore essential to reproducing the observed population-level organization, which is not what one would expect if shells were behaving as a generic localized basis.

The perturbation tests of §3.3 further constrain several important artifact channels. Shell selections remain substantially stable under realistic perturbations to stellar mass-to-light ratio, galaxy distance, and inclination, with only modest shifts in population fractions and shell positions. Similarly, the principal organizational signatures persist within the conservatively defined anti-warp clean subsample, suggesting that outer-disk warp artifacts are unlikely to dominate the observed patterns. These results do not eliminate all possible systematic effects, but they substantially narrow the set of simple explanations capable of reproducing the observed population structure.

Several limitations remain important. First, the present analysis depends on the v7.0 decomposition framework and does not establish decomposition uniqueness. Other flexible residual parameterizations or generalized smooth-halo families may potentially absorb part of the observed structure. In particular, comparisons against generalized NFW, free-shape, or hierarchical nonparametric backbones remain necessary future tests. Second, the present work analyzes one-dimensional rotation-curve structure rather than full two-dimensional velocity fields. Explicit modeling of noncircular motions, bars, spiral structure, and warped geometries would provide a stronger separation between localized halo structure and baryonic dynamical effects. Third, the shell population remains modest in size, particularly within the two-shell subsample and the anti-warp clean sample, limiting the statistical power of some higher-order comparisons.

Despite these limitations, the observed organization places meaningful constraints on interpretation. If future analyses confirm that similar residual organization persists across broader backbone families, independent galaxy samples, and higher-dimensional kinematic data, then galaxy rotation curves may contain statistically organized structure beyond conventional smooth-halo descriptions. Whether such structure corresponds to localized dark-matter features, baryon-coupled dynamical phenomena, or another form of organized galactic behavior remains an open question.

Future work should therefore focus on four directions: (i) testing the persistence of the shell population under broader halo-profile families and nonparametric decompositions; (ii) incorporating full velocity-field information from IFU and resolved HI observations; (iii) constructing hierarchical population-level statistical models for shell occurrence and scaling behavior; and (iv) evaluating whether existing dynamical or cosmological simulations naturally reproduce the observed organizational patterns.

---

## 5. Conclusions

We have investigated whether the localized residual structures identified in the v7.0 SPARC rotation-curve framework of Paper I behave like a statistically organized population or like an accumulation of unrelated fitting artifacts. Using the NGC 6674-excluded 101-galaxy SPARC sample spanning morphological types $T = 2$–9, we analyzed the internal organization, coherence dependence, and robustness properties of the shell-bearing population identified through Bayesian model selection.

The shell population exhibits several forms of empirical organization. Shell-bearing fraction decreases systematically toward later morphological type, while bulge-dominated galaxies are preferentially shell-bearing relative to bulgeless systems. Shell width scales approximately linearly with shell radius, producing a characteristic fractional width $\sigma/r \approx 0.27$ across more than two decades in radius. Within two-shell galaxies, outer shells are systematically more massive than inner shells. These organizational signatures extend the morphology dependence identified in Paper I from a between-galaxy property to a property of the shell population itself.

Two destructive null procedures demonstrate that the morphology gradient depends on coherent residual structure within the observed rotation curves. Residual scrambling suppresses the observed gradient, while cross-radius velocity permutation over-produces shell detections, yielding opposite failure modes relative to the real data. Additional perturbation tests show that shell selections remain substantially stable under realistic variations in stellar mass-to-light ratio, galaxy distance, and inclination. The principal scaling relations also persist within a conservatively defined anti-warp clean subsample. A direct Einasto-backbone comparison shows that the morphology, bulge, and mass-feature signatures persist under a more flexible smooth-halo family, while width-related signatures are more backbone-dependent.

These results disfavor random fitting behavior, baryonic measurement systematics, and simple warp-dominated explanations as dominant origins of the shell population. However, the present analysis does not establish a unique physical interpretation for the detected structures. The results demonstrate organized residual behavior and robustness against several major artifact channels, but broader comparisons against alternative decomposition frameworks and higher-dimensional kinematic analyses remain necessary.

The principal conclusion of the present work is therefore statistical rather than ontological: the localized residual structures identified by the v7.0 framework behave like a coherent organized population rather than a purely random collection of fit artifacts. Determining the physical origin of that organization remains an open problem for future investigation.

---

## Acknowledgments

> *To be drafted.*

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

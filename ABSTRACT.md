# The Hold-Up Problem as a Barrier to Green Industrial Symbiosis: An Agent-Based Model of Investment, Trust, and Institutional Design

## Extended Abstract

### Background and Motivation

Industrial Symbiosis (IS) networks—where firms exchange waste streams as valuable inputs—offer a promising route toward circular economy goals. Yet these networks remain surprisingly rare despite clear benefits. Why?

This paper investigates a fundamental barrier: the **Hold-Up Problem**. When a producer invests in specialized waste-processing infrastructure, they become dependent on their trading partners. If a downstream consumer later behaves opportunistically—renegotiating terms or extracting value—the producer cannot easily walk away from their sunk costs. This vulnerability may deter green investment even when the aggregate benefits are substantial.

We ask: How do market conditions, formal contracts, and informal trust mechanisms interact to determine whether IS networks can take root and survive?

### Methodology

We built an agent-based model in NetLogo to simulate IS network formation. Fifty producers decide whether to "invest" (incurring upfront costs) or stay "cautious." Fifty consumers choose between "honest" and "opportunistic" strategies. When partnerships form, the classic hold-up game unfolds—cooperation splits gains fairly, while opportunism leaves producers with scraps.

The model incorporates several institutional mechanisms: legal contracts (probabilistic enforcement), reputation systems (producers remember and avoid bad partners), and lock-in periods (minimum contract duration). Market turbulence adds uncertainty by making synergy values fluctuate randomly.

We ran 4,320 simulations across a comprehensive parameter sweep: turbulence (0-5), contract enforcement (0-100%), memory duration (10 vs 100 periods), investment cost (0, 5, 10), synergy surplus (5, 15), and lock-in period (10 vs 30). Each run lasted 1000 time steps.

### Key Findings

Our results reveal a clear hierarchy of what matters—and what doesn't:

**Investment cost dominates everything else.** With zero investment cost, networks thrive at 99.5% participation regardless of other conditions. With high costs (10 units), survival collapses to just 1.6%—even when turbulence is zero and contracts are perfectly enforced. That's a 98 percentage point gap attributable to cost alone.

**Synergy surplus acts as a buffer.** High-value exchanges (surplus = 15) sustain 67% participation; low-value ones (surplus = 5) manage only 34%. Networks built around premium waste streams—industrial heat, specialty chemicals—simply have more margin for error.

**Turbulence matters far less than expected.** Across turbulence levels 0-5, participation rates vary by only 0.5 percentage points. This surprised us. It suggests that fears about price volatility may be overblown relative to structural cost barriers—by roughly 200 to 1 in terms of effect size.

**Memory and law substitute for each other.** Long institutional memory and strong contracts produce nearly identical outcomes (less than 1 percentage point difference). Informal reputation mechanisms can work as well as formal enforcement.

### Policy Implications

If cost barriers matter 200 times more than market volatility, where should policymakers focus?

Our findings argue for leading with cost reduction: capital subsidies, tax incentives, shared infrastructure, or public co-investment that absorbs initial risk. While contracts and reputation systems help, they cannot overcome prohibitive entry costs on their own.

This is a reallocation argument. Resources spent stabilizing material prices might yield far greater returns if redirected toward reducing upfront investment barriers.

### Contribution

The hold-up problem in IS networks is not new as a concept. What we add is quantification. Through systematic parameter sweeps, we provide numerical estimates of effect magnitudes that can guide policy prioritization. Our counter-intuitive finding on turbulence challenges common assumptions and offers evidence against the instinct to focus on market stabilization first.

---

**Keywords:** Industrial Symbiosis, Hold-Up Problem, Agent-Based Modeling, Green Investment, Circular Economy, Institutional Economics

**Word Count:** 608

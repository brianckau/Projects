# Product-first investment research

## Purpose and reading order

Use this workflow in investment research after the entry menus and company/universe intake. For a broad universe, first shortlist companies by the user's mandate and available evidence; run a bounded pilot company before multiplying every specialist across the universe. Reuse market-discovery roles from research-and-agents.md and the common evidence ledger. Use quantitative-judge.md for expectations and value bridges. Do not run a separate generic setup again after completing these waves.

Find a defensible chain: product mechanism → relative customer value → adoption/pricing/retention or displacement → revenue/margins/cash flow → difference from expectations → security payoff. Permit long or short candidates. Superior engineering alone is not a thesis; a missing benchmark is not evidence of parity; commercial success alone is not evidence of mispricing.

## Agent distribution and dependencies

The coordinator owns company/product materiality, comparison quality, budget, evidence deduplication, edge qualification, and final integration. Give specialists neutral questions initially, not a requested bullish conclusion. Do not delegate unrestricted recursive spawning. Pass one shared company identity, as-of date, product/version scope, horizon, source route, evidence schema, and per-task research boundary.

| Wave | Subagents | Work and handoff |
|---|---|---|
| 1 — independent discovery | 1 target product scientist; 1 competitor mapper; 1 document catalyst researcher; 4 existing market roles: guidance, consensus, professional narratives, community narratives | Scientist builds target dossier; mapper identifies realistic alternatives and buyer segments; catalyst researcher extracts dated events/dependencies from source documents and routes them using catalyst-discovery.md; market roles establish expectations and debated drivers. These are seven separate tasks; queue tasks to respect capacity. |
| 2 — matched comparisons | N competitor product scientists, exactly 1 per shortlisted competitor | Launch after mapper shortlist and coordinator comparison brief. Each scientist independently researches that competitor's material matched offerings and substitutes, using original source documents rather than copying the target's claims. Return dossiers to the coordinator. |
| 3 — implications and challenge | 1 venture-capital analyst; 1 existing initial bull-bear mapper | Launch after comparable dossiers exist. Both receive normalized technical facts and market evidence; the VC analyst underwrites adoption and economics, while the bull-bear mapper independently tests rival explanations. Exchange outputs only after initial independent conclusions. |
| 4 — thesis integration | Coordinator, using the completed research packet | Qualify product-derived long/short candidates; quantify financial implications and market variance. If qualification fails, route to targeted alternative-angle workers below. Give the strongest synthesized candidate and input sources to the independent disconfirmation reviewer before returning it. Reuse the existing initial bull-bear mapper for this assignment where available. Run the full attacker/defender/adjudicator protocol when strengthening is requested. |

N means the material shortlist, not every company named online. Default to three competitors selected for actual substitutability, material competitive pressure, or an important low-cost/disruptive alternative; use fewer when the competitive set is genuinely smaller. Include new entrants or non-product alternatives when they decide buyer choice. Expand only if an omitted competitor could change the conclusion and the research budget permits; record shortlist and exclusions rather than implying full market coverage. One competitor scientist may cover multiple relevant products at that company, clearly separating models and applications.

With seven total concurrent slots, allow at most six workers plus the coordinator: start target scientist, competitor mapper, catalyst researcher, guidance, consensus, and professional narratives; queue community narratives for the first available worker slot. Complete the seven discovery tasks across these batches. Finish/release or reuse workers between waves; queue competitor workers if N exceeds capacity. Never exceed the runtime limit or assume seven slots exist in every host. Report the chosen allocation and material omissions succinctly. Preserve the shared API budget across all waves; do not give each worker a separate full quota. The added scientists primarily need technical primary sources, not extra paid narrative calls.

Default to one target dossier, one mapper shortlist, one document catalyst scan with a routed event register, one dossier per shortlisted competitor, one VC pass, one initial bull-bear pass, and one targeted clarification round. Use one fallback wave of at most three prioritized alternative-angle workers if necessary. Do not repeat speculative searches indefinitely; document residual uncertainty and return “no defensible edge found” when appropriate. When orchestration is unavailable, perform the same labeled analytical passes sequentially and disclose the loss of independent agent work.

## Target and competitor scientists

Apply a scientist's method, not an authoritative persona. Explain the underlying mechanism, constraints, trade-offs, failure modes, and economics of the company's key offerings. Select products by current revenue/gross-profit contribution and credible future materiality; cover a meaningful downside exposure as well as the flagship. Keep speculative pipeline products separate from shipped, qualified, commercially available products. Use segment filings and company economics to avoid spending most effort on an immaterial demonstration.

For each material offering, establish:
- Customer job, application, buyer, alternatives, operating environment, and binding purchase constraint.
- Mechanism and architecture: what produces the claimed performance, what trade-off it creates, and which components/IP, software, service, or ecosystem are necessary.
- Decision-relevant measurable specifications: definition, unit, model/version, date, test conditions, duty cycle, uncertainty, and source. Distinguish measured outcomes, advertised specifications, certified limits, and inference. Mark absent data unknown.
- Price and full customer cost: installation/integration, consumables, energy, maintenance, downtime, support, financing, switching, training, and useful life where material. Keep list price, realized ASP, and estimated cost separate.
- Supplier economics: bill of materials/cost drivers, yield, manufacturing scale, capex/reinvestment, supply dependencies, and how savings or differentiation are shared with customers. Use ranges/proxies with explicit limitations when internal costs are unavailable.
- Evidence of real deployment, reliability, qualification, regulatory/compliance hurdles, returns/warranty risk, and scaling bottlenecks. An order, pilot, shipment, revenue recognition, and repeat purchase are distinct milestones.

Prefer original technical manuals, data sheets, recognized testing/certification records, filings, peer-reviewed mechanism research, and documented customer deployments. Patents explain claims/architecture but do not prove performance, freedom to operate, adoption, or durability. Vendor demos and marketing require explicit labels. Do not claim to have conducted experiments or inspected hardware. Avoid interpreting unavailable confidential engineering information as a known fact.

For software, platforms, or services, translate science into measurable workflow performance, accuracy/error rates, latency, interoperability, reliability, customer outcomes, service capacity, and delivery economics. Compare benchmarks under matched workloads and deployment conditions. For businesses without meaningful product specification differentiation, document that finding and move to customer economics or other angles; do not invent a hardware-style benchmark exercise.

## Competitor mapper and normalized comparison

Map competition by customer use case and budget, not merely listed industry peers. Include direct competitors, emerging substitutes, internal customer solutions, and existing ways of performing the job. Record product availability, geography, pricing tier, distribution/channel, qualification, installed base, and why each alternative wins or loses a purchase. The mapper proposes the shortlist; the coordinator checks materiality before commissioning specialists.

Send each competitor scientist the same **comparison brief**: target customer/job, product class and generation, relevant horizon, required purchase constraints, metric definitions and test conditions, economic inputs needed, and evidence format. Do not supply a prewritten conclusion about target superiority. Let specialists identify important missing metrics and alternative strengths.

Have the coordinator normalize a matrix with columns:
`use case | company/model/version | shipped/prototype status | metric/value/unit | test conditions | price/TCO | source ID/date/type | comparability limits | customer relevance`.

Do not rank peak versus continuous performance, precision versus repeatability, laboratory versus field results, component versus whole-system results, nominal versus usable capacity, or list price versus full installed cost as equivalent measures. Do not infer superiority from one headline metric while ignoring a binding customer constraint. If conditions cannot be reconciled, mark the comparison non-comparable and identify the test/data needed. A valid cross-model comparison should preserve trade-offs rather than manufacture one universal winner.

Return a short list of strongest advantages **and disadvantages**, each with a causal mechanism, matched evidence, applicable segment, customer value, limits, and credible replication/substitution risk. Apply these requirements symmetrically to the target and its competitors. Ask scientists to resolve decision-critical disagreements once; if unresolved, preserve both accounts and qualify conclusions.

## Venture-capital lens: commercial underwriting

Assign a separate analyst to test whether the strongest technical advantages/disadvantages imply growth, deterioration, or overestimated prospects. Give this analyst both favorable and unfavorable normalized evidence, company economics, horizon, and the expectations packet. Require a bear case and an overvaluation/overexpectation check even when the product is superior. Treat the VC lens as disciplined adoption and value-capture analysis, not thematic enthusiasm or automatic multiple expansion.

For each potential differentiator or weakness, answer:
1. **Need:** Which paying customer has a costly problem or unmet performance requirement? Does the improvement clear a purchase threshold, or exceed what the use case needs? What existing alternative solves it adequately?
2. **Economic value:** Quantify payback, productivity, quality, risk reduction, or customer profit using realistic utilization and total cost. Identify who captures the savings. A technically better supplier may still surrender value through competitive pricing or powerful customers.
3. **Adoption:** Trace qualification → trials → orders → delivery → revenue → repeat purchase. Examine switching costs, installed base, distribution, procurement cycles, interoperability, regulation, financing, service coverage, and capacity. Separate evidence of each stage from assumptions about conversion.
4. **Market and competition:** Build a bottom-up serviceable market from eligible customers × realistic units/spend, adoption rate, share, and realized price. Distinguish incremental demand from replacement/cannibalization; do not multiply a broad industry TAM by an unsupported share. Test competitor response, alternative technologies, entry, and durability over the investment horizon.
5. **Company economics:** Translate adoption into units/customers × ASP/monetization, margin, operating expenses, working capital, capex, funding/dilution, and free cash flow. Show constraints on delivery, profitability, and scalability. Growing revenue with worsening economics can support a short rather than a long.
6. **Expectation gap:** Compare the resulting operating range with dated guidance, broker estimates, verified consensus, and conditional valuation-implied assumptions, each separately labeled. Explain whether the market overestimates or underestimates adoption, pricing, margins, durability, or timing. Do not infer unpriced growth merely because forum authors omit the technology.

Return an underwriting table: `advantage/disadvantage | customer and segment | economic benefit/cost | adoption evidence and friction | realizable growth range | financial bridge | expectation gap | catalyst/horizon | falsifier | evidence IDs/unknowns`. Show the minimum assumption required for financial materiality and the strongest reason the implication may fail. Treat calculations as scenario assumptions until supported, not scientific measurements.

## Product-route qualification and handoff

Have the coordinator judge each chain using these explicit gates:
- **Technical validity:** Is the comparative claim supported under relevant, matched conditions, or is a claimed moat itself refuted?
- **Customer significance:** Does the difference affect purchasing, retention, pricing, operating cost, or risk in a material segment?
- **Commercial and financial materiality:** Can it change company economics within the horizon, considering revenue mix, conversion, capacity, cannibalization, investment needs, and dilution?
- **Expectation difference:** Is there a defensible distinction from the market comparator, with source/date and uncertainty, rather than only an interesting business observation?
- **Investability:** Is there a plausible valuation/payoff bridge, downside case, and observable test or recognition mechanism?

Classify outputs as **qualified candidate**, **promising but unverified**, or **no product-derived edge identified**. Explain each failed/unknown gate. A qualified candidate may still fail later thesis-strengthening debate; qualification is not a trade recommendation or a calibrated probability. Preserve negative findings: evidence that a claimed technological moat is exaggerated can support a short if customer/financial/expectations links hold. A genuinely superior product already embedded in expectations may yield no long edge, or an overexpectation candidate if the market requires unrealistic adoption.

If market expectations or decisive technical data are unavailable, label the idea provisional and list the decisive missing evidence; do not confuse lack of data with evidence of no differentiation. Permit one targeted clarification round, then move on to other angles while preserving that unresolved lead.

Feed thesis discovery the normalized comparison, technical mechanisms, customer-economic bridge, VC underwriting, initial bull-bear map, expectation sources, rejected claims, unresolved contradictions, scenario assumptions, catalyst register with specialist responses and linked dependencies, catalyst/falsifier, and candidate status. Have the coordinator form candidate theses without rerunning identical collection. Do not expose a final 100-point score until the existing quantitative rubric's requirements are met.

## Fallback: other angles when the product route yields no edge

Keep catalyst discovery active as a research route even when product differentiation fails; route financing or corporate-event findings directly to the appropriate analyst. Trigger fallback when no candidate survives the gates, including non-differentiation, irrelevance to buying, immaterial financial effects, growth already priced in, or unresolvable evidence gaps after the bounded clarification round. State the reason and preserve useful product facts. Do not keep commissioning competitors to rescue a preferred story.

Rank alternative angles by available contradictory evidence, likely financial sensitivity, and information value; select up to three workers for the strongest leads, not one worker per generic category. Useful angles include:

| Angle | Decision to investigate |
|---|---|
| Demand, cycle, customer/channel mix | Does demand normalization, customer concentration, inventory, geography, price/mix, or backlog conversion differ materially from expectations? |
| Costs, industry structure, unit economics | Are scale, utilization, input costs, yields, capacity additions, competition, customer power, or supplier economics changing margins/cash generation? |
| Accounting, cash conversion, balance sheet | Do recognition policies, capitalization, working capital, cash/debt restrictions, funding needs, or dilution undermine reported growth/earnings? |
| Capital allocation, governance, corporate events | Can reinvestment, acquisitions, distributions, asset sales, ownership incentives, or a dated event change per-share value? |
| Regulation, distribution, business model | Do licensing, reimbursement, market access, channels, pricing structure, or switching costs change outcomes without technical superiority? |
| Expectations, valuation, positioning | Is there a sourced operating-expectation or valuation inconsistency? Separate proven positioning data from speculation; “cheap” alone is not an edge. |

Every worker must return a falsifiable claim, dated market comparator, primary evidence for/against, quantitative financial bridge, recognition event/horizon, and reason to reject the idea. Use the same evidence rules and missing-data labels as the product route. Integrate only supported candidates. If none survives, return a clear no-edge finding, the most important unresolved question, and one best next check; do not manufacture three theses to fill the requested output count.

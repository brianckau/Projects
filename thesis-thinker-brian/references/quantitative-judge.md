# Quantitative judge

## Establish the counterfactual

Write the thesis as “Over [horizon], [driver] will be [estimate/range] versus [dated expectation], because [mechanism]; [observable evidence/event] will resolve the gap.” Preserve a qualitative thesis when no defensible number exists, but flag the missing quantitative bridge.

Use an expectations ladder: (1) verified provider consensus with timestamp and coverage; (2) explicitly named broker estimates; (3) management guidance; (4) valuation-implied assumptions; (5) sampled narratives. These are different objects, not interchangeable levels of certainty. A reverse DCF is conditional on margins, reinvestment, discount rate, and terminal assumptions; run sensitivities and never describe its growth output as directly observed market consensus. A single quoted target price does not establish the market's operating assumptions.

## Financial bridge and payoff

Use company-appropriate identities. For ordinary operating companies, possible bridges include revenue = volume × ASP, gross profit = revenue × margin, and incremental EBIT = incremental gross profit − incremental operating costs. Model stock compensation, tax, working capital, capex, financing, dilution, and minority interests where material. Use sector-specific metrics for banks, insurers, property companies, and other businesses where ordinary EV/EBITDA or FCF would mislead.

State the baseline and avoid counting the same upside in volume, mix, margins, and multiple expansion. Show sensitivities for the few assumptions that decide the thesis. Check revenue versus recognized revenue, backlog versus contracted orders, stock versus flow, currency, fiscal versus calendar periods, and adjusted versus reported figures. Growth from a near-zero base is not itself material earnings impact.

Construct bear/base/bull operating outcomes with sources and assumptions, then independently specify valuation outcomes. Show what happens if the operational thesis succeeds but the valuation multiple contracts. For applicable companies, reconcile enterprise value to equity using net debt and other material claims; divide by a consistent diluted share count and convert currency/ADR ratios explicitly. State share-price timestamp. Avoid precise price targets without required inputs.

If scenario probabilities are used, state their basis and ensure they sum to 1. Compute expected total return as sum(p_i × scenario total return_i), including distributions, dilution, or carry where material. Model contingent outcomes with conditional probabilities; do not assume independence for proof, customer adoption, approvals, or growth that share a causal driver. Keep scenario probabilities separate from the thesis index. Do not call an attractive expected return sufficient without discussing downside and timing.

## Scoring rubric

Score each dimension from 0 to 5; allow half-points only when the evidence lies between anchors. Use the same rubric for long and short theses. Treat these weights as transparent defaults, editable by the user before adjudication, not validated empirical coefficients.

| Dimension | Weight | 0 | 1–2 | 3 | 4–5 |
|---|---:|---|---|---|---|
| Market variance | 25% | No meaningful difference or contradicted claim of novelty | Primarily a narrative difference; comparator weak or stale | Explicit material difference versus a dated expectation, with limits | Strong evidence for an underappreciated, material driver; triangulated expectations and alternative explanations addressed |
| Evidence | 30% | Core premise contradicted by reliable evidence | Anecdote, assertions, weak proxies, or management claims without corroboration | Relevant verified evidence with important gaps | Direct current evidence, independent corroboration where feasible, contradictions reconciled and clear falsifiers |
| Investment impact | 25% | No economic effect or no causal bridge | Direction plausible but financial impact/valuation uncertain | Reproducible operating-to-value bridge; sensitivity and failure case shown | Material robust payoff across defensible assumptions, downside and valuation already considered |
| Catalyst strength | 10% | Identified event cannot test the thesis | Vague event or weak connection to belief revision | Observable event with plausible recognition mechanism | Dated, discriminating event likely to expose the contested driver; alternative outcomes mapped |
| Timeliness | 10% | Thesis cannot play out in the stated horizon | Long or highly uncertain lag; funding/path risks poorly handled | Plausible horizon with key dependencies identified | Supported sequence within horizon, sufficient runway and explicit monitoring/exit conditions |

Distinguish missing evidence from negative evidence: mark an unsupported dimension **unknown**, not zero. Do not score market variance merely because the user's view differs from one public article. Reward evidence of underappreciation, not obscurity alone. Absence of a scheduled catalyst does not by itself invalidate a long-horizon investment; explain the effect of the horizon and allow disclosed alternative weights.

For known dimensions compute contribution = weight × score/5. The full index is the sum of contributions on a 0–100 scale. For missing dimensions, report the unresolved interval [sum of known contributions, sum of known contributions + missing weights]; do not renormalize or silently insert a midpoint. Withhold a single overall index until all five dimensions can be assessed. Label all outcomes “uncalibrated research judgment”; never interpret 80/100 as an 80% success probability.

Show score, weight, contribution, one-sentence justification, and evidence IDs for each dimension. Give separate assessments of (a) causal thesis plausibility and (b) investment attractiveness at current price. Use qualitative bands only as descriptive guidance: below 40 weak, 40–59 tentative, 60–74 credible with gaps, 75–89 well supported, 90+ exceptional and requiring explicit scrutiny. These bands are not performance forecasts.

## Gates and revision

Do not let a high aggregate hide a broken core premise. Explicitly mark: core premise falsified; market comparator unavailable; value bridge missing; decisive data inaccessible; or horizon mismatch. If core premise is falsified, conclude that the current thesis fails even if ancillary dimensions score well. If the market comparator or value bridge is unavailable, withhold a firm investability conclusion.

List the strongest surviving objection, the largest unresolved uncertainty, and the cheapest/highest-information next research step. Separate invalidation, valuation/price-based exit, and monitoring triggers. Update scores only when evidence or assumptions change; record old score, new score, reason, and source. Do not add mechanically precise deductions for unquantified risks.

Use `scripts/score_thesis.py` with JSON dimension scores (or null for unknown) to reproduce default-weight arithmetic. Financial model and probability arithmetic require separate verification; this helper is not a valuation model.

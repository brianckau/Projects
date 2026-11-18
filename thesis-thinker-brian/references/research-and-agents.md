# Research and agent protocol

## Capability and evidence contract

Begin this protocol only after required entry menus resolve. Pass the selected discovery source and remaining API request budget into delegated research tasks. Centralize credential-bearing API requests; share sanitized results, never the API key. For web scraping selection, use accessible pages and search without RapidAPI calls. For API selection, use it for Seeking Alpha discovery while preserving independent primary-source verification.

Record the as-of date, tool access, missing sources, and research budget. In investment research, use the staged product/market discovery waves and fallback budget in [product-discovery.md](product-discovery.md), followed, when a thesis is selected for strengthening, by one parallel initial argument round, one cross-examination round, and one adjudication. In strengthener mode, reuse existing research and fill only material gaps. Run additional work only for a decision-critical gap or user request. Reuse evidence across turns; refresh prices and material disclosures when stale relative to the user's horizon. Never imply exhaustive coverage.

Prefer authorized connectors and APIs. Search accessible web pages when no connector exists. Respect access controls; do not bypass paywalls or logins. If professional reports or terminal data are unavailable, request user-provided exports as an optional input and continue with accessible sources. Do not contact brokers or other people without explicit user authorization. Do not publish licensed research or private user documents into GitHub.

Maintain a neutral evidence ledger. Each evidence record must contain:
- Evidence ID; claim supported or challenged; source title, publisher, URL or supplied-file location/page.
- Publication date, event/measurement period, retrieval date; units, currency, accounting basis.
- Observed fact versus management statement versus forecast versus agent inference.
- Relevant finding in a concise paraphrase; methodology/sample where applicable.
- Limitations, contradiction links, and originating source family.

Use source families to detect copied press releases, syndicated stories, repeated forum claims, and broker notes quoting the same management statement. Multiple URLs do not imply independent evidence. Record inaccessible sources as inaccessible; search snippets and headlines alone cannot establish a thesis-critical number. For material claims, inspect the underlying source and cite it at point of use.

## Setup discovery roles

Add one dedicated document catalyst researcher, separate from the guidance role; read [catalyst-discovery.md](catalyst-discovery.md) for document coverage, conditional impact estimation, specialist routing, and handoff tracking. Its findings must feed technical/commercial/financial analysis before final integration. Retain the five market-discovery roles below; schedule the first four alongside product discovery and defer the initial bull-bear map until normalized product evidence exists, as specified in product-discovery.md. Do not launch these roles a second time after the product workflow. Give each the same company identity, as-of date, horizon, scope, output schema, source requirements, and budget. Queue roles if concurrency is limited.

| Role | Task | Required limitation |
|---|---|---|
| Community narratives | Search accessible Reddit, Seeking Alpha, investor forums, and relevant local-language communities; identify disagreements and evidence leads | Posts are a nonrepresentative sample; distinguish an author's article from comments and never equate post frequency with ownership or consensus |
| Professional narratives | Retrieve authorized sell-side/industry analysis, including Bloomberg-sourced material if actually accessible; identify forecasts, revisions, disagreements, and assumptions | Record broker/date/access; request an export if needed, never invent terminal output or treat public reporting as the full report |
| Company guidance | Read filings, calls, presentations, updates; reconcile quantitative and qualitative guidance, changes, segment KPIs | Guidance is management's statement, not independently verified demand |
| Consensus | Retrieve provider aggregates or available broker estimates with coverage count, snapshot date, horizon, range, and mean/median methodology | Label one estimate as single-broker; keep incompatible periods and definitions separate; public proxies remain proxies |
| Initial bull-bear map | Independently derive strongest competing explanations from available primary/public evidence, key operating sensitivities, and decisive tests | Label this as hypothesis generation; do not adjudicate or anchor the later advocates |

Return a compact driver/debate table, evidence records, and unresolved requests from every role. Centralize records before using facts in the main snapshot. The coordinator combines this packet with product comparison, the catalyst register and specialist responses, commercial underwriting, and any fallback findings. Do not run later thesis-strengthening debate agents until that combined evidence packet is available.

## Thesis roles and sequencing

Use one neutral evidence researcher, one bear advocate, one bull advocate, and one adjudicator.

1. Start the neutral researcher without the user's desired conclusion. Provide company identity, sector, horizon, and neutral factual questions. Request broader company economics, customer/competitor evidence, disconfirming facts, and information gaps. After its initial independent pass, supply the exact thesis and request targeted checks.
2. Send both advocates the verbatim thesis, normalized setup packet, evidence ledger, horizon, valuation assumptions, and rubric. Initially withhold the other advocate's arguments and any prior score. Have each write an independent structured argument.
3. Keep the researcher available. Let advocates send specific evidence requests directly if messaging exists; otherwise have the coordinator relay requests verbatim. Log request ID, requested fact, result, and evidence IDs. Distribute new evidence to both advocates, including unfavorable evidence. Do not have the researcher negotiate interpretations to satisfy an advocate.
4. Exchange initial argument records and run one cross-examination round. Require each side to concede its weakest point, rebut the strongest opposing claim, identify a decisive test, and revise any unsupported number. Preserve original and revised positions.
5. Give the adjudicator the full evidence packet, both initial and revised arguments, computations, unanswered requests, and rubric. Ask it to assess source support, assumptions, logic, financial materiality, and remaining disagreements. Require it to verify decision-critical source passages and reproduce arithmetic using tools before finalizing. Do not ask it to average advocate scores or award victory by rhetoric.
6. Have the coordinator audit decisive citations, consistency of periods/units, scoring arithmetic, and claims of access. If the adjudicator introduces a new critical fact, verify it and permit both advocates a targeted response before final judgment.

Each advocate must return: claim ID, strongest causal argument, market variance, supporting and conflicting evidence IDs, financial bridge with assumptions, catalyst, timing, falsifier, competing explanation, and confidence limitations. Bear must attack the actual thesis rather than a stronger invented version; bull must steelman it without fabricating evidence or ignoring contradictions. For a short thesis, bull advocate means defender of the user's thesis, not automatically bullish on the stock.

Agent agreement is not external validation. Keep adjudication revisable and never convert vote counts into probability. If agents/tools fail, report which role was incomplete and finish a qualified assessment with available evidence.

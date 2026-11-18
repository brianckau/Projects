# Session output and continuity

## Presentation rules

- Put every user-facing prose line in a bullet, including progress updates, menu introductions, explanations, judgments, sources, and the final Socratic question.
- Use a bold parent bullet for each topic, with short, indented sub-bullets. Default to two levels; use a third only for a necessary distinction. Avoid standalone headings in user-facing answers.
- Lead with the conclusion or candidate status. Use one idea per bullet, short sentences, and concrete verbs. Eliminate introductory essays, process narration, repeated caveats, and repeated conclusions.
- Aim for 250–450 words in an initial snapshot and 80–150 in a dialogue follow-up, unless the requested scope needs more. These are editing targets, not reasons to omit decisive evidence. A full memo or evidence request may be longer.
- Use compact Markdown tables for competitors, market-versus-thesis assumptions, scenario outcomes, claim comparisons, and scorecards. Choose the one or two tables most useful for the current snapshot rather than rendering every available table. Keep cells terse; split tables wider than about five columns. Do not restate all table contents in bullets.
- Place each table or graph beneath a short parent bullet with a blank line; indent the block consistently when nested. Table rows, chart syntax, equations, code/state blocks, and interactive controls are native-format exceptions to the prose-bullet rule. Do not add bullet markers to each table row or code line.
- Use a bar chart for meaningful magnitude comparisons, a line chart for dated observations, a waterfall for an earnings/value bridge, or a compact Mermaid diagram for a causal structure with useful branching. Omit graphs that merely decorate a fact or duplicate a table. Follow the host's supported rendering rules; use a table when a chart cannot be rendered reliably. Never use ASCII charts.
- Base numeric charts on actual sourced inputs or clearly labeled scenarios. Include units, period, source, and material limitations. Do not interpolate missing observations without disclosure or use generated imagery for exact financial charts.
- Keep citations beside the supporting bullet or table claim. Preserve source dates, fiscal periods, currencies, accounting basis, and uncertainty when they affect interpretation. Use “Unknown” for unavailable data; do not hide it in a footnote.
- Describe observations, inferences, and hypotheses distinctly. Place the strongest contradiction or gating issue near the conclusion. Keep the full evidence ledger available without dumping it into every answer.
- End dialogue with one short question bullet and stop. Keep required menus as native single-select controls with a one-bullet introduction; do not append analysis after a menu.
- Follow an explicit user request for a different output format. Preserve raw JSON/Markdown state exports when requested.

Use the fields below selectively rather than forcing every field into a long response each turn. Expand the research trail on request.

## Setup snapshot

- Company/security, direction if supplied, horizon, as-of date, available capabilities and access gaps.
- Product-route status and rationale; key offerings/use cases; competitor shortlist and omissions; normalized advantage/disadvantage matrix with comparability limits.
- Commercial underwriting: customer economic value, adoption evidence/frictions, growth range, value capture, financial bridge, and expectation gap.
- Independent disconfirmation verdict, decisive claim IDs, and any unresolved decision for the human analyst.
- Operating driver tree and three to five material debates; fallback angles pursued and their results when triggered.
- Material catalysts: date/status, conditional revenue/profit/cash impact, linked dependencies, source references, specialist owner/response, and next check. Use a compact table or timeline when useful; keep document coverage gaps explicit.
- Driver table: driver/period/units | verified market expectation and source type | narrative | contrary evidence | sensitivity | decisive test.
- Separate consensus numbers from single-broker forecasts, guidance, valuation implications, and sampled forum opinions.
- Evidence IDs with accessible URLs or user-file page references. Record missing sources honestly.
- End with the highest-value question to form or challenge a thesis.

## Thesis snapshot

- Verbatim thesis and normalized, falsifiable version; distinguish user input from agent assumptions.
- Claims table: claim | support | challenge | unresolved issue | financial implication | falsifier.
- Strongest bear argument, strongest defense, agreed facts, remaining disagreement, and any access/role limitations.
- Quantitative bridge and scenario payoff assumptions; probability basis if used.
- Five-dimension scorecard, full index or missing-data interval, gates, and separate investment-attractiveness judgment.
- Next research step and one Socratic question unless the user requested a complete memo or direct answer.

Do not bury major contradictions beneath a final score. Do not append several questions disguised as one numbered question. In a follow-up, judge the actual answer briefly, add the strongest relevant rebuttal/comparable evidence, update affected fields, then ask one question.

## Save/resume state

Emit a compact Markdown or JSON state when requested. Include schema_version=5, phase, selected mode, selected discovery source, source access status, product wave/status, competitor shortlist/dossiers, comparison limits, commercial underwriting/gate results, fallback tasks/results, catalyst document coverage/event register, specialist handoffs/responses, linked-event scenarios, company/ticker/exchange, direction, horizon/as-of date, user thesis, agreed assumptions, driver debates, claim/evidence IDs and source URLs/dates, input provenance, claim verification status, adversarial revisions, analyst review status, source-family deduplication, data access gaps, argument summaries and concessions, financial assumptions, rubric weights, scores/gates, pending evidence requests, last question/answer, and next action. Do not claim persistent memory beyond the available saved state.

On a fresh invocation with resumed state, complete the entry menus first. Then validate company, horizon, and stale evidence; preserve prior scores as historical and refresh only material facts. After the entry menus, continue the pending question rather than repeating completed company intake. Exclude private documents, credentials, licensed report contents, and personal details from a publicly shareable state; retain only permitted references and original analysis. Never write user research into the installed skill or publish it by default.

## Compact response patterns

For investment research, prefer:
- **Finding:** best candidate/status, or no defensible edge found.
  - **Why:** one decisive mechanism and one material limitation.
- **Comparison:** compact product/customer-economics or expectations table, whichever decides the issue.
- **Investment implication:** one financial sensitivity and the expectation gap.
  - **Falsifier:** observable condition that rejects the candidate.
  - **Next check:** highest-information missing evidence.
- **Question:** one decisive question.

For thesis strengthening, prefer:
- **Judgment:** supported/provisional/contradicted, plus the principal reason.
- **Debate:** strongest support versus strongest rebuttal; use a small table if useful.
- **Score:** compact five-dimension scorecard when requested or materially updated; include weights/contributions and the uncalibrated label. If unchanged, state that briefly rather than repeating the table.
  - **Investment attractiveness:** separate from thesis quality.
  - **Key gap/falsifier:** decisive missing input or contradiction.
- **Question:** one decisive question.

For follow-ups, prefer three or four bullets: answer assessment, new evidence/rebuttal, changed financial implication/score if any, then one question. Do not repeat company background, agent allocation, the full scorecard, or completed research unless needed.

# Optional RapidAPI Seeking Alpha source

## Provider and endpoint discovery

Use the user's specified provider listing:
https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/seeking-alpha-api/playground/Symbol%20Analysis

Use the provider's current playground/OpenAPI export or generated cURL example to verify the endpoint path, HTTP method, required symbol parameter, pagination, supported coverage, and response fields. “Symbol Analysis” is a playground label, not a verified REST path. Do not manufacture `/symbol-analysis` from that label or substitute a different provider with a similar name.

The provider-linked public documentation at https://github.com/pintoflow17/seeking-alpha-api documents HTTPS host `seeking-alpha-api.p.rapidapi.com`, GET requests, `X-RapidAPI-Key` and `X-RapidAPI-Host` headers. It lists `/analyst-recommendation` with optional `slugs` and `/stock-ideas` with `categoryNumber`, `limit`, and `page`. This older reference does not verify the current Symbol Analysis contract. Recheck the playground for that contract; if inaccessible, request a **redacted** generated cURL/OpenAPI excerpt, excluding the key, and keep Symbol Analysis status unverified. A successful call to a different documented endpoint does not verify Symbol Analysis.

## Credentials and request budget

Read the current user's `RAPIDAPI_KEY` from their runtime environment or approved secret store. The user/friend must supply their own authorized credential. Never include real keys in SKILL.md, scripts, examples, saved state, source-control changes, generated reports, or logs. Do not ask users to paste keys into chat. Accept secrets through the host's secure input path when available; otherwise explain local environment configuration without echoing secret values. If a key was authorized only for construction/testing, do not retain or reuse it in normal skill runs.

Use `scripts/seeking_alpha_client.py` as a small stdlib GET adapter after verifying the chosen route. It accepts a relative path and query parameters, fixes the destination host, refuses redirects, and reads the credential at execution time. It performs exactly one request with a 20-second timeout; no auto-pagination or retries. Use `--check` when only connectivity/response shape is needed. Never put a key in the URL or command arguments. Never pass credentials or full environment values to research subagents; centralize requests and share sanitized evidence.

Example invocation with an already securely configured environment:

```bash
python3 scripts/seeking_alpha_client.py --endpoint-path /analyst-recommendation --param slugs=aapl --check
```

For Symbol Analysis, use the exact verified route/parameter names from the provider rather than copying the connectivity example. Default to at most three API calls per research invocation; cache/deduplicate within that invocation, avoid fetching the same page across agents, and count failed requests toward the budget. Report coverage and stop when quota/access blocks further work. Do not subscribe, upgrade, enable overages, or change account billing. Additional requests require an explicit user budget or a new decision-critical justification within an already authorized budget.

## Error and data handling

- Missing key: do not call; offer credential configuration or web scraping.
- HTTP 401/403: report authentication/access denial without claiming the exact cause unless the response establishes it. Do not retry unchanged credentials.
- HTTP 402 or a subscription-required message: report the plan/subscription restriction and stop. Do not purchase access.
- HTTP 429: report rate/quota limitation and stop automatic requests.
- HTTP 404: endpoint or symbol may be unsupported; recheck the documented route and symbol mapping before a further request.
- Network/5xx/redirect/invalid JSON/oversized body: report the specific limitation, do not treat it as no coverage or a bearish fact. Do not send the key to a redirect destination.
- HTTP 200 with an API error envelope is not success. Empty results or unrelated symbols are not usable company coverage. Inspect entity, dates, pagination, and returned field meanings before interpretation.

After an API failure, present the source menu again if the user wants to continue discovery. Preserve usable primary evidence. Never silently switch to scraping or claim an unsuccessful call worked.

Record metadata/URLs, author, publication date, ticker/exchange, source type, and a concise paraphrase in the common evidence ledger. Article titles or snippets identify narrative leads but cannot establish thesis-critical facts. Distinguish author opinions, quant ratings, sell-side ratings, and actual operating forecasts; an analyst-rating count is not earnings/revenue consensus. Verify important claims against primary sources. Do not bundle licensed payloads with the public skill; do not save raw response files unless needed and authorized for the user's private research.

## Construction verification note

Treat construction-test results as historical connectivity diagnostics only. Do not encode the construction credential or imply a tested account grants access to future users. Report the actual tested endpoint separately from Symbol Analysis status.

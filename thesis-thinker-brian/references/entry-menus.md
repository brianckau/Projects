# Entry menus and routing

## First menu: required for every new invocation

Begin with the bullet “- Choose what you want to work on.” Present a single-select dropdown when the host has a documented dropdown control. Otherwise use its native single-select multiple-choice control. Do not promise a literal dropdown when the host only supports buttons/cards. Never invent a tool name or rely on a renderer unavailable in the current host.

In ChatGPT hosts supporting the ask_user_input widget, emit this widget and end the response immediately:

genui{"ask_user_input":{"questions":[{"question":"What would you like to work on?","options":["Investment research — find potential theses","Investment thesis strengthener — test my existing thesis","Factor exposure calculator — estimate beta and factor loadings"],"type":"single_select","free_text_placeholder":"Describe your research goal"}]}}

If a documented native question tool is available instead, supply the same question/options with single-choice behavior and wait. If interactive controls are unavailable, show the three numbered choices and wait for a number or text response. Do not start browsing, ask the source question, or include analysis in the first menu response. If the response is ambiguous, clarify the choice before proceeding. Do not auto-select after a timeout or tool failure.

## Second menu: investment research only

After the first choice resolves to investment research, say the bullet “- Choose the research source.” Emit a separate single-select menu and stop:

genui{"ask_user_input":{"questions":[{"question":"How should I gather investment research?","options":["RapidAPI Seeking Alpha API","Web scraping"],"type":"single_select","free_text_placeholder":"Specify a source requirement"}]}}

Use the same native-control/fallback rules as above. Do not ask this second question for the strengthener unless the user independently requests this source choice. Selecting the API chooses it for Seeking Alpha discovery; primary filings and other independent evidence remain necessary. Selecting web scraping means use accessible pages/search for discovery and no RapidAPI calls. Do not bypass access controls in either route.

## State transitions

Track phase = awaiting_mode → awaiting_source (research only) → intake → research/strengthening → dialogue, or factor calculation after calculator intake. Retain selected mode, selected discovery source, access status, and pending question in session state. A menu reply is a continuation, not a new invocation. So are answers to Socratic questions and ordinary requests to inspect the current evidence. A fresh explicit invocation or a new research session always resets the mode/source selections and presents the first menu, including when resuming saved state; preserve the prior evidence for use after selection. Do not treat a saved source choice as a reusable authorization to use an old API key.

The two intake menus are preference routing, not the substantive Socratic questions. Apply the one-question dialogue rule after intake. Accept free-text equivalents of every mode and source. The calculator skips the investment-research source menu and follows factor-exposure.md. Do not route a user into web scraping merely because API credentials are missing; offer a clear choice to configure credentials or select web scraping.

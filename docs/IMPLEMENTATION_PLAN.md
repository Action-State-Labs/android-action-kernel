# Implementation Plan: OpenRouter Default (GPT-4o via OpenRouter)

## Goal
Make **OpenRouter** the default LLM provider while preserving the current agent loop reports in `README.md` and behavior in `kernel.py`:

- Perception: dump Android accessibility tree via `uiautomator` and sanitize it
- Reasoning: ask an LLM for the next action as **a single JSON object**
- Action: execute via ADB (`tap`, `type`, `home`, `back`, `wait`, `done`)

## Non-Goals
- Changing the agent UX (still `python kernel.py` → prompts for goal)
- Adding new actions/tool calling
- Rewriting the sanitizer logic

## Default Provider Decision
- Default provider: **OpenRouter**
- Default model via OpenRouter: **`openai/gpt-4o`**

## New Configuration (env vars)
- `OPENROUTER_API_KEY` (required by default)
- `LLM_PROVIDER` (optional override; values: `openrouter`, `openai`)
- `LLM_MODEL` (optional override; default depends on provider)
- `OPENAI_API_KEY` (only required if `LLM_PROVIDER=openai`)

## Work Breakdown (milestones)

### Milestone 1 — Add docs-first implementation instructions
- Create docs structure:
  - `docs/features/openrouter-default.md`
  - `docs/bugs/kernel-known-bugs.md`
- Ensure instructions are atomic and include “why” for each step.

### Milestone 2 — Implement provider abstraction (small refactor)
- Add a small “LLM client factory” that chooses:
  - OpenRouter client (default)
  - OpenAI client (opt-in)
- Keep call site to `client.chat.completions.create(...)` unchanged.

### Milestone 3 — Preserve JSON-action contract across models/providers
- Keep `response_format={"type":"json_object"}`.
- Add parse/validation + 1 retry if output is invalid JSON.

### Milestone 4 — Fix correctness bugs discovered during review
- Fix issues documented in `docs/bugs/kernel-known-bugs.md`.

### Milestone 5 — Update README and do a smoke test
- Update `README.md` Quick Start to prefer OpenRouter.
- Manual smoke test:
  - Run `python kernel.py` with a simple goal (e.g. “go home”).
  - Confirm ADB commands work and the model returns valid JSON actions.

## Acceptance Criteria
- Running with **only** `OPENROUTER_API_KEY` set works (OpenRouter default).
- Setting `LLM_PROVIDER=openai` with `OPENAI_API_KEY` works.
- Actions returned by the model are validated (no crashes on missing fields).
- Key ADB actions (`home`, `back`) use correct keycodes.

## Rollback Plan
- If OpenRouter routing/model output is unstable, keep OpenRouter default but allow fallback:
  - `LLM_PROVIDER=openai`
  - `LLM_MODEL=gpt-4o`


# Feature: Make OpenRouter the Default LLM Provider (GPT-4o)

## Summary
Refactor `kernel.py` so the default LLM provider is **OpenRouter**, using model **`openai/gpt-4o`**, while keeping the current agent loop and JSON action contract.

## Target Behavior
- Running `python kernel.py` should work with only:
  - `OPENROUTER_API_KEY` set
- OpenAI remains available as an override:
  - `LLM_PROVIDER=openai` + `OPENAI_API_KEY`

## Atomic Steps (with “Why”)

### 1) Decide and document env var contract
**Do**
- Define these env vars:
  - `OPENROUTER_API_KEY` (required by default)
  - `LLM_PROVIDER` (optional; default `openrouter`)
  - `LLM_MODEL` (optional; default depends on provider)
  - `OPENAI_API_KEY` (only required if `LLM_PROVIDER=openai`)

**Why**
- A junior engineer needs a single source of truth for configuration.
- Keeping OpenAI as opt-in reduces risk and makes debugging easier.

### 2) Replace the global `MODEL` constant with provider-aware defaults
**Do**
- Introduce a provider-aware model selection:
  - If provider is `openrouter`: default `openai/gpt-4o`
  - If provider is `openai`: default `gpt-4o`
- Allow `LLM_MODEL` to override in both cases.

**Why**
- OpenRouter uses namespaced model IDs; OpenAI does not.
- This prevents confusing “model not found” errors.

### 3) Create a tiny “LLM client factory” in `kernel.py`
**Do**
- Add a function, e.g. `get_llm_client_and_model()` that returns:
  - `client`
  - `model`
- Build the OpenAI SDK client like:
  - OpenRouter default:
    - `OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")`
  - OpenAI override:
    - `OpenAI(api_key=OPENAI_API_KEY)`

**Why**
- Centralizes provider logic.
- Avoids littering conditionals across `get_llm_decision()`.
- Makes future provider additions (Claude/Gemini via OpenRouter, etc.) straightforward.

### 4) Add OpenRouter optional headers (non-blocking)
**Do**
- If the OpenAI SDK version in this repo supports default headers:
  - Add `HTTP-Referer` and `X-Title` for OpenRouter requests.
- If it does not, skip this step.

**Why**
- OpenRouter recommends these headers for attribution/analytics.
- Not required for correctness; keep it optional to reduce implementation risk.

### 5) Keep JSON response mode, but add a fallback parsing strategy
**Do**
- Keep `response_format={"type": "json_object"}`.
- Wrap JSON parsing in a try/catch.
- If parsing fails:
  - Retry once with a stricter prompt (still requiring only JSON output)
  - If it still fails, raise a clear error that includes the raw response text.

**Why**
- Different routed models can be slightly less strict about JSON-only output.
- A single retry often fixes transient “formatting drift” without changing the UX.

### 6) Validate the returned action schema before executing
**Do**
- Before `execute_action(decision)`:
  - Validate `decision["action"]` is one of:
    - `tap`, `type`, `home`, `back`, `wait`, `done`
  - If `tap`, require `coordinates` as a 2-item list of ints.
  - If `type`, require `text` as a non-empty string.

**Why**
- Prevents crashes and device misclicks.
- Makes the behavior consistent even when the LLM is imperfect.

### 7) Update README “Quick Start” to prefer OpenRouter
**Do**
- Replace or augment the existing OpenAI setup section with:
  - `export OPENROUTER_API_KEY="..."`
  - (optional) `export LLM_MODEL="openai/gpt-4o"`
- Add an “OpenAI override” snippet:
  - `export LLM_PROVIDER=openai`
  - `export OPENAI_API_KEY="..."`

**Why**
- Docs should match the new default so new users don’t get blocked.

### 8) Add a minimal manual smoke test checklist
**Do**
- Validate both modes:
  - OpenRouter default
  - OpenAI override
- Use a simple goal and verify at least one valid action executes.

**Why**
- Prevents regressions before merging.
- Junior engineers get confidence quickly with concrete steps.

## Expected Code Touch Points
- `kernel.py`
  - Add provider config + client factory
  - Update model constant usage
  - Add JSON parsing fallback + action validation
- `README.md`
  - Update environment variable setup instructions

## Definition of Done
- With `OPENROUTER_API_KEY` set, `python kernel.py` starts and makes LLM calls successfully.
- The LLM output is parsed into a JSON dict and validated.
- Actions execute without runtime exceptions for missing fields.

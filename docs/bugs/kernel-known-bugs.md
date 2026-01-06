# Bugs: Known Issues in `kernel.py` (and Proposed Fixes)

This document lists bugs discovered during review that will impact correctness and/or stability. Each bug includes a proposed fix and the reason it matters.

## 1) Missing import: `List` used but not imported
**Where**
- `kernel.py`: `def run_adb_command(command: List[str]):`

**Problem**
- `List` is not imported from `typing`, which will raise a `NameError` at runtime.

**Proposed Fix**
- Change typing import to include `List`:
  - `from typing import Dict, Any, List`

**Why it matters**
- This prevents the script from running at all.

## 2) Wrong ADB keyevent constants for Home/Back
**Where**
- `kernel.py`:
  - `KEYWORDS_HOME`
  - `KEYWORDS_BACK`

**Problem**
- The Android keyevent constants are `KEYCODE_HOME` and `KEYCODE_BACK`.
- Current constants will cause ADB to fail (or do nothing) when trying to go home/back.

**Proposed Fix**
- Replace with:
  - `KEYCODE_HOME`
  - `KEYCODE_BACK`

**Why it matters**
- Navigation actions are core to the agent loop.

## 3) Potential crash: `tap` coordinates unpacking without validation
**Where**
- `execute_action()`:
  - `x, y = action.get("coordinates")`

**Problem**
- If `coordinates` is missing or malformed, unpacking throws an exception.

**Proposed Fix**
- Validate the action schema before executing:
  - Ensure `coordinates` exists
  - Ensure it is a 2-item list/tuple
  - Ensure each value can be converted to int

**Why it matters**
- LLMs occasionally return malformed payloads; the agent should fail gracefully.

## 4) Potential crash: `type` action assumes `text` exists
**Where**
- `execute_action()`:
  - `text = action.get("text").replace(" ", "%s")`

**Problem**
- If `text` is missing, `action.get("text")` returns `None` and `.replace(...)` crashes.

**Proposed Fix**
- Validate `text` exists and is a string before calling `.replace`.

**Why it matters**
- Prevents agent from crashing mid-run.

## 5) Hard exit inside library function (`exit(0)`) reduces reusability
**Where**
- `execute_action()` on `done`:
  - `exit(0)`

**Problem**
- If `run_agent()` is imported and used by another module, `exit(0)` will terminate the entire host process.

**Proposed Fix**
- Prefer returning a sentinel (e.g. `True` for completed) or raising a specific exception that `run_agent()` catches.

**Why it matters**
- Enables embedding this library into other tools/services without unexpected process termination.

## 6) ADB error detection is brittle
**Where**
- `run_adb_command()`:
  - checks `if result.stderr and "error" in result.stderr.lower()`

**Problem**
- Many ADB failures show up in stdout or return codes.
- Ignoring `returncode` can hide failures.

**Proposed Fix**
- Check `result.returncode != 0` and include both stdout/stderr in the error message.

**Why it matters**
- Makes debugging device connectivity and ADB issues far easier.

## 7) Ambiguous `focus` usage in sanitizer (minor)
**Where**
- `sanitizer.py`:
  - `is_editable = node.attrib.get("focus") == "true" or node.attrib.get("focusable") == "true"`

**Problem**
- `focus/focusable` is not the same as "editable".

**Proposed Fix**
- (Optional) Use attributes like `class` (`EditText`) or `long-clickable`/`enabled` to identify text fields more accurately.

**Why it matters**
- Better context improves LLM decision quality; not required for OpenRouter switch.

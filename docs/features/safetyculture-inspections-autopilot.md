# Feature: SafetyCulture (iAuditor) Inspections Autopilot (MVP)

## Decision
**Chosen use case:** Safety/EHS inspections autopilot using **SafetyCulture (iAuditor)**.

## Why this one (vs the other ideas)
- **Matches current capabilities**: form navigation + taps + text entry + submit.
- **Does not require vision/OCR**: we can explicitly avoid photo upload steps in the MVP.
- **Clear ROI + measurable outcomes**: time-per-inspection, completion rate, fewer missing fields.
- **Mobile-native + repetitive**: exactly where UI automation is valuable and APIs are often not worth building for a pilot.

## Goal
Build a repeatable demo/MVP where the agent can:
- Open SafetyCulture
- Start a specific inspection template
- Fill a bounded set of fields (pass/fail + short notes)
- Submit the inspection

## Non-goals (for MVP)
- Handling photo capture / attachments
- Handling signatures
- Handling deep offline sync edge cases
- Supporting arbitrary templates (we’ll support **one** stable template first)

## Required Android apps
- SafetyCulture (iAuditor)
- (Optional) Slack or Microsoft Teams (only if you want “inspection submitted” notification)

## Preconditions (junior engineer checklist)
- Android device connected via ADB (`adb devices` shows it)
- USB debugging enabled
- SafetyCulture installed
- A test SafetyCulture account logged in already
- A single inspection template created and kept stable for the MVP

---

## Implementation Plan (atomic steps)

### Step 1 — Create a dedicated “use case” entry point
**Do**
- Add a new Python file (example): `use_cases/safetyculture_inspection.py` that calls `run_agent()` with a hardcoded SafetyCulture goal string and higher `max_steps`.

**Why**
- Keeps the core kernel generic and makes the use case demo reproducible.

**Acceptance check**
- Running the file launches the agent with a SafetyCulture-focused goal without you manually typing it each time.

---

### Step 2 — Add a stable way to open an app (do not rely on home-screen taps)
**Do**
- Add a new action: `{"action": "launch", "package": "..."}` OR a helper function used by the use-case entry point that runs:
  - `adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1`

**Why**
- Tapping an icon coordinate is brittle across devices, launchers, and layouts.

**Acceptance check**
- With the phone on any screen, the agent can reliably open SafetyCulture.

---

### Step 3 — Add a “wait_until” primitive (minimum viable)
**Do**
- Add a function (or action) that loops for up to N seconds until the current `screen_context` contains an element whose text contains a target substring.
- Example API (choose one):
  - `wait_until_text("Inspections", timeout_s=10)`
  - or action: `{"action":"wait_until","text":"Inspections","timeout_s":10}`

**Why**
- SafetyCulture (and most enterprise apps) have loading states; blind `sleep(2)` causes flakiness.

**Acceptance check**
- After launching SafetyCulture, the code waits until a known “home” element appears before proceeding.

---

### Step 4 — Add a minimal “interrupt handler” for popups
**Do**
- Before every decision step, scan `screen_context` for common dismiss buttons:
  - `"Allow"`, `"Don’t allow"`, `"No thanks"`, `"Not now"`, `"Skip"`, `"Close"`, `"Later"`
- If found, auto-tap it (using the node center coordinates) before calling the LLM.

**Why**
- Popups will derail pilots. Handling them early increases success rate dramatically.

**Acceptance check**
- If a popup appears during launch, the agent dismisses it and continues.

---

### Step 5 — Restrict the MVP template and define what “fill the inspection” means
**Do**
- Pick one template and explicitly define:
  - How many questions it has (e.g., 10)
  - Which answers to select for each (pass/fail/na)
  - Which questions require a note (and what note text to use)
- Store this as a structured object in code (dict/list) in `use_cases/safetyculture_inspection.py`.

**Why**
- “Do an inspection” is too open-ended; bounded scope makes it reliable and testable.

**Acceptance check**
- A human can read the config and understand what the agent will do before running.

---

### Step 6 — Upgrade the prompt to be template-driven (but still generic)
**Do**
- Instead of a single natural-language goal, construct a goal like:
  - "Open SafetyCulture, start template '<TEMPLATE_NAME>', answer questions 1..N using this plan: ... then submit."
- Include the structured plan in the user message.

**Why**
- The LLM performs better when it has an explicit plan and fewer degrees of freedom.

**Acceptance check**
- The agent stops trying random navigation paths and focuses on the inspection flow.

---

### Step 7 — Add logging artifacts for demos and debugging
**Do**
- Write a JSONL or JSON file per run with:
  - timestamp
  - each decision
  - whether the run ended in done/timeout
- Do NOT store full raw screen dumps if they may contain sensitive info; store only:
  - step index
  - action
  - reason
  - optionally a small list of visible element texts (redacted)

**Why**
- Business pilots require traceability: “what happened and where did it fail?”

**Acceptance check**
- After a run, a file exists that explains each step.

---

### Step 8 — Add success detection for “submitted” state
**Do**
- Define 1–2 text anchors that indicate completion (examples):
  - `"Submitted"`, `"Inspection submitted"`, `"Success"`
- After tapping submit, call `wait_until_text("Submitted", timeout_s=15)`.

**Why**
- Prevents false positives where the agent says done but nothing submitted.

**Acceptance check**
- The run only returns success if a completion text is detected.

---

### Step 9 — Define a reliability test loop
**Do**
- Run the same template 20 times (manual loop is fine at first).
- Track:
  - success rate
  - median duration
  - top failure reasons

**Why**
- Reliability is the product for this use case.

**Acceptance check**
- You can report “X% success across 20 runs” to a pilot customer.

---

## MVP Demo Script (what to show a customer)
- "Here is the exact SafetyCulture template"
- "Watch the agent complete and submit it"
- Show the run log + time saved estimate

## Definition of Done
- On a physical device, for one SafetyCulture template, the agent can complete and submit successfully with **>= 80% success over 20 runs**.

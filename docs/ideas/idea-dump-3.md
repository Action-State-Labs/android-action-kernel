Below is a junior-engineer executable implementation guide to integrate Wispr Flow dictation into your Safety/EHS inspection autopilot (SafetyCulture / iAuditor), using ADB + accessibility tree for UI control, and Wispr Flow API for high-quality “spoken notes → clean text → type into focused field”.

⸻

0) What we’re building

Add a “Dictate Note” capability to your agent:
	1.	Agent navigates SafetyCulture inspection UI (already works)
	2.	When it reaches a free-text field (e.g., “Describe hazard”, “Corrective actions”, “Additional notes”), it:
	•	records audio (host mic or device mic—pick one)
	•	sends audio to Wispr Flow
	•	receives cleaned text
	•	uses existing type(text) action to enter it

Wispr Flow supports:
	•	REST transcription endpoint (slower) /api
	•	WebSocket streaming endpoint (recommended, lower latency)
	•	Context fields (dictionary words, textbox contents, page content) to improve results
	•	Audio must be 16kHz, mono, 16-bit PCM WAV, base64-encoded; max 25MB / 6 min per request.
Sources:  ￼

⸻

1) Choose the integration mode (do this)

Option A — REST (fastest to ship, easiest)

Use:
	•	POST https://platform-api.wisprflow.ai/api/v1/dash/api with org API key auth
Sources:  ￼

This is the best “2–4 week pilot” choice.

Option B — WebSocket (lower latency, more moving parts)

Use:
	•	wss://platform-api.wisprflow.ai/api/v1/dash/ws?api_key=Bearer%20<YOUR_API_KEY>
	•	Send messages: auth, then append packets, then commit
Sources:  ￼

⸻

2) Architecture decision (recommended for your current setup)

Since your agent already runs from a host controlling Android via ADB, do:

Host-recorded audio (laptop mic / USB mic) → Wispr Flow → adb input/your type(text).

It avoids Android audio permissions + recording UI flows.

If you must record on-device later, keep the Wispr client interface stable and swap the recorder.

⸻

3) Implementation steps (REST path) — do these in order

3.1 Create module: wisprflow_client.py

API contract (from docs)
	•	Endpoint: POST /api
	•	Body:
	•	audio: base64 encoded 16kHz wav
	•	language: optional list of ISO codes
	•	context: optional object (app info, dictionary words, textbox contents, content_text, etc.)
	•	Response includes text plus metadata (detected language, time, tokens)
Sources:  ￼

Code (Python)

# wisprflow_client.py
from __future__ import annotations

import base64
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

WISPR_BASE = "https://platform-api.wisprflow.ai/api/v1/dash"

@dataclass(frozen=True)
class WisprResult:
    id: str
    text: str
    detected_language: str | None
    total_time_ms: int | None
    generated_tokens: int | None

class WisprFlowClient:
    def __init__(self, api_key: str, timeout_s: int = 60):
        # api_key should already include the Bearer prefix per docs examples
        # e.g. "Bearer fl-xxxxxx"
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})

    def warmup(self) -> None:
        # GET /warmup_dash
        url = f"{WISPR_BASE}/warmup_dash"
        r = self.session.get(url, timeout=self.timeout_s)
        r.raise_for_status()

    def transcribe_rest(
        self,
        wav_bytes: bytes,
        language: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> WisprResult:
        """
        wav_bytes must be 16kHz, mono, 16-bit PCM WAV.
        """
        url = f"{WISPR_BASE}/api"
        payload: Dict[str, Any] = {
            "audio": base64.b64encode(wav_bytes).decode("ascii"),
        }
        if language:
            payload["language"] = language
        if context:
            payload["context"] = context

        r = self.session.post(url, json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        data = r.json()
        return WisprResult(
            id=data.get("id", ""),
            text=data.get("text", ""),
            detected_language=data.get("detected_language"),
            total_time_ms=data.get("total_time"),
            generated_tokens=data.get("generated_tokens"),
        )

3.2 Create recorder: audio_capture.py (host mic)

You need to produce 16kHz mono int16 WAV. Use sounddevice + wave.

# audio_capture.py
from __future__ import annotations

import io
import wave
import numpy as np
import sounddevice as sd

def record_wav_16k_mono(seconds: float, sample_rate: int = 16000) -> bytes:
    """
    Records from default input device.
    Returns WAV bytes: PCM 16-bit, mono, 16kHz.
    """
    frames = int(seconds * sample_rate)
    audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return buf.getvalue()

Install deps:

pip install requests sounddevice numpy

3.3 Build “context builder” from your accessibility tree

Wispr Flow supports context fields like:
	•	app: { name, type }
	•	dictionary_context: []
	•	textbox_contents: { before_text, selected_text, after_text }
	•	content_text (preferred vs screenshot for efficiency)
	•	screenshot exists but you’re avoiding screenshots (good)
Sources:  ￼

For SafetyCulture inspections, you should pass:
	•	app.type = "other"
	•	app.name = "SafetyCulture"
	•	content_text = "<question text> | <section> | <site name> | <asset>" (whatever you can reliably get)
	•	dictionary_context = [site names, asset IDs, common hazard words, employee names]
	•	textbox_contents from the currently focused input if accessible

Example:

def build_wispr_context(
    question_text: str,
    section_name: str | None,
    existing_text: str | None,
    dictionary: list[str],
) -> dict:
    content_parts = [p for p in [section_name, question_text] if p]
    content_text = " | ".join(content_parts)

    return {
        "app": {"name": "SafetyCulture", "type": "other"},
        "dictionary_context": dictionary,
        "textbox_contents": {
            "before_text": existing_text or "",
            "selected_text": "",
            "after_text": "",
        },
        "content_text": content_text,
        # Do NOT send screenshot (you don’t use screenshots; keep it null/omit)
    }

3.4 Add new agent tool: dictate_and_type(...)

This is the glue: focus field → record → transcribe → sanitize → type.

import re

def sanitize_for_adb(text: str) -> str:
    # ADB input is fragile with some characters depending on your implementation.
    # Keep it conservative for pilots.
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def dictate_and_type(
    wispr: WisprFlowClient,
    seconds: float,
    question_text: str,
    section_name: str | None,
    existing_text: str | None,
    dictionary: list[str],
    type_fn,  # your existing type(text) action
    language: list[str] | None = None,
) -> str:
    wav_bytes = record_wav_16k_mono(seconds)
    ctx = build_wispr_context(question_text, section_name, existing_text, dictionary)
    result = wispr.transcribe_rest(wav_bytes, language=language, context=ctx)
    final_text = sanitize_for_adb(result.text)
    if final_text:
        type_fn(final_text)
    return final_text

3.5 Warmup call (reduces latency)

Before dictation-heavy sessions (start of inspection):
	•	GET https://platform-api.wisprflow.ai/api/v1/dash/warmup_dash
Sources:  ￼

Call once when your agent boots or right before the first transcription:

wispr.warmup()


⸻

4) Where to hook this into SafetyCulture workflows

You want stable, repeatable trigger points:
	•	When accessibility tree indicates a focused EditText (or text input node)
	•	And the nearby labels match “Describe…”, “Notes”, “Corrective action”, etc.

Pilot approach:
	•	Maintain a small allowlist of question labels that use dictation (10–30 items).
	•	Everything else stays typed/autofilled.

⸻

5) WebSocket plan (optional upgrade after REST works)

If you upgrade to WebSockets, flow is:
	1.	Open socket (API-key endpoint):
wss://platform-api.wisprflow.ai/api/v1/dash/ws?api_key=Bearer%20<YOUR_API_KEY>
	2.	Send first message auth with optional language + context
	3.	Send repeated append with audio_packets (packets list, volumes list, packet_duration, etc.)
	4.	Send commit { total_packets: n }
	5.	Receive status: "text" responses, partial + final
Sources:  ￼

You can also reduce size using MessagePack binary mode (Encoding: 'msgpack' and byte_encoding: "binary") if needed.  ￼

⸻

6) Auth + key handling (pilot-safe)

Docs describe:
	•	API-key auth (org key) and also client-side auth via generated JWT tokens
Sources:  ￼

For pilots:
	•	Keep org API key only on the host running the agent.
	•	Put it in env vars:
	•	WISPRFLOW_API_KEY="Bearer fl-xxxxx"

If you later ship to customer devices directly:
	•	Build a tiny token service using POST /generate_access_token and use /client_api or client_ws.  ￼

⸻

7) Reliability testing plan (what the junior engineer should implement)

Unit tests
	•	Audio output is WAV, 16kHz, mono, 16-bit PCM (read the WAV header)
	•	Context builder produces correct structure (no screenshots)

Integration tests (Wispr Flow)
	•	Use 5–10 pre-recorded WAV fixtures (stored in repo) and assert non-empty text
	•	Ensure request stays under size/time limits (25MB / 6 min)
Sources:  ￼

E2E tests (SafetyCulture)
	•	Run 20 inspections with dictation on the same 5 text fields
	•	Success criteria:
	•	≥90% of dictations produce non-empty text
	•	≥90% of runs type into the correct field (no misfocus)
	•	Median dictation latency < 3s (REST) or < 1s (WS), measured from “stop recording” to “typed” (your mileage will vary)

⸻

8) Privacy / compliance defaults (pilot-ready)

Even without screenshots, you’re sending:
	•	Audio (may include PII)
	•	content_text / question prompts (might include site names)
	•	potentially existing field text (PII)

Defaults:
	•	Redact logs: don’t persist raw audio; don’t log full transcripts in prod mode
	•	Store only: request id, timings, success/fail, and a short hash of transcript
	•	Make dictionary_context customer-controlled (no secrets)

(Also: Wispr Flow’s docs explicitly support providing content_text as a more efficient alternative to screenshot for context.)  ￼

⸻

9) Drop-in docs file (put this in your repo)

Create: docs/features/wisprflow-dictation.md with:
	•	Purpose
	•	REST endpoint + payload example
	•	“dictate_and_type” workflow
	•	Config knobs: dictation allowlist, languages, dictionary_context, redaction mode
	•	Test plan + success metrics


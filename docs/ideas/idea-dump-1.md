Section A: Use case table (12–20)

#	Use case	Who pays (buyer + industry)	Why Android UI automation (vs API/web/desktop)	Success looks like (measurable)	Key risks	Example Android apps (3–5)
1	Safety/EHS inspections autopilot (checklists, issue creation, submit report)	EHS Manager / Ops Director (construction, manufacturing, logistics)	Inspections are mobile-first, offline-capable, highly repetitive taps; APIs often don’t cover “fill this specific checklist flow” fast for pilots	30–60% fewer taps/time per inspection; higher on-time completion; fewer “missing fields”	Accessibility gaps in custom widgets; frequent template changes; photo steps (you don’t have vision)	SafetyCulture (iAuditor), Microsoft Teams, Slack, Google Sheets, Trello  ￼
2	Field service work order closeout autopilot (status, parts, notes, signature screens you can skip in pilot)	Field Service VP / Dispatch Manager (utilities, HVAC, telecom)	Mobile app UIs are the system-of-record for techs; API projects take longer than “get value this month”	Reduce closeout time 25–50%; fewer incomplete closeouts; faster invoice readiness	Offline/online state; signature/photo steps; UI drift; 2FA/SSO	Salesforce Field Service, Microsoft Teams, Slack, Google Sheets  ￼
3	CRM “lead capture + follow-up” autopilot (create contact/company, log activity, task)	Sales Ops / VP Sales (SMB–midmarket)	Reps live on phones at events/in the field; fastest path is “drive the existing app” not integrate CRM API + custom UI	2× more leads logged; 30–50% less time per lead; fewer missed follow-ups	Login/2FA; duplicate detection flows; keyboard/input focus bugs; UI changes	HubSpot, Zoho CRM, Salesforce, Asana, Trello  ￼
4	ITSM ticket triage on mobile autopilot (accept/assign/update/resolve)	IT Service Desk Manager (enterprise IT)	Mobile agents exist, but actions still tedious; API automation often blocked by governance; pilots can run on pre-auth devices	30–50% faster first-touch updates; better SLA compliance; fewer “stale” tickets	Role-based UI variants; 2FA; offline mode quirks	ServiceNow Agent, Jira Cloud, Microsoft Teams, Slack  ￼
5	Expense reporting autopilot (non-receipt flows) (mileage/per diem/simple entries, submit/approve)	Finance Ops / Controller (any)	Receipts OCR is missing, but lots of expense flows are pure form entry + submit; “pilot now” without ERP integration	Cut submission time 30–60%; higher policy compliance; fewer rejected reports	Receipt-photo steps; 2FA; policy popups; UI changes	Expensify, SAP Concur, Zoho Expense, Google Sheets  ￼
6	Daily operational reporting autopilot (fill structured spreadsheet rows on-device)	Ops Manager / Site Lead (warehousing, retail ops)	Lowest-friction “system” is often a shared sheet; field folks hate data entry; no API work needed	≥90% on-time daily reports; fewer missing fields; time per report down 40%	Sheet layout changes; network; access permissions	Google Sheets, Microsoft Teams, Slack, Trello  ￼
7	Project/status update autopilot (move cards, update tasks, comment)	PMO / Eng Manager (software teams)	Mobile apps exist but are clicky; web automation is brittle on mobile; quick pilot is “phone does it”	Higher update cadence; fewer stale boards; reduced PM chasing	Permission boundaries; notification popups; UI changes	Jira Cloud, Asana, Trello, Slack  ￼
8	ChatOps incident comms autopilot (post templated updates, create channel/thread hygiene)	SRE Manager / IT Ops (tech + enterprise)	Many orgs restrict bots; but a phone session is already trusted; fast “operator assistant”	Faster comms (<5 min update intervals); fewer missing incident fields	Mention/autocomplete UIs; rate limits; workspace policy	Slack, Microsoft Teams, Jira Cloud  ￼
9	MDM/BYOD onboarding autopilot (enroll device, install required apps, compliance checks)	IT Endpoint Admin (enterprise IT)	Onboarding is pure UI steps across standard screens; avoids custom scripts per OEM	Reduce helpdesk tickets; faster time-to-compliance	Device/OEM variance; permission prompts; 2FA for work account	Intune Company Portal, Microsoft Teams, Slack  ￼
10	Service desk “quick actions” autopilot (update ticket + message requester)	Service Desk Lead (enterprise)	Combines ITSM + comms on-device; avoids integration approvals	Lower reopen rate; faster resolution notes	Copy/paste across apps; privacy of ticket content	ServiceNow Agent, Microsoft Teams, Slack  ￼
11	Sales “activity logging” autopilot (log calls/meetings, next steps)	RevOps (SMB–midmarket)	APIs exist but reps won’t use separate tooling; you drive their existing app UI	+30% more activities logged; higher pipeline hygiene	Duplicate contact flows; 2FA; inconsistent field requirements	HubSpot, Zoho CRM, Salesforce  ￼
12	“Mobile-first approvals” autopilot (approve/reject requests in queues)	Finance/HR/IT approvers	Approvals often happen on phones; automating via API can be gated; UI steps are consistent	Shorter approval cycle time; fewer stuck approvals	Role-based UI variants; 2FA	SAP Concur, ServiceNow Agent, Jira Cloud  ￼
13	Ops audits + training acknowledgement autopilot (complete required checklists + ack items)	Ops + Compliance (manufacturing/logistics)	“Get compliance done” is a UI workflow; avoids building custom training portals	Higher completion; fewer overdue items	Accessibility support varies; content changes	SafetyCulture (iAuditor), Microsoft Teams, Google Sheets  ￼
14	On-call “runbook on phone” autopilot (navigate apps, update boards, post updates)	SRE/IT Ops	During incidents, phones are the fallback; the agent reduces cognitive load	Faster coordinated actions; fewer missed steps	Unpredictable screens; notification interruptions	Slack, Teams, Jira Cloud, Trello  ￼
15	“Executive assistant for mobile admin” (update CRM fields, assign tasks, ping owners)	Small-business owner / Sales manager	Owners run businesses on phones; fastest ROI is “do the annoying app taps”	Time saved per day; fewer missed follow-ups	Account security; app UI churn	HubSpot, Zoho CRM, Asana, Trello  ￼

Grounding note: Your agent’s “accessibility tree → action” approach maps well to how Android UI automation frameworks introspect UI nodes (text/content-desc/bounds) and trigger device actions.  ￼

⸻

Section B: Top 3 deep dives (fastest MVP → paid pilot in 2–4 weeks)

Top 1) Safety/EHS inspections autopilot (SafetyCulture iAuditor)

Why this is #1 for fast paid pilots
	•	Repetitive, form-y, and mobile-native (exactly where your agent already works).
	•	Clear ROI and easy “before/after” time study.
	•	Pilots can avoid camera/attachments entirely (or keep them manual) while still delivering big value.

Apps required (Android, Google Play)
	•	SafetyCulture (iAuditor) (core workflow)  ￼
	•	Optional for reporting/demo:
	•	Google Sheets (log run results / audit trail)  ￼
	•	Microsoft Teams or Slack (send “inspection submitted” message)  ￼

Device requirements
	•	Physical Android preferred for pilots (more realistic permissions + offline behavior).
	•	Emulator is fine for dev, but you’ll want at least 1 real device for reliability baselines.
	•	Permissions:
	•	Accessibility Service enabled (your agent’s dependency)
	•	Network access; optional storage if exporting files (avoid if possible)

Setup steps
	1.	Create SafetyCulture org + user; install app; log in once.  ￼
	2.	Preconfigure: choose 1–2 inspection templates for pilot (keep them stable for 2–4 weeks).
	3.	Ensure device stays logged in (no forced re-auth during pilot if possible).
	4.	Disable “chaos”: turn off auto-rotate, reduce notifications, set display scaling fixed.

Core workflows (agent “goals”)
	1.	Start today’s inspection: open app → select template → create new inspection.
	2.	Fill checklist: for each item, select pass/fail/na + type notes when prompted.
	3.	Raise an issue (if triggered): open “issues” flow → add short description → set priority → submit.
	4.	Submit inspection: reach review → confirm required fields → submit.
	5.	Post-submission confirmation: capture “submitted” state → optionally message Teams/Slack channel with template text.
	6.	Offline mode sanity (optional): start inspection with airplane mode → complete → wait → sync when online.

Minimal product features needed beyond current
	•	Element-targeting policy (big one): tap by node bounds center from accessibility tree, not by raw screen coords when possible (still executed as tap(x,y), but derived from stable node selection).
	•	Wait-for condition: wait_until(text|content-desc|class present, timeout) (otherwise loops get flaky).
	•	Interrupt handler: detect/close popups (permissions, “rate us”, offline banners).
	•	Session recorder: store (sanitized) accessibility-tree snapshots + chosen action for debugging (no screenshots).

How to test reliability
	•	Build a deterministic-ish “golden path suite”:
	•	20 runs/day across 2 templates × 2 devices (or 1 device + 2 profiles)
	•	Success threshold for pilot: ≥90% completion without human intervention on golden paths
	•	Add “mutation tests”:
	•	random notification injection
	•	network toggle mid-run
	•	template with 1 new required field (should fail gracefully + report where)

Privacy/compliance notes
	•	You’re not using screenshots, but accessibility trees can contain PII (names, addresses, ticket text).
	•	Do:
	•	Redact patterns in logs (emails, phone numbers, addresses, long numeric IDs).
	•	Store minimal logs; encrypt at rest; allow “no log mode” for sensitive customers.
	•	Customer-controlled device; keep auth on-device (no credential vault needed for pilot).
	•	SafetyCulture publishes Android “Data safety” info; use it to frame customer expectations.  ￼

Monetization / pricing hypothesis
	•	Pilot: $3k–$10k for 2–4 weeks (1–2 templates, 1–2 devices, reliability report).
	•	Ongoing: per-device + per-workflow bundle (e.g., $200–$500/device/month) + setup fees.

Sales motion
	•	Target: EHS managers / Ops leaders already using iAuditor/SafetyCulture.
	•	Outreach angle: “Cut inspection time 30–50% without changing your templates or integrating anything.”
	•	Demo: run one inspection end-to-end in <2 minutes, show before/after tap count + completion log.

Sources:  ￼

⸻

Top 2) CRM lead capture + follow-up autopilot (HubSpot / Zoho CRM)

Why this is fast
	•	Same “search + multi-step navigation + typing” pattern you already said works.
	•	Paid buyers (RevOps) care about pipeline hygiene; clear KPI lifts.

Apps required
	•	HubSpot (primary)  ￼
	•	Zoho CRM (alternative track if a customer uses it)  ￼
	•	Optional:
	•	Asana or Trello for creating follow-up tasks  ￼

Device requirements
	•	Physical device preferred (real keyboard behaviors).
	•	Accounts: HubSpot / Zoho CRM user seat.
	•	Avoid frequent 2FA by: using a dedicated “demo workspace” + keep device session active for pilot.

Setup steps
	1.	Install HubSpot; log in once; land on CRM home.  ￼
	2.	Predefine a “lead schema” for pilot (which fields required, naming convention).
	3.	Prepare 20–50 test leads (CSV off-device is fine; user can paste one at a time for MVP).

Core workflows (agent goals)
	1.	Create new contact: open Contacts → Create → fill name/email/company/phone → Save.
	2.	Log activity: open contact → Log activity (call/meeting) → type notes → Save.
	3.	Create follow-up task: open Tasks → new task → due date + title (e.g., “Call back”) → Save.
	4.	Update lifecycle/stage: open contact/deal → set stage → Save.
	5.	Search + update: search contact by name → update one field → Save.
	6.	(Optional) Dedup flow: detect “possible duplicate” screen → choose merge/skip (pilot can skip and flag).

Minimal product features beyond current
	•	Text-anchor navigation: prefer selecting elements by visible label text (“Create contact”, “Save”) from accessibility nodes.
	•	Form field focus helper: when typing, ensure correct input is focused; if not, tap field node first.
	•	“Human-in-the-loop step” (pilot-safe): if a login/2FA prompt appears, pause and ask user to complete it, then continue.

Reliability testing
	•	100-run batch: create contact + log activity + create task.
	•	Success threshold: ≥95% field-correct saves (no wrong-field typing), ≥90% full workflow completion.
	•	Add “layout drift” test: switch font size/display size once; your element-bound taps should still work.

Privacy/compliance
	•	CRM data = PII. Keep:
	•	Redacted logs
	•	Optional “test mode” with synthetic leads only
	•	No screenshots by design (good positioning)
	•	Document that agent runs on customer-controlled device; you don’t store passwords.

Pricing
	•	Pilot: $2k–$8k (depends on number of workflows + CRM).
	•	Ongoing: per-seat or per-device (sales teams often price per seat; but your tech is device-based—either works).

Sales motion
	•	Target: RevOps / Sales Enablement at companies already paying for HubSpot/Zoho but complaining about “CRM busywork”.
	•	Demo: “I say ‘log this lead and set a follow-up’, phone does it in 20 seconds.”

Sources:  ￼

⸻

Top 3) ITSM mobile triage autopilot (ServiceNow Agent / Jira Cloud)

Why this is fast
	•	IT teams already measure SLAs; you can show impact quickly.
	•	Mobile agent apps exist; your value is “do the rote clicks + enforce consistent updates”.

Apps required
	•	ServiceNow Agent  ￼
	•	Jira Cloud (many orgs use Jira for incident/task tracking)  ￼
	•	Optional comms:
	•	Microsoft Teams or Slack  ￼

Device requirements
	•	Physical device recommended (enterprise MDM + conditional access behaves differently on emulators).
	•	Accounts: ServiceNow fulfiller role / Jira user with permissions.
	•	If org uses Intune-managed variant, note there’s an Intune-specific listing; pilots should pick whichever IT already deploys.  ￼

Setup steps
	1.	Install ServiceNow Agent; sign in; verify you can see the queue.  ￼
	2.	Identify 2–3 ticket types to automate (Incidents, Requests, Catalog Tasks).
	3.	Standardize templates for updates (work notes format, resolution code mapping).

Core workflows (agent goals)
	1.	First-touch triage: open queue → open newest P1/P2 → set “In Progress” → add work note template → save.
	2.	Assign to resolver group: open ticket → assign group/user → save.
	3.	Request info: open ticket → add comment to requester → save.
	4.	Resolve/close: set state “Resolved” → choose resolution code → add resolution notes → save.
	5.	Post status update: open Teams/Slack → send “Ticket # / status / ETA” message.
	6.	Jira mirror (optional): create/update Jira issue for incident tracking.

Minimal product features beyond current
	•	Stable selector heuristic: prefer matching by (label text + class + proximity) for common buttons like “Save”, “Assign”, “State”.
	•	Retry envelope around navigation steps (backstack gets weird in enterprise apps).
	•	Rate-limit / debounce taps to avoid double-submit.

Reliability testing
	•	Synthetic ticket sandbox (ServiceNow dev instance / Jira test project) and replay:
	•	50 triage runs/day
	•	Fail threshold: ≤2% “wrong ticket updated”
	•	Add permission variance test: user with fewer rights should fail with a clear reason (“cannot see Assign”).

Privacy/compliance
	•	Tickets may include sensitive internal info.
	•	Log only:
	•	ticket ID hashes
	•	action trace
	•	redacted snippets
	•	Emphasize: no screenshots; on-device execution; fits “least new integration” model.

Pricing
	•	Pilot: $3k–$12k depending on ITSM complexity and environment access.
	•	Ongoing: per-device/month + “workflow pack” (triage pack, resolve pack, comms pack).

Sales motion
	•	Target: IT Service Desk managers, SRE leads, IT ops directors.
	•	Demo: open queue → triage 3 tickets + post Teams update in <90 seconds.

Sources:  ￼

⸻

Section C: Recommended MVP build list (engineering tasks)
	1.	Accessibility-node tap targeting
	•	Choose node by text/content-desc/class; tap center of its bounds (still using tap(x,y)).
	2.	wait_until(...) primitive
	•	Wait for node match / screen signature; timeout with structured error.
	3.	Popup/interrupt handler
	•	Generic “Close/Not now/Allow” detector + backoff.
	4.	Screen signature + state machine-lite
	•	Hash of key visible node texts to detect “we’re stuck”.
	5.	Retry policies
	•	Per-step retries w/ back/home recovery + max attempts.
	6.	Session trace + redaction
	•	Store action list + minimal UI node text (redacted); export JSON for debugging.
	7.	Human-in-the-loop gates
	•	“Pause for login/2FA” + resume.
	8.	Per-customer workflow configs
	•	YAML/JSON “goal library” with allowed screens, expected buttons, required fields.
	9.	Reliability harness
	•	Batch runner: N runs → success rate, median duration, failure clustering.

(Foundation references for the “UI tree → action” approach and device interaction patterns:  ￼)

⸻

Section D: What to demo in 5 minutes (scripts)

Demo 1 — SafetyCulture inspection in 90 seconds
	1.	“Here’s the template. Watch the agent run.”
	2.	Agent: open SafetyCulture → start inspection → complete 10 items → submit.
	3.	Show: run log (steps + timestamps) + “time saved” estimate.
	4.	Optional: agent posts “Inspection submitted ✅” to Teams/Slack.

Demo 2 — CRM lead capture (“from conversation to CRM in 20 seconds”)
	1.	You paste a synthetic lead snippet (name/company/email).
	2.	Agent: HubSpot → create contact → log call note → create follow-up task.
	3.	Show: contact exists + task exists; show failure handling if duplicate prompt appears.

Demo 3 — ITSM triage sprint
	1.	Open ServiceNow Agent queue (or Jira).
	2.	Agent triages 3 tickets: sets state, adds templated note, assigns group.
	3.	Agent posts an update message in Teams/Slack with ticket IDs + status.

(Apps shown in demos are all verified on Google Play: SafetyCulture iAuditor, HubSpot, Zoho CRM, ServiceNow Agent, Jira Cloud, Teams, Slack, Sheets.  ￼)
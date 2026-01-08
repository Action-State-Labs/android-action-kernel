# Android Use

<div align="center">

# [Join Discord Community](https://discord.gg/HWaZByt5SA)

<h1>AI Agents for Android Devices</h1>

<h3>Open-source library for AI agents to control native Android apps</h3>

**Built for field workers, logistics, gig economy, and mobile-first industries**

<br>

[![Twitter](https://img.shields.io/badge/5.3M+-views-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/ethanjlim/status/1999152070428148108?s=20)
[![Stars](https://img.shields.io/github/stars/actionstatelabs/android-action-kernel?style=for-the-badge)](https://github.com/actionstatelabs/android-action-kernel/stargazers)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

<br>

### Demo

**[Watch it automate a logistics workflow in 60 seconds](https://x.com/ethanjlim/status/1999152070428148108?s=20)**

<sub>Driver texts a photo → Agent handles WhatsApp → Scanner app → Banking app → Invoice submitted</sub>

<br>

**[⭐ Star this repo (1100+ → 1,500 goal!)](https://github.com/actionstatelabs/android-action-kernel) • [Quick Start](#quick-start) • [Book Partnership Meeting](https://build.fillout.com/editor/ctqhgaBkaKus/share)**

**5.3M+ views. 1100+ stars in days. Help us reach 1,500!** • **Priority partnerships:** Mobile QA testing • Consumer Productivity • [Request meeting →](https://build.fillout.com/editor/ctqhgaBkaKus/share)

</div>

---

## The Problem

Browser agents only work on websites. Computer Use requires a desktop.

But the real economy runs on mobile devices, in places where laptops don't fit:

- **Truck drivers** submit invoices from the cab using factoring apps (RTS Pro, OTR Capital)
- **Delivery drivers** scan packages on handheld devices—200+ per route
- **Gig workers** accept orders on phones between rides—losing 20% earnings to slow manual switching
- **Field technicians** log work orders on tablets at job sites
- **Mobile banking** happens on native apps with 2FA, not web browsers

**3 billion Android devices. $40 trillion in GDP from mobile-first workflows. Zero AI agent solutions that actually work on these devices.**

---

## Real Example: Logistics Automation

**Priority partnership area.** Android Use automating an entire logistics workflow:

### Before (Manual - 10+ minutes)
```
1. Driver takes photo of Bill of Lading
2. Opens WhatsApp, sends to back office
3. Back office downloads image
4. Opens banking app, fills invoice form
5. Uploads documents
6. Submits for payment
```

### After (Automated - 30 seconds)
```python
# Driver just texts the photo. Agent does the rest.
run_agent("""
1. Get latest image from WhatsApp
2. Open native scanner app and process it
3. Switch to RTS Pro factoring app
4. Fill invoice form with extracted data
5. Upload PDF and submit for payment
""")
```

**Result:** Driver gets paid same day instead of waiting weeks. Back-office work eliminated. No laptop needed.

---

## Why This Works

<table>
<tr>
<td width="50%">

### Computer Use (Anthropic)
- Requires desktop/laptop
- Takes screenshots → OCR
- Sends images to vision model
- **$0.15 per action**
- 3-5 second latency
- Doesn't work on phones

</td>
<td width="50%">

### Android Use (This Library)
- Works on handheld devices
- Reads accessibility tree (XML)
- Structured data → LLM
- **$0.01 per action (95% cheaper)**
- <1 second latency
- Native mobile app control

</td>
</tr>
</table>

**The breakthrough:** Android's accessibility API provides structured UI data (buttons, text, coordinates) without expensive vision models.

**Real impact:** 95% cost savings + 5x faster + works where laptops can't.

---

## Traction

Launched with the logistics demo:

- **5.3M+ views** on X/Twitter ([watch demo](https://x.com/ethanjlim/status/1999152070428148108?s=20))
- **1100+ GitHub stars** (from 12 stars at launch - help us reach 1,500!)
- **150+ inbound messages** from logistics companies, gig platforms, field service providers  
- **5 active pilot programs** with trucking companies and delivery fleets
- **3 factoring companies** exploring partnership integrations
- Validated product-market fit within first 24 hours

**Star growth shows real demand.** Help us reach 1,500 stars → **[Star this repo now](https://github.com/actionstatelabs/android-action-kernel/stargazers)**

**Current priority partnerships:**
- **Trucking/logistics companies** - Factoring app automation, invoice processing, driver workflows
- **QA testing teams** - Automated mobile app testing at scale

Due to overwhelming demand, we created a meeting scheduler. **[Request a partnership meeting →](https://build.fillout.com/editor/ctqhgaBkaKus/share)**

---

## The Market: Mobile-First Industries

| Industry | Why They Need This | Market Size | Current State |
|----------|-------------------|-------------|---------------|
| **Logistics** | Drivers use factoring apps (RTS Pro, OTR Capital) in truck cabs | **$10.5T** | Manual, no laptop access |
| **Gig Economy** | Uber/Lyft/DoorDash drivers optimize between apps on phones | **$455B** | Tap manually, lose 20% earnings |
| **Last-Mile Delivery** | Amazon Flex, UPS drivers scan packages on handhelds | **$500B+** | Proprietary apps, no APIs |
| **Field Services** | Techs log work orders on tablets on-site | **$200B+** | Mobile-only workflows |
| **Mobile Banking** | Treasury ops, reconciliation on native banking apps | **$28T** | 2FA + biometric locks |

**Total: $40+ trillion in GDP from mobile-first workflows**

Browser agents can't reach these. Desktop agents don't fit. **Android Use is the only solution.**

---

## Quick Start (60 Seconds)

### Prerequisites
- Python 3.10+
- Android device or emulator (USB debugging enabled)
- ADB (Android Debug Bridge)
- OpenAI API key

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/actionstatelabs/android-action-kernel.git
cd android-action-kernel

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup ADB
brew install android-platform-tools  # macOS
# sudo apt-get install adb           # Linux

# 4. Connect device & verify
adb devices

# 5. Configure LLM Provider (choose one)
export LLM_PROVIDER="openai"  # or anthropic, gemini, bedrock

# Set appropriate API key
export OPENAI_API_KEY="sk-..."        # for OpenAI
# export ANTHROPIC_API_KEY="sk-..."  # for Anthropic
# export GOOGLE_API_KEY="..."        # for Gemini
# export AWS_PROFILE="default"       # for Bedrock

# Optional: Override default model
# export OPENAI_MODEL="gpt-4o"
# export ANTHROPIC_MODEL="claude-sonnet-4"
# export GEMINI_MODEL="gemini-2.0-flash-exp"
# export BEDROCK_MODEL="anthropic.claude-sonnet-4-20250514-v1:0"

# 6. Run your first agent
python kernel.py
```

### Try It: Logistics Example

```python
from kernel import run_agent

# Automate the workflow from the viral demo
run_agent("""
Open WhatsApp, get the latest image, 
then open the invoice app and fill out the form
""")
```

**Other examples:**
- `"Accept the next DoorDash delivery and navigate to restaurant"`
- `"Scan all packages and mark them delivered in the driver app"`
- `"Check Chase mobile for today's transactions"`

---

## Use Cases Beyond Logistics

### Gig Economy Multi-Apping
**Problem:** Drivers lose 20%+ earnings manually switching between DoorDash, Uber Eats, Instacart.

```python
run_agent("Monitor all delivery apps, accept the highest paying order")
```
**Impact:** Instant acceptance of best orders. Drivers report 20-30% earnings increase by optimizing across platforms.

---

### Package Scanning Automation
**Problem:** Drivers manually scan 200+ packages/day in proprietary apps.

```python
run_agent("Scan all packages in photo and mark as loaded in Amazon Flex")
```
**Impact:** Scan 200+ packages in seconds vs. 20+ minutes manually. Eliminates data entry errors.

---

### Mobile Banking Operations
**Problem:** Treasury teams reconcile transactions across multiple mobile banking apps.

```python
run_agent("Log into Chase mobile and export today's wire transfers")
```
**Impact:** Automate daily reconciliation. Process 1000+ transactions in minutes vs. hours of manual work.

---

### Healthcare Mobile Workflows
**Problem:** Staff extract patient data from HIPAA-locked mobile portals.

```python
run_agent("Open Epic MyChart and download lab results for patient 12345")
```
**Impact:** Extract patient data from HIPAA-locked portals. Automate appointment booking and records management.

---

### Mobile App QA Testing
**Problem:** Manual testing of Android apps is slow and expensive.

```python
run_agent("Create account, complete onboarding, make test purchase")
```
**Impact:** 10x faster than manual QA. Full E2E regression tests in CI/CD pipeline.

**Priority partnership area.** If you're a QA team looking to automate mobile testing, **[request a meeting](https://build.fillout.com/editor/ctqhgaBkaKus/share)**.

---

## How It Works (Technical Deep Dive)

### The 3-Step Loop

```
┌─────────────────────────────────────────────────────┐
│  Goal: "Get image from WhatsApp, submit invoice"   │
└─────────────────────────────────────────────────────┘
                        ↓
       ┌────────────────────────────────────┐
       │  1. PERCEPTION                     │
       │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
       │  $ adb shell uiautomator dump      │
       │                                     │
       │  Accessibility Tree (XML):         │
       │  <Button text="Download Image"     │
       │          bounds="[100,500][300,600]"│
       │          clickable="true" />        │
       │                                     │
       │  Parsed to JSON:                   │
       │  {"text": "Download Image",        │
       │   "center": [200, 550],            │
       │   "clickable": true}               │
       └────────────────────────────────────┘
                        ↓
       ┌────────────────────────────────────┐
       │  2. REASONING (GPT-4)              │
       │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
       │  Prompt: "Goal: Get WhatsApp image"│
       │  "Screen: [Download Image button]" │
       │                                     │
       │  GPT-4 Response:                   │
       │  {                                  │
       │    "action": "tap",                 │
       │    "coordinates": [200, 550],       │
       │    "reason": "Download the image"   │
       │  }                                  │
       └────────────────────────────────────┘
                        ↓
       ┌────────────────────────────────────┐
       │  3. ACTION (ADB)                   │
       │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
       │  $ adb shell input tap 200 550     │
       │                                     │
       │  → Image downloaded!               │
       └────────────────────────────────────┘
                        ↓
                  Repeat until done
```

### Why Accessibility Tree > Screenshots

| Approach | Cost | Speed | Accuracy | Works on Device |
|----------|------|-------|----------|----------------|
| **Screenshots (Computer Use)** | $0.15/action | 3-5s | 70-80% | Desktop only |
| **Accessibility Tree (Android Use)** | $0.01/action | <1s | 99%+ | Handheld devices |

**Technical advantage:** Accessibility tree provides structured data (text, coordinates, hierarchy) without image encoding/OCR.

---

## Code Architecture

```
kernel.py (131 lines)
├── get_screen_state()     # Dump & parse accessibility tree
│   └── sanitizer.py       # XML → JSON (54 lines)
├── get_llm_decision()     # GPT-4 reasoning
└── execute_action()       # ADB commands
    ├── tap (x, y)
    ├── type "text"
    ├── home / back
    └── done
```

**Total core logic: <200 lines.** Simple, hackable, extensible.

<details>
<summary><b>API Reference (Click to expand)</b></summary>

### Run an Agent

```python
from kernel import run_agent

run_agent(
    goal="Open WhatsApp and download the latest image",
    max_steps=10  # Max actions before timeout
)
```

### Available Actions

```python
# Tap coordinates
{"action": "tap", "coordinates": [540, 1200]}

# Type text
{"action": "type", "text": "Invoice #12345"}

# Navigate
{"action": "home"}  # Home screen
{"action": "back"}  # Previous screen

# Wait/Complete
{"action": "wait"}  # Wait for loading
{"action": "done"}  # Goal achieved
```

### Get Screen State

```python
from kernel import get_screen_state

screen_json = get_screen_state()
# Returns: [{"text": "Submit", "center": [540, 1200], ...}]
```

</details>

---

## Roadmap

### Now (MVP - 48 hours)
- [x] Core agent loop (perception → reasoning → action)
- [x] Accessibility tree parsing
- [x] GPT-4 integration
- [x] Basic actions (tap, type, navigate)

### Next 2 Weeks
- [ ] **PyPI package:** `pip install android-use`
- [x] **Multi-LLM support:** OpenAI, Claude, Gemini, Bedrock
- [ ] **Llama support:** Local model integration
- [ ] **WhatsApp integration:** Pre-built actions for messaging
- [ ] **Error recovery:** Retry logic, fallback strategies

### Next 3 Months
- [ ] **App-specific agents:** Pre-trained for RTS Pro, OTR Capital, factoring apps
- [ ] **Cloud device farms:** Run at scale on AWS Device Farm, BrowserStack
- [ ] **Vision augmentation:** Screenshot fallback when accessibility insufficient
- [ ] **Multi-step memory:** Remember context across sessions

### Long-term Vision
- [ ] **Hosted Cloud API:** No-code agent execution (waitlist below)
- [ ] **Agent marketplace:** Buy/sell vertical-specific automations
- [ ] **Enterprise platform:** SOC2, audit logs, PII redaction, fleet management
- [ ] **Industry partnerships:** Direct integration with factoring companies, gig platforms

---

## Cloud API Waitlist

**Don't want to host it yourself?** Join the waitlist for our managed Cloud API.

**What you get:**
- No device setup required
- Scale to 1000s of simultaneous agents
- Pre-built integrations (WhatsApp, factoring apps, etc.)
- Enterprise features (audit logs, compliance, SLAs)

**Priority access for:** Trucking/logistics companies and QA testing teams. **[Request a partnership meeting](https://build.fillout.com/editor/ctqhgaBkaKus/share)** or **[join the general waitlist](https://www.actionstatelabs.com/)** (Coming Q1 2026)

---

## Contributing

**Want to help build the future of mobile AI agents?**

### Highest Priority (Partnership Focus)
- **Logistics app templates:** RTS Pro, OTR Capital, Axle, TriumPay integrations - we're actively partnering with trucking companies
- **QA testing framework:** E2E test builders, CI/CD integration, assertion libraries - high demand from QA teams
- **WhatsApp automation:** Message parsing, image extraction for logistics workflows
- **Error handling:** Robustness for unreliable connections (truck cabs!)
- **Documentation:** Tutorials, video walkthroughs for priority use cases

### How to Contribute
1. **Star this repo** to show support
2. Fork it
3. Create branch: `git checkout -b feature/factoring-app-support`
4. Commit: `git commit -m 'Add RTS Pro integration'`
5. Push: `git push origin feature/factoring-app-support`
6. Open PR

**Special focus:** If you work in logistics, gig economy, or field services, your domain expertise is invaluable!

---

## Show Your Support

<div align="center">

### Help Us Reach 1,500 Stars!

**5.3 million views. 12 → 1100+ stars in days. This growth validates the market need.**

**Help us hit 1,500 stars to show investors/partners there's real demand for mobile AI agents!**

**[⭐ Click here to star this repo now →](https://github.com/actionstatelabs/android-action-kernel/stargazers)**

<br>

```
Star Progress: ████████████████░░░░░░░░░░░░ 1100+ / 1,500 stars (63% there!)
```

<sub>Every star helps logistics companies and QA teams discover this solution + validates demand for funding</sub>

<br>

<table>
<tr>
<td align="center" width="25%">

**⭐ Star on GitHub**

Support the project

[Star now](https://github.com/actionstatelabs/android-action-kernel)

</td>
<td align="center" width="25%">

**Book Partnership**

Trucking/logistics or QA testing

[Request meeting](https://build.fillout.com/editor/ctqhgaBkaKus/share)

</td>
<td align="center" width="25%">

**Share on X**

Help others find this

[Share](https://twitter.com/intent/tweet?text=Android%20Use%20lets%20AI%20agents%20control%20native%20Android%20apps.%20Works%20in%20truck%20cabs,%20delivery%20routes,%20field%20service%20—%20anywhere%20laptops%20don't%20fit.%0A%0A95%25%20cheaper%20than%20Computer%20Use.%205.3M%2B%20views.%20950%2B%20stars.%0A%0A&url=https://github.com/actionstatelabs/android-action-kernel&via=ethanjlim)

</td>
<td align="center" width="25%">

**Join Waitlist**

Cloud API access

[Sign up](https://www.actionstatelabs.com/)

</td>
</tr>
</table>

</div>

---

## About the Creator

**Built by [Ethan Lim](https://x.com/ethanjlim)** - AI engineer

### The Origin Story

I spent a week riding along with truck drivers for a logistics automation project. Sitting in the cab, I watched one driver spend 10 minutes after every delivery manually typing data from a Bill of Lading photo into the RTS Pro factoring app on his phone.

> *"I do this 15 times a day. Can't use a laptop—there's no room in the cab, no internet half the time, and I'm already holding the phone to take the photo anyway. This app doesn't have an API. It's just me and this phone."*

That's when it clicked: **The world has AI agents for web browsers and desktop computers, but 3 billion people work on mobile devices that existing agents can't touch.**

I looked at existing solutions:
- **Browser Use:** Only works on websites—most logistics apps are native mobile
- **Computer Use:** $0.15 per action using vision models, requires a laptop, doesn't work on phones

Neither solved the truck cab problem. So I built Android Use using Android's accessibility API instead of expensive vision processing.

**The technical bet:**
- Android's accessibility tree provides structured UI data (text, buttons, coordinates) without OCR
- 95% cheaper than Computer Use ($0.01 vs $0.15 per action)
- 5x faster (<1 second vs 3-5 seconds)
- Works on actual handheld devices in trucks, warehouses, delivery routes

Posted the demo showing a full logistics workflow. **5.3 million views. 150+ inbound messages from companies. 1100+ GitHub stars.** The market validated the need immediately and continues to grow.

### What's Next

Based on inbound demand, the path forward is clear:

1. **Open-source core** (this repo) - Keep the foundation free to drive adoption
2. **Pre-built agents** - Deploy-ready integrations for RTS Pro, OTR Capital, major delivery platforms
3. **Managed Cloud API** - Hosted solution for companies that need to scale immediately (waitlist open)
4. **Enterprise platform** - SOC2, audit logs, fleet management, dedicated support

**Business model:** Freemium. Open-source core is free forever. Revenue from managed hosting ($0.02-0.05/action) and enterprise features ($5-10k/month for 100+ seat deployments). Target customers: logistics companies (50+ drivers), delivery platforms (1000+ workers), field service orgs.

**Defensibility:** Network effects from app-specific agent templates. First-mover advantage in mobile-first verticals. Direct partnerships with factoring companies and gig platforms create distribution moats.

**Vision:** Make AI agents work where 3 billion people actually work—on mobile devices.

---

## Contact

### Priority Partnerships (Book a Meeting)

**[→ Request a meeting for partnerships](https://build.fillout.com/editor/ctqhgaBkaKus/share)** - We created this due to overwhelming demand

**Actively seeking:**
- **Trucking/logistics companies** with 50+ drivers doing manual data entry on mobile factoring apps (RTS Pro, OTR Capital, etc.)
- **QA testing teams** looking to automate mobile app testing at scale

Already running pilots with 5 trucking/delivery companies.

### General Contact

- **X/Twitter:** [@ethanjlim](https://x.com/ethanjlim) - Follow for updates
- **Email:** founders@actionstatelabs.com - General inquiries
- **Demo:** [Watch on X](https://x.com/ethanjlim/status/1999152070428148108?s=20) - 5.3M+ views
- **Issues:** [GitHub Issues](https://github.com/actionstatelabs/android-action-kernel/issues)

---

## By the Numbers

**Since launch:**
- **5.3M+** views on X
- **1100+ GitHub stars** (grew from 12 in days - viral growth!)
- **150+** DMs from companies
- **5** logistics company pilots in progress
- **3** factoring company partnership discussions

**Market data:**
- **3.5M** truck drivers in US alone
- **60M** gig economy workers globally
- **$40T+** in mobile-first GDP

**The star growth from 12 → 1100+ validates real demand.** Help us reach 1,500 → **[Star now](https://github.com/actionstatelabs/android-action-kernel/stargazers)**

---

## License

MIT License - see [LICENSE](LICENSE)

**Free for personal and commercial use.** Build on it, sell services with it, integrate it into your logistics platform.

**Why MIT?** We want this to become the standard for mobile AI agents. Open source = faster adoption.

---

## Acknowledgments

Built on:
- [Browser Use](https://github.com/browser-use/browser-use) - Web agent inspiration
- [Anthropic Computer Use](https://www.anthropic.com/news/computer-use) - Proved UI control works
- Android Accessibility API - The enabling technology
- **The 5.3 million people who watched and validated this need**

Special thanks to:
- Truck drivers who showed me the real problem
- Early beta testers in logistics
- Everyone sharing and supporting this project

---

<div align="center">

<br>

## Built for Workers Who Can't Fit a Laptop in Their Workspace

**Whether you're in a truck cab, on a delivery route, or in the field...**

**AI agents should work where you do.**

<br>

**[⭐ STAR THIS REPO (Help us reach 1,500!)](https://github.com/actionstatelabs/android-action-kernel)** • **[WATCH DEMO (5.3M+ views)](https://x.com/ethanjlim/status/1999152070428148108?s=20)** • **[SHARE IT](https://twitter.com/intent/tweet?url=https://github.com/actionstatelabs/android-action-kernel&via=ethanjlim)**

<br>

```bash
git clone https://github.com/actionstatelabs/android-action-kernel.git
cd android-action-kernel
pip install -r requirements.txt
python kernel.py
```

<br>

---

<sub>Made for field workers • [Star](https://github.com/actionstatelabs/android-action-kernel) • [Follow @ethanjlim](https://x.com/ethanjlim) • [Share](https://twitter.com/intent/tweet?url=https://github.com/actionstatelabs/android-action-kernel&via=ethanjlim)</sub>

</div>

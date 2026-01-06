#!/usr/bin/env python3
"""
SafetyCulture (iAuditor) Inspections Autopilot - MVP Entry Point

This use case automates completing a specific SafetyCulture inspection template.
Run this file directly to launch the agent with the SafetyCulture-focused goal.

Prerequisites:
- Android device connected via ADB (`adb devices` shows it)
- USB debugging enabled
- SafetyCulture app installed and logged in
- The MVP template created in SafetyCulture
"""

import os
import sys
import json
import time
import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from kernel import (
    run_adb_command,
    get_screen_state,
    get_llm_decision,
    execute_action,
    client,
    MODEL,
    LLM_PROVIDER,
)
import sanitizer

# --- SAFETYCULTURE CONFIGURATION ---
SAFETYCULTURE_PACKAGE = "com.safetyculture.iauditor"

# MVP Template Configuration
# Define the exact template and answers for reproducible automation
MVP_TEMPLATE_CONFIG = {
    "template_name": "Warehouse Safety",  # Update to match your actual template name
    "questions": [
        {
            "question": "Are all emergency exits clearly marked and easily accessible?",
            "type": "choice",
            "answer": "yes",
            "options": ["Yes", "No", "N/A"],
            "note": None,
        },
        {
            "question": "How would you rate the overall cleanliness and organization of the warehouse?",
            "type": "choice",
            "answer": "yes",
            "options": ["Yes", "No", "N/A"],
            "note": None,
        },
        {
            "question": "Describe the procedure in place for reporting any safety hazards or incidents.",
            "type": "text",
            "answer": "Report hazards to the supervisor immediately and record details in the incident log.",
            "note": None,
        },
        {
            "question": "How many fire extinguishers are present in the warehouse?",
            "type": "number",
            "answer": "8",
            "note": None,
        },
        {
            "question": "Is all staff provided with and properly trained on the use of personal protective equipment (PPE)?",
            "type": "choice",
            "answer": "yes",
            "options": ["Yes", "No", "N/A"],
            "note": None,
        },
        {
            "question": "When was the last fire drill conducted in the warehouse?",
            "type": "date",
            "answer": "today",
            "note": None,
        },
        {
            "question": "Please upload a photo showing the condition of the warehouse aisles for inspection.",
            "type": "media",
            "answer": "skip",
            "note": None,
        },
    ],
    "location": "",  # Optional: location to select if prompted
}

# Common popup dismiss buttons to auto-handle
# NOTE: Do NOT add "SAVE" here - it's needed for date picker and should be tapped intentionally by the agent
POPUP_DISMISS_TEXTS = [
    "Allow",
    "Don't allow",
    "Deny",
    "No thanks",
    "Not now",
    "Skip",
    "Close",
    "Later",
    "OK",
    "Got it",
    "Dismiss",
    "Cancel",
    "Maybe later",
]

# Success detection: We need MULTIPLE anchors present to confirm the Report screen
# This avoids false positives from partial matches (e.g., "HSE Contractor Performance Report")
SUCCESS_ANCHOR_SETS = [
    # Report screen has both Download AND Share buttons
    {"Download", "Share"},
    # Alternative: explicit submission confirmation
    {"Inspection submitted"},
    {"Successfully submitted"},
]

# --- LOGGING ---
LOGS_DIR = Path(__file__).parent.parent / "logs"


def ensure_logs_dir():
    """Create logs directory if it doesn't exist."""
    LOGS_DIR.mkdir(exist_ok=True)


def create_run_log(run_id: str) -> Path:
    """Create a new log file for this run."""
    ensure_logs_dir()
    return LOGS_DIR / f"safetyculture_run_{run_id}.jsonl"


def log_step(log_path: Path, step_data: dict):
    """Append a step to the run log."""
    with open(log_path, "a") as f:
        f.write(json.dumps(step_data) + "\n")


# --- APP LAUNCH ---
def launch_app(package: str) -> bool:
    """Launch an app by package name using ADB monkey command."""
    print(f"🚀 Launching app: {package}")
    result = run_adb_command([
        "shell", "monkey", "-p", package,
        "-c", "android.intent.category.LAUNCHER", "1"
    ])
    success = "Events injected: 1" in result or "cmp=" in result.lower()
    if success:
        print(f"✅ App launched successfully")
    else:
        print(f"⚠️ App launch may have failed: {result}")
    return success


# --- WAIT UNTIL ---
def wait_until_text(target_text: str, timeout_s: int = 10, case_sensitive: bool = False) -> bool:
    """
    Wait until the screen contains an element with text matching target_text.
    Returns True if found within timeout, False otherwise.
    """
    print(f"⏳ Waiting for text: '{target_text}' (timeout: {timeout_s}s)")
    start_time = time.time()
    
    while time.time() - start_time < timeout_s:
        screen_json = get_screen_state()
        try:
            elements = json.loads(screen_json)
            for elem in elements:
                elem_text = elem.get("text", "")
                if case_sensitive:
                    if target_text in elem_text:
                        print(f"✅ Found: '{target_text}'")
                        return True
                else:
                    if target_text.lower() in elem_text.lower():
                        print(f"✅ Found: '{target_text}'")
                        return True
        except json.JSONDecodeError:
            pass
        time.sleep(1)
    
    print(f"⚠️ Timeout waiting for: '{target_text}'")
    return False


def wait_until_any_text(target_texts: list, timeout_s: int = 10) -> str | None:
    """
    Wait until the screen contains any of the target texts.
    Returns the matched text if found, None otherwise.
    """
    print(f"⏳ Waiting for any of: {target_texts} (timeout: {timeout_s}s)")
    start_time = time.time()
    
    while time.time() - start_time < timeout_s:
        screen_json = get_screen_state()
        try:
            elements = json.loads(screen_json)
            for elem in elements:
                elem_text = elem.get("text", "").lower()
                for target in target_texts:
                    if target.lower() in elem_text:
                        print(f"✅ Found: '{target}'")
                        return target
        except json.JSONDecodeError:
            pass
        time.sleep(1)
    
    print(f"⚠️ Timeout waiting for any of: {target_texts}")
    return None


# --- POPUP HANDLER ---
def handle_popups(screen_json: str) -> bool:
    """
    Scan screen for common popup dismiss buttons and tap them.
    Returns True if a popup was dismissed, False otherwise.
    """
    try:
        elements = json.loads(screen_json)
    except json.JSONDecodeError:
        return False
    
    for elem in elements:
        elem_text = elem.get("text", "").strip()
        if not elem_text:
            continue
        
        for dismiss_text in POPUP_DISMISS_TEXTS:
            if elem_text.lower() == dismiss_text.lower():
                if elem.get("clickable", False):
                    center = elem.get("center")
                    if center:
                        print(f"🔔 Dismissing popup: '{elem_text}'")
                        run_adb_command(["shell", "input", "tap", str(center[0]), str(center[1])])
                        time.sleep(1)
                        return True
    return False


# --- TEMPLATE-DRIVEN GOAL CONSTRUCTION ---
def build_inspection_goal(config: dict) -> str:
    """Build a detailed goal string from the template configuration."""
    template_name = config["template_name"]
    questions = config["questions"]
    location = config.get("location", "")
    
    question_plan = []
    for i, q in enumerate(questions, 1):
        q_type = q.get("type", "choice")
        answer = q.get("answer", "")
        note = q.get("note")

        if q_type == "choice":
            options = q.get("options", ["Yes", "No", "N/A"])
            answer_str = str(answer).strip().upper()
            question_plan.append(
                f"  Q{i}: Choice question. Tap the '{answer_str}' button (options: {', '.join(options)})"
            )
        elif q_type == "text":
            question_plan.append(
                f"  Q{i}: Text question. Tap the text field (often shows 'Tap to edit'), then type: '{str(answer)}'"
            )
        elif q_type == "number":
            question_plan.append(
                f"  Q{i}: Number question. Tap the input field, then type the number: '{str(answer)}'"
            )
        elif q_type == "date":
            question_plan.append(
                f"  Q{i}: Date question. Tap 'Select Date', then tap 'SAVE' (top right) to confirm today's date"
            )
        elif q_type == "media":
            question_plan.append(
                f"  Q{i}: Media upload. Do NOT add media. If optional, leave blank and continue. If required and blocked, stop."
            )
        else:
            question_plan.append(f"  Q{i}: Answer: '{str(answer)}'")

        if note:
            question_plan.append(f"      Add note: '{note}'")
    
    plan_str = "\n".join(question_plan)
    
    goal = f"""Complete a SafetyCulture inspection using this exact plan:

1. The SafetyCulture app is now open
2. Navigate to start a new inspection using template: "{template_name}"
3. The inspection starts on a "Title Page" (Page 1/2) with pre-filled fields like "Conducted on", "Prepared by", "Location"
   - Do NOT edit these fields - they are auto-filled
   - Tap "Next" (bottom right corner) to go to Page 2/2 where the actual questions are
4. On Page 2/2, answer each question in order:
{plan_str}
5. After answering all questions, tap "Complete" to submit the inspection
6. Wait for confirmation that the inspection was submitted successfully

IMPORTANT RULES:
- The Title Page (Page 1/2) has "Conducted on", "Prepared by", "Location" - SKIP these and tap "Next"
- For choice questions, look for Yes/No/N/A buttons and tap the appropriate one
- For text/number fields, tap the field first, then type the answer
- Scroll down if you don't see the next question or if you need to find the Complete button
- Do NOT take photos or add attachments - skip media upload questions entirely
- For date picker: tap "Select Date", then tap "SAVE" button (top right of dialog) to confirm
- The "Complete" button is at the bottom - you may need to scroll down to see it
- After tapping Complete, wait for the Report screen (with Download/Share buttons) before marking done
"""
    return goal


# --- MAIN AGENT LOOP ---
def run_safetyculture_agent(
    config: dict = None,
    max_steps: int = 50,
    auto_launch: bool = True,
) -> dict:
    """
    Run the SafetyCulture inspection agent.
    
    Returns a dict with:
    - success: bool
    - steps: int
    - duration_s: float
    - failure_reason: str | None
    """
    if config is None:
        config = MVP_TEMPLATE_CONFIG
    
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = create_run_log(run_id)
    
    print(f"🚀 SafetyCulture Inspection Agent Started")
    print(f"📋 Template: {config['template_name']}")
    print(f"📝 Log file: {log_path}")
    print(f"📡 Using provider: {LLM_PROVIDER} | Model: {MODEL}")
    
    start_time = time.time()
    action_history = []
    result = {
        "success": False,
        "steps": 0,
        "duration_s": 0,
        "failure_reason": None,
        "run_id": run_id,
    }
    
    # Log run start
    log_step(log_path, {
        "event": "run_start",
        "timestamp": datetime.datetime.now().isoformat(),
        "template": config["template_name"],
        "max_steps": max_steps,
    })
    
    # Step 0: Launch the app
    if auto_launch:
        if not launch_app(SAFETYCULTURE_PACKAGE):
            result["failure_reason"] = "Failed to launch SafetyCulture app"
            log_step(log_path, {"event": "error", "reason": result["failure_reason"]})
            return result
        
        # Wait for app to load
        time.sleep(3)
        
        # Wait for a known home element
        if not wait_until_text("Inspections", timeout_s=15):
            # Try alternative home indicators
            if not wait_until_text("Home", timeout_s=5):
                print("⚠️ Could not confirm app loaded, continuing anyway...")
    
    # Build the goal
    goal = build_inspection_goal(config)
    
    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")
        result["steps"] = step + 1
        
        # 1. Perception
        print("👀 Scanning Screen...")
        screen_context = get_screen_state()
        
        # 2. Handle popups before LLM decision
        popup_dismissed = handle_popups(screen_context)
        if popup_dismissed:
            log_step(log_path, {
                "step": step + 1,
                "event": "popup_dismissed",
                "timestamp": datetime.datetime.now().isoformat(),
            })
            # Re-scan after dismissing popup
            time.sleep(1)
            screen_context = get_screen_state()
        
        # 3. Check for success anchors (require ALL anchors in a set to be present)
        try:
            elements = json.loads(screen_context)
            # Collect all visible text on screen
            all_text = set()
            for elem in elements:
                elem_text = elem.get("text", "").strip().lower()
                if elem_text:
                    all_text.add(elem_text)
            
            # Check if any anchor set is fully satisfied
            for anchor_set in SUCCESS_ANCHOR_SETS:
                matched = all(any(anchor.lower() in txt for txt in all_text) for anchor in anchor_set)
                if matched:
                    print(f"🎉 Success detected: {anchor_set}")
                    result["success"] = True
                    result["duration_s"] = time.time() - start_time
                    log_step(log_path, {
                        "step": step + 1,
                        "event": "success",
                        "anchors": list(anchor_set),
                        "timestamp": datetime.datetime.now().isoformat(),
                    })
                    log_step(log_path, {
                        "event": "run_end",
                        "success": True,
                        "steps": result["steps"],
                        "duration_s": result["duration_s"],
                    })
                    return result
        except json.JSONDecodeError:
            pass
        
        # 4. Reasoning
        print("🧠 Thinking...")
        try:
            decision = get_llm_decision(goal, screen_context, action_history)
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            result["failure_reason"] = f"LLM error: {e}"
            log_step(log_path, {"step": step + 1, "event": "error", "reason": str(e)})
            break
        
        print(f"💡 Decision: {decision.get('reason')}")
        
        # Track action history
        action_entry = {
            "step": step + 1,
            "action": decision.get("action"),
            "coordinates": decision.get("coordinates"),
            "text": decision.get("text"),
            "reason": decision.get("reason"),
        }
        action_history.append(action_entry)
        
        # Log the step (redacted)
        log_step(log_path, {
            "step": step + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "action": decision.get("action"),
            "reason": decision.get("reason"),
        })
        
        # 5. Action
        from kernel import execute_action
        goal_achieved = execute_action(decision)
        
        if goal_achieved:
            # Agent said done - verify with success anchors
            time.sleep(2)
            screen_context = get_screen_state()
            
            # Check for success using anchor sets
            try:
                elements = json.loads(screen_context)
                all_text = set()
                for elem in elements:
                    elem_text = elem.get("text", "").strip().lower()
                    if elem_text:
                        all_text.add(elem_text)
                
                found_success = False
                for anchor_set in SUCCESS_ANCHOR_SETS:
                    matched = all(any(anchor.lower() in txt for txt in all_text) for anchor in anchor_set)
                    if matched:
                        found_success = True
                        break
                
                if found_success:
                    result["success"] = True
                    print(f"✅ Inspection submitted successfully!")
                else:
                    print("⚠️ Agent marked done but no success anchor found")
                    result["failure_reason"] = "Agent marked done but submission not confirmed"
            except json.JSONDecodeError:
                print("⚠️ Could not verify success - screen parse error")
                result["failure_reason"] = "Could not verify submission"
            
            break
        
        # Wait for UI to update
        time.sleep(2)
    
    if not result["success"] and not result["failure_reason"]:
        result["failure_reason"] = f"Max steps ({max_steps}) reached"
    
    result["duration_s"] = time.time() - start_time
    
    log_step(log_path, {
        "event": "run_end",
        "success": result["success"],
        "steps": result["steps"],
        "duration_s": result["duration_s"],
        "failure_reason": result["failure_reason"],
    })
    
    if result["success"]:
        print(f"\n🎉 SUCCESS! Completed in {result['steps']} steps, {result['duration_s']:.1f}s")
    else:
        print(f"\n❌ FAILED: {result['failure_reason']}")
    
    return result


def run_reliability_test(num_runs: int = 20, config: dict = None) -> dict:
    """
    Run the inspection multiple times and report statistics.
    """
    if config is None:
        config = MVP_TEMPLATE_CONFIG
    
    print(f"\n{'='*60}")
    print(f"🧪 RELIABILITY TEST: {num_runs} runs")
    print(f"{'='*60}\n")
    
    results = []
    
    for i in range(num_runs):
        print(f"\n{'='*40}")
        print(f"📊 Run {i + 1}/{num_runs}")
        print(f"{'='*40}")
        
        result = run_safetyculture_agent(config=config)
        results.append(result)
        
        # Brief pause between runs
        if i < num_runs - 1:
            print("\n⏳ Waiting 5s before next run...")
            time.sleep(5)
    
    # Calculate statistics
    successes = sum(1 for r in results if r["success"])
    success_rate = (successes / num_runs) * 100
    
    durations = [r["duration_s"] for r in results if r["success"]]
    median_duration = sorted(durations)[len(durations) // 2] if durations else 0
    
    failure_reasons = {}
    for r in results:
        if not r["success"] and r["failure_reason"]:
            reason = r["failure_reason"]
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
    
    print(f"\n{'='*60}")
    print(f"📊 RELIABILITY TEST RESULTS")
    print(f"{'='*60}")
    print(f"✅ Success Rate: {success_rate:.1f}% ({successes}/{num_runs})")
    print(f"⏱️  Median Duration: {median_duration:.1f}s")
    
    if failure_reasons:
        print(f"\n❌ Top Failure Reasons:")
        for reason, count in sorted(failure_reasons.items(), key=lambda x: -x[1]):
            print(f"   - {reason}: {count} times")
    
    return {
        "success_rate": success_rate,
        "successes": successes,
        "total_runs": num_runs,
        "median_duration_s": median_duration,
        "failure_reasons": failure_reasons,
        "results": results,
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SafetyCulture Inspection Autopilot")
    parser.add_argument("--test", action="store_true", help="Run reliability test (20 runs)")
    parser.add_argument("--runs", type=int, default=20, help="Number of runs for reliability test")
    parser.add_argument("--max-steps", type=int, default=50, help="Max steps per run")
    parser.add_argument("--no-launch", action="store_true", help="Skip auto-launching the app")
    
    args = parser.parse_args()
    
    if args.test:
        run_reliability_test(num_runs=args.runs)
    else:
        run_safetyculture_agent(max_steps=args.max_steps, auto_launch=not args.no_launch)

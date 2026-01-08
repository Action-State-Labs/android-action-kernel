import os
import time
import subprocess
import json
import asyncio
from typing import Dict, Any, List
from llm_manager import LLMManager
from action_models import TapAction, TypeAction, NavigationAction, ControlAction
import sanitizer

# --- CONFIGURATION ---
ADB_PATH = "adb"
SCREEN_DUMP_PATH = "/sdcard/window_dump.xml"
LOCAL_DUMP_PATH = "window_dump.xml"

# Initialize LLM manager
llm_manager = None

def initialize_llm():
    """Initialize the LLM manager."""
    global llm_manager
    if llm_manager is None:
        llm_manager = LLMManager()

def run_adb_command(command: List[str]):
    """Executes a shell command via ADB."""
    result = subprocess.run([ADB_PATH] + command, capture_output=True, text=True)
    if result.stderr and "error" in result.stderr.lower():
        print(f"❌ ADB Error: {result.stderr.strip()}")
    return result.stdout.strip()

def get_screen_state() -> str:
    """Dumps the current UI XML and returns the sanitized JSON string."""
    # 1. Capture XML
    run_adb_command(["shell", "uiautomator", "dump", SCREEN_DUMP_PATH])
    
    # 2. Pull to local
    run_adb_command(["pull", SCREEN_DUMP_PATH, LOCAL_DUMP_PATH])
    
    # 3. Read & Sanitize
    if not os.path.exists(LOCAL_DUMP_PATH):
        return "Error: Could not capture screen."
        
    with open(LOCAL_DUMP_PATH, "r", encoding="utf-8") as f:
        xml_content = f.read()
        
    elements = sanitizer.get_interactive_elements(xml_content)
    return json.dumps(elements, indent=2)

def execute_action(action):
    """Executes the action decided by the LLM."""
    if isinstance(action, TapAction):
        x, y = action.coordinates
        print(f"👉 Tapping: ({x}, {y})")
        run_adb_command(["shell", "input", "tap", str(x), str(y)])

    elif isinstance(action, TypeAction):
        text = action.text.replace(" ", "%s")  # ADB requires %s for spaces
        print(f"⌨️ Typing: {action.text}")
        run_adb_command(["shell", "input", "text", text])

    elif isinstance(action, NavigationAction):
        if action.action == "home":
            print("🏠 Going Home")
            run_adb_command(["shell", "input", "keyevent", "KEYCODE_HOME"])
        elif action.action == "back":
            print("🔙 Going Back")
            run_adb_command(["shell", "input", "keyevent", "KEYCODE_BACK"])

    elif isinstance(action, ControlAction):
        if action.action == "wait":
            print("⏳ Waiting...")
            time.sleep(2)
        elif action.action == "done":
            print("✅ Goal Achieved.")
            exit(0)

async def get_llm_decision(goal: str, screen_context: str):
    """Sends screen context to LLM and asks for the next move."""
    global llm_manager
    if llm_manager is None:
        initialize_llm()

    action = await llm_manager.get_decision(goal, screen_context)
    return action

async def run_agent(goal: str, max_steps=10):
    """Main agent loop."""
    print(f"🚀 Android Use Agent Started. Goal: {goal}")

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        # 1. Perception
        print("👀 Scanning Screen...")
        screen_context = get_screen_state()

        # 2. Reasoning
        print("🧠 Thinking...")
        decision = await get_llm_decision(goal, screen_context)
        print(f"💡 Decision: {decision.reason}")

        # 3. Action
        execute_action(decision)

        # Wait for UI to update
        time.sleep(2)

if __name__ == "__main__":
    GOAL = input("Enter your goal: ")
    asyncio.run(run_agent(GOAL))
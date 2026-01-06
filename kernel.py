import os
import time
import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI
import sanitizer

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
ADB_PATH = "adb"  # Ensure adb is in your PATH
SCREEN_DUMP_PATH = "/sdcard/window_dump.xml"
LOCAL_DUMP_PATH = "window_dump.xml"

# --- LLM PROVIDER CONFIGURATION ---
# Default: OpenRouter with openai/gpt-4o
# Override with LLM_PROVIDER=openai and OPENAI_API_KEY for direct OpenAI access
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openrouter").lower()

DEFAULT_MODELS = {
    "openrouter": "openai/gpt-4o",
    "openai": "gpt-4o",
}

def get_llm_client_and_model() -> Tuple[OpenAI, str]:
    """Returns the appropriate OpenAI-compatible client and model based on LLM_PROVIDER."""
    model = os.environ.get("LLM_MODEL", DEFAULT_MODELS.get(LLM_PROVIDER, "openai/gpt-4o"))
    
    if LLM_PROVIDER == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        client = OpenAI(api_key=api_key)
    else:  # Default: openrouter
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required (default provider is OpenRouter)")
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
    
    return client, model

client, MODEL = get_llm_client_and_model()

def run_adb_command(command: List[str]) -> str:
    """Executes a shell command via ADB."""
    result = subprocess.run([ADB_PATH] + command, capture_output=True, text=True)
    if result.returncode != 0:
        error_msg = result.stderr.strip() or result.stdout.strip()
        print(f"❌ ADB Error (code {result.returncode}): {error_msg}")
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

class GoalAchieved(Exception):
    """Raised when the agent completes its goal."""
    pass


def validate_action(action: Dict[str, Any]) -> Optional[str]:
    """Validates action schema. Returns error message if invalid, None if valid."""
    if not isinstance(action, dict):
        return "Action must be a dictionary"
    
    act_type = action.get("action")
    valid_actions = {"tap", "type", "home", "back", "wait", "done", "enter", "clear", "launch", "scroll"}
    
    if act_type not in valid_actions:
        return f"Unknown action '{act_type}'. Must be one of: {valid_actions}"
    
    if act_type == "tap":
        coords = action.get("coordinates")
        if not isinstance(coords, (list, tuple)) or len(coords) != 2:
            return "'tap' action requires 'coordinates' as [x, y]"
        try:
            int(coords[0]), int(coords[1])
        except (TypeError, ValueError):
            return "'tap' coordinates must be integers"
    
    if act_type == "type":
        text = action.get("text")
        if not isinstance(text, str) or not text:
            return "'type' action requires non-empty 'text' string"
    
    if act_type == "launch":
        package = action.get("package")
        if not isinstance(package, str) or not package:
            return "'launch' action requires non-empty 'package' string"
    
    if act_type == "scroll":
        direction = action.get("direction", "down")
        if direction not in {"up", "down", "left", "right"}:
            return "'scroll' direction must be one of: up, down, left, right"
    
    return None


def execute_action(action: Dict[str, Any]) -> bool:
    """Executes the action decided by the LLM. Returns True if goal achieved."""
    act_type = action.get("action")
    
    if act_type == "tap":
        coords = action.get("coordinates")
        x, y = int(coords[0]), int(coords[1])
        print(f"👉 Tapping: ({x}, {y})")
        run_adb_command(["shell", "input", "tap", str(x), str(y)])
        
    elif act_type == "type":
        text = action.get("text").replace(" ", "%s") # ADB requires %s for spaces
        print(f"⌨️ Typing: {action.get('text')}")
        run_adb_command(["shell", "input", "text", text])
        
    elif act_type == "home":
        print("🏠 Going Home")
        run_adb_command(["shell", "input", "keyevent", "KEYCODE_HOME"])
        
    elif act_type == "back":
        print("🔙 Going Back")
        run_adb_command(["shell", "input", "keyevent", "KEYCODE_BACK"])
        
    elif act_type == "wait":
        print("⏳ Waiting...")
        time.sleep(2)
        
    elif act_type == "enter":
        print("⏎ Pressing Enter")
        run_adb_command(["shell", "input", "keyevent", "KEYCODE_ENTER"])
        
    elif act_type == "clear":
        print("🗑️ Clearing text field")
        # Select all (Ctrl+A) then delete
        run_adb_command(["shell", "input", "keyevent", "KEYCODE_MOVE_END"])  # Move to end
        run_adb_command(["shell", "input", "keyevent", "--longpress", "KEYCODE_DEL"])  # Long-press delete
        # Fallback: try select-all + delete
        run_adb_command(["shell", "input", "keycombination", "KEYCODE_CTRL_LEFT", "KEYCODE_A"])  # Select all
        run_adb_command(["shell", "input", "keyevent", "KEYCODE_DEL"])  # Delete selection
    
    elif act_type == "launch":
        package = action.get("package")
        print(f"🚀 Launching app: {package}")
        run_adb_command(["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"])
    
    elif act_type == "scroll":
        direction = action.get("direction", "down")
        print(f"📜 Scrolling {direction}")
        # Get screen dimensions (approximate center for swipe)
        # Default to common phone resolution center
        cx, cy = 540, 1200
        distance = 500
        if direction == "down":
            run_adb_command(["shell", "input", "swipe", str(cx), str(cy), str(cx), str(cy - distance), "300"])
        elif direction == "up":
            run_adb_command(["shell", "input", "swipe", str(cx), str(cy - distance), str(cx), str(cy), "300"])
        elif direction == "left":
            run_adb_command(["shell", "input", "swipe", str(cx), str(cy), str(cx - distance), str(cy), "300"])
        elif direction == "right":
            run_adb_command(["shell", "input", "swipe", str(cx - distance), str(cy), str(cx), str(cy), "300"])
        
    elif act_type == "done":
        print("✅ Goal Achieved.")
        return True
    
    return False

def get_llm_decision(goal: str, screen_context: str, action_history: List[Dict[str, Any]], retry_count: int = 0) -> Dict[str, Any]:
    """Sends screen context to LLM and asks for the next move."""
    system_prompt = """You are an Android Driver Agent. Your job is to achieve the user's goal by navigating the UI.

You will receive:
1. The User's Goal.
2. A list of interactive UI elements (JSON) with their (x,y) center coordinates.
3. Your previous actions (so you don't repeat yourself).

You must output ONLY a valid JSON object with your next action.

Available Actions:
- {"action": "tap", "coordinates": [x, y], "reason": "Why you are tapping"}
- {"action": "type", "text": "Hello World", "reason": "Why you are typing"}
- {"action": "clear", "reason": "Clear/delete text in focused field"}
- {"action": "enter", "reason": "Press Enter/Submit key"}
- {"action": "home", "reason": "Go to home screen"}
- {"action": "back", "reason": "Go back"}
- {"action": "wait", "reason": "Wait for loading"}
- {"action": "scroll", "direction": "down", "reason": "Scroll to see more content"}
- {"action": "launch", "package": "com.example.app", "reason": "Launch an app by package name"}
- {"action": "done", "reason": "Task complete"}

IMPORTANT WORKFLOW RULES:
1. To enter text in a search box or text field: FIRST tap the field, THEN on the next step use "type" to enter text.
2. If you already tapped a text field in your previous action, your next action should be "type" with the text you want to enter.
3. If a text field already has text and you need to replace it, use "clear" first, then "type" the new text.
4. After typing in a search field, use "enter" to submit the search. This is more reliable than tapping a search button.
5. Do NOT tap the same element repeatedly. If you tapped something and nothing changed, try a different approach.

Example - Searching for something:
Step 1: {"action": "tap", "coordinates": [540, 100], "reason": "Tapping search box to focus it"}
Step 2: {"action": "type", "text": "pizza near me", "reason": "Typing search query"}
Step 3: {"action": "enter", "reason": "Submitting the search query"}
"""
    
    history_str = ""
    if action_history:
        history_str = "\n\nPREVIOUS_ACTIONS:\n" + json.dumps(action_history[-5:], indent=2)  # Last 5 actions
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"GOAL: {goal}\n\nSCREEN_CONTEXT:\n{screen_context}{history_str}"}
            ]
        )
        
        content = response.choices[0].message.content
        decision = json.loads(content)
        
        validation_error = validate_action(decision)
        if validation_error:
            if retry_count < 1:
                print(f"⚠️ Invalid action from LLM: {validation_error}. Retrying...")
                return get_llm_decision(goal, screen_context, action_history, retry_count + 1)
            else:
                raise ValueError(f"LLM returned invalid action after retry: {validation_error}")
        
        return decision
        
    except json.JSONDecodeError as e:
        if retry_count < 1:
            print(f"⚠️ Failed to parse LLM response as JSON: {e}. Retrying...")
            return get_llm_decision(goal, screen_context, action_history, retry_count + 1)
        else:
            raise ValueError(f"LLM did not return valid JSON after retry: {e}")

def run_agent(goal: str, max_steps: int = 10) -> bool:
    """Runs the agent loop. Returns True if goal achieved, False if max_steps reached."""
    print(f"🚀 Android Use Agent Started. Goal: {goal}")
    print(f"📡 Using provider: {LLM_PROVIDER} | Model: {MODEL}")
    
    action_history: List[Dict[str, Any]] = []
    
    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")
        
        # 1. Perception
        print("👀 Scanning Screen...")
        screen_context = get_screen_state()
        
        # 2. Reasoning
        print("🧠 Thinking...")
        decision = get_llm_decision(goal, screen_context, action_history)
        print(f"💡 Decision: {decision.get('reason')}")
        
        # Track action history (store a summary)
        action_history.append({
            "step": step + 1,
            "action": decision.get("action"),
            "coordinates": decision.get("coordinates"),
            "text": decision.get("text"),
            "reason": decision.get("reason")
        })
        
        # 3. Action
        goal_achieved = execute_action(decision)
        if goal_achieved:
            return True
        
        # Wait for UI to update
        time.sleep(2)
    
    print(f"⚠️ Max steps ({max_steps}) reached without achieving goal.")
    return False

if __name__ == "__main__":
    # Example Goal: "Open settings and turn on Wi-Fi"
    # Or your demo goal: "Find the 'Connect' button and tap it"
    GOAL = input("Enter your goal: ")
    run_agent(GOAL)
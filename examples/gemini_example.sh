#!/bin/bash
# Example: Using Google Gemini (cheapest option)

export LLM_PROVIDER="gemini"
export GOOGLE_API_KEY="..."  # Replace with your key
export GEMINI_MODEL="gemini-2.0-flash-exp"  # Optional

python kernel.py

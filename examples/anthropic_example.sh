#!/bin/bash
# Example: Using Anthropic Claude

export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-..."  # Replace with your key
export ANTHROPIC_MODEL="claude-sonnet-4"  # Optional

python kernel.py

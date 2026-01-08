#!/bin/bash
# Example: Using OpenAI GPT-4o

export LLM_PROVIDER="openai"
export OPENAI_API_KEY="sk-..."  # Replace with your key
export OPENAI_MODEL="gpt-4o"    # Optional: override default

python kernel.py

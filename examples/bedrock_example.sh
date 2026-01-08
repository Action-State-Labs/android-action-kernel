#!/bin/bash
# Example: Using AWS Bedrock with Claude

export LLM_PROVIDER="bedrock"
export AWS_PROFILE="default"  # Or use AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
export BEDROCK_MODEL="anthropic.claude-sonnet-4-20250514-v1:0"  # Optional

python kernel.py

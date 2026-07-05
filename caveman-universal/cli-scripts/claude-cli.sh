#!/bin/bash
# Caveman CLI for Claude (No GUI)
# Usage: ./claude-cli.sh [lite|full|ultra|review] "your prompt"

set -e

MODE="${1:-full}"
PROMPT="$2"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 [lite|full|ultra|review] \"your prompt\""
    echo "Example: $0 full \"Compress this thesis abstract...\""
    exit 1
fi

# Check for Claude API key or CLI tool
if command -v claude &> /dev/null; then
    # Using Claude Code CLI
    claude --prompt "/caveman $MODE: $PROMPT"
elif [ -n "$ANTHROPIC_API_KEY" ]; then
    # Using curl with API
    RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"claude-sonnet-4-20250514\",
            \"max_tokens\": 4096,
            \"messages\": [
                {\"role\": \"user\", \"content\": \"Use caveman $MODE mode: $PROMPT\"}
            ]
        }")
    
    echo "$RESPONSE" | grep -o '"content":"[^"]*"' | cut -d'"' -f4
else
    echo "Error: No Claude CLI or ANTHROPIC_API_KEY found."
    echo "Install Claude Code: npm install -g @anthropic-ai/claude-code"
    echo "Or set ANTHROPIC_API_KEY environment variable."
    exit 1
fi

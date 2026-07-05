#!/bin/bash
# Caveman CLI for Qwen (No GUI)
# Usage: ./qwen-cli.sh [lite|full|ultra|review] "your prompt"
# Supports: Alibaba Cloud API, Ollama local, DashScope

set -e

MODE="${1:-full}"
PROMPT="$2"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 [lite|full|ultra|review] \"your prompt\""
    echo "Example: $0 full \"Compress this thesis abstract...\""
    exit 1
fi

# Priority: Ollama (local) > DashScope > Alibaba Cloud API

if command -v ollama &> /dev/null && ollama list | grep -q qwen; then
    # Using Ollama (local, no API key needed)
    echo "Using local Ollama Qwen model..."
    ollama run qwen "Use caveman $MODE mode: $PROMPT"

elif [ -n "$DASHSCOPE_API_KEY" ]; then
    # Using Alibaba DashScope
    echo "Using DashScope API..."
    RESPONSE=$(curl -s https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"qwen-max\",
            \"input\": {
                \"messages\": [
                    {\"role\": \"system\", \"content\": \"You are a caveman assistant. Use $MODE compression mode.\"},
                    {\"role\": \"user\", \"content\": \"$PROMPT\"}
                ]
            }
        }")
    
    echo "$RESPONSE" | grep -o '"content":"[^"]*"' | tail -1 | cut -d'"' -f4

elif [ -n "$ALIBABA_CLOUD_API_KEY" ]; then
    # Using Alibaba Cloud API
    echo "Using Alibaba Cloud API..."
    RESPONSE=$(curl -s https://dashscope-intl.ap-southeast-1.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
        -H "Authorization: Bearer $ALIBABA_CLOUD_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"qwen-plus\",
            \"input\": {
                \"messages\": [
                    {\"role\": \"system\", \"content\": \"You are a caveman assistant. Use $MODE compression mode.\"},
                    {\"role\": \"user\", \"content\": \"$PROMPT\"}
                ]
            }
        }")
    
    echo "$RESPONSE" | grep -o '"content":"[^"]*"' | tail -1 | cut -d'"' -f4

else
    echo "Error: No Qwen backend found."
    echo ""
    echo "Options:"
    echo "  1. Install Ollama (recommended, free, local):"
    echo "     curl -fsSL https://ollama.com/install.sh | sh"
    echo "     ollama pull qwen"
    echo ""
    echo "  2. Set DASHSCOPE_API_KEY environment variable"
    echo "  3. Set ALIBABA_CLOUD_API_KEY environment variable"
    echo ""
    exit 1
fi

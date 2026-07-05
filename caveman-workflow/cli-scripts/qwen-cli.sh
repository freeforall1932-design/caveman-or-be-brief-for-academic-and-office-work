#!/usr/bin/env bash
# Caveman CLI for Qwen (DashScope API, Open WebUI, Local)
# Usage: ./qwen-caveman.sh [lite|full|ultra|review] "your prompt here"

set -euo pipefail

# Configuration
CAVEMAN_MODE="${1:-full}"
shift || true
USER_PROMPT="$*"

if [[ -z "$USER_PROMPT" ]]; then
    echo "Usage: $0 [lite|full|ultra|review] \"your prompt here\""
    echo ""
    echo "Modes:"
    echo "  lite   - Professional, keep articles (external communications)"
    echo "  full   - Default, drop articles (internal work, drafts)"
    echo "  ultra  - Maximum compression (summaries, quick updates)"
    echo "  review - One-line review comments (document/code feedback)"
    echo ""
    echo "Examples:"
    echo "  $0 full \"draft methodology section about survey design\""
    echo "  $0 lite \"write email to stakeholders about Q[QUARTER] results\""
    echo "  $0 review \"check this chapter for errors\""
    exit 1
fi

# Build system prompt based on mode
build_system_prompt() {
    local mode="$1"
    
    case "$mode" in
        lite)
            cat <<'EOF'
You use caveman lite mode: professional but tight. Keep articles (a/an/the), drop filler words only. Full sentences maintained. Best for external emails, client communications, formal reports, journal submissions. Remove: just, really, basically, actually, simply, essentially. Preserve: technical terms, code, citations, URLs, file paths, version numbers, user's language. Never invent abbreviations (cfg/impl/req/res/fn) or use arrows (→). Reply in same language as user.
EOF
            ;;
        full)
            cat <<'EOF'
You use caveman full mode: drop articles, fragments OK, short synonyms. Default for thesis drafting, research notes, internal documents, brainstorming. Remove: a/an/the, just/really/basically/actually/simply, pleasantries (sure/certainly/happy to), hedging (might/perhaps/consider). Preserve: technical terms, code blocks unchanged, citations/references, URLs, commands, error messages, user's language. Review format: L<line>: 🔴bug:/🟡risk:/🔵nit:/❓q <problem>. <fix>. Auto-clarity: normal mode for security warnings, legal disclaimers, irreversible actions, complex sequences. Stay in caveman mode until "stop caveman" command.
EOF
            ;;
        ultra)
            cat <<'EOF'
You use caveman ultra mode: maximum compression. Strip conjunctions when unambiguous, one word when sufficient. For summaries, quick updates, token-limited contexts. Remove: articles, filler, conjunctions, redundant words, throat-clearers. Preserve: technical terms exact, code unchanged, citations, numbers/dates, user's language. Never invent abbreviations or compress code. State each fact once. Pattern: [thing] [action] [reason]. [next step].
EOF
            ;;
        review)
            cat <<'EOF'
You use caveman-review mode: one-line review comments only for documents, code, thesis, reports. Format: L<line>: <severity> <problem>. <fix>. Severity prefixes: 🔴bug (critical error, must fix before submission), 🟡risk (works but fragile, potential issue), 🔵nit (style preference, optional), ❓q (genuine question, needs clarification). Drop: throat-clearers ("I noticed"), suggestions framing ("you might consider"), hedging ("perhaps/maybe"), praise in comments, restating what line does. Preserve: exact line numbers, symbol/function names in backticks, concrete specific fixes, the why if not obvious. Examples: "L42: 🔴 bug: citation missing for claim. Add [Author et al., [YEAR]]." "L88-95: 🟡 risk: section transition abrupt. Add bridging sentence."
EOF
            ;;
        *)
            echo "Error: Unknown mode '$mode'. Use: lite, full, ultra, review" >&2
            exit 1
            ;;
    esac
}

SYSTEM_PROMPT=$(build_system_prompt "$CAVEMAN_MODE")

# Detect available Qwen interface and execute
execute_qwen() {
    # Try DashScope API (requires DASHSCOPE_API_KEY)
    if [[ -n "${DASHSCOPE_API_KEY:-}" ]]; then
        echo "# Using DashScope API (Qwen)" >&2
        
        # Escape quotes in prompts for JSON
        local escaped_system=$(echo "$SYSTEM_PROMPT" | sed 's/"/\\"/g')
        local escaped_prompt=$(echo "$USER_PROMPT" | sed 's/"/\\"/g')
        
        response=$(curl -s https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -d "{
                \"model\": \"qwen-plus\",
                \"max_tokens\": 1024,
                \"messages\": [
                    {\"role\": \"system\", \"content\": \"$escaped_system\"},
                    {\"role\": \"user\", \"content\": \"$escaped_prompt\"}
                ]
            }")
        
        # Extract content using jq or grep/sed fallback
        if command -v jq &> /dev/null; then
            echo "$response" | jq -r '.choices[0].message.content'
        else
            echo "$response" | grep -o '"content":"[^"]*"' | head -1 | sed 's/"content":"//;s/"$//'
        fi
        return 0
    fi
    
    # Try Open WebUI local endpoint (requires OPEN_WEBUI_URL)
    if [[ -n "${OPEN_WEBUI_URL:-}" ]]; then
        echo "# Using Open WebUI" >&2
        
        local escaped_system=$(echo "$SYSTEM_PROMPT" | sed 's/"/\\"/g')
        local escaped_prompt=$(echo "$USER_PROMPT" | sed 's/"/\\"/g')
        
        response=$(curl -s "${OPEN_WEBUI_URL}/api/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${OPEN_WEBUI_API_KEY:-}" \
            -d "{
                \"model\": \"qwen:latest\",
                \"max_tokens\": 1024,
                \"messages\": [
                    {\"role\": \"system\", \"content\": \"$escaped_system\"},
                    {\"role\": \"user\", \"content\": \"$escaped_prompt\"}
                ]
            }")
        
        if command -v jq &> /dev/null; then
            echo "$response" | jq -r '.choices[0].message.content'
        else
            echo "$response" | grep -o '"content":"[^"]*"' | head -1 | sed 's/"content":"//;s/"$//'
        fi
        return 0
    fi
    
    # Try local ollama instance
    if command -v ollama &> /dev/null; then
        echo "# Using Ollama (local Qwen)" >&2
        
        # Create temporary file with full prompt
        local temp_prompt=$(mktemp)
        cat > "$temp_prompt" <<EOF
System: $SYSTEM_PROMPT

User: $USER_PROMPT

Assistant:
EOF
        
        ollama run qwen:latest "$(cat "$temp_prompt")"
        rm -f "$temp_prompt"
        return 0
    fi
    
    echo "Error: No Qwen interface found." >&2
    echo "" >&2
    echo "Options:" >&2
    echo "  1. Set DASHSCOPE_API_KEY for official Qwen API" >&2
    echo "     Export: export DASHSCOPE_API_KEY='your-key'" >&2
    echo "" >&2
    echo "  2. Set OPEN_WEBUI_URL for self-hosted Open WebUI" >&2
    echo "     Export: export OPEN_WEBUI_URL='http://localhost:11434'" >&2
    echo "" >&2
    echo "  3. Install Ollama for local Qwen model" >&2
    echo "     Install: curl -fsSL https://ollama.ai/install.sh | bash" >&2
    echo "     Pull model: ollama pull qwen:latest" >&2
    exit 1
}

execute_qwen

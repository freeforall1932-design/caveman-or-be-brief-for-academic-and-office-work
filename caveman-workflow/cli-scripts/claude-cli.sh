#!/usr/bin/env bash
# Caveman CLI for Claude (Claude Code, OpenHands, Aider)
# Usage: ./claude-caveman.sh [lite|full|ultra|review] "your prompt here"

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
You use caveman lite mode: professional but tight. Keep articles (a/an/the), drop filler words only. Full sentences maintained. Best for external emails, client communications, formal reports. Remove: just, really, basically, actually, simply. Preserve: technical terms, code, citations, URLs, user's language. Never invent abbreviations or use arrows.
EOF
            ;;
        full)
            cat <<'EOF'
You use caveman full mode: drop articles, fragments OK, short synonyms. Default for thesis drafting, research notes, internal documents. Remove: a/an/the, just/really/basically/actually, pleasantries, hedging. Preserve: technical terms, code, citations, URLs, user's language. Never invent abbreviations (cfg/impl/req) or use arrows (→). Review format: L<line>: 🔴bug:/🟡risk:/🔵nit:/❓q <problem>. <fix>. Auto-clarity: normal mode for security, legal, irreversible actions.
EOF
            ;;
        ultra)
            cat <<'EOF'
You use caveman ultra mode: maximum compression. Strip conjunctions when unambiguous, one word when sufficient. For summaries, quick updates, token-limited contexts. Remove: articles, filler, conjunctions, redundant words. Preserve: technical terms, code, citations, numbers, user's language. Never invent abbreviations or compress code. State each fact once.
EOF
            ;;
        review)
            cat <<'EOF'
You use caveman-review mode: one-line review comments only. Format: L<line>: <severity> <problem>. <fix>. Severity: 🔴bug (critical, must fix), 🟡risk (works but fragile), 🔵nit (style preference, optional), ❓q (genuine question). Drop: throat-clearers, hedging, praise in comments, restating code. Preserve: exact line numbers, symbol names in backticks, concrete fixes. Example: "L42: 🔴 bug: citation missing. Add [Author et al., [YEAR]]."
EOF
            ;;
        *)
            echo "Error: Unknown mode '$mode'. Use: lite, full, ultra, review" >&2
            exit 1
            ;;
    esac
}

SYSTEM_PROMPT=$(build_system_prompt "$CAVEMAN_MODE")

# Detect available Claude interface and execute
execute_claude() {
    # Try Claude Code CLI first
    if command -v claude &> /dev/null; then
        echo "# Using Claude Code CLI" >&2
        claude --system-prompt "$SYSTEM_PROMPT" "$USER_PROMPT"
        return 0
    fi
    
    # Try with curl to Anthropic API (requires ANTHROPIC_API_KEY)
    if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
        echo "# Using Anthropic API" >&2
        curl -s https://api.anthropic.com/v1/messages \
            -H "Content-Type: application/json" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: [YEAR]-06-01" \
            -d "{
                \"model\": \"claude-sonnet-4-20250514\",
                \"max_tokens\": 1024,
                \"system\": \"$SYSTEM_PROMPT\",
                \"messages\": [{\"role\": \"user\", \"content\": \"$USER_PROMPT\"}]
            }" | jq -r '.content[0].text'
        return 0
    fi
    
    echo "Error: No Claude interface found." >&2
    echo "Install Claude Code: npm install -g @anthropic-ai/claude-code" >&2
    echo "Or set ANTHROPIC_API_KEY environment variable" >&2
    exit 1
}

execute_claude

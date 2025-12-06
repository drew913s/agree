#!/bin/bash
# Domain-specific Autonomous Build Loop for Agree
# Usage: ./domain-loop.sh <domain-id>
# Example: ./domain-loop.sh Q-14

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOMAIN_ID="${1:-}"

if [ -z "$DOMAIN_ID" ]; then
    echo "Usage: $0 <domain-id>"
    echo "Example: $0 Q-14"
    exit 1
fi

# Normalize domain ID (uppercase)
DOMAIN_ID=$(echo "$DOMAIN_ID" | tr '[:lower:]' '[:upper:]')

# Map domain ID to domain name
declare -A DOMAIN_MAP=(
    ["Q-14"]="security"
    ["Q-10"]="storage"
    ["Q-08"]="auth"
    ["Q-07"]="audit"
    ["Q-01"]="documents"
    ["Q-02"]="fields"
    ["Q-03"]="signing"
    ["Q-04"]="workflow"
    ["Q-05"]="parties"
    ["Q-06"]="notifications"
    ["Q-09"]="api"
    ["Q-12"]="templates"
    ["Q-13"]="automations"
)

DOMAIN_NAME="${DOMAIN_MAP[$DOMAIN_ID]}"
if [ -z "$DOMAIN_NAME" ]; then
    echo "Error: Unknown domain ID: $DOMAIN_ID"
    exit 1
fi

# File paths
SPEC_FILE="$SCRIPT_DIR/specs/${DOMAIN_ID}-${DOMAIN_NAME^^}.md"
PROGRESS_FILE="$SCRIPT_DIR/progress/${DOMAIN_ID}-PROGRESS.md"
LOG_FILE="$SCRIPT_DIR/progress/${DOMAIN_ID}.log"
PID_FILE="$SCRIPT_DIR/progress/${DOMAIN_ID}.pid"

# Telegram communication (shared with other domains)
TELEGRAM_DIR="/tmp/claude-autonomous"
INBOX_FILE="$TELEGRAM_DIR/inbox-agree-${DOMAIN_ID}.txt"
OUTBOX_FILE="$TELEGRAM_DIR/outbox-agree.txt"
mkdir -p "$TELEGRAM_DIR"

# Tracking
SESSION_COUNT=0
LAST_COMMIT_TIME=$(date +%s)
MAX_STUCK_TIME=1800  # 30 minutes

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [$DOMAIN_ID] $1"
    echo "$msg" | tee -a "$LOG_FILE"
}

send_telegram() {
    echo "[$DOMAIN_ID] $1" >> "$OUTBOX_FILE"
}

check_inbox() {
    if [ -f "$INBOX_FILE" ]; then
        local msg=$(tail -1 "$INBOX_FILE" | cut -d'|' -f2-)
        rm -f "$INBOX_FILE"
        echo "$msg"
    fi
}

count_completed_bricks() {
    if [ -f "$PROGRESS_FILE" ]; then
        grep -c "^\- \[x\]" "$PROGRESS_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

total_bricks() {
    if [ -f "$PROGRESS_FILE" ]; then
        grep -c "^\- \[" "$PROGRESS_FILE" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

check_for_blockers() {
    # Check PROGRESS.md for blockers section
    if [ -f "$PROGRESS_FILE" ]; then
        local blockers=$(grep -A 10 "## Blockers" "$PROGRESS_FILE" | \
            grep -v "^##" | \
            grep -v "^---" | \
            grep -v "^|" | \
            grep -v "^\s*$" | \
            grep -vi "^none$" | \
            grep -v "^\[Anything Claude is stuck on" | \
            grep -v "^\[Write any blockers" | \
            grep -v "^No blockers" | \
            grep -v "^(Bricks move here" | \
            grep -v "^(none)" | \
            grep -vi "^n/a$" | \
            head -5)

        # Only return if there's actual content (not just whitespace)
        if [ -n "$blockers" ] && [ -n "$(echo "$blockers" | tr -d '[:space:]')" ]; then
            echo "$blockers"
        fi
    fi
}

is_domain_complete() {
    if [ -f "$PROGRESS_FILE" ]; then
        grep -q "Status:.*COMPLETE" "$PROGRESS_FILE" && return 0
    fi
    return 1
}

run_claude() {
    log "Starting Claude session #$SESSION_COUNT for $DOMAIN_NAME domain"

    local prompt="You are Princess $DOMAIN_ID building bricks for the $DOMAIN_NAME domain.

READ these files first:
1. autonomous/specs/${DOMAIN_ID}-${DOMAIN_NAME^^}.md - Your brick specifications
2. autonomous/progress/${DOMAIN_ID}-PROGRESS.md - What's done, what's remaining

BRICK RULES:
- Maximum 50 lines of code per brick (excluding comments/blanks)
- Return format: {'result': X, 'error': str|None}
- Create {name}.py + {name}.meta.json + test_{name}.py for each brick
- Location: bricks/${DOMAIN_NAME}/

WORKFLOW:
1. Update PROGRESS.md 'Current Brick' with what you're starting
2. Build the next incomplete brick from the checklist
3. Run: python3 colony.py complete ${DOMAIN_NAME}/{brick_name} after each brick
4. Commit after each completed brick
5. If stuck, write your question in PROGRESS.md under 'Blockers'
6. Continue until all bricks are complete
7. When done, change Status to COMPLETE

IMPORTANT:
- Follow patterns in existing bricks if any
- Make small, frequent commits
- Update PROGRESS.md continuously"

    local user_input=$(check_inbox)
    if [ -n "$user_input" ]; then
        if [ "$user_input" = "__STOP__" ]; then
            log "Stop command received"
            return 2
        elif [ "$user_input" = "__SKIP__" ]; then
            prompt="$prompt

USER SAYS: Skip the current blocker and move to the next brick."
        else
            prompt="$prompt

USER RESPONSE: $user_input"
        fi
    fi

    cd "$PROJECT_DIR"

    claude \
        --dangerously-skip-permissions \
        --max-turns 50 \
        -p "$prompt" \
        2>&1 | tee -a "$LOG_FILE"

    return $?
}

initialize_progress() {
    if [ ! -f "$PROGRESS_FILE" ]; then
        log "Creating progress file from spec..."
        cat > "$PROGRESS_FILE" << EOF
# $DOMAIN_ID Progress: ${DOMAIN_NAME^} Domain

## Status: IN PROGRESS

## Current Brick
Starting...

---

## Completed
(Bricks move here when done - include commit hash)

---

## Remaining

EOF
        # Extract bricks from spec file and add to progress
        if [ -f "$SPEC_FILE" ]; then
            grep "^### [0-9]" "$SPEC_FILE" | while read -r line; do
                brick_name=$(echo "$line" | sed 's/### [0-9]*\. //' | sed 's/\.py//')
                echo "- [ ] $brick_name" >> "$PROGRESS_FILE"
            done
        fi

        cat >> "$PROGRESS_FILE" << EOF

---

## Blockers

---

## Session Log

| Session | Started | Commits | Notes |
|---------|---------|---------|-------|
EOF
    fi
}

main() {
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "Error: Domain $DOMAIN_ID is already running (PID: $OLD_PID)"
            exit 1
        fi
    fi

    # Save PID
    echo $$ > "$PID_FILE"
    trap "rm -f $PID_FILE" EXIT

    log "=========================================="
    log "Domain Loop Started"
    log "Domain: $DOMAIN_ID ($DOMAIN_NAME)"
    log "Project: $PROJECT_DIR"
    log "=========================================="

    # Verify spec file exists
    if [ ! -f "$SPEC_FILE" ]; then
        log "ERROR: Spec file not found: $SPEC_FILE"
        send_telegram "Error: Spec file not found for $DOMAIN_NAME"
        exit 1
    fi

    # Initialize progress file
    initialize_progress

    # Start Telegram bot if configured
    if [ -f "$HOME/.claude/.env" ]; then
        log "Starting shared Telegram bot..."
        python3 "$HOME/.claude/autonomous/telegram/bot.py" "agree" &
        BOT_PID=$!
        trap "kill $BOT_PID 2>/dev/null; rm -f $PID_FILE" EXIT
        sleep 2
    fi

    send_telegram "Starting autonomous build for $DOMAIN_NAME domain"

    # Main loop
    while true; do
        SESSION_COUNT=$((SESSION_COUNT + 1))

        # Check if domain is complete
        if is_domain_complete; then
            COMPLETED=$(count_completed_bricks)
            TOTAL=$(total_bricks)
            log "DOMAIN COMPLETE! $COMPLETED/$TOTAL bricks"
            send_telegram "COMPLETE ($COMPLETED/$TOTAL bricks)"

            # Update colony.py
            python3 "$PROJECT_DIR/colony.py" assign "$DOMAIN_ID" "COMPLETE" 2>/dev/null || true
            break
        fi

        # Check for blockers
        local blockers=$(check_for_blockers)
        if [ -n "$blockers" ]; then
            log "Blocker detected: $blockers"
            send_telegram "QUESTION: $blockers"

            log "Waiting for user response..."
            while true; do
                sleep 5
                local response=$(check_inbox)
                if [ -n "$response" ]; then
                    log "Received response: $response"
                    break
                fi
            done
        fi

        # Run Claude
        run_claude
        EXIT_CODE=$?

        if [ $EXIT_CODE -eq 2 ]; then
            log "Build stopped by user"
            send_telegram "Stopped by user command"
            break
        fi

        # Check for stuck state
        CURRENT_TIME=$(date +%s)
        TIME_SINCE_COMMIT=$((CURRENT_TIME - LAST_COMMIT_TIME))

        if [ $TIME_SINCE_COMMIT -gt $MAX_STUCK_TIME ]; then
            log "WARNING: No progress in ${MAX_STUCK_TIME}s"
            send_telegram "Possibly stuck - no commits in 30 min. Reply /skip to continue"
            LAST_COMMIT_TIME=$(date +%s)
        fi

        log "Session complete. Restarting in 5 seconds..."
        sleep 5
    done

    log "Domain loop ended."
}

main "$@"

#!/bin/bash
# ============================================================================
# health_check.sh — Automated health check runner (non-interactive)
# ============================================================================
#
# PURPOSE:
# Instead of manually opening OpsWatch and typing URLs one by one, this
# script runs health checks AUTOMATICALLY against a list of URLs and
# services.  This is useful for:
#   - Scheduled checks (cron jobs or systemd timers)
#   - Quick "is everything up?" verification
#   - Scripted monitoring without human interaction
#
# USAGE:
#   chmod +x health_check.sh
#   ./health_check.sh
#
# You can also schedule it to run every 5 minutes (explained in the guide).
# ============================================================================

# --- Configuration ----------------------------------------------------------

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="python3"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
# ^ "date" is a Linux command that prints the current date/time.
#   The '+%Y-%m-%d %H:%M:%S' part is a format string:
#     %Y = year, %m = month, %d = day, %H = hour, %M = minute, %S = second

# --- URLs to check ---------------------------------------------------------
# This is a Bash ARRAY — a list of values.
# Arrays use parentheses and spaces (not commas) between items.

URLS=(
    "https://google.com"
    "https://github.com"
    "https://cloudflare.com"
)
# ^ Add or remove URLs here. These are the sites that will be checked
#   every time this script runs.

# --- Services to check (Linux services) ------------------------------------

SERVICES=(
    "sshd"
    "cron"
)
# ^ Add service names relevant to your system.
#   Common ones: sshd (SSH), nginx (web server), docker, cron (scheduler)

# --- Main -------------------------------------------------------------------

echo "[$TIMESTAMP] 🔄 Running automated health checks..."
echo "---------------------------------------------------"

# "for url in ${URLS[@]}" loops through every item in the URLS array.
# The [@] means "all elements". The quotes preserve items with spaces.

echo ""
echo "🌐 URL Checks:"
for url in "${URLS[@]}"; do
    # We use Python directly with the -c flag to run a one-line command.
    # This imports our checker module and calls check_url() for each URL.
    cd "$PROJECT_DIR"
    $PYTHON -c "from checker import check_url; check_url('$url')"
done

echo ""
echo "🔍 Service Checks:"
for service in "${SERVICES[@]}"; do
    cd "$PROJECT_DIR"
    $PYTHON -c "from checker import check_service; check_service('$service')"
done

echo ""
echo "[$TIMESTAMP] ✅ Automated health checks complete."
echo "📋 Results logged to: $PROJECT_DIR/logs/opswatch.log"


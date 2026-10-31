#!/bin/bash
# ============================================================================
# run_opswatch.sh — Simple launcher script for OpsWatch
# ============================================================================
#
# WHAT IS A BASH SCRIPT?
# A Bash script is a text file containing commands that the Linux shell
# executes one by one, top to bottom — like a recipe for the computer.
#
# The first line (#!/bin/bash) is called a "shebang". It tells Linux
# which program should interpret this file. Without it, Linux wouldn't
# know this is a Bash script.
#
# HOW TO USE:
#   chmod +x run_opswatch.sh    (make it executable — one time only)
#   ./run_opswatch.sh           (run it)
# ============================================================================

# --- Variables --------------------------------------------------------------
# Variables in Bash don't use keywords like "let" or "var".
# IMPORTANT: No spaces around the = sign!  PROJECT_DIR = "..." would FAIL.

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
# ^ This finds the folder where THIS script lives, no matter where you
#   call it from.  It works in two steps:
#   1. dirname "$0"  → gets the directory part of the script's path
#   2. cd ... && pwd → enters that directory and prints its full path

PYTHON="python3"
# ^ The command to run Python. On most Linux systems, "python3" is correct.
#   On some systems you might need just "python".

LOG_FILE="$PROJECT_DIR/logs/opswatch.log"
# ^ Where OpsWatch saves its health-check logs.

# --- Helper Functions -------------------------------------------------------
# Functions in Bash are defined with function_name() { ... }
# They group commands together so you can reuse them.

print_header() {
    echo ""
    echo "=========================================="
    echo "  🛠  OpsWatch Launcher"
    echo "=========================================="
    echo ""
}

check_python() {
    # "command -v" checks if a program exists on this system.
    # The "if ! ..." means "if this command FAILS" (the ! flips true/false).
    if ! command -v "$PYTHON" &> /dev/null; then
        echo "❌ Python3 is not installed."
        echo "   Install it with:  sudo apt update && sudo apt install python3 python3-pip"
        exit 1
        # "exit 1" stops the script immediately. The number 1 means "error".
        # exit 0 would mean "success". This is called an "exit code".
    fi
    echo "✅ Python3 found: $($PYTHON --version)"
}

check_dependencies() {
    echo "📦 Checking Python dependencies..."

    # pip install -r ... installs packages listed in requirements.txt.
    # The --quiet flag hides the noisy output.
    $PYTHON -m pip install --quiet -r "$PROJECT_DIR/requirements.txt"

    # $? is a special variable that holds the exit code of the LAST command.
    # 0 = success, anything else = failure.
    if [ $? -eq 0 ]; then
        echo "✅ All dependencies installed."
    else
        echo "⚠  Some dependencies may have failed to install."
    fi
}

# --- Main Execution ---------------------------------------------------------
# Everything below runs in order when the script starts.

print_header
check_python
check_dependencies

echo ""
echo "🚀 Starting OpsWatch..."
echo "   Log file: $LOG_FILE"
echo ""

# "cd" changes into the project directory before running main.py.
# This ensures Python can find all the module files (checker.py, etc.)
cd "$PROJECT_DIR"

# Finally, run the actual application.
$PYTHON main.py


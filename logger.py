"""
logger.py — Health-check result logging

This module is responsible for saving health-check results to local log files.
Every check (service or URL) produces a timestamped entry that is appended to
a log file inside the `logs/` directory.

Key concepts demonstrated:
- File I/O with `open()` in append mode
- os.path for portable path handling
- datetime formatting
- Ensuring directories exist with os.makedirs
"""

import os
from datetime import datetime


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Directory where log files are stored, relative to the project root.
# os.path.dirname(__file__) gives us the folder where THIS script lives,
# so logs/ will always be created next to main.py regardless of where
# the user runs the command from.
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

# Name of the log file that stores all health-check results.
LOG_FILE = os.path.join(LOG_DIR, "opswatch.log")


# ---------------------------------------------------------------------------
# Helper — ensure the logs directory exists
# ---------------------------------------------------------------------------

def _ensure_log_dir():
    """
    Create the logs/ directory if it does not already exist.

    os.makedirs with exist_ok=True is safe to call repeatedly — it will
    not raise an error if the directory is already present.
    """
    os.makedirs(LOG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def log_result(check_type: str, target: str, result: str, details: str = ""):
    """
    Append a single health-check result to the log file.

    Parameters
    ----------
    check_type : str
        The kind of check that was performed, e.g. "SERVICE" or "URL".
    target : str
        What was checked — a service name, URL, etc.
    result : str
        The outcome, e.g. "OK", "FAIL", "ERROR".
    details : str, optional
        Any extra information (status code, response time, error message).

    Each log line follows this format:
        [YYYY-MM-DD HH:MM:SS] [CHECK_TYPE] target — result | details

    Example:
        [2026-10-29 21:15:00] [URL] https://google.com — OK | 200, 0.23s
    """
    _ensure_log_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build the log entry
    entry = f"[{timestamp}] [{check_type}] {target} — {result}"
    if details:
        entry += f" | {details}"

    # Append to the log file.  mode="a" opens the file for *appending*,
    # which means new content is added to the end without erasing what is
    # already there.  The file is created automatically if it doesn't exist.
    try:
        with open(LOG_FILE, mode="a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except OSError as e:
        # If we can't write to the log, print a warning but don't crash
        # the whole application — the user still gets the on-screen output.
        print(f"  ⚠  Could not write to log file: {e}")


def read_logs(lines: int = 20) -> str:
    """
    Read and return the last *lines* entries from the log file.

    Parameters
    ----------
    lines : int
        Number of most-recent lines to return (default 20).

    Returns
    -------
    str
        The log content, or a message indicating the log is empty / missing.
    """
    if not os.path.exists(LOG_FILE):
        return "No log file found. Run some checks first!"

    try:
        with open(LOG_FILE, mode="r", encoding="utf-8") as f:
            all_lines = f.readlines()
    except OSError as e:
        return f"Could not read log file: {e}"

    if not all_lines:
        return "Log file is empty."

    # Return only the last N lines so the output stays manageable.
    tail = all_lines[-lines:]
    return "".join(tail)


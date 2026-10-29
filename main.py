"""
main.py — OpsWatch application entry point and CLI menu

This is the file you run to start OpsWatch:

    python main.py

It presents an interactive menu that loops until the user chooses to exit.
Each menu option delegates to the appropriate module:

    checker.py     → service checks, URL health checks
    system_info.py → system information display
    logger.py      → reading back saved logs

Key concepts demonstrated:
- Program entry point with `if __name__ == "__main__"`
- Infinite loop with `while True` for a menu-driven CLI
- Input validation and error handling
- Clean separation of concerns (each module has one job)
"""

from checker import check_service, check_url
from system_info import display_system_info
from logger import read_logs


# ---------------------------------------------------------------------------
# Menu Display
# ---------------------------------------------------------------------------

def show_menu():
    """
    Print the main menu to the terminal.

    This is a simple function with no logic — it just prints text.
    Separating it makes it easy to update the menu in one place.
    """
    print("\n" + "=" * 50)
    print("            🛠  OpsWatch — Health Monitor")
    print("=" * 50)
    print("  1. Check Service Status")
    print("  2. Check URL Health")
    print("  3. View System Information")
    print("  4. View Recent Logs")
    print("  5. Exit")
    print("=" * 50)


# ---------------------------------------------------------------------------
# Menu Handlers
# ---------------------------------------------------------------------------
# Each handler prompts the user for input (if needed) and calls the
# appropriate function from the other modules.  Keeping this logic in
# separate small functions makes main() clean and readable.


def handle_service_check():
    """Prompt for a service name and run the check."""
    service = input("  Enter service name (e.g. sshd, nginx, wuauserv): ").strip()

    if not service:
        print("  ⚠  No service name entered.")
        return

    check_service(service)


def handle_url_check():
    """Prompt for a URL and run the health check."""
    url = input("  Enter URL (e.g. https://google.com): ").strip()

    if not url:
        print("  ⚠  No URL entered.")
        return

    check_url(url)


def handle_view_logs():
    """Display the most recent log entries."""
    print("\n" + "=" * 50)
    print("        📋  Recent Health-Check Logs")
    print("=" * 50)
    print(read_logs(lines=20))
    print("=" * 50)


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------

def main():
    """
    The main application loop.

    How it works:
    1. Display the menu.
    2. Read the user's choice.
    3. Call the appropriate handler.
    4. Repeat until the user selects "Exit".

    The `while True` creates an infinite loop.  The only way out is the
    `break` statement inside the "Exit" branch, or pressing Ctrl+C.
    """
    print("\n🚀 Welcome to OpsWatch!")
    print("   Your system health monitoring companion.\n")

    while True:
        show_menu()

        choice = input("  Choose an option [1-5]: ").strip()

        if choice == "1":
            handle_service_check()

        elif choice == "2":
            handle_url_check()

        elif choice == "3":
            display_system_info()

        elif choice == "4":
            handle_view_logs()

        elif choice == "5":
            print("\n👋 Goodbye! Stay operational.\n")
            break   # ← exits the while True loop

        else:
            # The user typed something we don't recognise.
            print("  ⚠  Invalid option. Please enter a number from 1 to 5.")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
# This block runs ONLY when you execute this file directly:
#     python main.py           ← __name__ is "__main__"
#
# It does NOT run when another file imports from this module:
#     from main import main    ← __name__ is "main"

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully instead of showing an ugly traceback.
        print("\n\n👋 OpsWatch interrupted. Goodbye!\n")


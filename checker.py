"""
checker.py — Service and URL health-check logic

This module contains two main capabilities:

1. **Service check**  — Verifies whether a local system service is running.
   On Linux this queries systemd via `systemctl`.  On Windows it uses
   `sc query`.  On macOS it falls back to `launchctl`.

2. **URL health check** — Sends an HTTP GET request to a URL and reports
   the status code and response time.

Key concepts demonstrated:
- subprocess for running shell commands safely
- requests for HTTP calls
- Measuring elapsed time
- Platform detection for cross-OS support
- Error handling with try/except
"""

import platform
import subprocess
import time

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from logger import log_result


# ---------------------------------------------------------------------------
# 1. Service Check
# ---------------------------------------------------------------------------

def check_service(service_name: str):
    """
    Check whether a system service is currently running.

    Parameters
    ----------
    service_name : str
        The name of the service to check (e.g. "sshd", "nginx", "wuauserv").

    How it works
    ------------
    - Linux   → runs `systemctl is-active <service>`
    - Windows → runs `sc query <service>` and looks for "RUNNING"
    - macOS   → runs `launchctl list` and greps for the service name

    The function prints its findings and logs the result.
    """
    current_os = platform.system()

    print(f"\n🔍 Checking service: {service_name}")
    print("-" * 40)

    try:
        if current_os == "Linux":
            # systemctl is-active returns a single word: "active", "inactive",
            # "failed", etc.  capture_output grabs stdout so we can read it.
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,      # capture stdout and stderr
                text=True,                # decode bytes → str automatically
                timeout=10,               # don't hang forever
            )
            status = result.stdout.strip()

            if status == "active":
                print(f"  ✅ Service '{service_name}' is RUNNING.")
                log_result("SERVICE", service_name, "OK", "active")
            else:
                print(f"  ❌ Service '{service_name}' is NOT running (status: {status}).")
                log_result("SERVICE", service_name, "FAIL", status)

        elif current_os == "Windows":
            # `sc query` returns multi-line output.  We look for the word
            # "RUNNING" anywhere in that output.
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout

            if "RUNNING" in output:
                print(f"  ✅ Service '{service_name}' is RUNNING.")
                log_result("SERVICE", service_name, "OK", "RUNNING")
            elif "STOPPED" in output:
                print(f"  ⏸  Service '{service_name}' is STOPPED.")
                log_result("SERVICE", service_name, "FAIL", "STOPPED")
            elif result.returncode != 0:
                print(f"  ⚠  Service '{service_name}' was not found.")
                log_result("SERVICE", service_name, "ERROR", "not found")
            else:
                # Extract the STATE line for more detail
                print(f"  ❌ Service '{service_name}' is NOT running.")
                log_result("SERVICE", service_name, "FAIL", output.strip()[:80])

        elif current_os == "Darwin":  # macOS
            result = subprocess.run(
                ["launchctl", "list"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if service_name in result.stdout:
                print(f"  ✅ Service '{service_name}' is LOADED.")
                log_result("SERVICE", service_name, "OK", "loaded")
            else:
                print(f"  ❌ Service '{service_name}' not found in launchctl.")
                log_result("SERVICE", service_name, "FAIL", "not found")

        else:
            print(f"  ⚠  Unsupported operating system: {current_os}")
            log_result("SERVICE", service_name, "ERROR", f"unsupported OS: {current_os}")

    except FileNotFoundError:
        # The command itself (systemctl / sc / launchctl) was not found
        print(f"  ⚠  Service check command not available on this system.")
        log_result("SERVICE", service_name, "ERROR", "command not found")
    except subprocess.TimeoutExpired:
        print(f"  ⚠  Service check timed out.")
        log_result("SERVICE", service_name, "ERROR", "timeout")
    except Exception as e:
        print(f"  ⚠  Unexpected error: {e}")
        log_result("SERVICE", service_name, "ERROR", str(e))


# ---------------------------------------------------------------------------
# 2. URL Health Check
# ---------------------------------------------------------------------------

def check_url(url: str):
    """
    Check the reachability of a URL by sending an HTTP GET request.

    Parameters
    ----------
    url : str
        The URL to check (e.g. "https://google.com").

    What it reports
    ---------------
    - HTTP status code (200 = OK, 404 = Not Found, etc.)
    - Response time in seconds
    - Whether the request succeeded or failed

    The function also logs the result via logger.log_result().
    """
    if not REQUESTS_AVAILABLE:
        print("\n  ⚠  The 'requests' library is not installed.")
        print("     Run: pip install requests")
        log_result("URL", url, "ERROR", "requests library not installed")
        return

    # Prepend https:// if the user didn't include a scheme.
    # This is a small quality-of-life improvement so the user can type
    # "google.com" instead of "https://google.com".
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"\n🌐 Checking URL: {url}")
    print("-" * 40)

    try:
        # time.time() gives us a float of seconds since the Unix epoch.
        # By recording the time before and after the request we can
        # measure the response time.
        start_time = time.time()

        response = requests.get(
            url,
            timeout=10,            # seconds to wait for a response
            allow_redirects=True,   # follow 301/302 redirects
        )

        elapsed = time.time() - start_time

        status_code = response.status_code

        # HTTP status codes in the 200–299 range are considered successful.
        if 200 <= status_code < 300:
            print(f"  ✅ Status: {status_code} OK")
        elif 300 <= status_code < 400:
            print(f"  🔀 Status: {status_code} (Redirect)")
        elif 400 <= status_code < 500:
            print(f"  ⚠  Status: {status_code} (Client Error)")
        else:
            print(f"  ❌ Status: {status_code} (Server Error)")

        print(f"  ⏱  Response time: {elapsed:.3f}s")

        # Determine result string for logging
        result = "OK" if 200 <= status_code < 300 else "FAIL"
        log_result("URL", url, result, f"{status_code}, {elapsed:.3f}s")

    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection error — could not reach {url}")
        log_result("URL", url, "FAIL", "connection error")

    except requests.exceptions.Timeout:
        print(f"  ❌ Request timed out after 10 seconds.")
        log_result("URL", url, "FAIL", "timeout")

    except requests.exceptions.MissingSchema:
        print(f"  ⚠  Invalid URL format. Include http:// or https://")
        log_result("URL", url, "ERROR", "invalid URL format")

    except requests.exceptions.RequestException as e:
        # Catch-all for any other requests error
        print(f"  ❌ Request failed: {e}")
        log_result("URL", url, "FAIL", str(e))


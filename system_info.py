"""
system_info.py — Basic system information collection

This module gathers information about the machine OpsWatch is running on.
It uses two standard-library modules plus one third-party package:

- platform  (stdlib)  — OS name, version, architecture, Python version
- socket    (stdlib)  — hostname
- psutil    (PyPI)    — CPU count, CPU usage %, memory usage, disk usage

Key concepts demonstrated:
- Using the standard library for system introspection
- Working with a third-party package (psutil)
- Formatting bytes into human-readable units
- Returning structured data from a function
"""

import platform
import socket

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


# ---------------------------------------------------------------------------
# Helper — human-readable byte sizes
# ---------------------------------------------------------------------------

def _bytes_to_human(num_bytes: float) -> str:
    """
    Convert a byte count into a human-readable string (KB, MB, GB, …).

    The function divides by 1024 repeatedly until the value is below 1024
    or we run out of unit labels.

    Examples:
        _bytes_to_human(1024)       → "1.00 KB"
        _bytes_to_human(1073741824) → "1.00 GB"
    """
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} PB"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_system_info() -> dict:
    """
    Collect and return basic system information as a dictionary.

    Returns
    -------
    dict
        Keys include:
        - hostname, os, os_version, architecture, python_version
        - cpu_count, cpu_usage_percent          (if psutil is available)
        - total_memory, used_memory, memory_percent  (if psutil is available)
        - total_disk, used_disk, disk_percent        (if psutil is available)
    """
    info = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }

    if PSUTIL_AVAILABLE:
        # CPU -----------------------------------------------------------
        info["cpu_count"] = psutil.cpu_count(logical=True)
        info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)

        # Memory --------------------------------------------------------
        mem = psutil.virtual_memory()
        info["total_memory"] = _bytes_to_human(mem.total)
        info["used_memory"] = _bytes_to_human(mem.used)
        info["memory_percent"] = mem.percent

        # Disk (root partition) -----------------------------------------
        disk = psutil.disk_usage("/") if platform.system() != "Windows" else psutil.disk_usage("C:\\")
        info["total_disk"] = _bytes_to_human(disk.total)
        info["used_disk"] = _bytes_to_human(disk.used)
        info["disk_percent"] = disk.percent
    else:
        info["note"] = "Install psutil for CPU, memory, and disk details."

    return info


def display_system_info():
    """
    Print the collected system information in a formatted, readable way.

    This is a convenience wrapper that calls get_system_info() and then
    iterates over the dictionary to print each key-value pair.
    """
    info = get_system_info()

    print("\n" + "=" * 50)
    print("        📊  System Information")
    print("=" * 50)

    # Labels for nicer display (maps raw dict keys → friendly names)
    labels = {
        "hostname":          "Hostname",
        "os":                "Operating System",
        "os_version":        "OS Version",
        "architecture":      "Architecture",
        "python_version":    "Python Version",
        "cpu_count":         "CPU Cores (logical)",
        "cpu_usage_percent": "CPU Usage",
        "total_memory":      "Total Memory",
        "used_memory":       "Used Memory",
        "memory_percent":    "Memory Usage",
        "total_disk":        "Total Disk",
        "used_disk":         "Used Disk",
        "disk_percent":      "Disk Usage",
        "note":              "Note",
    }

    for key, value in info.items():
        label = labels.get(key, key)

        # Add a '%' suffix to percentage values for clarity
        if "percent" in key and isinstance(value, (int, float)):
            value = f"{value}%"

        print(f"  {label:<22}: {value}")

    print("=" * 50)


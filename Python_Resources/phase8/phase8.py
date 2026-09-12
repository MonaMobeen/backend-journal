import sys


def is_running_in_virtual_env() -> bool:
    """
    Detects whether the current Python process is running inside a
    virtual environment. When a venv is active, sys.prefix (the venv's
    own path) differs from sys.base_prefix (the system-wide Python path).
    """
    return sys.prefix != sys.base_prefix


if is_running_in_virtual_env():
    print(f"Running INSIDE a virtual environment: {sys.prefix}")
else:
    print("Running with the SYSTEM Python (no virtual environment active).")

print(f"Python executable in use: {sys.executable}")
 
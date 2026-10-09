# -*- coding: utf-8 -*-
"""
Experiment 1 - Part 0: Check the Python environment
Prints the Python version, the interpreter path, and the version of every
library this project needs. Each line ends with OK or MISSING.

Run with the Anaconda Python (see README "Environment"):
    python code/check_env.py
Screenshot the output into screenshots/1_setup/06_check_env_output.png
"""
import importlib
import os
import sys

MIN_PYTHON = (3, 8)

# (name to show, module to import)
LIBRARIES = [
    ("numpy", "numpy"),
    ("matplotlib", "matplotlib"),
    ("tkinter", "tkinter"),
    ("Pillow", "PIL"),
]


# ---------- 1. Helpers ----------
def library_version(module_name):
    """Import a library and return its version text, or None if it is missing."""
    try:
        module = importlib.import_module(module_name)
        if module_name == "tkinter":
            # Tcl() loads the Tcl library without opening a window, so a broken
            # Tcl/Tk install is found now and not later in the GUI steps.
            module.Tcl()
            return str(module.TkVersion)
        return module.__version__
    except Exception:  # not installed, or installed but broken
        return None


def is_conda_python():
    """Anaconda (and every conda env) keeps a conda-meta folder next to python.exe."""
    return os.path.isdir(os.path.join(sys.prefix, "conda-meta"))


def status_line(label, value, ok):
    """One aligned line that ends with OK or MISSING."""
    return f"{label:<12} {value:<40} {'OK' if ok else 'MISSING'}"


# ---------- 2. Main ----------
def main():
    conda = is_conda_python()
    checks = [
        ("Python", sys.version.split()[0], sys.version_info >= MIN_PYTHON),
        ("Interpreter", sys.executable, os.path.exists(sys.executable)),
        ("Anaconda", sys.prefix if conda else "not a conda Python", conda),
    ]
    for label, module_name in LIBRARIES:
        version = library_version(module_name)
        checks.append((label, version or "not installed", version is not None))

    print("Experiment 1 - environment check")
    print("-" * 60)
    for label, value, ok in checks:
        print(status_line(label, value, ok))
    print("-" * 60)

    missing = [label for label, _, ok in checks if not ok]
    if missing:
        print("NOT READY. Missing: " + ", ".join(missing))
        return 1
    print("All OK. The environment is ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

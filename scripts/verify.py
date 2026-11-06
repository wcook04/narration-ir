#!/usr/bin/env python3
"""The same bounded validation entry used locally and in CI."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    commands = [
        ["scripts/check_layout.py", "--root", "."],
        ["scripts/test_check_layout.py"],
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
        ["skills/narration-ir/scripts/narration_ir.py", "validate", "skills/narration-ir/examples/interview/plan.json"],
    ]
    for command in commands:
        result = subprocess.run([sys.executable, *command], cwd=ROOT)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

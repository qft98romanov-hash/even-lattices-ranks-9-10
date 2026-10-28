#!/usr/bin/env python3
"""Check the retained audit snapshot's byte identity (not mathematical truth)."""
import hashlib
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
manifest = root / "SHA256SUMS.txt"
failed = []
checked = 0
for line in manifest.read_text(encoding="utf-8").splitlines():
    if not line or line.startswith("#"):
        continue
    expected, relative = line.split("  ", 1)
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failed.append(relative + ": missing or invalid path")
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    checked += 1
    if actual != expected:
        failed.append(relative + ": SHA256 mismatch")
for failure in failed:
    print("FAIL", failure)
print("ADDON_HASH_CHECK", "FAIL" if failed else "PASS", "files", checked)
sys.exit(1 if failed else 0)

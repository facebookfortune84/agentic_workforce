"""
REALM FORGE: ROOT REPAIR & HASH VERIFICATION v1.0
-------------------------------------------------
Scans the entire project, replaces old root references with the new canonical root,
and verifies file integrity with SHA-256 before and after.

USAGE:
    python repair_paths_and_verify.py
"""

import os
import hashlib
from pathlib import Path
import json

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path("F:/agentic_workforce")

OLD_ROOTS = [
    "F:/agentic_workforce",
    "F:/agentic_workforce_PROD",
    "F:\\RealmForge",
    "F:\\RealmForge_PROD",
    "F:/agentic_workforce",
    "F:/agentic_workforce",
]

NEW_ROOT = "F:/agentic_workforce"

EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    "venv",
    "env",
    ".next",
}

TEXT_EXTENSIONS = {
    ".py", ".json", ".yaml", ".yml", ".txt", ".md",
    ".html", ".css", ".js", ".ts", ".tsx",
}

LOG_PATH = PROJECT_ROOT / "root_repair_log.jsonl"


# ============================================================
# HASHING
# ============================================================

def sha256_file(path: Path) -> str:
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha.update(block)
        return sha.hexdigest()
    except Exception:
        return "ERROR"


# ============================================================
# MAIN REPAIR LOGIC
# ============================================================

def repair_file(path: Path):
    before_hash = sha256_file(path)

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None  # skip unreadable files

    original_text = text

    for old in OLD_ROOTS:
        text = text.replace(old, NEW_ROOT)

    if text == original_text:
        return None  # no changes

    # Write updated file
    path.write_text(text, encoding="utf-8")

    after_hash = sha256_file(path)

    # Log the change
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(json.dumps({
            "file": str(path),
            "before_hash": before_hash,
            "after_hash": after_hash,
            "changed": before_hash != after_hash
        }) + "\n")

    return path


def walk_and_repair():
    changed_files = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            path = Path(root) / file

            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue

            result = repair_file(path)
            if result:
                changed_files.append(str(result))

    return changed_files


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("🔧 Starting root repair...")
    changed = walk_and_repair()
    print(f"✔ Completed. Files updated: {len(changed)}")
    print(f"📄 Log written to: {LOG_PATH}")
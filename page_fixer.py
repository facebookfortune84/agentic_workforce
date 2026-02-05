#!/usr/bin/env python3
import re
import os
import subprocess

TARGET_FILE = "F:/agentic_workforce/client/app/page.tsx"

def load_file():
    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_file(text):
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def remove_duplicate_mounted_state(text):
    pattern = r"const\s*\[\s*mounted\s*,\s*setMounted\s*\]\s*=\s*useState\(false\);"
    matches = re.findall(pattern, text)
    if len(matches) > 1:
        # keep the first, remove the rest
        first = True
        def repl(m):
            nonlocal first
            if first:
                first = False
                return m.group(0)
            return ""
        text = re.sub(pattern, repl, text)
    return text

def remove_stray_braces(text):
    # Remove isolated braces on their own line
    return re.sub(r"^\s*}\s*$", "", text, flags=re.MULTILINE)

def fix_unclosed_tags(text):
    # Very simple JSX tag balancer
    stack = []
    tag_pattern = re.compile(r"<(/?)([A-Za-z0-9_]+)[^>]*?>")
    for match in tag_pattern.finditer(text):
        closing, tag = match.groups()
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
        else:
            stack.append(tag)

    # If tags remain unclosed, append closing tags
    for tag in reversed(stack):
        text += f"\n</{tag}>"

    return text

def remove_any_types(text):
    return re.sub(r"\bany\b", "unknown", text)

def run_tsc():
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(TARGET_FILE)
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Could not run tsc: {e}"

def main():
    print("\n=== TITANFORGE AUTO-REPAIR ===\n")

    text = load_file()
    original = text

    # Apply repairs
    text = remove_duplicate_mounted_state(text)
    text = remove_stray_braces(text)
    text = fix_unclosed_tags(text)
    text = remove_any_types(text)

    # Ensure newline at EOF
    if not text.endswith("\n"):
        text += "\n"

    # Save repaired file
    save_file(text)

    print("[WRITE] ✔ Repaired file saved.")
    print("\n[TS CHECK]")
    print(run_tsc())

    print("\n=== END REPAIR ===\n")

if __name__ == "__main__":
    main()
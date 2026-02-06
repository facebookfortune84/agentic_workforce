# Save as signature_shield.py and run: python signature_shield.py
import os

print("🛡️  SIGNATURE SHIELD: Scanning for fragile function definitions...")
backend_path = "src"

for root, dirs, files in os.walk(backend_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                # If we find a tool or internal function with only 1 argument, it's a risk
                if "def " in line and "(*args, **kwargs)" not in line:
                    if "get_tools" in line or "process_step" in line:
                        print(f"⚠️  [RISK]: {path} line {i+1} is missing a signature shield.")
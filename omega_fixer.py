import os
import re
import json
import shutil
from pathlib import Path

class TitanOmegaFixer:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.stats = {"fixed": 0, "scanned": 0, "failed": []}
        # Files to ignore
        self.ignore = [".next", "node_modules", "venv", ".git", "__pycache__", ".bak"]

    def log_fault(self, file_path, reason):
        self.stats["failed"].append({"file": str(file_path), "reason": reason})

    def backup_file(self, file_path):
        shutil.copy(file_path, str(file_path) + ".bak")

    def fix_python_none_get(self, content):
        """
        Transforms unsafe lookups:
        '(res or {}).get("key")' -> '(res or {}).get("key")'
        """
        # Pattern 1: (dictionary or {}).get()
        # This regex looks for variables followed by .get but not preceded by a check
        pattern = r'(?<!or \{ \})\b([a-zA-Z_][a-zA-Z0-9_]*)\.get\('
        replacement = r'(\1 or {}).get('
        
        fixed_content = re.sub(pattern, replacement, content)
        
        # Pattern 2: response.choices[0] (Groq/OpenAI specific)
        if "choices[0]" in fixed_content and "getattr" not in fixed_content:
            fixed_content = fixed_content.replace(
                "choices[0].message.content", 
                "getattr(getattr(getattr(res, 'choices', [None])[0], 'message', None), 'content', '')"
            )
        return fixed_content

    def fix_ts_optional_chaining(self, content):
        """
        Ensures frontend lookups are safe:
        'vitals.cpu' -> 'vitals?.cpu'
        """
        # Specific target for your common frontend vitals
        targets = ["vitals", "config", "selectedNode", "activeAgent"]
        fixed = content
        for t in targets:
            fixed = re.sub(fr'\b{t}\.([a-zA-Z_])', fr'{t}?.\1', fixed)
        return fixed

    def scan_and_heal(self):
        print("🛠️  TITAN OMEGA FIXER: Initiating System-Wide Repair...")
        
        for root, dirs, files in os.walk(self.root):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore]
            
            for file in files:
                file_path = Path(root) / file
                self.stats["scanned"] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original = f.read()

                    new_content = original
                    
                    # Apply Logic Heals
                    if file.endswith(".py"):
                        new_content = self.fix_python_none_get(new_content)
                    
                    elif file.endswith((".tsx", ".ts")):
                        new_content = self.fix_ts_optional_chaining(new_content)

                    # Only write if changes were made
                    if new_content != original:
                        self.backup_file(file_path)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        self.stats["fixed"] += 1
                        print(f"✅ HEALED: {file_path.relative_to(self.root)}")

                except Exception as e:
                    self.log_fault(file_path, str(e))

    def check_infrastructure(self):
        print("\n🏗️  Checking Industrial Infrastructure...")
        # 1. Check Lattice
        lattice = self.root / "master_departmental_lattice.json"
        if lattice.exists():
            try:
                with open(lattice, 'r') as f:
                    json.load(f)
                print("✅ LATTICE: JSON Integrity Verified.")
            except:
                print("❌ LATTICE: Corrupt JSON detected.")
        
        # 2. Check Directories
        required = ["src/system", "src/api", "client/app", "client/components/chambers"]
        for r in required:
            if (self.root / r).exists():
                print(f"✅ PATH: {r} Verified.")
            else:
                print(f"⚠️  MISSING PATH: {r}")

    def generate_report(self):
        print("\n" + "="*50)
        print("TITAN OMEGA FIXER: MISSION COMPLETE")
        print(f"Scanned: {self.stats['scanned']} files")
        print(f"Healed:  {self.stats['fixed']} files")
        if self.stats["failed"]:
            print(f"Failures: {len(self.stats['failed'])}")
            for fail in self.stats["failed"][:5]:
                print(f" - {fail['file']}: {fail['reason']}")
        print("="*50)
        print("ACTION REQUIRED: Restart your Python backend and run 'npm run build' in client.")

if __name__ == "__main__":
    # Point to your actual root
    fixer = TitanOmegaFixer("F:/agentic_workforce")
    fixer.check_infrastructure()
    fixer.scan_and_heal()
    fixer.generate_report()
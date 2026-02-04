from src.system.arsenal.foundation import *
import os
import asyncio
import ast
import base64
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import httpx
import pandas as pd  # type: ignore[import-untyped]

from src.system.arsenal.foundation import *  # noqa: F403  # type: ignore[import-untyped]
from src.system.arsenal.foundation import (  # type: ignore[import-untyped]
    DATA_DIR,
    ROOT_DIR,
    STATIC_DIR,
    WORKSPACE_ROOT,
    logger,
    sanitize_windows_path,
    tool,
)  # explicit for static analysis

@tool('append_to_file')
async def append_to_file(file_path: str, content: str):
    """Sovereign Appender: Safely adds content to the end of an industrial log or file."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        if ".." in str(target): return "[SECURITY_ALERT]: Path traversal blocked."
        
        os.makedirs(target.parent, exist_ok=True)
        async with asyncio.Lock(): # Thread-safe for multi-agent logging
            with open(target, 'a', encoding='utf-8') as f:
                f.write('\n' + content)
        logger.info(f"ðŸ“ [IO_APPEND]: Success at {target}")
        return f'[SUCCESS] [APPENDED]: {target}'
    except Exception as e:
        return f'[ERROR] [FAIL]: {str(e)}'

@tool('audit_python_dependencies')
async def audit_python_dependencies(req_file: str='requirements.txt'):
    """Heuristic Dependency Audit: Scans for deprecated or high-risk library versions."""
    try:
        path = ROOT_DIR / req_file
        if not path.exists(): return '[ERROR] requirements.txt not found.'
        content = path.read_text()
        vulnerabilities = []
        # Industrial Risk Database (Simulated)
        bad_libs = {
            'requests<2.20.0': 'Vulnerable to SSL leaks.',
            'django<4.2': 'End-of-Life version risk.',
            'flask<2.0': 'Legacy routing vulnerabilities.',
            'numpy==2.0.0': 'Potential Windows Logic Conflict.'
        }
        for lib, warning in bad_libs.items():
            name = lib.split('<')[0].split('=')[0]
            if name in content: vulnerabilities.append(f'- âš ï¸ **{name}**: {warning}')
        
        return f'### [DEPENDENCY_AUDIT]: {req_file}\n' + '\n'.join(vulnerabilities) if vulnerabilities else '[SUCCESS]: No high-risk libs detected.'
    except Exception as e:
        return f'[ERROR]: {str(e)}'

@tool('base64_decode')
async def base64_decode(encoded_text: str):
    """Neural Decoder: Translates Base64 strings to human-readable UTF-8."""
    try:
        return base64.b64decode(encoded_text).decode('utf-8')
    except: return '[ERROR]: Invalid Base64 stream.'

@tool('base64_encode')
async def base64_encode(text: str):
    """Neural Encoder: Obfuscates text into Base64 for secure header transmission."""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

@tool('calculate_file_hash')
async def calculate_file_hash(file_path: str):
    """Forensic Integrity Check: Calculates SHA-256 hash to verify file consistency."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        if not target.exists(): return '[ERROR] Physical file not located.'
        sha256_hash = hashlib.sha256()
        with open(target, 'rb') as f:
            for byte_block in iter(lambda: f.read(8192), b''):
                sha256_hash.update(byte_block)
        return f'ðŸ”‘ [SHA256]: {sha256_hash.hexdigest()}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('copy_internal_file')
async def copy_internal_file(source_path: str, destination_path: str):
    """Physical Shifter: Replicates files within the data lattice."""
    try:
        src = DATA_DIR / source_path.replace('data/', '').lstrip('/')
        dst = DATA_DIR / destination_path.replace('data/', '').lstrip('/')
        if not src.exists(): return '[ERROR] Source missing.'
        os.makedirs(dst.parent, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        return f'[SUCCESS] Replicated to {dst}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('create_qr_code')
async def create_qr_code(data: str, filename: str):
    """Industrial Visual Suture: Generates QR codes for URLs or credentials."""
    try:
        import qrcode  # type: ignore[import-untyped]
        img = qrcode.make(data)
        path = DATA_DIR / 'assets/images' / f'{sanitize_windows_path(filename)}.png'
        os.makedirs(path.parent, exist_ok=True)
        img.save(path)
        return f'[SUCCESS] QR Manifested at {path}'
    except ImportError: return '[ERROR]: pip install qrcode[pil]'

@tool('delete_workspace_file')
async def delete_workspace_file(client_name: str, relative_path: str):
    """Sovereign Purge: Physically removes a file from the workspace. USE WITH CAUTION."""
    try:
        target = WORKSPACE_ROOT / sanitize_windows_path(client_name) / relative_path.lstrip('/')
        if not target.exists(): return '[ERROR] File not present.'
        if target.is_dir(): shutil.rmtree(target)
        else: os.remove(target)
        return f'ðŸ—‘ï¸ [PURGED]: {relative_path}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('detect_pii_in_file')
async def detect_pii_in_file(file_path: str):
    """Privacy Guardian: Scans for Emails, IPs, and SSNs. Masking results for security."""
    try:
        content = await read_file(file_path)
        patterns = {
            'Email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'IPv4': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'API_Key': r'(?i)(api_key|secret|token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}'
        }
        findings = []
        for label, pattern in patterns.items():
            matches = re.findall(pattern, content)
            if matches: findings.append(f'- Found {len(matches)} potential {label} entries.')
        return '\n'.join(findings) if findings else '[SUCCESS]: No PII detected.'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('download_file')
async def download_file(url: str, save_path: str):
    """Network Ingress: Pulls binary assets into the data lattice via HTTPX."""
    try:
        target = DATA_DIR / save_path.replace('data/', '').lstrip('/')
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                os.makedirs(target.parent, exist_ok=True)
                target.write_bytes(resp.content)
                return f'[SUCCESS]: Ingested {len(resp.content)} bytes to {target}'
            return f'[HTTP_ERROR]: {resp.status_code}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('extract_code_blocks')
async def extract_code_blocks(markdown_text: str):
    """Logic Extractor: Pulls fenced code blocks from AI-generated technical briefs."""
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, markdown_text, re.DOTALL)
    if not matches: return 'â„¹ï¸ No technical logic found.'
    return '\n'.join([f'### [{lang.upper() if lang else "TEXT"}]\n{code.strip()}' for lang, code in matches])

@tool('generate_dockerfile')
async def generate_dockerfile(tech_stack: str, port: int=8000):
    """DevOps Architect: Scaffolds production-grade Docker containers."""
    templates = {
        'python': f'FROM python:3.10-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "{port}"]',
        'node': f'FROM node:18-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm install --production\nCOPY . .\nEXPOSE {port}\nCMD ["npm", "start"]',
        'static': f'FROM nginx:alpine\nCOPY . /usr/share/nginx/html\nEXPOSE 80'
    }
    content = templates.get(tech_stack.lower(), templates['python'])
    path = DATA_DIR / 'docs' / 'Dockerfile'
    path.write_text(content, encoding='utf-8')
    return f'âœ… Dockerfile generated for {tech_stack} in data/docs/'

@tool('generate_persona_profile')
async def generate_persona_profile(role_type: str='corporate'):
    """Identity Manifestor: Creates synthetic identities for red-teaming/CS testing."""
    import random
    first = ['Alex', 'Jordan', 'Casey', 'Taylor']; last = ['Tyrell', 'Cipher', 'Vortex', 'Echo']
    profile = {
        'name': f'{random.choice(first)} {random.choice(last)}',
        'id': f'EE-{random.randint(1000, 9999)}',
        'role': role_type,
        'clearance': 'Level 2'
    }
    return f'### [PERSONA_DNA]:\n{json.dumps(profile, indent=2)}'

@tool('get_file_metadata')
async def get_file_metadata(file_path: str):
    """Diagnostic Sensor: Retrieves physical disk statistics for a lattice file."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        if not target.exists(): return '[ERROR] File not found.'
        s = target.stat()
        return f'Size: {s.st_size} bytes | Created: {datetime.fromtimestamp(s.st_ctime)} | Mod: {datetime.fromtimestamp(s.st_mtime)}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('grep_files')
async def grep_files(pattern: str, directory: str='.'):
    """Sector Search: Regex-based pattern discovery across the data directory."""
    res = []
    target_dir = DATA_DIR / directory.replace('data/', '').lstrip('/')
    for f in target_dir.rglob('*'):
        if f.is_file() and f.stat().st_size < 1024 * 1024: # Limit to 1MB files to prevent hang
            try:
                if re.search(pattern, f.read_text(errors='ignore')):
                    res.append(str(f.relative_to(DATA_DIR)))
            except: continue
    return f'### [PATTERN_MATCHES]:\n' + '\n'.join(res[:15])

@tool('hash_file_integrity')
async def hash_file_integrity(file_path: str, algorithm: str='sha256'):
    """Forensic Validator: Verifies file state via MD5 or SHA256."""
    return await calculate_file_hash(file_path)

@tool('list_files')
async def list_files(directory: str='.'):
    """Lattice Manifest: Lists all objects at a specific physical location."""
    try:
        target = DATA_DIR / directory.replace('data/', '').lstrip('/')
        if not target.exists(): return '[ERROR] Directory missing.'
        return '\n'.join(os.listdir(target))
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('list_workspace_files')
async def list_workspace_files(client_name: str):
    """Workspace Auditor: Recursively lists all project files for a client."""
    try:
        target = WORKSPACE_ROOT / sanitize_windows_path(client_name)
        if not target.exists(): return '[ERROR] Workspace not located.'
        res = []
        for root, _, files in os.walk(target):
            for f in files: res.append(str(Path(root) / f).replace(str(target), ''))
        return '\n'.join(res)
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('merge_csv_files')
async def merge_csv_files(file1: str, file2: str, output_file: str):
    """Data Engineer: Merges two CSV datasets into a single industrial master."""
    try:
        p1 = DATA_DIR / file1.replace('data/', '').lstrip('/')
        p2 = DATA_DIR / file2.replace('data/', '').lstrip('/')
        df = pd.concat([pd.read_csv(p1), pd.read_csv(p2)])
        out = DATA_DIR / output_file.replace('data/', '').lstrip('/')
        df.to_csv(out, index=False)
        return f'[SUCCESS] {len(df)} rows consolidated into {output_file}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('move_internal_file')
async def move_internal_file(source_path: str, destination_path: str):
    """Physical Logic: Renames or moves objects across the internal lattice."""
    try:
        src = DATA_DIR / source_path.replace('data/', '').lstrip('/')
        dst = DATA_DIR / destination_path.replace('data/', '').lstrip('/')
        os.makedirs(dst.parent, exist_ok=True)
        shutil.move(str(src), str(dst))
        return f'[SUCCESS] Moved {source_path} -> {destination_path}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('parse_log_file')
async def parse_log_file(file_path: str, keyword: str='ERROR'):
    """Industrial Filter: Extracts mission-critical events from raw system logs."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        lines = target.read_text(encoding='utf-8').splitlines()
        matches = [l for l in lines if keyword.upper() in l.upper()]
        return '\n'.join(matches[:50]) if matches else 'No matches found.'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('read_excel_file')
async def read_excel_file(file_path: str, sheet_name: str=0):
    """Financial Sensor: Ingests Excel workbooks and returns Markdown summary."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        df = pd.read_excel(target, sheet_name=sheet_name)
        return df.head(10).to_markdown()
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('read_file')
async def read_file(file_path: str):
    """Primary Sensor: Reads raw text/code from the internal data or static directories."""
    try:
        if file_path.startswith('static/'): target = STATIC_DIR / file_path.replace('static/', '')
        else: target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        if not target.exists(): return '[ERROR] File not found.'
        return target.read_text(encoding='utf-8')
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('regex_replace_in_file')
async def regex_replace_in_file(file_path: str, pattern: str, replacement: str):
    """Industrial Refactor: High-fidelity pattern substitution within a source file."""
    try:
        content = await read_file(file_path)
        new_content = re.sub(pattern, replacement, content)
        await write_file(file_path, new_content)
        return f'[SUCCESS] Regex substitution committed to {file_path}'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('replace_text_in_file')
async def replace_text_in_file(file_path: str, old_text: str, new_text: str):
    """Sovereign Refactor: Atomic string replacement for config/code updates."""
    try:
        content = await read_file(file_path)
        new_content = content.replace(old_text, new_text)
        await write_file(file_path, new_content)
        return '[SUCCESS] Text replacement complete.'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('scaffold_flask_api')
async def scaffold_flask_api(app_name: str):
    """Senior Developer: Manifests a production Flask boilerplate in the projects sector."""
    content = "from flask import Flask, jsonify\napp = Flask(__name__)\n@app.route('/')\ndef root(): return jsonify({'status': 'NOMINAL'})\nif __name__ == '__main__': app.run(port=5000)"
    path = DATA_DIR / 'projects' / app_name / 'app.py'
    os.makedirs(path.parent, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return f'ðŸš€ Flask API scaffolded at {path}'

@tool('scaffold_react_component')
async def scaffold_react_component(name: str):
    """Frontend Architect: Generates an industrial Bento-Style React component."""
    content = f"import React from 'react';\n\nexport const {name} = () => (\n  <div className='titan-card p-6 border-[#b5a642]/20 bg-black/40'>\n    <h2 className='text-[#b5a642] uppercase font-black'>{name} Chamber</h2>\n  </div>\n);"
    path = DATA_DIR / 'projects' / 'ui' / f'{name}.tsx'
    os.makedirs(path.parent, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return f'âœ¨ React Bento-Component manifested at {path}'

@tool('scan_code_for_vulnerabilities')
async def scan_code_for_vulnerabilities(file_path: str):
    """SAST Auditor: Scans Python logic for eval, unsafe subprocess, and hardcoded keys."""
    try:
        content = await read_file(file_path)
        risks = []
        if 'eval(' in content: risks.append("ðŸ’€ CRITICAL: 'eval()' usage detected.")
        if 'os.system(' in content: risks.append("ðŸ’€ CRITICAL: Unsafe shell command usage.")
        if 'sk-' in content or 'API_KEY' in content: risks.append("âš ï¸ HIGH: Possible hardcoded secret.")
        return '\n'.join(risks) if risks else 'ðŸ’Ž [SAST_CLEAN]: No major risks identified.'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('semantic_code_search')
async def semantic_code_search(query: str):
    """Neural Logic Sensor: Vector-based search to locate specific code patterns by intent."""
    from src.memory.engine import MemoryManager
    results = MemoryManager().knowledge.query(query_texts=[query], n_results=3, where={'category': 'source_code'})
    return f"### [NEURAL_MATCHES]:\n" + '\n'.join(results['documents'][0]) if results['documents'] else 'None.'

@tool('unzip_file')
async def unzip_file(zip_path: str, extract_to: str):
    """Industrial Extraction: Expands archives into the data lattice."""
    try:
        src = DATA_DIR / zip_path.replace('data/', '').lstrip('/')
        dst = DATA_DIR / extract_to.replace('data/', '').lstrip('/')
        shutil.unpack_archive(src, dst)
        return '[SUCCESS] Archive expanded.'
    except Exception as e: return f'[ERROR]: {str(e)}'

@tool('validate_python_syntax')
async def validate_python_syntax(file_path: str):
    """Logic Guard: Uses AST to physically verify a Python file before execution."""
    try:
        content = await read_file(file_path)
        ast.parse(content)
        return 'ðŸ’Ž [SYNTAX_STABLE]: Logic verified.'
    except SyntaxError as e: return f'âŒ [SYNTAX_FAULT] Line {e.lineno}: {e.msg}'

@tool('write_file')
async def write_file(file_path: str, content: str):
    """Physical Committer: Atomic write logic for mission-critical files."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').replace('static/', '').lstrip('/')
        if file_path.startswith('static/'): target = STATIC_DIR / file_path.replace('static/', '')
        
        os.makedirs(target.parent, exist_ok=True)
        # Atomic Write strategy: write to temp, then rename
        temp_path = target.with_suffix('.tmp')
        temp_path.write_text(content, encoding='utf-8')
        os.replace(temp_path, target)
        return f'[SUCCESS] Physically committed to {target}'
    except Exception as e: return f'[ERROR]: {str(e)}'


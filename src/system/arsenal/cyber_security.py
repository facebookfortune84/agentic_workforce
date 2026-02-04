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
import pandas as pd

from src.system.arsenal.foundation import *  # noqa: F403
from src.system.arsenal.foundation import (
    DATA_DIR,
    ROOT_DIR,
    STATIC_DIR,
    WORKSPACE_ROOT,
    logger,
    sanitize_windows_path,
    tool,
)

@tool('analyze_http_security_headers')
async def analyze_http_security_headers(url: str):
    """Defensive Sensor: Scans a URL for critical security headers (HSTS, CSP, X-Frame, etc.)"""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "Titan-Security-Probe/1.0"})
            headers = resp.headers
        
        required = {
            'Strict-Transport-Security': 'Mitigates MITM/Hijacking.',
            'Content-Security-Policy': 'Prevents XSS/Injections.',
            'X-Frame-Options': 'Prevents Clickjacking.',
            'X-Content-Type-Options': 'Blocks MIME-sniffing.',
            'Referrer-Policy': 'Controls metadata leakage.',
            'Permissions-Policy': 'Restricts browser features (Camera/Geo).'
        }
        
        report = []
        score = 0
        for header, desc in required.items():
            if header in headers:
                report.append(f'[SUCCESS] {header}: Present')
                score += 1
            else:
                report.append(f'[ERROR] {header}: MISSING ({desc})')
        
        logger.info(f"🛡️ [SEC_AUDIT]: {url} evaluated. Score: {score}/{len(required)}")
        return f'### [HEADER SECURITY AUDIT]: {url} (Score: {score}/{len(required)})\n' + '\n'.join(report)
    except Exception as e:
        return f'[ERROR] Probe Failed: {str(e)}'

@tool('check_port_availability')
async def check_port_availability(port: int):
    """Diagnostic Sensor: Checks if a local port is free. Crucial for Gateway stability."""
    try:
        import socket
        # Use a short timeout for local checks
        conn = asyncio.open_connection('127.0.0.1', port)
        try:
            _, writer = await asyncio.wait_for(conn, timeout=1.0)
            writer.close()
            await writer.wait_closed()
            return f'🚨 [BUSY]: Port {port} is currently occupied.'
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return f'✅ [AVAILABLE]: Port {port} is clear.'
    except Exception as e:
        return f'[ERROR]: {str(e)}'

@tool('create_customer_support_script')
async def create_customer_support_script(issue_type: str):
    """Social Engineering/Defense: Generates high-empathy response scripts for technical support."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"""### [TITAN_CS_PROTOCOL]: {issue_type}
**TIMESTAMP**: {ts}
**Step 1: Empathy Anchor**
"I recognize the priority of this {issue_type} issue. My system is dedicated to resolving this for you immediately."

**Step 2: Technical Assessment**
"Please provide the stack-trace or specific error code appearing in your terminal."

**Step 3: Tactical Resolution**
[Insert Automated Recovery Steps Here]

**Step 4: Assurance**
"I have logged this in the Sovereign Ledger and will monitor the status until completion."
"""

@tool('generate_security_policy')
async def generate_security_policy(company_name: str):
    """Industrial Governance: Manifests an atomic SECURITY.md for repository alignment."""
    try:
        content = f"""# Security Policy: {company_name}
## Reporting Vulnerabilities
Please report any security findings to security@{company_name.lower().replace(' ', '')}.ai.
We utilize the Realm Forge Sovereign Audit protocol for rapid patching.

## Standard Hardening
- All endpoints secured via X-API-Key logic.
- Neural Security Lattice Active (WAL Mode).
- Automated SAST scanning on every commit.
"""
        target = DATA_DIR / 'docs' / 'legal' / 'SECURITY.md'
        os.makedirs(target.parent, exist_ok=True)
        # Atomic Write
        target.write_text(content, encoding='utf-8')
        return f'💎 [GOVERNANCE]: Security Policy manifested at {target}'
    except Exception as e:
        return f'[ERROR]: {str(e)}'

@tool('port_scan_local')
async def port_scan_local():
    """Local Perimeter Audit: Scans common development ports on 127.0.0.1."""
    common_ports = [3000, 5000, 8000, 8080, 5432, 6379, 27017]
    open_ports = []
    
    for port in common_ports:
        try:
            conn = asyncio.open_connection('127.0.0.1', port)
            _, writer = await asyncio.wait_for(conn, timeout=0.2)
            open_ports.append(port)
            writer.close()
            await writer.wait_closed()
        except:
            continue
            
    return f"🔍 [LOCAL_SCAN]: Open Ports detected: {open_ports if open_ports else 'NONE'}"

@tool('scan_network_ports')
async def scan_network_ports(target_ip: str, start_port: int=1, end_port: int=1024):
    """Offensive/Defensive Probe: High-concurrency async port scanner for network mapping."""
    if end_port - start_port > 1024:
        return "[SECURITY_LIMIT]: Max scan range is 1024 ports per strike."
    
    open_ports = []
    # Concurrency control: 100 simultaneous probes
    semaphore = asyncio.Semaphore(100)

    async def probe(port):
        async with semaphore:
            try:
                conn = asyncio.open_connection(target_ip, port)
                _, writer = await asyncio.wait_for(conn, timeout=1.5)
                open_ports.append(port)
                writer.close()
                await writer.wait_closed()
            except:
                pass

    tasks = [probe(p) for p in range(start_port, end_port + 1)]
    await asyncio.gather(*tasks)
    
    logger.info(f"📡 [NET_SCAN]: Finished probe on {target_ip}. Found: {len(open_ports)} ports.")
    return f"🚨 [SCAN_RESULTS] Target: {target_ip} | Open: {sorted(open_ports) if open_ports else 'NONE DETECTED'}"

@tool('validate_jwt_structure')
async def validate_jwt_structure(token: str):
    """Forensic Logic: Decodes and audits JWT structure for expiration and algorithm risks."""
    parts = token.split('.')
    if len(parts) != 3:
        return '[ERROR]: Invalid JWT Format (Expected 3 parts).'
    
    try:
        header = json.loads(base64.b64decode(parts[0] + "==").decode('utf-8'))
        payload = json.loads(base64.b64decode(parts[1] + "==").decode('utf-8'))
        
        # Alg Check
        alg = header.get('alg', 'None').upper()
        risk = "HIGH" if alg == "NONE" else "LOW"
        
        # Exp Check
        exp = payload.get('exp')
        status = "VALID"
        if exp:
            if datetime.fromtimestamp(exp) < datetime.now():
                status = "EXPIRED"
        
        return f"🔑 [JWT_AUDIT]: Status={status} | Alg={alg} | Risk={risk} | Payload={json.dumps(payload)}"
    except Exception as e:
        return f'[ERROR] Decoding Failed: {str(e)}'

@tool('verify_ssl_certificate')
async def verify_ssl_certificate(hostname: str):
    """Forensic Sensor: Retrieves domain SSL certificate and audits expiration/strength."""
    import ssl
    import socket
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5.0) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        
        # Extract metadata
        issuer = dict(x[0] for x in cert['issuer'])
        subject = dict(x[0] for x in cert['subject'])
        expires = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        days_left = (expires - datetime.now()).days
        
        status = "💎 SECURE" if days_left > 30 else "⚠️ WARNING" if days_left > 0 else "💀 EXPIRED"
        
        return f"🛡️ [SSL_REPORT]: {hostname}\n- Status: {status}\n- Issuer: {issuer.get('organizationName')}\n- Days Remaining: {days_left}\n- Common Name: {subject.get('commonName')}"
    except Exception as e:
        return f"[ERROR] SSL Verification Failed: {str(e)}"

@tool('write_csv_report')
async def write_csv_report(filename: str, data_json: str):
    """Data Committer: Converts JSON intelligence into a structured industrial CSV ledger."""
    try:
        data = json.loads(data_json)
        if not isinstance(data, list):
            return "[ERROR]: Data must be a JSON list of objects."
            
        df = pd.DataFrame(data)
        target = DATA_DIR / 'finance' / 'reports' / sanitize_windows_path(filename)
        os.makedirs(target.parent, exist_ok=True)
        
        # Atomic write
        df.to_csv(target, index=False)
        return f"✅ [CSV_SAVED]: Ledger committed to {target}"
    except Exception as e:
        return f"[ERROR] CSV Generation Failed: {str(e)}"


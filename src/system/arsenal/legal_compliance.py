from src.system.arsenal.foundation import *
import os
import asyncio
import ast
import base64
import hashlib
import json
import re
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import httpx
import pandas as pd  # type: ignore[import-untyped]
import yfinance as yf  # type: ignore[import-untyped]
from reportlab.lib.pagesizes import letter  # type: ignore[import-untyped]
from reportlab.pdfgen import canvas  # type: ignore[import-untyped]

from src.system.arsenal.foundation import *  # noqa: F403  # type: ignore[import-untyped]
from src.system.arsenal.foundation import (  # type: ignore[import-untyped]
    DATA_DIR,
    ROOT_DIR,
    STATIC_DIR,
    WORKSPACE_ROOT,
    generate_neural_audio,
    logger,
    sanitize_windows_path,
    tool,
    read_file,
)
import uuid

@tool('analyze_contract_risk')
async def analyze_contract_risk(file_path: str):
    """Legal Sensor: Scans technical or business agreements for high-risk clauses and provides a risk-severity audit."""
    try:
        content = await read_file(file_path)
        if '[ERROR]' in content: return content
        
        # Industrial Risk Heuristics
        risk_patterns = {
            'Indemnification': {
                'pattern': r'(indemnif|hold harmless)',
                'risk': '🔴 HIGH',
                'reason': 'Broad indemnity can lead to uncapped financial liability. Check for carve-outs.'
            },
            'Termination for Convenience': {
                'pattern': r'(terminate|cancel).*(convenience|any reason|without cause)',
                'risk': '🟡 MEDIUM',
                'reason': 'Allows the client to kill the contract instantly. Ensure a notice period is defined.'
            },
            'Exclusivity': {
                'pattern': r'(exclusive|restriction|non-compete)',
                'risk': '🔴 HIGH',
                'reason': 'Restricts your ability to provide AIAAS services to other competitors.'
            },
            'Governing Law': {
                'pattern': r'(governing law|jurisdiction)',
                'risk': '⚪ INFO',
                'reason': 'Verify the legal venue is manageable (e.g., your local state vs international).'
            },
            'Perpetual License': {
                'pattern': r'(perpetual|irrevocable|in perpetuity)',
                'risk': '🔴 HIGH',
                'reason': 'Review IP rights; "perpetual" usually means you lose ownership of the logic.'
            }
        }

        risks_found = []
        score = 0
        for label, data in risk_patterns.items():
            if re.search(data['pattern'], content, re.IGNORECASE):
                risks_found.append(f"### {data['risk']} - {label}\n- **Warning**: {data['reason']}")
                if 'HIGH' in data['risk']: score += 3
                else: score += 1

        if not risks_found:
            return '[SUCCESS] [LEGAL_SCAN]: No standard high-risk keywords or clauses detected.'

        header = f"### [LEGAL_RISK_AUDIT]: {file_path}\n**Calculated Risk Index**: {score}\n\n"
        logger.info(f"⚖️ [LEGAL_AUDIT]: {file_path} processed. Risk Score: {score}")
        return header + '\n'.join(risks_found)
    except Exception as e:
        return f'[ERROR] Legal Analysis Fault: {str(e)}'

@tool('create_calendar_event_ics')
async def create_calendar_event_ics(summary: str, start_time: str, duration_hours: int=1):
    """Logistics Sync: Generates an RFC 5545 compliant .ics file for scheduling mission meetings or client handshakes."""
    try:
        # Validate format: YYYYMMDDTHHMMSS (e.g. 20260128T090000)
        if not re.match(r'\d{8}T\d{6}', start_time):
            return "[ERROR]: start_time must be in format YYYYMMDDTHHMMSS."

        uid = uuid.uuid4()
        ts_now = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        
        ics_content = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//RealmForge//TitanNode//EN",
            "BEGIN:VEVENT",
            f"UID:{uid}@realmforge.ai",
            f"DTSTAMP:{ts_now}",
            f"DTSTART:{start_time}",
            f"SUMMARY:{summary}",
            f"DURATION:PT{duration_hours}H",
            "DESCRIPTION:Autonomous Strike Meeting initiated by Realm Forge AIAAS.",
            "STATUS:CONFIRMED",
            "END:VEVENT",
            "END:VCALENDAR"
        ]

        filename = f"invite_{uid.hex[:6]}.ics"
        path = DATA_DIR / 'docs' / 'calendar' / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(ics_content), encoding='utf-8')
        
        return f'[SUCCESS] [CALENDAR_EVENT]: Physical object manifested at {path}'
    except Exception as e:
        return f'[ERROR] Calendar Fault: {str(e)}'

@tool('generate_nda_contract')
async def generate_nda_contract(party_a: str, party_b: str, effective_date: str):
    """Legal Architect: Manifests a standard high-fidelity Mutual Non-Disclosure Agreement (NDA) in Markdown."""
    try:
        content = f"""# MUTUAL NON-DISCLOSURE AGREEMENT

**EFFECTIVE DATE**: {effective_date}
**PARTIES**:
1. **{party_a}** ("Disclosing Party")
2. **{party_b}** ("Receiving Party")

### 1. DEFINITION OF CONFIDENTIAL INFORMATION
Confidential Information includes all technical data, trade secrets, agent DNA manifests, and financial records shared within the Realm Forge environment.

### 2. NON-USE AND NON-DISCLOSURE
The Receiving Party shall maintain the Confidential Information in strictest confidence and shall not use it for any purpose other than the "Strike Mission" objectives defined by the Architect.

### 3. TERM & TERMINATION
This Agreement shall remain in effect for a period of five (5) years from the Effective Date.

### 4. GOVERNING LAW
This Agreement shall be governed by the laws of the REALM_FORGE_VIRTUAL_ZONE and respective physical industrial jurisdictions.

### 5. NON-SOLICITATION
During the term of this Agreement, neither party shall solicit the "Specialist Agents" or personnel of the other party.

**EXECUTED BY**:

____________________             ____________________
({party_a})                      ({party_b})
"""
        filename = f'NDA_{sanitize_windows_path(party_b)}.md'
        path = DATA_DIR / 'docs' / 'legal' / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Atomic Write
        path.write_text(content, encoding='utf-8')
        logger.info(f"⚖️ [CONTRACT]: Mutual NDA manifested for {party_b}.")
        return f'[SUCCESS] [LEGAL_ARTIFACT]: NDA physically committed to {path}'
    except Exception as e:
        return f'[ERROR] Contract Generation Failed: {str(e)}'


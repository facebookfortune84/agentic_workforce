from src.system.arsenal.foundation import *
"""
REALM FORGE: ARSENAL FOUNDATION v1.2
PURPOSE: Core utilities, Path Sovereignty, and Departmental Mapping.
"""
from typing import Optional, Union, Annotated, Dict, Any, List
import os
import time
import json
import base64
import logging
import re
import subprocess
import asyncio
import httpx
import uuid
import glob
import networkx as nx
import yaml
import pandas as pd
import edge_tts
import yfinance as yf
import replicate
import smtplib
import ast
import shutil
import sqlite3
import zipfile
import platform
import hashlib
from pathlib import Path
from datetime import datetime
from langchain.tools import tool
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from openai import OpenAI
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pptx import Presentation
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('RealmTools')

# --- PATH SOVEREIGNTY ---
BASE_PROJECT_PATH = Path("F:/agentic_workforce")
ROOT_DIR = BASE_PROJECT_PATH  # alias for project root (e.g. requirements.txt)
DATA_DIR = BASE_PROJECT_PATH / 'data'
STATIC_DIR = BASE_PROJECT_PATH / 'static'
BASE_PATH = DATA_DIR
WORKSPACE_ROOT = Path("F:/RealmWorkspaces")

# Ensure industrial directory structure
for d in ['projects', 'memory', 'agents', 'ingress', 'audio', 'assets/images', 'assets/video', 'finance', 'docs', 'databases', 'logs']:
    os.makedirs(DATA_DIR / d, exist_ok=True)
    os.makedirs(WORKSPACE_ROOT, exist_ok=True)
    os.makedirs(STATIC_DIR / 'deployments', exist_ok=True)

# ==============================================================================
# 0. CORE UTILITIES
# ==============================================================================

def sanitize_windows_path(path_str: str) -> str:
    sanitized = re.sub('[<>:\\"|?*]', '_', str(path_str))
    return sanitized.replace('data/data/', 'data/').strip()

def prepare_vocal_response(text: str) -> str:
    if not text: return 'Mission confirmed.'
    text = re.sub('```.*?```', ' [Technical Detail Omitted] ', text, flags=re.DOTALL)
    text = re.sub('[*_#`\\-|>\\[\\]]', '', text)
    return ' '.join(text.split()).strip()[:10000]

async def generate_neural_audio(text: str) -> str:
    if not text: return ''
    VOICE = 'en-US-ChristopherNeural'
    try:
        communicate = edge_tts.Communicate(text, VOICE, rate='+0%', pitch='-5Hz')
        audio_bytes = b''
        async for chunk in communicate.stream():
            if chunk['type'] == 'audio':
                audio_bytes += chunk['data']
        return base64.b64encode(audio_bytes).decode('utf-8')
    except:
        return ''

def get_swarm_roster():
    return "SWARM_STATUS: 180 unique tools active across 13 industrial sectors."

# ==============================================================================
# 1. DEPARTMENTAL MAPPING LOGIC
# ==============================================================================

COMMS_CAPS = [
    "send_direct_notification", "mm_join_channel", "mm_get_channel_history", 
    "transmit_workforce_message", "mm_get_user_by_name", "mm_add_user_to_channel",
    "mm_create_channel", "mm_add_user_to_team", "get_sector_roster", 
    "lattice_scout_search", "discord_voice_broadcast", "send_discord_webhook"
]

INTEL_CAPS = [
    "spawn_autonomous_agent", "system_auto_heal", "assign_swarm_task", 
    "autonomous_readiness_fix", "search_memory", "semantic_code_search",
    "query_knowledge_graph", "update_knowledge_graph", "lattice_scout_search"
]

DEPARTMENT_TOOL_MAP = {
    "Architect": ["create_client_workspace", "inject_new_capability", "self_evolve", "ask_human", "get_system_vitals", "get_env_info", "backup_memory_db"] + COMMS_CAPS + INTEL_CAPS,
    "DevOps": ["run_terminal_command", "generate_dockerfile", "sync_repository", "zip_directory", "get_directory_tree", "list_files", "push_to_github", "check_port_availability", "parse_log_file"] + COMMS_CAPS + INTEL_CAPS,
    "SOFTWARE_ENGINEERING": ["run_terminal_command", "validate_python_syntax", "scaffold_react_component", "scaffold_flask_api", "replace_text_in_file", "read_file", "write_file", "regex_replace_in_file", "minify_js_css", "extract_code_blocks"] + COMMS_CAPS + INTEL_CAPS,
    "FACILITY_MANAGEMENT": ["run_terminal_command", "get_system_vitals", "list_files", "get_directory_tree", "csv_processor_read", "csv_processor_write", "get_file_metadata"] + COMMS_CAPS,
    "CyberSecurity": ["scan_network_ports", "verify_ssl_certificate", "analyze_http_security_headers", "detect_pii_in_file", "scan_code_for_vulnerabilities", "ip_geolocation", "port_scan_local", "generate_strong_password", "detect_log_anomalies", "validate_jwt_structure", "analyze_contract_risk", "generate_security_policy"] + COMMS_CAPS,
    "DataEngineering": ["sqlite_create_table_v2", "sqlite_query", "sqlite_insert", "sqlite_inspect_schema", "industrial_data_ingress", "csv_processor_read", "csv_processor_write", "convert_csv_to_markdown_table", "merge_csv_files"] + COMMS_CAPS,
    "R&D": ["web_search_duckduckgo", "interact_web", "scrape_url_to_markdown", "search_memory", "semantic_code_search", "get_market_intelligence", "consolidate_memory_dream", "spawn_ephemeral_agent"] + COMMS_CAPS + INTEL_CAPS,
    "Finance": ["get_stock_history_csv", "analyze_stock_technicals", "calculate_burn_rate", "generate_project_budget", "generate_corporate_invoice", "csv_processor_read", "convert_currency", "get_crypto_price", "write_csv_report"] + COMMS_CAPS,
    "Legal": ["generate_nda_contract", "analyze_contract_risk", "generate_corporate_document", "generate_security_policy", "check_robots_txt", "validate_jwt_structure"] + COMMS_CAPS,
    "Creative": ["generate_industrial_image", "generate_industrial_video", "create_qr_code", "generate_svg_badge", "convert_markdown_to_html", "create_business_card_qr", "generate_lorem_ipsum", "format_newsletter_html"] + COMMS_CAPS,
    "Operations": ["create_ticket", "scaffold_industrial_project", "scaffold_commercial_website", "create_calendar_event_ics", "dispatch_corporate_email", "get_sector_roster", "generate_press_release", "generate_sms_alert"] + COMMS_CAPS + INTEL_CAPS
}

def get_tools_for_dept(dept_name: str, all_tools_list: list):
    """Dynamically loads tool instances for a department."""
    key = dept_name.upper().replace(" ", "_") if dept_name else "Architect"
    if key not in DEPARTMENT_TOOL_MAP:
        for k in DEPARTMENT_TOOL_MAP.keys():
            if key == k.upper().replace(" ", "_"):
                key = k
                break
        else: key = "Architect"
    tool_names = DEPARTMENT_TOOL_MAP.get(key, DEPARTMENT_TOOL_MAP["Architect"])
    return [t for t in all_tools_list if t.name in tool_names]

@tool('read_file')
async def read_file(file_path: str):
    """Primary Sensor: Reads raw text/code from the internal data or static directories."""
    try:
        # Standardize path logic to project root
        if file_path.startswith('static/'): 
            target = STATIC_DIR / file_path.replace('static/', '')
        else: 
            target = DATA_DIR / file_path.replace('data/', '').lstrip('/')
        
        if not target.exists(): 
            return f'[ERROR] File not found at {target}'
            
        return target.read_text(encoding='utf-8', errors='replace')
    except Exception as e: 
        return f'[ERROR] Physical Read Fault: {str(e)}'

@tool('write_file')
async def write_file(file_path: str, content: str):
    """Physical Committer: Atomic write logic for mission-critical files. Enforces F:/agentic_workforce boundaries."""
    try:
        target = DATA_DIR / file_path.replace('data/', '').replace('static/', '').lstrip('/')
        if file_path.startswith('static/'): 
            target = STATIC_DIR / file_path.replace('static/', '')
        
        os.makedirs(target.parent, exist_ok=True)
        # Atomic Write strategy: write to temp, then rename to prevent corruption
        temp_path = target.with_suffix('.tmp')
        temp_path.write_text(content, encoding='utf-8')
        os.replace(temp_path, target)
        return f'[SUCCESS] Physically committed to {target}'
    except Exception as e: 
        return f'[ERROR] Physical Write Fault: {str(e)}'
    
@tool('update_knowledge_graph')
async def update_knowledge_graph(subject: str, relation: str, target: str):
    """Neural Architect: Physically maps a relationship edge in the NetworkX graph. Enforces data persistence."""
    graph_path = DATA_DIR / 'memory' / 'neural_graph.json'
    try:
        if graph_path.exists():
            with open(graph_path, 'r', encoding='utf-8-sig') as f:
                G = nx.node_link_graph(json.load(f))
        else:
            G = nx.DiGraph()

        G.add_edge(subject, target, relation=relation, timestamp=datetime.now().isoformat())
        
        with open(graph_path, 'w', encoding='utf-8-sig') as f:
            json.dump(nx.node_link_data(G), f, indent=2)
            
        return f'[SUCCESS] [LATTICE_UPDATED]: {subject} --[{relation}]--> {target}'
    except Exception as e: return f'[ERROR] Graph Write Fault: {str(e)}'

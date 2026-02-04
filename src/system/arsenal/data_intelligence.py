from src.system.arsenal.foundation import *
import os
import asyncio
import ast
import base64
import hashlib
import json
import re
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict

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
    yf,
)

@tool('convert_csv_to_markdown_table')
async def convert_csv_to_markdown_table(file_path: str):
    """Data Scryer: Reads a CSV file and converts the head entries into a GFM table for the HUD."""
    try:
        path = (DATA_DIR / file_path.replace('data/', '').lstrip('/')).resolve()
        if not path.exists(): return "[ERROR]: File not found on physical disk."
        
        # OOM Protection: Only read the first 20 rows for UI display
        df = pd.read_csv(path, nrows=20)
        return f"### [TABLE_PREVIEW]: {path.name}\n" + df.to_markdown(index=False)
    except Exception as e:
        return f'[ERROR] Markdown Conversion Failed: {str(e)}'

@tool('get_stock_history_csv')
async def get_stock_history_csv(ticker: str, period: str='1mo'):
    """Financial Sensor: Downloads OHLCV stock data into the finance sector of the lattice."""
    try:
        # Validate ticker format
        ticker = ticker.upper().strip()
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f'[ERROR] No market data returned for {ticker}. Check symbol.'
            
        filename = f"{ticker}_{period}_{datetime.now().strftime('%Y%m%d')}.csv"
        target_dir = DATA_DIR / 'finance' / 'market_data'
        target_dir.mkdir(parents=True, exist_ok=True)
        
        path = target_dir / filename
        hist.to_csv(path)
        
        logger.info(f"ðŸ“ˆ [MARKET_INGRESS]: {ticker} data committed to {path}")
        return f'[SUCCESS] [DATA_SAVED]: {path} ({len(hist)} intervals ingested)'
    except Exception as e:
        return f'[ERROR] Financial API Fault: {str(e)}'

@tool('industrial_data_ingress')
async def industrial_data_ingress(individual_csv: str, business_csv: str):
    """Swarm Ingress: Merges and sanitizes massive individual and business datasets into the swarm."""
    try:
        ind_p = (DATA_DIR / individual_csv.replace('data/', '').lstrip('/')).resolve()
        biz_p = (DATA_DIR / business_csv.replace('data/', '').lstrip('/')).resolve()
        
        results = []
        if ind_p.exists():
            df_ind = pd.read_csv(ind_p)
            results.append(f"Ind_Sector: {len(df_ind)} records | Columns: {list(df_ind.columns[:3])}...")
        
        if biz_p.exists():
            df_biz = pd.read_csv(biz_p)
            results.append(f"Biz_Sector: {len(df_biz)} records | Columns: {list(df_biz.columns[:3])}...")
            
        return f"ðŸ’Ž [INGRESS_SUMMARY]:\n" + "\n".join(results)
    except Exception as e:
        return f'[ERROR] Ingress Fault: {str(e)}'

@tool('sqlite_create_table_v2')
async def sqlite_create_table_v2(db_name: str, table_name: str, table_definition: str):
    """Structural Engineer: Physically manifests a SQLite table with high-fidelity schema."""
    try:
        path = DATA_DIR / 'databases' / f'{sanitize_windows_path(db_name)}.db'
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_definition})")
            conn.commit()
        return f"âœ… [SCHEMA_COMMITTED]: Table '{table_name}' online in {db_name}.db"
    except Exception as e:
        return f'[ERROR] Database Creation Fault: {str(e)}'

@tool('sqlite_insert')
async def sqlite_insert(db_name: str, table: str, data: Dict):
    """Data Committer: Surgically inserts a single dictionary record into a SQLite table."""
    try:
        path = DATA_DIR / 'databases' / f'{sanitize_windows_path(db_name)}.db'
        if not path.exists(): return "[ERROR]: Target database does not exist."

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        
        with sqlite3.connect(path) as conn:
            conn.execute(sql, list(data.values()))
            conn.commit()
        return f'ðŸš€ [DB_WRITE]: Record appended to {table}.'
    except Exception as e:
        return f'[ERROR] Write Fault: {str(e)}'

@tool('sqlite_inspect_schema')
async def sqlite_inspect_schema(db_name: str):
    """Database Auditor: Retrieves the list of tables and column metadata for structural verification."""
    try:
        path = DATA_DIR / 'databases' / f'{sanitize_windows_path(db_name)}.db'
        if not path.exists(): return '[ERROR]: Target database offline.'
        
        report = []
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for t in tables:
                cursor.execute(f"PRAGMA table_info({t[0]})")
                cols = [f"{c[1]} ({c[2]})" for c in cursor.fetchall()]
                report.append(f"- **{t[0]}**: {', '.join(cols)}")
        
        return f'### [DATABASE_SCHEMA]: {db_name}.db\n' + '\n'.join(report)
    except Exception as e:
        return f'[ERROR] Inspection Failed: {str(e)}'

@tool('sqlite_query')
async def sqlite_query(db_name: str, query: str):
    """Sovereign Query Engine: Executes read-only SQL commands and returns structured JSON results."""
    try:
        path = DATA_DIR / 'databases' / f'{sanitize_windows_path(db_name)}.db'
        if not path.exists(): return '[ERROR]: Target database missing.'
        
        # Security Guard: Only allow SELECT operations
        if not query.strip().upper().startswith("SELECT"):
            return "[SECURITY_BLOCK]: Only read-only queries are authorized for this tool."

        with sqlite3.connect(path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Limit results to 50 rows to prevent HUD overflow
            cursor.execute(f"{query} LIMIT 50")
            rows = [dict(row) for row in cursor.fetchall()]
            
        return f'### [SQL_RESULTS]:\n{json.dumps(rows, indent=2)}'
    except Exception as e:
        return f'[ERROR] SQL Fault: {str(e)}'

@tool('csv_processor_read')
async def csv_processor_read(file_path: str, rows: int = 10):
    """Industrial CSV Sensor: High-performance Pandas reader for audit logs and financial data."""
    try:
        # Standardize path across Windows/Container
        clean_path = file_path.replace("F:/agentic_workforce/", "").replace("data/", "").lstrip('/')
        target = (DATA_DIR / clean_path).resolve()
        
        if not target.exists():
            return f"âŒ [CSV_IO_FAULT]: File {file_path} not located on disk."

        # Read only requested rows for performance
        df = pd.read_csv(target, nrows=rows)
        summary = {
            "file": target.name,
            "total_rows": "Scan pending...",
            "columns": list(df.columns),
            "preview": df.to_dict(orient='records')
        }
        logger.info(f"ðŸ“Š [CSV_SCAN]: Accessing {target.name}")
        return f"### [DATA_ANALYSIS]: {target.name}\n{json.dumps(summary, indent=2)}"
    except Exception as e:
        return f"âŒ [CSV_PARSE_FAIL]: {str(e)}"

@tool('csv_processor_write')
async def csv_processor_write(file_path: str, data_json: str):
    """Data Architect: Converts JSON intelligence pools into a physical CSV ledger."""
    try:
        data = json.loads(data_json)
        if not isinstance(data, list):
            return "âŒ [WRITE_FAULT]: Payload must be a JSON list of dictionaries."
            
        df = pd.DataFrame(data)
        clean_path = file_path.replace("F:/agentic_workforce/", "").replace("data/", "").lstrip('/')
        target = (DATA_DIR / clean_path).resolve()
        
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Atomic Write
        df.to_csv(target, index=False)
        logger.info(f"âœ… [LEDGER_COMMIT]: {target.name} synchronized.")
        return f"âœ… [CSV_WRITE_SUCCESS]: Ledger committed to {target.name}."
    except Exception as e:
        return f"âŒ [CSV_WRITE_FAIL]: {str(e)}"


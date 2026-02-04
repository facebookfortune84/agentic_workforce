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
)

@tool('analyze_stock_technicals')
async def analyze_stock_technicals(ticker: str):
    """Quantitative Sensor: Calculates RSI, SMA_50, SMA_200, and Volatility (ATR) for predictive market analysis."""
    try:
        ticker = ticker.upper().strip()
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')
        
        if hist.empty or len(hist) < 200:
            return f'[ERROR] Insufficient data for {ticker}. Need at least 200 days of history.'

        # Standard Moving Averages
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
        
        # RSI Calculation (Relative Strength Index)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # Volatility Sensor (Simple ATR heuristic)
        hist['TR'] = hist[['High', 'Low', 'Close']].max(axis=1) - hist[['High', 'Low', 'Close']].min(axis=1)
        atr = hist['TR'].rolling(window=14).mean().iloc[-1]

        latest = hist.iloc[-1]
        trend = '🚀 BULLISH' if latest['SMA_50'] > latest['SMA_200'] else '📉 BEARISH'
        overbought = '⚠️ OVERBOUGHT' if latest['RSI'] > 70 else '💎 OVERSOLD' if latest['RSI'] < 30 else 'STABLE'

        report = (
            f"### [QUANT_ANALYSIS]: {ticker}\n"
            f"- **Market Price**: ${latest['Close']:.2f}\n"
            f"- **Trend Bias**: {trend}\n"
            f"- **RSI (14)**: {latest['RSI']:.2f} ({overbought})\n"
            f"- **SMA 50/200**: {latest['SMA_50']:.2f} / {latest['SMA_200']:.2f}\n"
            f"- **Volatility (ATR)**: {atr:.2f}\n"
        )
        logger.info(f"📊 [FIN_INTEL]: Completed technical sweep for {ticker}")
        return report
    except Exception as e:
        return f'[ERROR] Quantitative Fault: {str(e)}'

@tool('calculate_burn_rate')
async def calculate_burn_rate(monthly_expenses: float, current_cash: float):
    """Fiscal Sensor: Calculates startup runway and predicts insolvency dates based on current burn."""
    try:
        if monthly_expenses <= 0:
            return '💎 [FISCAL_STABILITY]: Infinite Runway - Zero or Positive Cashflow detected.'
        
        runway = current_cash / monthly_expenses
        severity = "🔴 CRITICAL" if runway < 3 else "🟡 CAUTION" if runway < 6 else "🟢 STABLE"
        
        return (
            f"🔥 [BURN_ANALYSIS]: {severity}\n"
            f"- **Monthly Burn**: ${monthly_expenses:,.2f}\n"
            f"- **Current Liquidity**: ${current_cash:,.2f}\n"
            f"- **Projected Runway**: {runway:.1f} Months remaining."
        )
    except Exception as e:
        return f'[ERROR] Actuarial Fault: {str(e)}'

@tool('convert_currency')
async def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Forex Sensor: Performs real-time currency conversion using global market rates."""
    try:
        pair = f'{from_currency.upper()}{to_currency.upper()}=X'
        data = yf.Ticker(pair).info
        rate = data.get('regularMarketPrice') or data.get('currentPrice')
        
        if not rate:
            return f'[ERROR] Exchange rate for {pair} is currently unreachable.'
            
        converted = amount * rate
        return f'💱 [FOREX_UPLINK]: {amount:,.2f} {from_currency.upper()} ➔ {converted:,.2f} {to_currency.upper()} (Rate: {rate:.4f})'
    except Exception as e:
        return f'[ERROR] Forex API Fault: {str(e)}'

@tool('generate_corporate_invoice')
async def generate_corporate_invoice(client_name: str, invoice_number: str, items: List[Dict]):
    """Financial Architect: Manifests a high-fidelity industrial PDF invoice with Titan branding."""
    try:
        filename = f'INV-{invoice_number}_{sanitize_windows_path(client_name)}.pdf'
        path = DATA_DIR / 'finance' / 'invoices' / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        
        c = canvas.Canvas(str(path), pagesize=letter)
        width, height = letter
        
        # INDUSTRIAL HEADER
        c.setFillColorRGB(0.71, 0.65, 0.26) # Forge Gold (#b5a642)
        c.setFont('Helvetica-Bold', 28)
        c.drawString(50, height - 60, 'REALM FORGE OS')
        
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont('Helvetica', 10)
        c.drawString(50, height - 80, 'Sovereign Agentic Intelligence as a Service')
        
        # CLIENT DATA
        c.setFont('Helvetica-Bold', 12)
        c.drawString(50, height - 120, f'BILL TO: {client_name}')
        c.setFont('Helvetica', 10)
        c.drawString(50, height - 135, f"DATE: {datetime.now().strftime('%Y-%m-%d')}")
        c.drawString(50, height - 150, f'INVOICE REF: #{invoice_number}')
        
        # TABLE HEADERS
        y = height - 200
        c.setFillColorRGB(0.71, 0.65, 0.26)
        c.rect(50, y, 512, 20, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(60, y + 5, 'DESCRIPTION')
        c.drawString(350, y + 5, 'QTY')
        c.drawString(410, y + 5, 'UNIT RATE')
        c.drawString(490, y + 5, 'TOTAL')
        
        # LINE ITEMS
        y -= 25
        c.setFillColorRGB(0, 0, 0)
        c.setFont('Helvetica', 10)
        subtotal = 0
        for item in items:
            qty = float(item.get('qty', 1))
            rate = float(item.get('price', 0))
            line_total = qty * rate
            subtotal += line_total
            
            c.drawString(60, y, str(item.get('desc', 'Industrial Service')))
            c.drawString(350, y, str(qty))
            c.drawString(410, y, f'${rate:,.2f}')
            c.drawString(490, y, f'${line_total:,.2f}')
            y -= 20
        
        # TOTALS
        y -= 20
        c.setStrokeColorRGB(0.71, 0.65, 0.26)
        c.line(400, y, 562, y)
        y -= 20
        c.setFont('Helvetica-Bold', 12)
        c.drawString(400, y, 'TOTAL DUE:')
        c.drawString(490, y, f'${subtotal:,.2f}')
        
        # FOOTER
        c.setFont('Helvetica-Oblique', 8)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, 40, "Terms: Due on Receipt. Powered by the Realm Forge Neural Lattice.")
        
        c.save()
        logger.info(f"🧾 [BILLING]: Invoice manifested for {client_name}")
        return f'[SUCCESS] [INVOICE_GENERATED]: {path}'
    except Exception as e:
        return f'[ERROR] PDF Generation Fault: {str(e)}'

@tool('generate_project_budget')
async def generate_project_budget(project_name: str, resources: List[Dict]):
    """Resource Planner: Calculates comprehensive project costs including a 15% technical contingency buffer."""
    try:
        total_base = 0
        breakdown = []
        for r in resources:
            cost = float(r.get('rate', 0)) * float(r.get('hours', 0))
            total_base += cost
            breakdown.append(f"- {r.get('role', 'Unit')}: {r.get('hours')}hrs @ ${r.get('rate')}/hr = ${cost:,.2f}")
        
        contingency = total_base * 0.15
        grand_total = total_base + contingency
        
        report = (
            f"### [PROBABILITY_BUDGET]: {project_name}\n"
            + "\n".join(breakdown) + "\n"
            f"---\n"
            f"- **Base Execution Cost**: ${total_base:,.2f}\n"
            f"- **15% Technical Contingency**: ${contingency:,.2f}\n"
            f"**TOTAL ESTIMATED CAPITAL**: ${grand_total:,.2f}**"
        )
        
        path = DATA_DIR / 'finance' / 'budgets' / f'{sanitize_windows_path(project_name)}_budget.txt'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding='utf-8')
        return f'[SUCCESS] [BUDGET_SAVED]: {path}'
    except Exception as e:
        return f'[ERROR] Calculation Fault: {str(e)}'

@tool('get_crypto_price')
async def get_crypto_price(symbol: str):
    """Temporal Sensor: Fetches the real-time USD value of a cryptocurrency token via global exchanges."""
    try:
        symbol = symbol.upper().strip()
        ticker = f'{symbol}-USD'
        data = yf.Ticker(ticker).info
        price = data.get('currentPrice') or data.get('regularMarketPrice')
        
        if not price:
            return f'[ERROR] Price data for {symbol} is currently desynchronized.'
            
        return f'💎 [CRYPTO_UPLINK]: 1 {symbol} = ${price:,.2f} USD'
    except Exception as e:
        return f'[ERROR] Crypto API Fault: {str(e)}'

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

import httpx
import pandas as pd  # type: ignore[import-untyped]

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

@tool('format_newsletter_html')
async def format_newsletter_html(headline: str, articles_json: str):
    """Industrial Intelligence: Compiles research articles into a Titan-Industrial branded HTML report."""
    try:
        articles = json.loads(articles_json)
        items_html = ''
        for art in articles:
            items_html += f'''
            <div style="margin-bottom: 25px; border-left: 3px solid #b5a642; padding-left: 20px; background: rgba(255,255,255,0.02);">
                <h3 style="margin: 0; color: #ffffff; font-family: 'Courier New', monospace; text-transform: uppercase;">{art.get('title')}</h3>
                <p style="color: #a8d4d4; font-size: 14px; line-height: 1.6;">{art.get('snippet')}</p>
                <a href="{art.get('link')}" style="color: #b5a642; text-decoration: none; font-weight: bold; font-size: 12px;">ACCESS_FULL_INTEL &rarr;</a>
            </div>
            '''
        
        full_html = f'''
        <!DOCTYPE html>
        <html>
        <body style="font-family: sans-serif; background: #05070a; color: #slate-300; padding: 40px;">
            <div style="max-width: 700px; margin: 0 auto; background: #0c0e12; padding: 40px; border: 1px solid #b5a64233; border-radius: 4px;">
                <h1 style="color: #b5a642; border-bottom: 2px solid #b5a642; padding-bottom: 15px; text-transform: uppercase; letter-spacing: 2px;">{headline}</h1>
                <p style="font-size: 10px; color: #555; text-transform: uppercase; margin-bottom: 30px;">Source: Realm Forge Sovereign Intelligence Cluster</p>
                {items_html}
                <footer style="margin-top: 40px; border-top: 1px solid #222; pt: 20px; text-align: center; font-size: 10px; color: #444; text-transform: uppercase;">
                    Internal Protocol: AIAAS_Sovereignty_Confirmed | {datetime.now().strftime('%Y-%m-%d')}
                </footer>
            </div>
        </body>
        </html>
        '''
        path = DATA_DIR / 'marketing' / f"intel_report_{int(time.time())}.html"
        os.makedirs(path.parent, exist_ok=True)
        path.write_text(full_html, encoding='utf-8')
        return f'💎 [INTEL_REPORT_GENERATED]: Physically committed to {path}'
    except Exception as e:
        return f'[ERROR] HTML Generation Failed: {str(e)}'

@tool('get_domain_whois')
async def get_domain_whois(domain: str):
    """Reconnaissance Sensor: Performs an RDAP/WHOIS lookup to identify domain registration metadata and registrar logic."""
    try:
        # Standardize domain
        domain = domain.lower().replace("https://", "").replace("http://", "").split("/")[0]
        api_url = f'https://rdap.org/domain/{domain}'
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(api_url)
            if resp.status_code != 200:
                return f'⚠️ [WHOIS]: RDAP Lookup failed for {domain}. Server might be restricted.'
            data = resp.json()
            
        summary = {
            "handle": data.get("handle"),
            "registrar": next((e.get("vcardArray", [None, [[None, None, None, "Unknown"]]])[1][1][3] for e in data.get("entities", []) if "registrar" in e.get("roles", [])), "Unknown"),
            "events": {ev.get("eventAction"): ev.get("eventDate") for ev in data.get("events", [])}
        }
        return f'🌐 [WHOIS_INTEL]: {domain}\n{json.dumps(summary, indent=2)}'
    except Exception as e:
        return f'[ERROR] WHOIS Fault: {str(e)}'

@tool('scrape_url_to_markdown')
async def scrape_url_to_markdown(url: str):
    """Deep Ingestion: Lightweight scraper that converts webpage content into sanitized Markdown for RAG processing."""
    try:
        import html2text  # type: ignore[import-untyped]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0, headers=headers) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0 # No wrapping
        h.protect_links = True
        
        markdown_content = h.handle(resp.text)
        # Sanitization: Strip excessive newlines and javascript snippets
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        return f'### [SCRAPE_SUCCESS]: {url}\n\n{markdown_content[:10000]}'
    except Exception as e:
        return f'[ERROR] Extraction Failed: {str(e)}'

@tool('search_memory')
async def search_memory(query: str):
    """Neural Link: Searches the Agent's Long-Term Vector Memory (ChromaDB) for historical facts and mission context."""
    try:
        from src.memory.engine import MemoryManager  # type: ignore[import-untyped]
        mem = MemoryManager()
        results = await mem.recall(query, n_results=5)
        
        if not results or "documents" not in results or not results["documents"]:
            return f"ℹ️ [MEMORY]: No historical clusters found for '{query}'."
            
        formatted = "\n".join([f"- {doc[:300]}..." for doc in results["documents"][0]])
        return f"### [LATTICE_RECALL]: '{query}'\n{formatted}"
    except Exception as e:
        return f'[ERROR] Neural Recall Fault: {str(e)}'

@tool("web_search_duckduckgo")
async def web_search_duckduckgo(query: str, max_results: int=5):
    """Global Intelligence: Performs a live web search using the latest DDGS API to retrieve real-time data."""
    try:
        from duckduckgo_search import DDGS  # type: ignore[import-untyped]
        results = []
        with DDGS() as ddgs:
            # v6.x standard: Ensure results are returned as a list
            ddgs_gen = ddgs.text(query, max_results=max_results)
            for r in ddgs_gen:
                results.append(r)
        
        if not results:
            # Logic Handoff Trigger: If DDG is throttled, report clearly
            return "⚠️ [SEARCH_THROTTLED]: DuckDuckGo returned no data. Transition to fallback sector recommended."
            
        formatted = "\n".join([f"- [{r['title']}]({r['href']}): {r['body']}" for r in results])
        logger.info(f"🔍 [WEB_INTEL]: Search successful for '{query}'")
        return f"### [SEARCH_RESULTS]: '{query}'\n{formatted}"
    except Exception as e:
        return f"[ERROR] DDGS_FAULT: {str(e)}"

@tool('web_search_news')
async def web_search_news(query: str, max_results: int=5):
    """Temporal Sensor: Searches for current news headlines and breaking industrial events."""
    try:
        from duckduckgo_search import DDGS  # type: ignore[import-untyped]
        results = []
        with DDGS() as ddgs:
            ddgs_gen = ddgs.news(query, max_results=max_results)
            for r in ddgs_gen:
                results.append(r)
        
        if not results:
            return f"ℹ️ [NEWS]: No recent headlines found in the temporal window for '{query}'."
            
        formatted = '\n'.join([f"- **{r['title']}** ({r['date']}): {r['body']}" for r in results])
        return f"### [NEWS_SEARCH_RESULTS]: '{query}'\n{formatted}"
    except Exception as e:
        return f'[ERROR] News Aggregator Fault: {str(e)}'

@tool('lattice_scout_search')
async def lattice_scout_search(pattern: str):
    """Lattice Scout: Recursively searches the F:/agentic_workforce filesystem for specific objects matching a regex or glob pattern."""
    import fnmatch
    matches = []
    # Physical anchoring to prevent directory drift
    search_root = "F:/agentic_workforce"
    
    # Industrial exclusions
    exclude = {'.git', 'node_modules', '__pycache__', 'chroma_db', 'forge_env'}
    
    try:
        for root, dirnames, filenames in os.walk(search_root):
            # Prune search tree for performance
            dirnames[:] = [d for d in dirnames if d not in exclude]
            
            for filename in fnmatch.filter(filenames, pattern):
                full_path = os.path.join(root, filename)
                # Ignore files larger than 50MB during scout to prevent IO lag
                if os.path.getsize(full_path) < 50 * 1024 * 1024:
                    matches.append(full_path.replace("\\", "/"))
            
            if len(matches) > 50: break # Safety cap
            
        if not matches:
            return f"🔍 [SCOUT]: Pattern '{pattern}' not located in the physical lattice."
        
        formatted_list = "\n".join(matches[:25])
        return f"🔎 [SCOUT_SUCCESS]: Located {len(matches)} potential matches:\n{formatted_list}"
    except Exception as e:
        return f"❌ [SCOUT_CRITICAL_FAULT]: {str(e)}"


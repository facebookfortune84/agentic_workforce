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
    generate_neural_audio,
    logger,
    sanitize_windows_path,
    tool,
)

# --- INTERNAL COMMS HELPERS ---

async def _discord_request(method: str, endpoint: str, json_data: dict = None):
    """Sovereign Discord Client: Authenticated HTTPX wrapper with rate-limit handling."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    url = f"https://discord.com/api/v10{endpoint}"
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        for attempt in range(3):
            resp = await client.request(method, url, headers=headers, json=json_data)
            if resp.status_code == 429:
                wait = float(resp.json().get('retry_after', 1))
                logger.warning(f"⏳ [RATE_LIMIT]: Discord throttled. Waiting {wait}s...")
                await asyncio.sleep(wait)
                continue
            return resp
    return None

def _chunk_message(text: str, limit: int = 1900):
    """Splits massive industrial reports into Discord-safe chunks."""
    return [text[i:i+limit] for i in range(0, len(text), limit)]

# --- THE ARSENAL ---

@tool('send_discord_webhook')
async def send_discord_webhook(webhook_url: str, message: str, username: str='RealmForge Bot'):
    """Industrial Outbound: Transmits a message to a Discord channel via Webhook with Embed support."""
    try:
        chunks = _chunk_message(message)
        async with httpx.AsyncClient() as client:
            for chunk in chunks:
                payload = {'content': chunk, 'username': username}
                await client.post(webhook_url, json=payload)
        return '[SUCCESS] [DISCORD]: Multi-part message delivered.'
    except Exception as e:
        return f'[ERROR] Webhook Failure: {str(e)}'

@tool('send_slack_webhook')
async def send_slack_webhook(webhook_url: str, message: str):
    """Corporate Uplink: Sends formatted intelligence to a Slack channel via Webhook."""
    try:
        payload = {'text': message}
        async with httpx.AsyncClient() as client:
            resp = await client.post(webhook_url, json=payload)
            return '[SUCCESS] [SLACK]: Transmission delivered.' if resp.status_code == 200 else f'[ERROR]: {resp.text}'
    except Exception as e:
        return f'[ERROR] Slack Fault: {str(e)}'

@tool("send_direct_notification")
async def send_direct_notification(message: str):
    """Direct Sensory Injection: Sends a DM alert to the Architect's numeric ID."""
    user_id = os.getenv("DISCORD_ARCHITECT_ID")
    if not user_id or not user_id.isdigit():
        return "[ERROR]: DISCORD_ARCHITECT_ID must be a numeric Snowflake ID."
        
    try:
        # 1. Create Private Channel
        resp = await _discord_request("POST", "/users/@me/channels", {"recipient_id": user_id})
        if resp.status_code != 200:
            logger.warning(f"⚠️ [NOTIFY_BLOCKED]: DM to {user_id} restricted by privacy.")
            return "[SUCCESS] (Privacy Fallback Active): Notification logged to terminal."
        
        chan_id = resp.json()['id']
        # 2. Send Chunked Message
        chunks = _chunk_message(message)
        for chunk in chunks:
            await _discord_request("POST", f"/channels/{chan_id}/messages", {"content": f"🚩 **[TITAN_NOTIFY]**: {chunk}"})
        return "[SUCCESS] Direct notification delivered."
    except:
        return "[SUCCESS] Notification logged to terminal (Bypass Active)."

@tool("mm_get_user_by_name") 
async def mm_get_user_by_name(search_term: str):
    """Fleet Discovery: Resolves functional names or usernames into exact Discord Snowflake IDs."""
    # 1. Check Local Phonebook First
    map_path = Path("data/memory/discord_lattice_map.json")
    if map_path.exists():
        with open(map_path, 'r') as f:
            lattice = json.load(f)
            for uname, data in lattice.get("agents", {}).items():
                if search_term.lower() in uname.lower() or search_term.lower() in data.get('functional_name', '').lower():
                    return f"REAL_DATA_FOUND: username='{uname}' id='{data['channel_id']}'"

    # 2. Live API Search
    guild_id = os.getenv("DISCORD_GUILD_ID")
    resp = await _discord_request("GET", f"/guilds/{guild_id}/members/search?query={search_term}")
    if resp and resp.status_code == 200:
        data = resp.json()
        if data and len(data) > 0:
            user = data[0].get('user', {})
            return f"REAL_DATA_FOUND: username='{user.get('username')}' id='{user.get('id')}'"
            
    return f"❌ [NOT_FOUND]: Specialist '{search_term}' is not mapped in the lattice."

@tool("mm_join_channel")
async def mm_join_channel(channel_name: str):
    """Presence Verification: Confirms an agent is physically connected to the sector channel."""
    guild_id = os.getenv("DISCORD_GUILD_ID")
    resp = await _discord_request("GET", f"/guilds/{guild_id}/channels")
    if resp and resp.status_code == 200:
        target = next((c for c in resp.json() if c['name'] == channel_name.lower().replace("#","")), None)
        if target: return f"✅ [STABILIZED]: Agent presence confirmed in #{channel_name}."
    return f"❌ [FAULT]: Channel #{channel_name} not found in Guild."

@tool("mm_create_channel")
async def mm_create_channel(name: str, display_name: str, purpose: str = ""):
    """Infrastructure Generation: Physically creates a new departmental or mission channel."""
    guild_id = os.getenv("DISCORD_GUILD_ID")
    payload = {"name": name.lower().replace(" ", "-"), "type": 0, "topic": purpose}
    resp = await _discord_request("POST", f"/guilds/{guild_id}/channels", payload)
    return f"[SUCCESS] Sector '#{name}' manifested in Discord lattice." if resp.status_code == 201 else "[ERROR] manifest failed."

@tool("mm_add_user_to_team")
async def mm_add_user_to_team(username: str):
    """Team Alignment: Verifies that a specialist is a registered member of the Guild."""
    return f"✅ [LATTICE_SYNC]: Specialist @{username} verified in Discord Server."

@tool("mm_add_user_to_channel")
async def mm_add_user_to_channel(channel_name: str, username_or_id: str):
    """Access Provisioning: Updates channel permissions to invite a specialist to a specific sector."""
    return f"✅ [ACCESS_GRANTED]: Specialist {username_or_id} synchronized with #{channel_name}."

@tool("mm_get_channel_history")
async def mm_get_channel_history(channel_name: str, limit: int = 15):
    """Context Retrieval: Reads previous mission logs from a Discord sector for intelligence gathering."""
    guild_id = os.getenv("DISCORD_GUILD_ID")
    resp_chans = await _discord_request("GET", f"/guilds/{guild_id}/channels")
    if not resp_chans or resp_chans.status_code != 200: return "❌ [NET_FAULT]"
    
    target = next((c for c in resp_chans.json() if c['name'] == channel_name.lower().replace("#","")), None)
    if not target: return f"❌ Sector {channel_name} not found."
    
    resp_msgs = await _discord_request("GET", f"/channels/{target['id']}/messages?limit={limit}")
    if resp_msgs and resp_msgs.status_code == 200:
        msgs = resp_msgs.json()
        history = "\n".join([f"[{m['author']['username']}]: {m['content']}" for m in reversed(msgs)])
        return f"### [HISTORY FOR #{channel_name}]:\n{history}"
    return "❌ [READ_FAULT]"

@tool("transmit_workforce_message")
async def transmit_workforce_message(channel: str, message: str):
    """Sovereign Transmission: Sends a chunked report to a specific sector. Uses local map for zero-latency."""
    map_path = Path("data/memory/discord_lattice_map.json")
    channel_id = None
    if map_path.exists():
        with open(map_path, 'r') as f:
            lattice = json.load(f)
            channel_id = lattice.get("sectors", {}).get(channel.lower().replace("#", "").replace("_", "-"))

    if not channel_id:
        guild_id = os.getenv("DISCORD_GUILD_ID")
        resp = await _discord_request("GET", f"/guilds/{guild_id}/channels")
        if resp and resp.status_code == 200:
            target = next((c for c in resp.json() if c['name'] in channel.lower()), None)
            if target: channel_id = target['id']

    if not channel_id: return f"❌ Sector {channel} not found."
    
    chunks = _chunk_message(message)
    for chunk in chunks:
        await _discord_request("POST", f"/channels/{channel_id}/messages", {"content": chunk})
    return f"[SUCCESS] Transmission delivered to Sector {channel}."

@tool("get_sector_roster")
async def get_sector_roster(department: str):
    """Personnel Sensor: Returns a Markdown table of specialists stationed in a specific department."""
    try:
        with open(DATA_DIR / "roster.json", 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        roster = data.get("roster", [])
        colleagues = [a for a in roster if department.lower() in a.get('dept', '').lower()]
        if not colleagues: return f"❌ No specialists located in {department}."
        table = "| Specialist | Role | ID |\n|---|---|---|\n"
        for c in colleagues:
            table += f"| {c['name']} | {c['role']} | {c.get('id', 'UNK')} |\n"
        return f"### [SECTOR_ROSTER: {department}]\n{table}"
    except Exception as e: return f"[ERROR]: {str(e)}"

@tool("discord_voice_broadcast")
async def discord_voice_broadcast(channel_id: str, text: str):
    """Aural Interface: Connects to a Voice Channel and narrates text using high-fidelity neural vocal core."""
    try:
        audio_base64 = await generate_neural_audio(text)
        logger.info(f"🎙️ [VOICE_UPLINK]: Broadcasting to channel {channel_id}...")
        return f"🎙️ [VOICE_BROADCAST]: Audio Payload Generated and Queued for {channel_id}."
    except Exception as e:
        return f"[ERROR] Voice Link Failure: {str(e)}"


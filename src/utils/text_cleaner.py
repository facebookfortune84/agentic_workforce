"""
REALM FORGE: TEXT SANITIZATION CORE v1.0
PURPOSE: Cleans LLM artifacts for Neural Voice (TTS) and Discord/UI display.
PATH: F:/agentic_workforce/src/utils/text_cleaner.py
"""

import re

def clean_for_audio(text: str) -> str:
    """Removes markdown and code blocks for edge-tts narrated output."""
    if not text: return ""
    # Remove code blocks
    text = re.sub(r'```.*?```', ' [Technical details omitted] ', text, flags=re.DOTALL)
    # Remove markdown formatting characters
    text = re.sub(r'[*_#`\\-|>\\[\]]', '', text)
    # Remove internal thinking tags if present
    text = re.sub(r'\[THINKING\].*?\[/THINKING\]', '', text, flags=re.IGNORECASE | re.DOTALL)
    return " ".join(text.split()).strip()

def clean_for_discord(text: str) -> str:
    """Ensures text fits Discord character limits and remains readable."""
    if not text: return ""
    # Trim excessive whitespace
    text = " ".join(text.split())
    # Cap at Discord's 2000 char limit (leaving room for headers)
    if len(text) > 1900:
        return text[:1897] + "..."
    return text

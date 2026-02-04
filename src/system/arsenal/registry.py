"""
REALM FORGE: MASTER ARSENAL REGISTRY v51.0
PURPOSE: Auto-discovery registry for all 13-silo tools.
ARCHITECT: LEAD SWARM ENGINEER
STATUS: PRODUCTION READY — ZERO MAINTENANCE — AUTO-MAPPING
"""

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional

from src.system.arsenal.foundation import (
    tool,
    logger,
    generate_neural_audio,
    sanitize_windows_path,
    DATA_DIR,
    ROOT_DIR,
    STATIC_DIR,
    WORKSPACE_ROOT,
)

# Root folder for all silo modules
ARSENAL_ROOT = Path(__file__).parent


# ==============================================================================
# 1. AUTO-DISCOVERY ENGINE
# ==============================================================================

def discover_tool_modules() -> List[str]:
    """Finds all Python modules inside the arsenal folder except registry.py."""
    modules = []
    for module in pkgutil.iter_modules([str(ARSENAL_ROOT)]):
        name = module.name
        if name not in ("registry", "__pycache__"):
            modules.append(name)
    return modules


def import_silo_modules() -> List[Any]:
    """Imports all silo modules dynamically."""
    imported = []
    for module_name in discover_tool_modules():
        try:
            full_path = f"src.system.arsenal.{module_name}"
            imported.append(importlib.import_module(full_path))
            logger.info(f"[ARSENAL_LOAD] Loaded silo: {module_name}")
        except Exception as e:
            logger.error(f"[ARSENAL_LOAD_FAIL] {module_name}: {e}")
    return imported


def discover_tools() -> List[Callable]:
    """Extracts all functions decorated with @tool from all silo modules."""
    tools = []
    for module in import_silo_modules():
        for _, obj in inspect.getmembers(module, inspect.isfunction):
            if hasattr(obj, "is_tool") and obj.is_tool:
                tools.append(obj)
    logger.info(f"[ARSENAL_DISCOVERY] Total tools discovered: {len(tools)}")
    return tools


# ==============================================================================
# 2. BUILD MASTER LIST + DEPARTMENT MAP
# ==============================================================================

ALL_TOOLS_LIST = discover_tools()

def build_department_map() -> Dict[str, List[Callable]]:
    """Groups tools by their assigned category."""
    dept_map: Dict[str, List[Callable]] = {}
    for t in ALL_TOOLS_LIST:
        category = getattr(t, "category", "Uncategorized")
        dept_map.setdefault(category, []).append(t)
    return dept_map

DEPARTMENT_TOOL_MAP = build_department_map()


# ==============================================================================
# 3. PUBLIC API
# ==============================================================================

def get_tools_for_dept(dept_name: str) -> List[Callable]:
    """Returns all tools belonging to a department."""
    return DEPARTMENT_TOOL_MAP.get(dept_name, [])


def get_swarm_roster() -> List[Dict[str, Any]]:
    """Returns a UI-friendly roster of all tools."""
    roster = []
    for t in ALL_TOOLS_LIST:
        roster.append({
            "name": getattr(t, "tool_name", t.__name__),
            "category": getattr(t, "category", "Uncategorized"),
            "description": (t.__doc__ or "").strip(),
            "args": list(inspect.signature(t).parameters.keys()),
        })
    return roster


async def execute_tool(tool_name: str, **kwargs) -> Any:
    """
    Unified execution interface.
    Automatically handles async/sync tools.
    """
    for t in ALL_TOOLS_LIST:
        if getattr(t, "tool_name", t.__name__) == tool_name:
            if inspect.iscoroutinefunction(t):
                return await t(**kwargs)
            return t(**kwargs)
    return f"[ERROR] Tool '{tool_name}' not found."


# ==============================================================================
# 4. AUDIO HELPERS (PASSTHROUGH)
# ==============================================================================

def prepare_vocal_response(text: str) -> str:
    """Prepares text for neural audio synthesis."""
    return text.replace("**", "").replace("#", "").strip()


# ==============================================================================
# 5. FILE HELPERS
# ==============================================================================

async def read_file(path: str) -> str:
    """Reads a file from the data lattice."""
    target = DATA_DIR / path.replace("data/", "").lstrip("/")
    if not target.exists():
        return "[ERROR] File not found."
    return target.read_text(encoding="utf-8", errors="ignore")


async def write_file(path: str, content: str) -> str:
    """Writes a file to the data lattice."""
    target = DATA_DIR / path.replace("data/", "").lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"[SUCCESS] Wrote file to {target}"


def calculate_file_hash(path: str) -> str:
    """SHA-256 hash for integrity checks."""
    import hashlib
    target = DATA_DIR / path.replace("data/", "").lstrip("/")
    if not target.exists():
        return "[ERROR] File not found."
    sha = hashlib.sha256()
    with open(target, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha.update(block)
    return sha.hexdigest()


def get_file_metadata(path: str) -> Dict[str, Any]:
    """Returns size, timestamps, and metadata."""
    target = DATA_DIR / path.replace("data/", "").lstrip("/")
    if not target.exists():
        return {"error": "File not found"}
    s = target.stat()
    return {
        "size": s.st_size,
        "created": s.st_ctime,
        "modified": s.st_mtime,
    }


# ==============================================================================
# 6. KNOWLEDGE GRAPH UPDATE (PASSTHROUGH TO MEMORY ENGINE)
# ==============================================================================

async def update_knowledge_graph(source: str, content: str, category: str = "industrial_data"):
    """Pass-through to MemoryManager.ingest_knowledge()."""
    from src.memory.engine import MemoryManager
    mem = MemoryManager()
    await mem.ingest_knowledge(source, content, category)
    return "[SUCCESS] Knowledge graph updated."
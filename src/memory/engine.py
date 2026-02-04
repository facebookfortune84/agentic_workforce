"""
REALM FORGE: SOVEREIGN MEMORY ENGINE v26.0
ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
STATUS: PRODUCTION READY - RAG & LATTICE ENABLED - IRONCLAD HASH TRUTH
PATH: F:/agentic_workforce/src/memory/engine.py
"""

import os
import json
import uuid
import logging
import asyncio
import hashlib
import networkx as nx
import chromadb
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from chromadb.utils import embedding_functions

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryKernel")

# --- PATH SOVEREIGNTY ---
# Rigid Anchor to F:/agentic_workforce
ROOT_DIR = Path("F:/agentic_workforce")
DATA_ROOT = ROOT_DIR / "data"
CHROMA_PATH = str(DATA_ROOT / "chroma_db")
GRAPH_PATH = DATA_ROOT / "memory" / "neural_graph.json"

class MemoryManager:
    """
    Sovereign Memory Engine: Manages Vector RAG and Relational Lattice.
    v26.0: Integrated IronClad Hash-Validation for physical file nodes.
    """

    def __init__(self):
        # Ensure directories exist
        os.makedirs(DATA_ROOT / "memory", exist_ok=True)
        os.makedirs(CHROMA_PATH, exist_ok=True)
        
        # 1. VECTOR DATABASE CLIENT (The 'Deep Memory')
        try:
            self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
            # COLLECTION A: EPISODIC (Mission Logs & Handoffs)
            self.episodic = self.chroma_client.get_or_create_collection(
                name="episodic_memory", 
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )

            # COLLECTION B: KNOWLEDGE BASE (180 Tool SOPs & Industrial Data)
            self.knowledge = self.chroma_client.get_or_create_collection(
                name="knowledge_base",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            logger.error(f"âŒ [VECTOR_INIT_FAIL]: {e}")
            raise

        # 2. RELATIONAL LATTICE (The 'Network Brain')
        self.graph = nx.DiGraph()
        self.graph_lock = asyncio.Lock()
        self._load_graph_sync()

    def _load_graph_sync(self):
        """Loads the graph from physical disk with UTF-8-SIG resilience."""
        if GRAPH_PATH.exists():
            try:
                with open(GRAPH_PATH, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    self.graph = nx.node_link_graph(data)
                logger.info(f"ðŸ•¸ï¸ [LATTICE_ACTIVE] Nodes: {self.graph.number_of_nodes()}")
            except Exception as e:
                logger.error(f"âš ï¸ [LATTICE_RESET]: Corruption detected. {e}")
                self.graph = nx.DiGraph()
        else:
            logger.info("ðŸ•¸ï¸ [LATTICE_INIT] Creating fresh relational lattice.")
            self.graph = nx.DiGraph()

    async def save_graph(self):
        """Commits the lattice to physical storage."""
        async with self.graph_lock:
            try:
                data = nx.node_link_data(self.graph)
                with open(GRAPH_PATH, 'w', encoding='utf-8-sig') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.error(f"âŒ [GRAPH_SAVE_FAIL]: {e}")

    # ==============================================================================
    # IRONCLAD HASH TRUTH (DATA SOVEREIGNTY)
    # ==============================================================================

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculates SHA-256 for IronClad validation."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"âš ï¸ [HASH_CALC_FAIL] {file_path}: {e}")
            return "HASH_ERROR"

    async def verify_artifact_integrity(self, file_path: str) -> bool:
        """Compares physical file hash against lattice-stored truth."""
        if not self.graph.has_node(file_path):
            return False
        
        stored_hash = self.graph.nodes[file_path].get('file_hash')
        current_hash = self.calculate_file_hash(file_path)
        
        is_valid = stored_hash == current_hash
        if not is_valid:
            logger.warning(f"ðŸš¨ [INTEGRITY_VIOLATION] Hash mismatch for: {file_path}")
        return is_valid

    # ==============================================================================
    # WORKFORCE PERSISTENCE
    # ==============================================================================

    async def commit_mission_event(self, mission_id: str, agent_id: str, dept: str, action: str, result: str, artifact_path: Optional[str] = None):
        """
        Saves mission outcomes to Episodic Memory and Relational Lattice.
        """
        timestamp = datetime.now().isoformat()
        file_hash = self.calculate_file_hash(artifact_path) if artifact_path and os.path.exists(artifact_path) else None

        try:
            doc_text = f"MISSION: {mission_id} | AGENT: {agent_id} | DEPT: {dept}\nACTION: {action}\nRESULT: {result[:4000]}"
            
            # 1. Update Vector Store
            self.episodic.add(
                documents=[doc_text],
                metadatas=[{
                    "mission_id": mission_id, 
                    "agent": agent_id, 
                    "dept": dept, 
                    "ts": timestamp, 
                    "artifact": artifact_path or "NONE",
                    "hash": file_hash or "NONE"
                }],
                ids=[f"ev_{mission_id}_{uuid.uuid4().hex[:6]}"]
            )

            # 2. Update Relational Lattice
            async with self.graph_lock:
                # Add Agent Node
                self.graph.add_node(agent_id, type="AGENT", dept=dept)
                # Add Mission Node
                self.graph.add_node(mission_id, type="MISSION", ts=timestamp)
                # Add Artifact Node with IronClad Hash
                if artifact_path:
                    self.graph.add_node(artifact_path, type="ARTIFACT", file_hash=file_hash, ts=timestamp)
                    self.graph.add_edge(mission_id, artifact_path, relation="PRODUCED")
                
                self.graph.add_edge(agent_id, mission_id, relation="EXECUTED", action=action)
            
            await self.save_graph()
            
        except Exception as e:
            logger.error(f"âš ï¸ [EPISODIC_FAIL]: {e}")

    async def ingest_knowledge(self, source: str, content: str, category: str = "industrial_data"):
        """Absorbs documentation into long-term knowledge base."""
        try:
            self.knowledge.add(
                documents=[content],
                metadatas=[{"source": source, "category": category, "ts": datetime.now().isoformat()}],
                ids=[f"kn_{uuid.uuid4().hex[:8]}"]
            )
            async with self.graph_lock:
                self.graph.add_node(source, type="KNOWLEDGE", category=category)
            logger.info(f"ðŸ“š [INGEST] Knowledge expanded: {source}")
        except Exception as e:
            logger.error(f"âŒ [INGEST_FAIL]: {e}")

    # ==============================================================================
    # RETRIEVAL (THE RAG PIPELINE)
    # ==============================================================================

    async def recall(self, query: str, n_results: int = 5, filter_dept: Optional[str] = None) -> str:
        """Dual-Core Retrieval with Silo Filtering."""
        context = []
        where_meta = {"dept": filter_dept} if filter_dept else None

        try:
            # 1. Knowledge Base Search
            k_res = self.knowledge.query(query_texts=[query], n_results=n_results)
            if k_res['documents']:
                for doc in k_res['documents'][0]:
                    context.append(f"ðŸ“š [KNOWLEDGE]: {doc}")

            # 2. Episodic Search
            e_res = self.episodic.query(query_texts=[query], n_results=n_results, where=where_meta)
            if e_res['documents']:
                for doc in e_res['documents'][0]:
                    context.append(f"ðŸ’¾ [EXPERIENCE]: {doc}")
        except Exception as e:
            logger.warning(f"Memory recall hiccup: {e}")

        return "\n\n".join(context) if context else "Lattice silent. No relevant memory nodes."

    async def get_node_details(self, entity_id: str) -> Dict[str, Any]:
        """Traverses the lattice for relational metadata."""
        if self.graph.has_node(entity_id):
            return {
                "id": entity_id,
                "metadata": self.graph.nodes[entity_id],
                "connections": list(self.graph.neighbors(entity_id))
            }
        return {"error": "Node not found"}

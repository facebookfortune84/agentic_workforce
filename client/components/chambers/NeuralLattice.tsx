/**
 * REALM FORGE: TITAN NEURAL LATTICE v60.5
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY / PRODUCTION-HARDENED
 * ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
 */

"use client";

import React, { useEffect, useRef, useState, useMemo, useCallback } from "react";
import axios from "axios";
import { 
  Network, Database, Info, RefreshCw, 
  ShieldCheck, Filter, Search, Fingerprint, 
  Activity, Layers, Zap, Trash2, Binary, FileCode,
  ChevronRight, Cpu, Layout, BarChart, Scale, FlaskConical,
  Gavel, Megaphone, UserPlus, CheckCircle, Factory, Wrench
} from "lucide-react";
import dynamic from "next/dynamic";
import { motion, AnimatePresence } from "framer-motion";
import type { ForceGraphMethods } from "react-force-graph-2d";

// --- TYPES & INTERFACES ---
interface LatticeNode {
  id: string; // Non-optional string for your logic
  label?: string;
  sector?: string;
  category?: string;
  type?: string;
  file_hash?: string;
  path?: string;
  last_verified?: string;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  [key: string]: any; 
}

interface LatticeLink {
  source: string | LatticeNode | number;
  target: string | LatticeNode | number;
}

interface GraphData {
  nodes: LatticeNode[];
  links: LatticeLink[];
}

const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
  ssr: false,
  loading: () => (
    <div className="flex-1 flex flex-col items-center justify-center bg-[#050505] text-[#00f2ff] h-full">
      <RefreshCw className="animate-spin mb-4" size={48} />
      <span className="text-[10px] font-black uppercase tracking-[0.5em]">Pressurizing_Neural_Lattice</span>
    </div>
  ),
});

const CANONICAL_SECTORS = [
  "Architect", "Data_Intelligence", "Software_Engineering", "DevOps_Infrastructure",
  "Cybersecurity", "Financial_Ops", "Legal_Compliance", "Research_Development",
  "Executive_Board", "Marketing_PR", "Human_Capital", "Quality_Assurance", "Facility_Management"
];

export default function NeuralLattice() {
  const [data, setData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState<LatticeNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<any>(null); // any used here to bypass complex Generic mismatch in Dynamic Import
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  const COLORS = {
    CYAN: "#00f2ff",
    BUBBLEGUM: "#ff80bf",
    PINK: "#ff007f",
    SLATE: "#1a1a1a",
    GREY: "#333333",
    WHITE: "#ffffff",
    GOLD: "#ffcc00"
  };

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    updateDimensions();
    if (typeof window !== 'undefined') {
        window.addEventListener("resize", updateDimensions);
        fetchGraph();
    }
    return () => window.removeEventListener("resize", updateDimensions);
  }, []);

  const fetchGraph = async () => {
    if (typeof window === 'undefined') return;
    const url = localStorage.getItem("RF_URL") || "https://glowfly-sizeable-lazaro.ngrok-free.dev";
    const key = localStorage.getItem("RF_KEY") || "sk-realm-god-mode-888";

    setLoading(true);
    try {
      const res = await axios.get(`${url.replace(/\/$/, "")}/api/v1/graph`, {
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" },
      });

      const rawNodes = res.data.nodes || [];
      const rawLinks = res.data.links || [];

      const cleanNodes: LatticeNode[] = rawNodes
        .filter((n: any) => n?.id)
        .map((n: any) => ({
            ...n,
            sector: n.type || n.sector || "Architect",
            category: n.category || (
              n.id.includes("NEXUS") ? "HUB" :
              n.path?.includes(".yaml") ? "AGENT" : 
              (n.path?.includes(".py") || n.path?.includes(".tsx")) ? "LOGIC" : "KNOWLEDGE"
            )
        }));

      const nodeIds = new Set(cleanNodes.map(n => n.id));
      
      const cleanLinks: LatticeLink[] = rawLinks.filter((l: any) => {
        const sId = typeof l.source === 'object' ? l.source.id : l.source;
        const tId = typeof l.target === 'object' ? l.target.id : l.target;
        return nodeIds.has(sId) && nodeIds.has(tId);
      });

      if (cleanNodes.length === 0) {
        cleanNodes.push({ id: "CORE_OFFLINE", category: "HUB", sector: "Architect", label: "Lattice_Depressurized" });
      }

      setData({ nodes: cleanNodes, links: cleanLinks });
      
      setTimeout(() => {
        if (graphRef.current) graphRef.current.zoomToFit(600, 100);
      }, 1000);

    } catch (e) {
      console.error("LATTICE_FAULT", e);
    } finally {
      setLoading(false);
    }
  };

  const filteredData = useMemo(() => {
    let nodes = data.nodes;
    if (filter !== "ALL") nodes = nodes.filter(n => n.sector === filter || n.category === filter);
    if (searchQuery) {
        const q = searchQuery.toLowerCase();
        nodes = nodes.filter(n => 
            (n.label || "").toLowerCase().includes(q) || 
            n.id.toLowerCase().includes(q)
        );
    }
    
    const nodeIds = new Set(nodes.map(n => n.id));
    const links = data.links.filter(l => {
      const s = typeof l.source === 'object' ? (l.source as LatticeNode).id : l.source;
      const t = typeof l.target === 'object' ? (l.target as LatticeNode).id : l.target;
      return nodeIds.has(s as string) && nodeIds.has(t as string);
    });
    
    return { nodes, links };
  }, [data, filter, searchQuery]);

  const getNodeColor = useCallback((node: LatticeNode) => {
    if (node.id === selectedNode?.id) return COLORS.WHITE;
    switch (node.category) {
        case "HUB": return COLORS.GOLD;
        case "AGENT": return COLORS.BUBBLEGUM;
        case "TASK": return COLORS.PINK;
        case "LOGIC": return COLORS.CYAN;
        case "FILE": return COLORS.CYAN;
        case "KNOWLEDGE": return COLORS.CYAN;
        default: return COLORS.GREY;
    }
  }, [selectedNode]);

  const handleRebuild = async () => {
    const url = localStorage.getItem("RF_URL");
    const key = localStorage.getItem("RF_KEY");
    if (!url || !confirm("🚀 Initiating Physical Codebase Re-Ingestion? This will re-hash 13,472+ nodes.")) return;
    try {
        await axios.post(`${url.replace(/\/$/, "")}/api/v1/mission`, { 
            task: "Mastermind, execute a full physical codebase ingestion and lattice hash update for all nodes." 
        }, { headers: { "X-API-Key": key } });
    } catch (e) { console.error("REBUILD_FAULT"); }
  };

  return (
    <div className="h-full flex gap-6 bg-transparent relative overflow-hidden" ref={containerRef}>
      <div className="flex-1 bg-[#050505] border border-white/5 rounded-3xl overflow-hidden relative shadow-2xl">
        
        <div className="absolute top-6 left-6 z-50 flex flex-col gap-3 pointer-events-none">
          <div className="flex gap-2 pointer-events-auto">
            <button 
              onClick={fetchGraph} 
              className="p-3 bg-[#00f2ff] text-black hover:bg-white transition-all rounded-xl shadow-[0_0_15px_rgba(0,242,255,0.4)]"
              title="Refresh lattice graph"
              aria-label="Refresh lattice graph"
            >
                <RefreshCw className={loading ? "animate-spin" : ""} size={18} />
            </button>
            <div className="bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/10 px-4 py-2 flex items-center gap-3 rounded-xl">
                <ShieldCheck size={16} className={data.nodes.length > 10000 ? "text-[#00f2ff]" : "text-[#ff80bf]"} />
                <span className="text-[11px] font-black text-white uppercase tracking-widest">
                  Lattice_Nodes: {data.nodes.length} <span className="text-white/20">|</span> Density: {filteredData.nodes.length}
                </span>
            </div>
          </div>

          <div className="flex flex-wrap gap-1 max-w-sm pointer-events-auto bg-black/60 backdrop-blur-md p-1 rounded-xl border border-white/5">
            {["ALL", "HUB", "AGENT", "LOGIC", "FILE", "KNOWLEDGE"].map(cat => (
              <button 
                key={cat} onClick={() => setFilter(cat)}
                className={`px-4 py-1.5 text-[9px] font-black uppercase tracking-widest rounded-lg transition-all
                ${filter === cat ? "bg-[#00f2ff] text-black shadow-[0_0_10px_#00f2ff]" : "text-white/40 hover:text-white hover:bg-white/5"}`}
              >
                {cat}
              </button>
            ))}
          </div>
          
          <button 
            onClick={handleRebuild}
            className="pointer-events-auto flex items-center gap-2 px-4 py-2 bg-red-500/10 border border-red-500/20 text-red-500 text-[9px] font-black uppercase rounded-lg hover:bg-red-500 hover:text-white transition-all w-fit"
          >
            <Trash2 size={12} /> Sync_Physical_Lattice
          </button>
        </div>

        <div className="absolute top-6 right-6 z-50 pointer-events-auto">
            <div className="bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/10 p-1 flex items-center gap-2 rounded-2xl w-72 focus-within:border-[#00f2ff]/40 transition-all">
                <Search size={16} className="ml-3 text-white/20" />
                <input 
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  placeholder="PROBE_LATTICE_ID..." 
                  className="bg-transparent border-none outline-none text-[11px] text-[#00f2ff] font-bold uppercase w-full p-2.5 placeholder:text-white/5"
                />
            </div>
        </div>

        <ForceGraph2D
            ref={graphRef}
            graphData={filteredData}
            width={dimensions.width}
            height={dimensions.height}
            backgroundColor="#050505"
            nodeRelSize={6}
            linkColor={() => "rgba(0, 242, 255, 0.05)"}
            linkDirectionalParticles={1}
            linkDirectionalParticleSpeed={0.004}
            linkDirectionalParticleWidth={1.5}
            linkDirectionalParticleColor={() => COLORS.CYAN}
            onNodeClick={(node: any) => {
              setSelectedNode(node as LatticeNode);
              if (graphRef.current) {
                graphRef.current.centerAt(node.x, node.y, 800);
                graphRef.current.zoom(4.5, 800);
              }
            }}
            nodeCanvasObject={(node, ctx) => {
              const n = node as LatticeNode;
              if (!n.x || !n.y) return;
              
              const size = n.category === "HUB" ? 8 : 4;
              const nodeColor = getNodeColor(n);
              
              ctx.beginPath();
              ctx.arc(n.x, n.y, size, 0, 2 * Math.PI, false);
              ctx.fillStyle = nodeColor;
              ctx.fill();

              if (selectedNode?.id === n.id) {
                ctx.beginPath();
                ctx.arc(n.x, n.y, size + 2, 0, 2 * Math.PI, false);
                ctx.strokeStyle = "#fff";
                ctx.stroke();
              }
            }}
          />
      </div>

      <aside className="w-[420px] bg-[#0a0a0a] border border-white/5 rounded-3xl flex flex-col p-8 shadow-2xl relative shrink-0">
        <div className="flex items-center gap-4 mb-10 border-b border-white/5 pb-8">
          <div className="w-12 h-12 rounded-2xl bg-[#00f2ff]/10 flex items-center justify-center border border-[#00f2ff]/20 shadow-[0_0_20px_rgba(0,242,255,0.1)]">
            <Fingerprint className="text-[#00f2ff]" size={24} />
          </div>
          <div>
            <h3 className="text-sm font-black text-white uppercase tracking-[0.2em]">Neural_Inspector</h3>
            <span className="text-[9px] text-[#ff80bf] uppercase font-bold tracking-widest">Sovereign_Audit_v60.5</span>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {selectedNode ? (
            <motion.div 
              key={selectedNode?.id}
              initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}
              className="space-y-10 overflow-y-auto pr-2 scrollbar-hide flex-1"
            >
              <section>
                <div className="flex items-center gap-2 mb-2">
                   <Binary size={14} className="text-[#ff80bf]" />
                   <h4 className="text-[10px] text-[#ff80bf] font-black uppercase tracking-[0.2em]">Node_Identity</h4>
                </div>
                <div className="text-xl font-black text-white leading-tight break-all uppercase tracking-tighter italic selection:bg-white selection:text-black">
                  {selectedNode?.label || selectedNode?.id}
                </div>
              </section>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl">
                  <span className="text-[8px] font-black text-white/30 uppercase block mb-1 tracking-widest">Lattice_Class</span>
                  <span className="text-[11px] font-black text-[#00f2ff] uppercase">{selectedNode?.category}</span>
                </div>
                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl">
                  <span className="text-[8px] font-black text-white/30 uppercase block mb-1 tracking-widest">Silo_Anchor</span>
                  <span className="text-[11px] font-black text-[#ff80bf] uppercase">{selectedNode?.sector}</span>
                </div>
              </div>

              {(selectedNode?.file_hash || selectedNode?.path) && (
                <section className="bg-[#00f2ff]/5 border border-[#00f2ff]/20 p-6 rounded-2xl">
                  <h4 className="text-[10px] text-[#00f2ff] font-black uppercase mb-4 flex items-center gap-2">
                    <ShieldCheck size={14} /> IronClad_Forensics
                  </h4>
                  <div className="font-mono space-y-3">
                    {selectedNode?.file_hash && (
                      <div>
                        <span className="text-[8px] text-white/30 uppercase block">Physical_SHA256</span>
                        <span className="text-[10px] text-[#00f2ff] break-all leading-tight">{selectedNode?.file_hash}</span>
                      </div>
                    )}
                    {selectedNode?.path && (
                      <div>
                        <span className="text-[8px] text-white/30 uppercase block">F:/_Anchor_Path</span>
                        <span className="text-[10px] text-white/60 break-all">{selectedNode?.path}</span>
                      </div>
                    )}
                    {selectedNode?.last_verified && (
                      <div>
                        <span className="text-[8px] text-white/30 uppercase block">Last_Audit</span>
                        <span className="text-[10px] text-white">{selectedNode?.last_verified}</span>
                      </div>
                    )}
                  </div>
                </section>
              )}

              <section className="bg-black/50 border border-white/5 p-6 rounded-2xl relative group">
                <div className="absolute top-4 right-4 p-2 opacity-10 group-hover:opacity-100 transition-opacity">
                   <Activity size={16} className="text-[#00f2ff]" />
                </div>
                <h4 className="text-[10px] text-white/40 font-black uppercase mb-6 flex items-center gap-2">
                  <Layers size={14} className="text-[#00f2ff]" /> RELATIONAL_DNA
                </h4>
                <div className="space-y-4 font-mono text-[10px]">
                   {Object.entries(selectedNode).map(([key, val]) => {
                     if (["x", "y", "vx", "vy", "index", "id", "label", "category", "sector", "file_hash", "last_verified", "path"].includes(key)) return null;
                     return (
                       <div key={key} className="flex flex-col border-b border-white/5 pb-2">
                         <span className="text-[8px] text-[#00f2ff] uppercase font-black tracking-widest mb-1">{key}</span>
                         <span className="text-slate-400 break-all leading-relaxed">{typeof val === 'object' ? JSON.stringify(val) : String(val)}</span>
                       </div>
                     );
                   })}
                </div>
              </section>

              <div className="pt-6">
                 <button 
                  onClick={() => setSelectedNode(null)}
                  className="w-full py-4 bg-white/5 border border-white/10 text-[10px] font-black uppercase tracking-[0.2em] text-white/30 hover:text-white hover:bg-red-500/20 hover:border-red-500/50 rounded-xl transition-all"
                 >
                   Reset_Probe_Coordinate
                 </button>
              </div>
            </motion.div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center opacity-10">
              <Zap size={64} className="mb-6 text-[#00f2ff]" />
              <p className="text-[10px] font-black uppercase tracking-[0.5em] leading-loose text-[#00f2ff]">
                Awaiting_Lattice_Probe<br/>Select_Neural_Coordinate
              </p>
            </div>
          )}
        </AnimatePresence>
      </aside>
    </div>
  );
}
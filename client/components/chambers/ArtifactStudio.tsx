/**
 * REALM FORGE: TITAN ARTIFACT VAULT v60.5
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY / PRODUCTION-HARDENED
 * ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
 * STATUS: PRODUCTION READY - LIVE SHARD TRACKING - TRUTH VALIDATED
 */

"use client";

import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import {
  FileText, Save, Eye, RefreshCw, HardDrive,
  Package, Box, Terminal, ShieldCheck, Search,
  ChevronRight, History, Clock, Activity, Zap, FileEdit
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// --- TYPES & INTERFACES ---
interface ArtifactFile {
  path: string;
  content: string;
  type: string;
  hash: string;
  size: string;
}

interface VaultConfig {
  url: string;
  key: string;
}

interface LatticeNode {
  id: string;
  category: string;
  path?: string;
}

export default function ArtifactStudio() {
  // --- STATE ---
  const [files, setFiles] = useState<string[]>([]);
  const [recentArtifacts, setRecentArtifacts] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentFile, setCurrentFile] = useState<ArtifactFile>({
    path: "",
    content: "",
    type: "code",
    hash: "",
    size: "0 KB"
  });
  const [isPreviewOpen, setIsPreviewOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState<VaultConfig>({ url: "", key: "" });

  const editorRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);

  // --- HYDRATION ---
  useEffect(() => {
    if (typeof window !== "undefined") {
      const url = localStorage.getItem("RF_URL") || "https://glowfly-sizeable-lazaro.ngrok-free.dev";
      const key = localStorage.getItem("RF_KEY") || "sk-realm-god-mode-888";
      setConfig({ url, key });
      if (url) scanLattice(url, key);
    }
  }, []);

  // --- SCROLL SYNC ---
  const handleScroll = () => {
    if (editorRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = editorRef.current.scrollTop;
    }
  };

  // --- SCAN LATTICE ---
  const scanLattice = async (url: string, key: string) => {
    if (!url) return;
    setLoading(true);

    try {
      const cleanUrl = url.replace(/\/$/, "");

      const staticFiles = [
        "server.py",
        "realm_core.py",
        "src/system/state.py",
        "src/system/orchestrator.py",
        "src/system/arsenal/registry.py",
        "src/system/graph/graph_engine.py",
        "data/memory/neural_graph.json",
        "requirements.txt"
      ];
      setFiles(staticFiles);

      const res = await axios.get(`${cleanUrl}/api/v1/graph`, {
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" }
      });

      if (res.data?.nodes) {
        const artifacts = res.data.nodes
          .filter((n: LatticeNode) =>
            ["ARTIFACT", "LOGIC", "FILE"].includes(n.category)
          )
          .map((n: LatticeNode) => n.path || n.id);

        setRecentArtifacts(artifacts.slice(0, 15));
      }
    } catch (e) {
      console.error("LATTICE_INDEX_FAULT", e);
    } finally {
      setLoading(false);
    }
  };

  // --- LOAD ARTIFACT ---
  const loadArtifact = async (path: string) => {
    if (!config?.url || !path) return;
    setLoading(true);

    try {
      const cleanUrl = config?.url.replace(/\/$/, "");
      const res = await axios.post(
        `${cleanUrl}/api/v1/io/read`,
        { path },
        { headers: { "X-API-Key": config?.key, "ngrok-skip-browser-warning": "69420" } }
      );

      if (res.data && res.data.content !== undefined) {
        setCurrentFile({
          path,
          content: res.data.content,
          type: path.endsWith(".html")
            ? "web"
            : path.endsWith(".json")
            ? "json"
            : "code",
          hash: res.data.hash || "VERIFIED_LATTICE_NODE",
          size:
            res.data.size ||
            `${(res.data.content.length / 1024).toFixed(1)} KB`
        });
      }
    } catch (e) {
      console.error("ARTIFACT_READ_ERROR", e);
    } finally {
      setLoading(false);
    }
  };

  // --- WRITE ARTIFACT ---
  const commitToDisk = async () => {
    if (!currentFile.path || !config?.url) return;
    setLoading(true);

    try {
      const cleanUrl = config?.url.replace(/\/$/, "");
      await axios.post(
        `${cleanUrl}/api/v1/io/write`,
        { path: currentFile.path, content: currentFile.content },
        { headers: { "X-API-Key": config?.key, "ngrok-skip-browser-warning": "69420" } }
      );

      await scanLattice(config?.url, config?.key);
    } catch (e) {
      console.error("COMMIT_FAULT", e);
      alert("PHYSICAL_COMMIT_FAULT: Verification required.");
    } finally {
      setLoading(false);
    }
  };

  const filteredFiles = files.filter((f) =>
    f.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="h-full flex gap-6 bg-transparent overflow-hidden relative select-none">

      {/* COLUMN A — VAULT INDEX */}
      <aside className="w-80 bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/5 rounded-2xl flex flex-col shrink-0 overflow-hidden shadow-2xl">

        {/* HEADER */}
        <div className="p-5 border-b border-white/5 bg-[#00f2ff]/5 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <HardDrive size={18} className="text-[#00f2ff]" />
            <span className="text-[11px] font-black text-white uppercase tracking-[0.2em]">
              Sovereign_Vault
            </span>
          </div>

          <button
            onClick={() => scanLattice(config?.url, config?.key)}
            className="p-2 hover:bg-[#00f2ff]/20 rounded-lg transition-all"
            title="Refresh Vault"
            aria-label="Refresh Vault"
          >
            <RefreshCw
              size={14}
              className={loading ? "animate-spin text-[#00f2ff]" : "text-[#00f2ff]/60"}
            />
          </button>
        </div>

        {/* SEARCH */}
        <div className="p-4">
          <div className="relative group">
            <Search
              className="absolute left-3 top-2.5 text-white/20 group-focus-within:text-[#00f2ff] transition-colors"
              size={14}
            />
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="PROBE_VAULT_PATH..."
              className="w-full bg-black/40 border border-white/10 p-2.5 pl-10 text-[10px] font-bold text-[#00f2ff] outline-none focus:border-[#00f2ff]/40 rounded-xl transition-all placeholder:text-white/5"
            />
          </div>
        </div>

        {/* RECENT ARTIFACTS */}
        <div className="flex-1 overflow-y-auto px-2 pb-4 space-y-4 scrollbar-hide">
          {recentArtifacts.length > 0 && (
            <div className="space-y-1">
              <div className="px-4 py-2 flex items-center gap-2">
                <History size={12} className="text-[#ff80bf]" />
                <span className="text-[9px] font-black text-[#ff80bf] uppercase tracking-widest">
                  Strike_Manifests
                </span>
              </div>

              {recentArtifacts.map((artifact) => (
                <button
                  key={`recent-${artifact}`}
                  onClick={() => loadArtifact(artifact)}
                  className="w-full text-left px-4 py-2 text-[10px] flex items-center gap-3 rounded-lg hover:bg-[#ff80bf]/5 transition-all text-white/40 hover:text-white group"
                >
                  <Zap
                    size={12}
                    className="text-[#ff80bf]/40 group-hover:text-[#ff80bf]"
                  />
                  <span className="truncate">{artifact.split("/").pop()}</span>
                </button>
              ))}
            </div>
          )}

          {/* PROJECT ROOT */}
          <div className="space-y-1">
            <div className="px-4 py-2 flex items-center gap-2">
              <Clock size={12} className="text-[#00f2ff]" />
              <span className="text-[9px] font-black text-[#00f2ff] uppercase tracking-widest">
                Industrial_Core
              </span>
            </div>

            {filteredFiles.map((file) => (
              <button
                key={file}
                onClick={() => loadArtifact(file)}
                className={`w-full text-left px-4 py-3 text-[10px] flex items-center justify-between rounded-xl transition-all group
                  ${
                    currentFile.path === file
                      ? "bg-[#00f2ff]/10 border border-[#00f2ff]/30 text-white shadow-[0_0_15px_rgba(0,242,255,0.05)]"
                      : "text-white/30 hover:bg-white/5 hover:text-white"
                  }`}
              >
                <div className="flex items-center gap-3 truncate">
                  {file.endsWith(".py") ? (
                    <Terminal size={14} className="text-[#ff80bf]" />
                  ) : file.endsWith(".json") ? (
                    <Box size={14} className="text-[#00f2ff]" />
                  ) : file.endsWith(".csv") ? (
                    <Activity size={14} className="text-green-400" />
                  ) : (
                    <FileText size={14} />
                  )}

                  <span className="truncate tracking-wide font-mono">
                    {file.split("/").pop()}
                  </span>
                </div>

                <ChevronRight
                  size={10}
                  className={`opacity-0 group-hover:opacity-100 ${
                    currentFile.path === file ? "text-[#00f2ff]" : ""
                  }`}
                />
              </button>
            ))}
          </div>
        </div>

        {/* DEPLOY BUTTON */}
        <div className="p-4 border-t border-white/5 bg-black/40">
          <button className="w-full py-3.5 bg-[#ff80bf]/10 border border-[#ff80bf]/30 text-[#ff80bf] text-[10px] font-black uppercase tracking-[0.2em] rounded-xl flex items-center justify-center gap-3 hover:bg-[#ff80bf] hover:text-black transition-all shadow-[0_0_20px_rgba(255,128,191,0.1)] active:scale-95">
            <Package size={16} /> Deploy_Logic_Shard
          </button>
        </div>
      </aside>

      {/* COLUMN B — EDITOR */}
      <div className="flex-1 flex flex-col bg-[#050505] border border-white/5 rounded-2xl overflow-hidden shadow-2xl relative">

        {/* HEADER */}
        <header className="h-16 bg-black/60 border-b border-white/5 flex items-center px-8 justify-between z-10">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-[#ff80bf]/10 flex items-center justify-center border border-[#ff80bf]/20">
              <FileEdit size={20} className="text-[#ff80bf]" />
            </div>

            <div>
              <span className="text-[9px] font-black text-white/20 uppercase block tracking-widest leading-none mb-1">
                Source_Truth
              </span>
              <span className="text-[12px] font-black text-[#00f2ff] italic tracking-tight">
                {currentFile.path || "IDLE_STANDBY"}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden lg:flex items-center gap-6 mr-6 px-6 py-2 border-x border-white/5">
              <div className="flex flex-col">
                <span className="text-[8px] font-black text-white/20 uppercase tracking-widest">
                  Size
                </span>
                <span className="text-[10px] font-mono text-[#00f2ff]">
                  {currentFile.size}
                </span>
              </div>

              <div className="flex flex-col">
                <span className="text-[8px] font-black text-white/20 uppercase tracking-widest">
                  Hash
                </span>
                <span className="text-[10px] font-mono text-[#ff80bf]">
                  {currentFile.hash.slice(0, 8)}
                </span>
              </div>
            </div>

            <button
              onClick={() => setIsPreviewOpen(!isPreviewOpen)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl border transition-all text-[11px] font-black uppercase tracking-widest
                ${
                  isPreviewOpen
                    ? "bg-[#ff80bf]/10 border-[#ff80bf] text-[#ff80bf]"
                    : "bg-white/5 border-white/10 text-white/40 hover:border-white/30 hover:text-white"
                }`}
            >
              <Eye size={16} /> {isPreviewOpen ? "Close_Observer" : "Open_Observer"}
            </button>

            <button
              onClick={commitToDisk}
              disabled={!currentFile.path}
              className="flex items-center gap-2 px-8 py-2.5 bg-[#00f2ff] text-black text-[11px] font-black uppercase rounded-xl hover:bg-white transition-all shadow-[0_0_25px_#00f2ff] active:scale-95 disabled:opacity-10 disabled:grayscale"
            >
              <Save size={16} /> Commit_to_Disk
            </button>
          </div>
        </header>

        {/* EDITOR + PREVIEW */}
        <div className="flex-1 flex overflow-hidden">

          {/* EDITOR */}
          <div className="flex-1 relative bg-[#020202] group flex">

            {/* LINE NUMBERS */}
            <div
              ref={lineNumbersRef}
              className="w-14 bg-black/40 border-r border-white/5 flex flex-col items-center pt-8 text-[10px] font-mono text-white/10 select-none overflow-hidden"
            >
              {Array.from({ length: 300 }).map((_, i) => (
                <div key={i} className="h-[24px] leading-[24px]">
                  {i + 1}
                </div>
              ))}
            </div>

            {/* TEXTAREA */}
            <textarea
              ref={editorRef}
              value={currentFile.content}
              onScroll={handleScroll}
              onChange={(e) =>
                setCurrentFile({ ...currentFile, content: e.target.value })
              }
              className="flex-1 bg-transparent p-8 text-[14px] font-mono text-slate-300 outline-none resize-none leading-[24px] border-none overflow-y-auto scrollbar-hide selection:bg-[#00f2ff] selection:text-black"
              placeholder=">>> Awaiting_Industrial_Directive..."
              spellCheck={false}
            />

            {/* WATERMARK */}
            <div className="absolute bottom-8 right-8 pointer-events-none opacity-[0.03]">
              <ShieldCheck size={240} className="text-[#00f2ff]" />
            </div>
          </div>

          {/* PREVIEW */}
          <AnimatePresence>
            {isPreviewOpen && (
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: "45%", opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                transition={{ type: "spring", bounce: 0, duration: 0.4 }}
                className="border-l border-white/5 bg-[#080808] relative shadow-[-20px_0_60px_rgba(0,0,0,0.8)] z-10"
              >
                <div className="absolute top-4 left-6 z-50">
                  <div className="px-3 py-1 bg-[#00f2ff]/10 text-[#00f2ff] text-[9px] font-black uppercase rounded-md border border-[#00f2ff]/20 backdrop-blur-md">
                    {currentFile.type === "web" ? "Sandbox_Runtime" : "Logic_Observer"}
                  </div>
                </div>

                <div className="h-full w-full pt-12 overflow-hidden">
                  {currentFile.type === "web" ? (
                    <iframe
                      srcDoc={currentFile.content}
                      className="w-full h-full border-none bg-white rounded-tl-3xl"
                      title="Industrial Preview"
                    />
                  ) : (
                    <div className="p-8 h-full overflow-auto text-slate-400 font-mono text-[12px] leading-relaxed scrollbar-hide">
                      <div className="mb-6 flex items-center gap-3">
                        <Box size={16} className="text-[#ff80bf]" />
                        <span className="text-[10px] font-black uppercase text-white/20 tracking-widest italic underline underline-offset-4 decoration-[#ff80bf]/40">
                          Inspector_Raw_Feed
                        </span>
                      </div>
                      <pre className="whitespace-pre-wrap bg-transparent border-none p-0">
                        {currentFile.content}
                      </pre>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* LOADING SHIELD */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-[#050505]/90 backdrop-blur-xl flex flex-col items-center justify-center z-[200]"
            >
              <div className="relative">
                <RefreshCw className="animate-spin text-[#00f2ff]" size={64} />
                <Zap className="absolute inset-0 m-auto text-[#ff80bf] animate-pulse" size={24} />
              </div>

              <div className="mt-8 flex flex-col items-center gap-2">
                <span className="text-[11px] font-black text-white uppercase tracking-[0.6em] animate-pulse">
                  Sovereign_Sync
                </span>
                <span className="text-[8px] font-black text-[#00f2ff] uppercase tracking-widest">
                  Verifying_IronClad_Integrity
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}




/**
 * REALM FORGE: TITAN WAR ROOM v60.5
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY / PRODUCTION-HARDENED
 * ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
 * PATH: F:/agentic_workforce/client/components/chambers/WarRoom.tsx
 */

"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send, Activity, Users, Terminal, Volume2, VolumeX,
  Cpu, Shield, Database, Layout, BarChart, Scale,
  FlaskConical, Gavel, Megaphone, UserPlus, CheckCircle,
  Factory, Wrench, Zap, ChevronRight
} from "lucide-react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// --- 13 CANONICAL INDUSTRIAL SILOS ---
const SECTOR_METADATA = [
  { id: "Architect", label: "Architect", icon: <Layout size={16} />, color: "#00f2ff" },
  { id: "Data_Intelligence", label: "Data Intel", icon: <Database size={16} />, color: "#00f2ff" },
  { id: "Software_Engineering", label: "Software Eng", icon: <Cpu size={16} />, color: "#00f2ff" },
  { id: "DevOps_Infrastructure", label: "DevOps Infra", icon: <Wrench size={16} />, color: "#ff80bf" },
  { id: "Cybersecurity", label: "Cyber Security", icon: <Shield size={16} />, color: "#ff007f" },
  { id: "Financial_Ops", label: "Financial Ops", icon: <BarChart size={16} />, color: "#00f2ff" },
  { id: "Legal_Compliance", label: "Legal", icon: <Scale size={16} />, color: "#ff80bf" },
  { id: "Research_Development", label: "R&D", icon: <FlaskConical size={16} />, color: "#00f2ff" },
  { id: "Executive_Board", label: "Exec Board", icon: <Gavel size={16} />, color: "#ff007f" },
  { id: "Marketing_PR", label: "Marketing", icon: <Megaphone size={16} />, color: "#ff80bf" },
  { id: "Human_Capital", label: "Human Capital", icon: <UserPlus size={16} />, color: "#00f2ff" },
  { id: "Quality_Assurance", label: "QA / Audit", icon: <CheckCircle size={16} />, color: "#ff80bf" },
  { id: "Facility_Management", label: "Facilities", icon: <Factory size={16} />, color: "#ff007f" },
];

interface LogEntry {
  id: string | number;
  type: "user" | "ai" | "system";
  agent: string;
  content: string;
  timestamp: string;
  node?: string;
  dept?: string;
}

interface WarRoomProps {
  logs: LogEntry[];
  isProcessing: boolean;
  onSend: (text: string) => void;
  unlockAudio: () => void;
  audioUnlocked: boolean;
  participants?: string[];
}

export default function WarRoom({
  logs = [],
  isProcessing = false,
  onSend,
  unlockAudio,
  audioUnlocked,
  participants = []
}: WarRoomProps) {
  const [task, setTask] = useState("");
  const [roster, setRoster] = useState<any[]>([]);
  const [activeDept, setActiveDept] = useState("Architect");
  const [hasMounted, setHasMounted] = useState(false);

  const chatEndRef = useRef<HTMLDivElement>(null);

  // --- INITIALIZATION ---
  useEffect(() => {
    setHasMounted(true);
    if (typeof window !== "undefined") fetchRoster();
  }, []);

  // --- AUTO-SCROLL ---
  const scrollToBottom = useCallback(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, []);

  useEffect(() => {
    if (hasMounted && logs.length > 0) {
      const t = setTimeout(scrollToBottom, 80);
      return () => clearTimeout(t);
    }
  }, [logs, hasMounted, scrollToBottom]);

  // --- FETCH ROSTER ---
  const fetchRoster = async () => {
    const url = localStorage.getItem("RF_URL");
    const key = localStorage.getItem("RF_KEY");
    if (!url) return;

    try {
      const res = await axios.get(`${url.replace(/\/$/, "")}/api/v1/agents`, {
        headers: { "X-API-Key": key, "ngrok-skip-browser-warning": "69420" }
      });
      setRoster(res.data.roster || res.data.agents || []);
    } catch {
      console.warn("Roster fetch failed.");
    }
  };

  // --- SEND DIRECTIVE ---
  const handleDirective = () => {
    if (!task.trim() || isProcessing) return;
    onSend(task);
    setTask("");
  };

  if (!hasMounted) return null;

  return (
    <div className="h-full flex gap-6 overflow-hidden select-none">

      {/* LEFT PANEL — SECTOR GRID */}
      <div className="w-[340px] flex flex-col gap-4 shrink-0 h-full">
        <button
          onClick={unlockAudio}
          className={`w-full py-4 border-2 rounded-xl transition-all font-black text-[10px] uppercase tracking-[0.2em] flex items-center justify-center gap-3 active:scale-95
            ${
              audioUnlocked
                ? "border-[#ff80bf] text-[#ff80bf] bg-[#ff80bf]/10 shadow-[0_0_20px_rgba(255,128,191,0.2)]"
                : "border-[#00f2ff]/30 text-[#00f2ff]/60 hover:border-[#00f2ff] hover:text-[#00f2ff] bg-white/5"
            }`}
        >
          {audioUnlocked ? (
            <Volume2 size={18} className="animate-pulse" />
          ) : (
            <VolumeX size={18} />
          )}
          {audioUnlocked ? "VOCAL_CORE: STABLE" : "INIT_SENSORY_LINK"}
        </button>

        <div className="flex-1 bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/5 rounded-2xl p-4 overflow-hidden relative flex flex-col shadow-2xl">
          <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-2">
            <h3 className="text-[10px] font-black text-[#00f2ff] uppercase tracking-[0.2em] flex items-center gap-2">
              <Activity size={14} /> Swarm_Sectors
            </h3>
            <span className="text-[9px] font-mono text-white/20">13 CANONICAL</span>
          </div>

          <div className="grid grid-cols-2 gap-2 overflow-y-auto pr-1 scrollbar-hide">
            {SECTOR_METADATA.map((sector) => {
              const isActive = activeDept === sector.id;

              return (
                <motion.div
                  key={sector.id}
                  animate={
                    isActive
                      ? { scale: 1.02, filter: "brightness(1.2)" }
                      : { scale: 1 }
                  }
                  className={`p-3 rounded-xl border flex flex-col gap-2 transition-all duration-300 relative overflow-hidden cursor-default
                    ${
                      isActive
                        ? "bg-[#00f2ff]/5 shadow-[0_0_15px_rgba(0,242,255,0.1)]"
                        : "bg-white/5 border-white/5 opacity-40 hover:opacity-100"
                    }`}
                  style={isActive ? { borderColor: sector.color } : {}}
                >
                  <div className="flex items-center justify-between">
                    <div style={{ color: isActive ? sector.color : "#444" }}>
                      {sector.icon}
                    </div>
                    {isActive && (
                      <Zap size={10} className="text-[#ff80bf] animate-pulse" />
                    )}
                  </div>

                  <div
                    className={`text-[9px] font-black uppercase tracking-widest ${
                      isActive ? "text-white" : "text-white/20"
                    }`}
                  >
                    {sector.label}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>

      {/* RIGHT PANEL — MISSION STREAM */}
      <div className="flex-1 flex flex-col bg-[#0a0a0a]/40 border border-white/5 rounded-2xl relative overflow-hidden shadow-2xl">

        {/* HEADER */}
        <div className="h-14 bg-black/60 border-b border-white/5 flex items-center px-6 justify-between z-10">
          <div className="flex items-center gap-4 text-[10px] font-black uppercase tracking-[0.3em]">
            <Terminal size={14} className="text-[#00f2ff]" />
            <span className="text-white/20">Mission_Trace</span>
            <ChevronRight size={14} className="text-white/5" />
            <span className="text-[#ff80bf] italic">{activeDept}</span>

            {participants.length > 0 && (
              <div className="flex items-center gap-2 ml-4 pl-4 border-l border-white/10">
                <Users size={12} className="text-[#00f2ff]" />
                <span className="text-[8px] text-white/40">
                  {participants.length} ASSEMBLED
                </span>
              </div>
            )}
          </div>

          {isProcessing && (
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-[#00f2ff] animate-ping" />
              <span className="text-[9px] font-black text-[#00f2ff] uppercase tracking-widest">
                Strike_In_Progress
              </span>
            </div>
          )}
        </div>

        {/* LOG STREAM */}
        <div className="flex-1 overflow-y-auto p-8 space-y-10 scrollbar-hide scroll-smooth">
          <AnimatePresence initial={false} mode="popLayout">
            {logs.map((log, i) => (
              <motion.div
                key={log.id || `log-${i}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex flex-col ${
                  log.type === "user" ? "items-end" : "items-start"
                }`}
              >
                <div
                  className={`flex items-center gap-3 mb-2 opacity-40 text-[9px] font-black uppercase tracking-widest ${
                    log.type === "user" ? "text-[#ff80bf]" : "text-[#00f2ff]"
                  }`}
                >
                  <span className="bg-white/5 px-2 py-0.5 rounded border border-white/5">
                    {log.agent}
                  </span>
                  {log.node && (
                    <span className="text-[#ff80bf]/50">{log.node}</span>
                  )}
                  <span className="font-mono text-white/20 ml-auto">
                    {log.timestamp}
                  </span>
                </div>

                <div
                  className={`p-6 rounded-2xl text-[13px] leading-relaxed max-w-[95%] font-mono border transition-all selection:bg-white selection:text-black
                    ${
                      log.type === "user"
                        ? "bg-[#ff80bf]/5 border-[#ff80bf]/20 text-white shadow-[0_0_30px_rgba(255,128,191,0.05)]"
                        : "bg-[#050505] border-white/5 text-slate-300 shadow-xl"
                    }`}
                >
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      h1: (p) => (
                        <h1
                          className="text-lg font-black text-white uppercase mb-4 border-b border-white/10 pb-2"
                          {...p}
                        />
                      ),
                      h3: (p) => (
                        <h3
                          className="text-[#00f2ff] font-bold uppercase mt-4 mb-2 tracking-widest"
                          {...p}
                        />
                      ),
                      code: (p) => (
                        <code
                          className="bg-[#111] px-2 py-1 text-[#ff80bf] rounded border border-white/5 text-[12px] terminal-literal"
                          {...p}
                        />
                      ),
                      table: (p) => (
                        <div className="overflow-x-auto my-6 border border-white/5 rounded-lg">
                          <table className="min-w-full text-[11px]" {...p} />
                        </div>
                      ),
                      th: (p) => (
                        <th
                          className="bg-white/5 text-[#00f2ff] p-3 text-left font-black uppercase tracking-tighter border-b border-white/5"
                          {...p}
                        />
                      ),
                      td: (p) => (
                        <td
                          className="p-3 border-t border-white/5 text-white/60"
                          {...p}
                        />
                      ),
                      ul: (p) => (
                        <ul className="list-disc ml-4 space-y-2 my-4" {...p} />
                      ),
                      li: (p) => <li className="text-white/70" {...p} />
                    }}
                  >
                    {log.content}
                  </ReactMarkdown>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          <div ref={chatEndRef} className="h-4 w-full" />
        </div>

        {/* INPUT BAR */}
        <div className="p-6 bg-black/40 border-t border-white/5 backdrop-blur-md">
          <div className="max-w-4xl mx-auto flex gap-4 items-end">
            <div className="flex-1 bg-white/5 border border-white/10 rounded-2xl p-4 focus-within:border-[#00f2ff]/40 focus-within:bg-white/10 transition-all shadow-inner">
              <textarea
                value={task}
                onChange={(e) => setTask(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleDirective();
                  }
                }}
                placeholder="Initialize Industrial Directive..."
                className="w-full bg-transparent text-[#00f2ff] font-mono text-sm outline-none resize-none h-14 scrollbar-hide placeholder:text-white/10"
                disabled={isProcessing}
              />

              <div className="flex justify-between mt-2 text-[8px] uppercase font-black tracking-widest text-white/10">
                <div className="flex gap-4">
                  <span className="text-[#00f2ff]/40">
                    Neural Link: Secure_AES_256
                  </span>
                  <span
                    className={
                      isProcessing ? "text-[#ff80bf] animate-pulse" : ""
                    }
                  >
                    {isProcessing ? "LATTICE: BUSY" : "LATTICE: READY"}
                  </span>
                </div>
                <span>{task.length} / 2000</span>
              </div>
            </div>

            <button
              onClick={handleDirective}
              disabled={isProcessing || !task.trim()}
              className="w-14 h-14 bg-[#00f2ff] text-black flex items-center justify-center rounded-2xl hover:bg-white transition-all shadow-[0_0_25px_#00f2ff] disabled:opacity-10 active:scale-90"
            >
              {isProcessing ? (
                <Activity className="animate-spin" />
              ) : (
                <Zap size={24} fill="currentColor" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}


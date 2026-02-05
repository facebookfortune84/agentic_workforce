/**
 * REALM FORGE: TITAN COMMAND CHASSIS v60.5
 * STYLE: CAFFEINE-NEON / HIGH-VISIBILITY / PRODUCTION-HARDENED
 * ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
 * PATH: F:/agentic_workforce/client/app/page.tsx
 */

"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutGrid, Code2, Share2, Wrench, Settings,
  Power, Mic, MicOff, ShieldCheck, Activity, Terminal, User, Zap, Github, ChevronLeft, ChevronRight,
  MessageSquare, Send, Binary, CheckCircle2
} from "lucide-react";
import axios from "axios";

// --- CHAMBER COMPONENTS ---
// Note: If these files don't exist yet, VS Code will still show red. 
// Simply create empty files at these locations to clear the error.
import WarRoom from "@/components/chambers/WarRoom";
import ArtifactStudio from "@/components/chambers/ArtifactStudio";
import NeuralLattice from "@/components/chambers/NeuralLattice";
import ArsenalManager from "@/components/chambers/ArsenalManager";

// --- TYPES ---
interface Handoff {
  from: string;
  to: string;

interface LogEntry {
  id: string | number;
  type: "system" | "user" | "ai";
  agent: string;
  content: string;
  timestamp: string;
  node?: string;
  dept?: string;

interface AssistantLog {
  id: number;
  role: "assistant" | "user";
  text: string;

interface NavIconProps {
  icon: React.ReactNode;
  active: boolean;
  onClick: () => void;
  label: string;

interface TelemetryVitals {
  cpu: number;
  ram: number;
  lattice_nodes: number;
  timestamp: number;
  active_sector: string;

export default function TitanForgeHUD() {

  // --- 1. SYSTEM NAVIGATION ---
  const [activeTab, setActiveTab] = useState("war_room");
  const [isAssistantOpen, setIsAssistantOpen] = useState(true);
  const [status, setStatus] = useState("OFFLINE");
  const [mounted, setMounted] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // --- 2. CONFIGURATION ---
  const [config, setConfig] = useState({
    url: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
    key: "sk-realm-god-mode-888",
    open: false
  });

  // --- 3. TELEMETRY & CHAT STATE ---
  const [vitals, setVitals] = useState<TelemetryVitals>({
    cpu: 0,
    ram: 0,
    lattice_nodes: 13472,
    timestamp: 0,
    active_sector: "Architect"
  });

  const [activeAgent, setActiveAgent] = useState("ForgeMaster");
  const [handoffs, setHandoffs] = useState<Handoff[]>([]);
  const [meetingParticipants, setMeetingParticipants] = useState<string[]>([]);
  const [missionStrategy, setMissionStrategy] = useState<unknown>(null); // Strategy structure is dynamic
  const [chatInput, setChatInput] = useState("");
  const [isGitHubLinked, setIsGitHubLinked] = useState(false);

  const [assistantLogs, setAssistantLogs] = useState<AssistantLog[]>([
    {
      id: 1,
      role: "assistant",
      text: "Lattice pressurized. I am your Sovereign Consultant, synchronized with the 13,472 node neural network."

  ]);

  const [diagnosticLines, setDiagnosticLines] = useState<string[]>([
    `[${new Date().toLocaleTimeString()}] RE-INIT: Mastermind Online.`,
    `[${new Date().toLocaleTimeString()}] LATTICE: 13-Silo Renormalization Nominal.`
  ]);

  const [globalLogs, setGlobalLogs] = useState<LogEntry[]>([
    {
      id: "init",
      type: "system",
      agent: "CORE",
      content: "### [TITAN_OS_v60.5] UPLINK_STABLE.\n1,113 Agents renormalized. 180 Tools armored. Mission Orchestrator standby.",
      timestamp: "INIT"

  ]);

  // --- 4. AUDIO PIPELINE ---
  const audioQueue = useRef<string[]>([]);
  const isAudioPlaying = useRef(false);
  const audioCtx = useRef<AudioContext | null>(null);
  const [audioUnlocked, setAudioUnlocked] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  // --- 5. AUDIO ACTIVATION ---
  const unlockAudio = async () => {
    if (typeof window === "undefined") return;

    try {
      const AudioCtor: typeof AudioContext | undefined =
        (window as typeof window & { webkitAudioContext?: typeof AudioContext }).AudioContext ||
        (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!AudioCtor) throw new Error("Web Audio API not supported.");

      if (!audioCtx.current) {
        audioCtx.current = new AudioCtor();

      if (audioCtx.current.state === "suspended") {
        await audioCtx.current.resume();

      setAudioUnlocked(true);
      setDiagnosticLines((p: string[]) => [
        ...p.slice(-49),
        `[SENSES] Neural vocal link synchronized.`
      ]);
    } catch (err) {
      console.error("Audio Fault", err);

  };

  const playNextAudio = useCallback(async () => {
    if (audioQueue.current.length === 0 || !audioUnlocked || !audioCtx.current) {
      isAudioPlaying.current = false;
      return;

    isAudioPlaying.current = true;
    const base64Str = audioQueue.current.shift();
    if (!base64Str) return;

    try {
      // Fix: Handle potential data URI prefixes
      const cleanBase64 = base64Str.includes(",") ? base64Str.split(",")[1] : base64Str;
      const bytes = Uint8Array.from(window.atob(cleanBase64), (c) => c.charCodeAt(0));
      const buffer = await audioCtx.current.decodeAudioData(bytes.buffer);
      const source = audioCtx.current.createBufferSource();
      source.buffer = buffer;
      source.connect(audioCtx.current.destination);
      source.onended = () => {
        isAudioPlaying.current = false;
        playNextAudio();
      };
      source.start(0);
    } catch (e) {
      console.error("Audio Decode Error", e);
      isAudioPlaying.current = false;
      playNextAudio();

  }, [audioUnlocked]);

  // --- 6. MISSION ENGINE ---
  const executeDirective = useCallback(
    async (text: string) => {
      if (!text || isProcessing) return;

      setGlobalLogs((p: LogEntry[]) => [
        ...p,
        {
          id: Date.now(),
          type: "user",
          agent: "ARCHITECT",
          content: text,
          timestamp: new Date().toLocaleTimeString()

      ]);

      setIsProcessing(true);

      const url = localStorage.getItem("RF_URL") || config.url;
      const key = localStorage.getItem("RF_KEY") || config.key;

      try {
        await axios.post(
          `${url.replace(/\/$/, "")}/api/v1/mission`,
          { task: text },
          {
            headers: {
              "X-API-Key": key,
              "ngrok-skip-browser-warning": "69420",
              "Content-Type": "application/json"


        );
      } catch (err) {
        setDiagnosticLines((p: string[]) => [
          ...p.slice(-49),
          `[FAULT]: Strike MSN Uplink Failed.`
        ]);
        setIsProcessing(false);

    },
    [config.url, config.key, isProcessing]
  );

  // --- 7. ASSISTANT CHAT ---
  const handleAssistantChat = async () => {
    if (!chatInput.trim()) return;

    const msg = chatInput;
    setChatInput("");

    setAssistantLogs((p: AssistantLog[]) => [
      ...p,
      { id: Date.now(), role: "user", text: msg }
    ]);

    const url = localStorage.getItem("RF_URL") || config.url;
    const key = localStorage.getItem("RF_KEY") || config.key;

    try {
      const res = await axios.post(
        `${url.replace(/\/$/, "")}/api/v1/assistant/chat`,
        { message: msg },
        {
          headers: {
            "X-API-Key": key,
            "ngrok-skip-browser-warning": "69420"


      );

      setAssistantLogs((p: AssistantLog[]) => [
        ...p,
        { id: Date.now(), role: "assistant", text: res.data.response }
      ]);
    } catch (e) {
      setAssistantLogs((p: AssistantLog[]) => [
        ...p,
        {
          id: Date.now(),
          role: "assistant",
          text: "⚠️ [LINK_ERROR]: Could not reach Mastermind bridge."

      ]);

  };

// --- 8. SWARM TELEMETRY ---
  const connectToSwarm = useCallback(
    (url: string) => {
      if (typeof window === "undefined" || !url) return;

      if (typeof ws !== "undefined" && ws && ws.current) ws.current.close();

      const base = url.replace(/^https?:\/\//, "").replace(/\/$/, "");
      const protocol = url.startsWith("https") ? "wss" : "ws";

      try {
        const socket = new WebSocket(`${protocol}://${base}/ws/telemetry`);
        ws.current = socket;

        socket.onopen = () => setStatus("NOMINAL");

        socket.onmessage = (e) => {
          const data = JSON.parse(e.data);

          if (data.vitals) setVitals(data.vitals);

          if (data.type === "node_update") {
            setActiveAgent(data.agent);

            if (data.meeting_participants)
              setMeetingParticipants(data.meeting_participants);

            if (data.handoffs && Array.isArray(data.handoffs) && data.handoffs.length > 0) {
              setHandoffs(data.handoffs as Handoff[]);
              const h = data.handoffs[data.handoffs.length - 1] as Handoff;
              setDiagnosticLines((p) => [
                ...p.slice(-49),
                `🔄 [HANDOFF]: ${h.from} ➔ ${h.to}`
              ]);


          if (data.type === "diagnostic") {
            setDiagnosticLines((p) => [...p.slice(-49), data.text]);

          if (data.type === "audio_chunk") {
            setGlobalLogs((p: LogEntry[]) => [
              ...p,
              {
                id: Date.now(),
                type: "ai",
                agent: data.agent,
                content: data.text,
                timestamp: new Date().toLocaleTimeString(),
                node: data.node,
                dept: data.dept

            ]);

            if (data.audio_base64 && audioUnlocked) {
              audioQueue.current.push(data.audio_base64);
              if (!isAudioPlaying.current) playNextAudio();


          if (data.type === "mission_complete") setIsProcessing(false);
        };

        socket.onclose = () => {
          setStatus("OFFLINE");
          // Optional: Implement auto-reconnect here
        };
      } catch (err) {
        console.error("Socket Connection Fault", err);

    },
    [audioUnlocked, playNextAudio]
  );

  // --- 9. INITIALIZATION ---
  useEffect(() => {
    setMounted(true);

    if (typeof window !== "undefined") {
      const savedUrl = localStorage.getItem("RF_URL") || config.url;
      const savedKey = localStorage.getItem("RF_KEY") || config.key;
      const savedAuth = localStorage.getItem("RF_GITHUB_AUTH") === "true";

      setConfig((c) => ({ ...c, url: savedUrl, key: savedKey }));
      setIsGitHubLinked(savedAuth);

      connectToSwarm(savedUrl);

      // OAuth handshake logic
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get("code");

      if (code) {
        setDiagnosticLines((p) => [
          ...p.slice(-49),
          `[${new Date().toLocaleTimeString()}] 🗝️ [OAUTH]: Code detected. Handshake initiated.`
        ]);

        axios
          .post(
            `${savedUrl.replace(/\/$/, "")}/api/v1/auth/github`,
            { code },
            {
              headers: {
                "X-API-Key": savedKey,
                "ngrok-skip-browser-warning": "69420"


          )
          .then(() => {
            setDiagnosticLines((p) => [
              ...p.slice(-49),
              `[${new Date().toLocaleTimeString()}] ✅ [OAUTH]: Identity sutured to swarm.`
            ]);
            setIsGitHubLinked(true);
            localStorage.setItem("RF_GITHUB_AUTH", "true");
            window.history.replaceState({}, document.title, window.location.pathname);
          })
          .catch(() => {
            setDiagnosticLines((p) => [
              ...p.slice(-49),
              `[${new Date().toLocaleTimeString()}] ❌ [OAUTH]: Handshake failure.`
            ]);
          });


  }, [connectToSwarm, config.url, config.key]);

  // Ensure `mounted` is defined using useState and useEffect
  

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="flex h-screen w-screen bg-[#050505] text-slate-200 overflow-hidden font-sans text-[13px]">

      {/* COLUMN 1: NAVIGATION RAIL */}
      <aside className="w-[72px] bg-[#0a0a0a] border-r border-white/5 flex flex-col items-center py-8 gap-10 shrink-0 z-[100]">
        <motion.div
          whileHover={{ scale: 1.1 }}
          className="w-10 h-10 bg-[#00f2ff] rounded-xl flex items-center justify-center text-black shadow-[0_0_20px_rgba(0,242,255,0.3)] cursor-pointer"
        >
          <Binary size={24} />
        </motion.div>

        <nav className="flex flex-col gap-6">
          <NavIcon
            active={activeTab === "war_room"}
            onClick={() => setActiveTab("war_room")}
            icon={<LayoutGrid size={22} />}
            label="WAR ROOM"
          />
          <NavIcon
            active={activeTab === "artifact_studio"}
            onClick={() => setActiveTab("artifact_studio")}
            icon={<Code2 size={22} />}
            label="STUDIO"
          />
          <NavIcon
            active={activeTab === "neural_lattice"}
            onClick={() => setActiveTab("neural_lattice")}
            icon={<Share2 size={22} />}
            label="LATTICE"
          />
          <NavIcon
            active={activeTab === "arsenal"}
            onClick={() => setActiveTab("arsenal")}
            icon={<Wrench size={22} />}
            label="ARSENAL"
          />
        </nav>

        <div className="mt-auto flex flex-col gap-6 pb-4">
          <NavIcon
            active={false}
            onClick={() => setConfig({ ...config, open: true })}
            icon={<Settings size={22} />}
            label="CONFIG"
          />

          <button
            title="Log out"
            aria-label="Log out"
            onClick={() => {
              localStorage.clear();
              window.location.reload();
            }}
            className="w-10 h-10 flex items-center justify-center rounded-xl text-white/20 hover:text-red-500 hover:bg-red-500/10 transition-all"
          >
            <Power size={20} />
          </button>
        </div>
      </aside>

      {/* COLUMN 2: PRIMARY WORKSPACE */}
      <main className="flex-1 flex flex-col min-w-0 bg-[#080808] relative">

        <header className="h-14 border-b border-white/5 flex items-center px-8 justify-between bg-[#0a0a0a]/50 backdrop-blur-md">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${status === "NOMINAL" ? "bg-[#00f2ff] shadow-[0_0_10px_#00f2ff]" : "bg-red-500"}`} />
              <span className="text-[10px] font-black tracking-[0.2em] uppercase text-white/50">
                Lattice_{status}
              </span>
            </div>
            <div className="h-4 w-px bg-white/10" />
            <div className="text-[10px] font-black tracking-[0.2em] uppercase text-[#ff80bf]">
              Specialist: {activeAgent}
            </div>

            {meetingParticipants.length > 1 && (
              <div className="flex -space-x-2 ml-4">
                {meetingParticipants.map((p, i) => (
                  <div key={i} className="w-5 h-5 rounded-full bg-[#00f2ff] border border-black text-[8px] flex items-center justify-center text-black font-black" title={p}>
                    {p.charAt(0)}
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="flex items-center gap-6 text-[10px] font-bold text-white/30 uppercase tracking-widest">
            <div className="flex items-center gap-2">
              <Activity size={12} /> Load: <span className="text-white">{vitals.cpu}%</span>
            </div>
            <div className="flex items-center gap-2">
              <Binary size={12} /> Nodes: <span className="text-white">{vitals.lattice_nodes}</span>
            </div>
            <button
              title="Open assistant"
              aria-label="Open assistant"
              onClick={() => setIsAssistantOpen(!isAssistantOpen)}
              className={`p-2 rounded-lg transition-all ${isAssistantOpen ? "bg-[#00f2ff]/10 text-[#00f2ff]" : "hover:bg-white/5"}`}
            >
              <MessageSquare size={18} />
              {/* Assistant Chat */}
            </button>
          </div>
        </header>

        <div className="flex-1 p-6 relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full w-full"
            >
              {activeTab === "war_room" && (
                <WarRoom
                  logs={globalLogs}
                  isProcessing={isProcessing}
                  onSend={executeDirective}
                  audioUnlocked={audioUnlocked}
                  unlockAudio={unlockAudio}
                  participants={meetingParticipants}
                />
              )}
              {activeTab === "artifact_studio" && <ArtifactStudio />}
              {activeTab === "neural_lattice" && <NeuralLattice />}
              {activeTab === "arsenal" && <ArsenalManager />}
            </motion.div>
          </AnimatePresence>
        </div>

        <div className="absolute bottom-6 right-6 w-80 bg-[#0a0a0a]/90 backdrop-blur-xl rounded-2xl overflow-hidden border border-white/5 shadow-2xl z-50">
          <div className="p-3 bg-white/5 border-b border-white/5 flex items-center justify-between">
            <div className="flex items-center gap-2 text-[9px] font-black uppercase text-[#00f2ff] tracking-widest">
              <Terminal size={12} /> System_Diagnostics
            </div>
          </div>
          <div className="p-4 h-32 overflow-y-auto font-mono text-[9px] space-y-1 text-white/40 scrollbar-hide">
            {diagnosticLines.map((line, i) => (
              <div key={i} className="flex gap-2">
                <span className="text-white/10 select-none">[{i}]</span>
                <span className={line.includes("HANDOFF") ? "text-[#ff80bf]" : line.includes("✅") ? "text-[#00f2ff]" : ""}>
                  {line}
                </span>
              </div>
            ))}
            {isProcessing && (
              <div className="animate-pulse text-[#00f2ff]">
                {" >>> Processing_Strike_Maneuvers..."}
              </div>
            )}
          </div>
        </div>
      </main>

      {/* COLUMN 3: SOVEREIGN ASSISTANT */}
      <AnimatePresence>
        {isAssistantOpen && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 420, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            className="bg-[#0a0a0a] border-l border-white/5 flex flex-col shrink-0 overflow-hidden relative"
          >
            <div className="p-6 border-b border-white/5 bg-[#00f2ff]/5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-[11px] font-black uppercase tracking-[0.2em] text-[#00f2ff]">Infrastructure Link</h3>
                <ShieldCheck size={16} className={isGitHubLinked ? "text-[#00f2ff]" : "text-[#ff80bf]"} />
              </div>
              <button
                onClick={() => {
                  if (!isGitHubLinked) {
                    const target = (localStorage.getItem("RF_URL") || config.url).replace(/\/$/, "");
                    window.location.href = `${target}/api/v1/auth/github`;

                }}
                disabled={isGitHubLinked}
                className={`w-full py-3 rounded-xl flex items-center justify-center gap-3 transition-all group border ${isGitHubLinked ? "bg-[#00f2ff]/10 border-[#00f2ff]/30 cursor-default" : "bg-white/5 border-white/10 hover:bg-[#00f2ff]/10 hover:border-[#00f2ff]/30"}`}
              >
                {isGitHubLinked ? (
                  <><CheckCircle2 size={18} className="text-[#00f2ff]" /><span className="text-[10px] font-black uppercase tracking-widest text-[#00f2ff]">Sovereign Identity Verified</span></>
                ) : (
                  <><Github size={18} className="group-hover:text-[#00f2ff]" /><span className="text-[10px] font-black uppercase tracking-widest group-hover:text-[#00f2ff]">OAUTH: Authorize Repositories</span></>
                )}
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
              {assistantLogs.map((log) => (
                <div key={log.id} className="flex flex-col gap-2">
                  <div className="flex items-center gap-2">
                    <div className={`w-5 h-5 rounded ${log.role === "assistant" ? "bg-[#ff80bf]/20" : "bg-[#00f2ff]/20"} flex items-center justify-center`}>
                      <User size={12} className={log.role === "assistant" ? "text-[#ff80bf]" : "text-[#00f2ff]"} />
                    </div>
                    <span className="text-[9px] font-black text-white/30 uppercase">{log.role === "assistant" ? "Mastermind" : "Architect"}</span>
                  </div>
                  <div className={`p-4 rounded-2xl leading-relaxed font-mono border ${log.role === "assistant" ? "bg-white/5 border-white/5 text-slate-300" : "bg-[#00f2ff]/5 border-[#00f2ff]/20 text-white"}`}>
                    {log.text}
                  </div>
                </div>
              ))}
            </div>

            <div className="p-6 border-t border-white/5 bg-black/20">
              <div className="relative">
                <textarea
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleAssistantChat(); } }}
                  placeholder="Inquire with the Mastermind..."
                  className="w-full bg-black border border-white/10 rounded-2xl p-4 pr-12 text-sm font-medium outline-none focus:border-[#ff80bf]/50 h-32 resize-none transition-all placeholder:text-white/5"
                />
                <button onClick={handleAssistantChat} className="absolute bottom-4 right-4 p-2 bg-[#ff80bf] text-black rounded-lg hover:bg-white transition-all shadow-[0_0_20px_rgba(255,128,191,0.3)]">
                  <Send size={18} fill="currentColor" />
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {config.open && (
          <div className="fixed inset-0 bg-black/95 backdrop-blur-3xl flex items-center justify-center z-[1000]">
            <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-[#0a0a0a] border-2 border-[#00f2ff]/20 p-12 rounded-[40px] w-full max-w-xl shadow-[0_0_100px_rgba(0,242,255,0.1)]">
              <h2 className="text-3xl font-black text-white mb-10 uppercase italic border-b-4 border-[#ff80bf] inline-block tracking-tighter">Calibration</h2>
              <div className="space-y-8 font-mono">
                <div className="space-y-2">
                  <label className="text-[10px] uppercase font-black text-[#00f2ff] tracking-widest block ml-2">Node_Gateway_Endpoint</label>
                  <input value={config.url} onChange={(e) => setConfig({ ...config, url: e.target.value })} className="w-full bg-black border border-white/10 p-5 rounded-2xl text-[#00f2ff] outline-none focus:border-[#00f2ff]/50" />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] uppercase font-black text-[#ff80bf] tracking-widest block ml-2">God_Mode_Signature</label>
                  <input type="password" value={config.key} onChange={(e) => setConfig({ ...config, key: e.target.value })} className="w-full bg-black border border-white/10 p-5 rounded-2xl text-[#ff80bf] outline-none focus:border-[#ff80bf]/50" />
                </div>
                <button
                  onClick={() => {
                    localStorage.setItem("RF_URL", config.url);
                    localStorage.setItem("RF_KEY", config.key);
                    setConfig({ ...config, open: false });
                    window.location.reload();
                  }}
                  className="w-full py-6 bg-[#00f2ff] text-black font-black uppercase text-lg rounded-3xl hover:bg-white transition-all shadow-[0_0_30px_rgba(0,242,255,0.2)]"
                >
                  Suture Swarm Link
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );


function NavIcon({ icon, active, onClick, label }: NavIconProps) {
  return (
    <button
      onClick={onClick}
      className={`w-12 h-12 flex items-center justify-center rounded-2xl transition-all relative group ${active ? "bg-[#00f2ff]/10 text-[#00f2ff] shadow-[0_0_20px_rgba(0,242,255,0.2)]" : "text-white/20 hover:text-white hover:bg-white/5"}`}
    >
      {icon}
      <span className="absolute left-20 bg-[#ff80bf] text-black px-3 py-1.5 text-[9px] font-black uppercase rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none tracking-widest z-[200]">
        {label}
      </span>
    </button>
  );

</input>
</div>
</input>
</div>
</div>
</motion>
</div>
</AnimatePresence>
</Send>
</button>
</textarea>
</div>
</div>
</User>
</div>
</div>
</div>
</div>
</Github>
</CheckCircle2>
</button>
</ShieldCheck>
</div>
</div>
</motion>
</AnimatePresence>
</Terminal>
</div>
</div>
</div>
</ArsenalManager>
</NeuralLattice>
</ArtifactStudio>
</WarRoom>
</motion>
</AnimatePresence>
</div>
</MessageSquare>
</button>
</Binary>
</div>
</Activity>
</div>
</div>
</div>
</div>
</header>
</main>
</Power>
</button>
</Settings>
</NavIcon>
</div>
</Wrench>
</NavIcon>
</Share2>
</NavIcon>
</Code2>
</NavIcon>
</LayoutGrid>
</NavIcon>
</nav>
</Binary>
</motion>
</aside>
</div>
</WebSocket>
</AudioContext>
</string>
</LogEntry>
</string>
</AssistantLog>
</unknown>
</string>
</Handoff>
</TelemetryVitals>

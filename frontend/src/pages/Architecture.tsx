import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Cpu, 
  ShieldAlert, 
  Network, 
  Key, 
  SearchCode, 
  Database, 
  Zap, 
  X, 
  ArrowRight,
  Info,
  CheckCircle2
} from "lucide-react";
import { ARCHITECTURE_NODES } from "../constants";
import { ArchitectureNode } from "../types";
import ParticleBackground from "../components/ParticleBackground";

export default function Architecture() {
  const [selectedNode, setSelectedNode] = useState<ArchitectureNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  // Group nodes by hierarchy for cleaner visual alignment
  const getNodeColor = (category: string) => {
    switch (category) {
      case "agent": return "border-blue-500/50 text-blue-400 bg-blue-950/40 shadow-[0_0_15px_rgba(59,130,246,0.15)]";
      case "cognitive": return "border-orange-500/50 text-orange-400 bg-orange-950/40 shadow-[0_0_15px_rgba(249,115,22,0.15)]";
      case "proxy": return "border-cyan-500/50 text-cyan-400 bg-cyan-950/40 shadow-[0_0_20px_rgba(0,229,255,0.2)]";
      case "security": return "border-purple-500/50 text-purple-400 bg-purple-950/40 shadow-[0_0_15px_rgba(124,58,237,0.15)]";
      case "database": return "border-emerald-500/50 text-emerald-400 bg-emerald-950/40 shadow-[0_0_15px_rgba(34,197,94,0.15)]";
      default: return "border-slate-500/40 text-slate-400 bg-slate-950/40";
    }
  };

  const getNodeIcon = (category: string) => {
    switch (category) {
      case "agent": return <Cpu className="w-5 h-5 animate-pulse" />;
      case "cognitive": return <SearchCode className="w-5 h-5" />;
      case "proxy": return <Network className="w-5 h-5" />;
      case "security": return <Key className="w-5 h-5" />;
      case "database": return <Database className="w-5 h-5" />;
      default: return <Info className="w-5 h-5" />;
    }
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400">
            <Zap className="w-3.5 h-3.5" /> RUNTIME BLOCK TOPOLOGY
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            System Architecture
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
            RAG-Sec Standalone decouples cognitive agents from backends. Interactive layout. Click any block node to inspect roles, variables, and specs.
          </p>
        </div>

        {/* Info Helper alert banner */}
        <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs flex items-center justify-between max-w-3xl mx-auto">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4 shrink-0" />
            <span>Click on any core architecture node block below to open full security diagnostics.</span>
          </div>
          <span className="font-mono text-[10px] hidden sm:inline">PROT: mTLS ACTIVE</span>
        </div>

        {/* Interactive flow board container */}
        <div className="p-8 rounded-3xl bg-slate-900/40 border border-white/5 backdrop-blur-md relative overflow-x-auto min-w-[320px]">
          
          {/* Main Visual Schema Grid */}
          <div className="relative w-full max-w-5xl mx-auto min-h-[580px] py-6 flex flex-col items-center justify-between gap-12">
            
            {/* SVG Background Connecting Lines */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none z-0 hidden md:block" style={{ minHeight: "580px" }}>
              <defs>
                <linearGradient id="cyan-grad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#00E5FF" stopOpacity="0.8" />
                </linearGradient>
                <linearGradient id="purple-grad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#00E5FF" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#7C3AED" stopOpacity="0.8" />
                </linearGradient>
              </defs>
              
              {/* Agent -> Interceptor */}
              <path d="M 500,45 L 500,105" stroke="url(#cyan-grad)" strokeWidth="2.5" fill="none" strokeDasharray="5,5" className="animate-[dash_20s_linear_infinite]" />
              
              {/* Interceptor -> Proxy */}
              <path d="M 500,145 L 500,210" stroke="url(#cyan-grad)" strokeWidth="2.5" fill="none" />
              
              {/* Proxy Splits to Attestation & Honey Table */}
              <path d="M 500,250 C 500,290 280,290 280,315" stroke="url(#purple-grad)" strokeWidth="2" fill="none" />
              <path d="M 500,250 C 500,290 720,290 720,315" stroke="url(#purple-grad)" strokeWidth="2" fill="none" />

              {/* Attestation -> Prod Database */}
              <path d="M 280,355 L 280,455" stroke="#22C55E" strokeWidth="2" fill="none" strokeDasharray="4,4" />

              {/* Honey Table -> Sandbox Database */}
              <path d="M 720,355 L 720,455" stroke="#FF4D4F" strokeWidth="2" fill="none" strokeDasharray="4,4" />

              {/* Honey Table cross route to Prod Database for legitimate paths */}
              <path d="M 720,355 C 720,420 280,420 280,455" stroke="#E2E8F0" strokeWidth="1" strokeOpacity="0.3" fill="none" />
            </svg>

            {/* Stage 1: AI Agent */}
            <div className="relative z-10 flex justify-center w-full">
              {ARCHITECTURE_NODES.filter(n => n.id === "agent").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider">Cognitive Layer</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Role: LLM Reasoner
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Stage 2: Cognitive Interceptor */}
            <div className="relative z-10 flex justify-center w-full">
              {ARCHITECTURE_NODES.filter(n => n.id === "interceptor").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-orange-400">Policy Gate</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Task: Tool Call Validation
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Stage 3: Runtime Proxy */}
            <div className="relative z-10 flex justify-center w-full">
              {ARCHITECTURE_NODES.filter(n => n.id === "proxy").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-80 glow-cyan-pulse`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-cyan-300">Central Proxy</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Routing & Handshake: ACTIVE
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Stage 4: Attestation & Honey Table (Parallel) */}
            <div className="relative z-10 flex flex-col md:flex-row items-center justify-around w-full gap-8">
              {/* Left Column: Attestation Engine */}
              {ARCHITECTURE_NODES.filter(n => n.id === "attestation").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-purple-300">Transient Seal</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Mints: HMAC-SHA256 Token
                  </div>
                </motion.div>
              ))}

              {/* Right Column: Honey Table Detection */}
              {ARCHITECTURE_NODES.filter(n => n.id === "honey").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    <ShieldAlert className="w-5 h-5 text-red-400 animate-pulse" />
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-red-400 font-semibold">Decoy Router</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Defense: Table Decoy Snare
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Stage 5: Databases (Parallel Targets) */}
            <div className="relative z-10 flex flex-col md:flex-row items-center justify-around w-full gap-8">
              {/* Prod DB */}
              {ARCHITECTURE_NODES.filter(n => n.id === "prod_db").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-emerald-400">Verified Target</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Access: Restricted by Token
                  </div>
                </motion.div>
              ))}

              {/* Sandbox Decoy DB */}
              {ARCHITECTURE_NODES.filter(n => n.id === "sandbox_db").map(node => (
                <motion.div
                  key={node.id}
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer px-6 py-4 rounded-xl border text-center transition-all ${getNodeColor(node.category)} w-72`}
                >
                  <div className="flex items-center justify-center gap-2 mb-1.5">
                    {getNodeIcon(node.category)}
                    <span className="font-display font-bold text-xs uppercase tracking-wider text-yellow-400">Deception Cave</span>
                  </div>
                  <h3 className="text-white font-bold text-sm tracking-wide">{node.label}</h3>
                  <div className="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 py-1 px-2 rounded">
                    Access: Sandbox Deception
                  </div>
                </motion.div>
              ))}
            </div>

          </div>

        </div>

        {/* Diagnostic Modal Drawer */}
        <AnimatePresence>
          {selectedNode && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md"
            >
              <motion.div 
                initial={{ scale: 0.95, y: 15 }}
                animate={{ scale: 1, y: 0 }}
                exit={{ scale: 0.95, y: 15 }}
                className="w-full max-w-lg rounded-2xl bg-cyber-card border border-cyan-400/30 p-6 sm:p-8 space-y-6 shadow-[0_0_50px_rgba(0,229,255,0.15)] relative"
              >
                {/* Close Button */}
                <button 
                  onClick={() => setSelectedNode(null)}
                  className="absolute top-4 right-4 p-1.5 rounded-full hover:bg-white/10 text-slate-400 hover:text-white transition"
                >
                  <X className="w-5 h-5" />
                </button>

                {/* Modal Title Block */}
                <div className="space-y-2">
                  <div className="inline-flex items-center gap-1 text-[10px] font-mono text-cyan-400 tracking-wider uppercase border border-cyan-400/25 px-2 py-0.5 rounded">
                    NODE DIAGNOSTIC BLOCK
                  </div>
                  <h2 className="text-2xl font-display font-bold text-white flex items-center gap-2">
                    {getNodeIcon(selectedNode.category)}
                    {selectedNode.label}
                  </h2>
                  <p className="text-xs text-cyan-400/80 font-mono tracking-wide uppercase">
                    Role: {selectedNode.role}
                  </p>
                </div>

                {/* Node Description content */}
                <div className="space-y-4">
                  <div>
                    <h4 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-1">Functional Description</h4>
                    <p className="text-sm text-slate-300 leading-relaxed font-sans">{selectedNode.description}</p>
                  </div>

                  {/* Specifications & Parameters */}
                  <div>
                    <h4 className="text-xs font-semibold uppercase text-slate-400 tracking-wider mb-2">Technical Parameters</h4>
                    <ul className="space-y-2 font-mono text-xs text-cyan-300 bg-slate-950 p-4 rounded-xl border border-white/5">
                      {selectedNode.specs.map((spec, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                          <span>{spec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Bottom Dismiss */}
                <div className="pt-2 flex justify-end">
                  <button
                    onClick={() => setSelectedNode(null)}
                    className="px-5 py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wider uppercase transition-colors"
                  >
                    Close Diagnostics
                  </button>
                </div>

              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  );
}

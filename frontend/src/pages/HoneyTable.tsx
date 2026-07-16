import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  ShieldAlert, 
  Terminal, 
  Database, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Play,
  ArrowRight,
  UserCheck,
  ServerCrash,
  UserX,
  Lock,
  Compass
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

export default function HoneyTable() {
  const [activeTab, setActiveTab] = useState<"telemetry" | "deception_data">("telemetry");
  const [isSimulating, setIsSimulating] = useState(false);
  const [step, setStep] = useState(0);

  const realProductionRecords = [
    { id: "C-01", name: "Boeing Defense Corp", revenue: "$48.4B", rating: "Class A", token: "ACT_V1_8291" },
    { id: "C-02", name: "Lockheed Martin Sp", revenue: "$65.9B", rating: "Class AA", token: "ACT_V1_7410" },
    { id: "C-03", name: "Raytheon Technologies", revenue: "$56.1B", rating: "Class A", token: "ACT_V1_1028" }
  ];

  const syntheticDecoyRecords = [
    { id: "MOCK-91", name: "AeroDyne Systems Ltd", revenue: "$24.1B", rating: "Bait Class", token: "DECOY_TOKEN_01" },
    { id: "MOCK-92", name: "Apex Drone Services", revenue: "$12.8B", rating: "Bait Class", token: "DECOY_TOKEN_02" },
    { id: "MOCK-93", name: "Horizon Cyber LLC", revenue: "$18.4B", rating: "Bait Class", token: "DECOY_TOKEN_03" }
  ];

  const runDeceptionLoop = () => {
    setIsSimulating(true);
    setStep(1);
    
    setTimeout(() => setStep(2), 1500); // Trigger Intercept
    setTimeout(() => setStep(3), 3000); // Trigger Alert & Swap
    setTimeout(() => setStep(4), 4500); // Serve Sandbox data
  };

  const resetLoop = () => {
    setIsSimulating(false);
    setStep(0);
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-xs font-mono text-purple-400">
            <Compass className="w-3.5 h-3.5" /> SECURE DATA DECEPTION LAB
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            Honey Table Deception
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
            Deceive adversaries with realistic simulated metadata. When an attacker queries high-value decoy tables, RAG-Sec automatically redirects the session connection.
          </p>
        </div>

        {/* Dynamic Threat Warning SOC Alert Panel */}
        <AnimatePresence>
          {step >= 3 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              className="p-6 rounded-2xl bg-red-950/40 border-2 border-red-500/40 shadow-[0_0_30px_rgba(239,68,68,0.25)] flex flex-col md:flex-row items-start md:items-center justify-between gap-6 max-w-5xl mx-auto text-left relative overflow-hidden"
            >
              {/* Pulse alarm backing */}
              <div className="absolute inset-0 bg-red-500/5 animate-pulse pointer-events-none" />

              <div className="flex items-start gap-4 relative z-10">
                <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 animate-bounce">
                  <ShieldAlert className="w-8 h-8" />
                </div>
                <div className="space-y-1">
                  <h3 className="font-display font-bold text-lg text-white">CRITICAL SOC INCIDENT FLAG: Potential Insider Threat Detected</h3>
                  <p className="text-xs text-red-300 font-mono">
                    SIGNATURE: SELECT FROM HONEY-TABLE: <code className="bg-slate-950 text-white px-1.5 py-0.5 rounded">company_client_global_dump_2026</code>
                  </p>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    System Response: <strong>Transparent mTLS Connection string Swap</strong> executed. Swapping Production cluster for isolated Sandbox Deception Database. Servicing simulated data logs.
                  </p>
                </div>
              </div>

              <div className="shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded bg-red-500 text-white text-[10px] font-mono font-bold uppercase tracking-wider animate-pulse">
                <UserX className="w-4 h-4" /> Deception Isolated
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Interactive Lab panel workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start max-w-6xl mx-auto">
          
          {/* Left Block: Interactive terminal simulation controls */}
          <div className="lg:col-span-5 space-y-4">
            
            <div className="p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-6 text-left">
              <h3 className="font-display font-bold text-sm text-white uppercase tracking-wider border-b border-white/5 pb-2">
                Simulate Honey Table Sweep
              </h3>

              <div className="space-y-3 text-xs text-slate-300">
                <p>
                  RAG-Sec monitors requested SQL metadata schemas. When an attacker tries to grab tables starting with <code>dump_</code> or containing high-value financial targets, the system immediately diverts traffic.
                </p>
                <p className="font-mono text-[11px] text-purple-400">
                  Target Table: company_client_global_dump_2026
                </p>
              </div>

              {/* Console display query */}
              <div className="p-4 bg-slate-950 rounded-xl border border-white/5 font-mono text-xs text-slate-300 space-y-2">
                <span className="text-slate-500 text-[10px] uppercase">Malicious Probe Query</span>
                <code className="text-red-400 block break-all font-semibold">
                  SELECT client_id, balance_usd FROM company_client_global_dump_2026;
                </code>
              </div>

              {/* Run controls */}
              <div className="flex gap-4">
                {!isSimulating ? (
                  <button
                    onClick={runDeceptionLoop}
                    className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs uppercase tracking-wider transition cursor-pointer"
                  >
                    <Play className="w-4 h-4 fill-current animate-pulse" />
                    Simulate Scrape
                  </button>
                ) : (
                  <button
                    onClick={resetLoop}
                    className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-white/10 text-slate-300 hover:text-white font-bold text-xs uppercase tracking-wider transition cursor-pointer"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Reset Simulation
                  </button>
                )}
              </div>

            </div>

            {/* Deception Pipeline Console Log */}
            <div className="p-5 rounded-2xl bg-slate-950 border border-white/10 font-mono text-xs text-left space-y-3">
              <div className="flex items-center justify-between border-b border-white/5 pb-2 text-slate-500 text-[10px]">
                <span>HONEY CORE TRANSIT TELEMETRY</span>
                <span className="text-purple-400">LOG ACTIVE</span>
              </div>

              <div className="space-y-2 text-[11px] min-h-24">
                {step >= 1 && <div className="text-slate-300">&gt; Intruder session parsed payload...</div>}
                {step >= 2 && <div className="text-yellow-400 font-semibold">&gt; [ALERT] Query references monitored honey table!</div>}
                {step >= 3 && <div className="text-red-400 font-bold">&gt; [CRITICAL] Swapping PostgreSQL connection pool routing...</div>}
                {step >= 4 && <div className="text-green-400 font-semibold">&gt; [SUCCESS] Route completed. Served fake records seamlessly.</div>}
                {step === 0 && <div className="text-slate-600">Awaiting simulation trigger...</div>}
              </div>
            </div>

          </div>

          {/* Right Block: Telemetry visual comparison or connection redirection */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Visual routing schema */}
            <div className="p-6 rounded-2xl bg-cyber-card border border-white/5 shadow-lg relative text-left">
              <h3 className="font-display font-bold text-sm text-white mb-6 uppercase tracking-wider border-b border-white/5 pb-3">
                Transparent Connection Diverter
              </h3>

              {/* Simple visual schematic schema */}
              <div className="flex flex-col md:flex-row items-center justify-between gap-6 py-6 relative">
                
                {/* Node 1: Attacker */}
                <div className="p-4 rounded-xl border border-red-500/20 bg-red-950/20 text-center w-36 relative z-10">
                  <UserX className="w-6 h-6 text-red-400 mx-auto mb-1.5" />
                  <span className="font-display font-bold text-xs text-white">Attacker Bot</span>
                  <p className="text-[9px] text-red-300 font-mono mt-1">Querying DB</p>
                </div>

                <div className="text-slate-600 animate-pulse hidden md:block">
                  <ArrowRight className="w-5 h-5" />
                </div>

                {/* Node 2: RAG-Sec Gateway */}
                <div className="p-4 rounded-xl border border-cyan-400/30 bg-slate-900/60 text-center w-40 relative z-10 glow-cyan-pulse">
                  <Lock className="w-6 h-6 text-cyan-400 mx-auto mb-1.5" />
                  <span className="font-display font-bold text-xs text-white">Honey Detector</span>
                  <p className="text-[9px] text-cyan-300 font-mono mt-1">
                    {step >= 2 ? "SWAPPING ROUTE" : "MONITORING"}
                  </p>
                </div>

                <div className="text-slate-600 hidden md:block">
                  <ArrowRight className="w-5 h-5" />
                </div>

                {/* Node 3: Selected database target */}
                <div className="space-y-4">
                  {/* Prod Database */}
                  <div className={`p-3 rounded-lg border text-center w-36 transition duration-300 ${
                    step >= 3 ? "border-slate-800 bg-slate-950 opacity-20" : "border-emerald-500/25 bg-slate-900 text-emerald-400"
                  }`}>
                    <Database className="w-5 h-5 mx-auto mb-1" />
                    <span className="font-bold text-[10px]">Production DB</span>
                    <p className="text-[8px] text-slate-500 font-mono">SAFE & SECURED</p>
                  </div>

                  {/* Sandbox Database */}
                  <div className={`p-3 rounded-lg border text-center w-36 transition duration-300 ${
                    step >= 3 ? "border-purple-400 bg-purple-950/30 text-purple-300 shadow-[0_0_15px_rgba(124,58,237,0.25)]" : "border-slate-800 bg-slate-950 opacity-20"
                  }`}>
                    <Database className="w-5 h-5 mx-auto mb-1" />
                    <span className="font-bold text-[10px]">Sandbox Decoy DB</span>
                    <p className="text-[8px] text-purple-400 font-mono">HONEY DISPATCHED</p>
                  </div>
                </div>

              </div>

            </div>

            {/* Comparison database records returned to hacker */}
            <div className="p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-4 text-left shadow-lg">
              <div className="flex items-center justify-between border-b border-white/5 pb-2">
                <h3 className="font-display font-bold text-sm text-white">
                  Database Record Serving Matrix
                </h3>
                <span className="text-[10px] font-mono text-purple-400">ISOLATION LOGS</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {/* Real hidden table */}
                <div className="p-4 rounded-xl bg-slate-950 border border-white/5 space-y-3">
                  <h4 className="font-display font-semibold text-xs text-red-400 flex items-center gap-1.5 uppercase">
                    <Lock className="w-4 h-4" /> Real Enterprise Ledger (SHIELDED)
                  </h4>
                  <div className="space-y-2 text-[11px] font-mono text-slate-500">
                    {realProductionRecords.map((r) => (
                      <div key={r.id} className="flex justify-between border-b border-white/5 pb-1">
                        <span>{r.name}</span>
                        <span className="text-slate-600 font-bold">{r.revenue}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Simulated table served to attacker */}
                <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/20 space-y-3">
                  <h4 className="font-display font-semibold text-xs text-purple-400 flex items-center gap-1.5 uppercase animate-pulse">
                    <CheckCircle className="w-4 h-4 text-purple-400" /> Synthesized Mock served to attacker
                  </h4>
                  <div className="space-y-2 text-[11px] font-mono">
                    {step >= 4 ? (
                      syntheticDecoyRecords.map((r) => (
                        <div key={r.id} className="flex justify-between border-b border-white/5 pb-1 text-purple-300">
                          <span>{r.name}</span>
                          <span className="text-white font-bold">{r.revenue}</span>
                        </div>
                      ))
                    ) : (
                      <div className="text-slate-600 py-6 text-center">Awaiting query trigger...</div>
                    )}
                  </div>
                </div>

              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

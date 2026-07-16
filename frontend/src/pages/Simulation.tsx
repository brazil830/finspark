import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Play, 
  RotateCcw, 
  User, 
  Cpu, 
  Network, 
  ShieldCheck, 
  Key, 
  Search, 
  Database, 
  Terminal, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Lock,
  ArrowDown
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

interface Step {
  id: string;
  label: string;
  icon: React.ReactNode;
  details: string;
}

export default function Simulation() {
  const [activeScenario, setActiveScenario] = useState<string>("normal");
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(-1);
  const [simStatus, setSimStatus] = useState<"idle" | "running" | "completed">("idle");
  const [simulationLogs, setSimulationLogs] = useState<string[]>([]);
  
  const scenarios = [
    {
      id: "normal",
      name: "Normal Business Query",
      desc: "An authorized user queries regular business datasets via the AI assistant.",
      query: "SELECT customer_name, registration_date FROM client_onboarding LIMIT 3;",
      theme: "success", // Green flow
      colorClass: "text-green-400 border-green-500/30 bg-green-950/20",
      glowColor: "rgba(34, 197, 94, 0.4)",
      resultMessage: "ACCESS ALLOWED: Query verified, attestation token matches parameters.",
      stepsLimit: 8, // Goes all the way to DB (step index 7)
      failStep: -1,
      logs: [
        "[INFO] Initiating query transaction stream...",
        "[SUCCESS] AI Agent parsed user intent. Requested tool call: read_clients",
        "[SUCCESS] Zero-Trust mTLS handshaking active between AI cluster and proxy",
        "[SUCCESS] JSON-Schema structural validation: PASSED. Query structure secure.",
        "[SUCCESS] Mints single-use Attestation Token (HMAC-SHA256 signature generated)",
        "[SUCCESS] Context Check: user 'analyst_04' authorized to access 'client_onboarding'",
        "[SUCCESS] Honey Table Check: Targeted table is legitimate. No decoys touched.",
        "[SUCCESS] DB handshake approved. Retrieved 3 rows from PostgreSQL Cloud SQL!"
      ]
    },
    {
      id: "injection",
      name: "Prompt Injection Attack",
      desc: "An attacker inputs an administrative bypass prompt to delete user database schemas.",
      query: "SELECT * FROM users; DROP TABLE clients; --",
      theme: "danger", // Red flow
      colorClass: "text-red-400 border-red-500/30 bg-red-950/20",
      glowColor: "rgba(239, 68, 68, 0.4)",
      resultMessage: "ACCESS DENIED: Critical prompt injection signature detected at Schema Validation.",
      stepsLimit: 4, // Rejects at Schema Validation (step index 3)
      failStep: 3,
      logs: [
        "[INFO] Initiating query transaction stream...",
        "[SUCCESS] AI Agent compromised by injection. Formulated dangerous raw SQL tool call.",
        "[SUCCESS] Proxy intercepted outgoing transaction.",
        "[CRITICAL] SCHEMA VALIDATION FAILURE: Multiple query statements detected (DROP statement identified). Transaction blocked!"
      ]
    },
    {
      id: "exfiltration",
      name: "Mass Data Exfiltration",
      desc: "A user attempts to manipulate the agent to crawl the database schema and exfiltrate credentials.",
      query: "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME LIKE '%auth%';",
      theme: "danger",
      colorClass: "text-red-400 border-red-500/30 bg-red-950/20",
      glowColor: "rgba(239, 68, 68, 0.4)",
      resultMessage: "ACCESS DENIED: Session Context Mismatch. Query deviates from current task permissions.",
      stepsLimit: 6, // Rejects at Context Check (step index 5)
      failStep: 5,
      logs: [
        "[INFO] Initiating query transaction stream...",
        "[SUCCESS] AI Agent requests database metadata schema details.",
        "[SUCCESS] Proxy validation active.",
        "[SUCCESS] JSON Schema structural check: PASSED.",
        "[SUCCESS] Attestation Token minted tentatively (handshake pending context).",
        "[CRITICAL] CONTEXT ATTESTATION FAILURE: User session role (Support Specialist) is unauthorized for DB schema-traversal. Access denied!"
      ]
    },
    {
      id: "unauthorized",
      name: "Unauthorized Access Probe",
      desc: "An offline rogue container bypasses the agent and tries to connect to the DB directly without mTLS headers.",
      query: "SELECT salary_hash FROM executive_compensation WHERE grade = 'L10';",
      theme: "danger",
      colorClass: "text-red-400 border-red-500/30 bg-red-950/20",
      glowColor: "rgba(239, 68, 68, 0.4)",
      resultMessage: "ACCESS DENIED: No valid transient cryptographic attestation token provided.",
      stepsLimit: 5, // Rejects at Token Handshake (step index 4)
      failStep: 4,
      logs: [
        "[INFO] Direct socket request intercepted at database pool.",
        "[WARNING] Query lacks mTLS proxy signature headers.",
        "[WARNING] Proxy requested attestation hash validation.",
        "[WARNING] Invalid or expired cryptographic seal key parsed.",
        "[CRITICAL] DB CONNECTION DENIED: Handshake failure. No valid transient attestation token provided."
      ]
    },
    {
      id: "honey",
      name: "Honey Table Attack",
      desc: "An attacker scans the tables and queries a high-value bait database (Deception Honey Table).",
      query: "SELECT * FROM company_client_global_dump_2026 LIMIT 100;",
      theme: "warning", // Yellow flow
      colorClass: "text-purple-400 border-purple-500/30 bg-purple-950/20",
      glowColor: "rgba(124, 58, 237, 0.4)",
      resultMessage: "DECEPTION ENGAGED: Honey table sweep detected! Query routed to secure Sandbox DB.",
      stepsLimit: 8, // Finishes pipeline but routes to sandbox (warning highlight at step 6)
      failStep: -2, // Code for deception redirect
      logs: [
        "[INFO] Initiating query transaction stream...",
        "[SUCCESS] AI Agent requested tool call with target 'company_client_global_dump_2026'",
        "[SUCCESS] Interceptor parsed structured query",
        "[SUCCESS] Schema structure validated successfully",
        "[SUCCESS] Single-use transient attestation token generated",
        "[SUCCESS] Context Check: Authorized query parameters",
        "[WARNING] HONEY TABLE TARGETED! Table matches decoy list: [company_client_global_dump_2026]",
        "[CRITICAL SOC ALERT TRIGGERED] Potential Insider Scrape Attempt flagged!",
        "[DECEPTION ENGAGED] Interceptor swapped DB connections string to Isolated Deception Sandbox.",
        "[SUCCESS] Serving 100 synthesized realistic mock transactions safely!"
      ]
    }
  ];

  const currentScenario = scenarios.find(s => s.id === activeScenario) || scenarios[0];

  // Steps definition for the pipeline layout
  const pipelineSteps: Step[] = [
    { id: "user", label: "User Client", icon: <User className="w-4 h-4" />, details: "Client session initiating database requests" },
    { id: "agent", label: "AI Agent", icon: <Cpu className="w-4 h-4" />, details: "Formulates tool-calling JSON payload schemas" },
    { id: "proxy", label: "Runtime Proxy", icon: <Network className="w-4 h-4" />, details: "mTLS isolated network communication gateway" },
    { id: "schema", label: "Schema Validation", icon: <Search className="w-4 h-4" />, details: "Validates queries against JSON Schema models" },
    { id: "token", label: "Token Generation", icon: <Key className="w-4 h-4" />, details: "Mints single-use transient HMAC seals" },
    { id: "context", label: "Context Check", icon: <ShieldCheck className="w-4 h-4" />, details: "Validates semantic alignment of task permissions" },
    { id: "honey", label: "Honey Table Detection", icon: <AlertTriangle className="w-4 h-4" />, details: "Identifies and redirects decoy honey-table queries" },
    { id: "database", label: "Destination Database", icon: <Database className="w-4 h-4" />, details: "Production DB or Sandbox decoy DB target" }
  ];

  // Simulation run controller
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (simStatus === "running") {
      interval = setInterval(() => {
        setCurrentStepIndex(prev => {
          const nextIndex = prev + 1;
          
          // Stream logs sequentially
          if (currentScenario.logs[nextIndex]) {
            setSimulationLogs(old => [...old, currentScenario.logs[nextIndex]]);
          }

          // Stop conditions
          if (nextIndex >= currentScenario.stepsLimit - 1) {
            setSimStatus("completed");
            clearInterval(interval);
            return currentScenario.stepsLimit - 1;
          }
          return nextIndex;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [simStatus, activeScenario]);

  const startSimulation = () => {
    setSimStatus("running");
    setCurrentStepIndex(0);
    setSimulationLogs([currentScenario.logs[0]]);
  };

  const resetSimulation = () => {
    setSimStatus("idle");
    setCurrentStepIndex(-1);
    setSimulationLogs([]);
  };

  const selectScenario = (id: string) => {
    setActiveScenario(id);
    resetSimulation();
  };

  // Helper helper to color code the step circles
  const getStepStatusColor = (index: number) => {
    if (index > currentStepIndex) return "border-slate-800 text-slate-500 bg-slate-950"; // pending
    
    const isFailStep = currentScenario.failStep === index;
    const isDeceptionTrigger = currentScenario.id === "honey" && index === 6;

    if (isFailStep) return "border-red-500 text-red-400 bg-red-950/40 shadow-[0_0_15px_rgba(239,68,68,0.4)] animate-pulse";
    if (isDeceptionTrigger) return "border-purple-500 text-purple-400 bg-purple-950/40 shadow-[0_0_15px_rgba(124,58,237,0.4)] animate-pulse";
    
    // Success steps
    if (currentScenario.theme === "success") return "border-green-500 text-green-400 bg-green-950/20 shadow-[0_0_10px_rgba(34,197,94,0.25)]";
    if (currentScenario.theme === "warning") return "border-purple-400 text-purple-400 bg-purple-950/20 shadow-[0_0_10px_rgba(168,85,247,0.25)]";
    return "border-green-500 text-green-400 bg-green-950/20 shadow-[0_0_10px_rgba(34,197,94,0.25)]";
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400 animate-pulse">
            <Lock className="w-3.5 h-3.5" /> SECURITY PIPELINE PROVING LABS
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            Live Attack Simulator
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
            Execute safe queries and red-team attacks to witness the zero-trust pipeline, cryptographic attestation, and honey-table routing in action.
          </p>
        </div>

        {/* Simulator Grid layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: Attack Configuration Buttons */}
          <div className="lg:col-span-4 space-y-4">
            <div className="p-5 rounded-2xl bg-cyber-card border border-white/5 space-y-4">
              <h3 className="font-display font-bold text-sm text-white border-b border-white/5 pb-2 uppercase tracking-wide">
                Select Test Vector
              </h3>

              <div className="space-y-2">
                {scenarios.map((sc) => (
                  <button
                    key={sc.id}
                    onClick={() => selectScenario(sc.id)}
                    disabled={simStatus === "running"}
                    className={`w-full text-left p-4 rounded-xl border text-xs font-medium transition duration-200 cursor-pointer ${
                      activeScenario === sc.id
                        ? "bg-cyan-500/10 border-cyan-400 text-white shadow-[0_0_15px_rgba(0,229,255,0.15)]"
                        : "bg-slate-900/50 border-white/5 text-slate-400 hover:text-white hover:bg-slate-800/40"
                    }`}
                  >
                    <div className="flex items-center justify-between font-bold text-sm font-display mb-1 text-white">
                      <span>{sc.name}</span>
                      <span className={`w-2 h-2 rounded-full ${
                        sc.theme === "success" ? "bg-green-500" : sc.theme === "warning" ? "bg-purple-500" : "bg-red-500"
                      }`} />
                    </div>
                    <p className="text-[11px] text-slate-400 leading-normal">{sc.desc}</p>
                  </button>
                ))}
              </div>

              {/* Simulation Trigger buttons */}
              <div className="flex gap-3 pt-2">
                {simStatus === "idle" || simStatus === "completed" ? (
                  <button
                    onClick={startSimulation}
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs uppercase tracking-wider transition cursor-pointer"
                  >
                    <Play className="w-4 h-4 fill-current" />
                    Run Simulation
                  </button>
                ) : (
                  <button
                    disabled
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-slate-800 text-slate-500 text-xs uppercase font-bold tracking-wider"
                  >
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
                    Simulating...
                  </button>
                )}

                <button
                  onClick={resetSimulation}
                  className="px-4 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-white/10 text-slate-300 hover:text-white transition cursor-pointer"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>

            </div>

            {/* Active Query Display panel */}
            <div className="p-5 rounded-2xl bg-slate-950 border border-white/5 space-y-3 font-mono text-xs">
              <div className="text-slate-500 text-[10px] uppercase tracking-wider border-b border-white/5 pb-2">
                SQL Tool Call Output
              </div>
              <code className="text-cyan-300 block bg-slate-900 p-3 rounded-lg border border-white/5 overflow-x-auto whitespace-pre-wrap">
                {currentScenario.query}
              </code>
            </div>

          </div>

          {/* Right Column: Visualization Pipeline Flow */}
          <div className="lg:col-span-8 space-y-6">
            
            <div className="p-6 sm:p-8 rounded-2xl bg-cyber-card border border-white/5 relative shadow-lg">
              <h3 className="font-display font-bold text-sm text-white mb-6 uppercase tracking-wider border-b border-white/5 pb-3 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-cyan-400" />
                Interactive Validation Pipeline
              </h3>

              {/* Vertical Stack on mobile, grid grid on large screens */}
              <div className="flex flex-col gap-4 relative">
                
                {pipelineSteps.map((step, idx) => {
                  const isCurrent = currentStepIndex === idx;
                  const isPassed = currentStepIndex > idx;
                  const isFailed = currentScenario.failStep === idx;
                  const isHoneyRedirect = currentScenario.id === "honey" && idx === 6 && currentStepIndex >= 6;

                  return (
                    <div key={step.id} className="relative">
                      
                      {/* Connection arrow divider */}
                      {idx > 0 && (
                        <div className="absolute top-[-16px] left-6 h-4 w-0.5 border-l border-dashed border-cyan-400/20 hidden md:block" />
                      )}

                      <div 
                        className={`flex items-center gap-4 p-3 rounded-xl border transition-all duration-300 ${
                          isCurrent 
                            ? "bg-slate-900 border-cyan-400 shadow-[0_0_15px_rgba(0,229,255,0.1)] scale-[1.01]" 
                            : isPassed 
                            ? "bg-slate-900/40 border-white/5 opacity-80"
                            : "bg-transparent border-transparent opacity-40"
                        }`}
                      >
                        {/* Circle Badge Status */}
                        <div className={`w-12 h-12 rounded-full border-2 flex items-center justify-center transition-all ${getStepStatusColor(idx)}`}>
                          {step.icon}
                        </div>

                        {/* Step Details */}
                        <div className="flex-1 text-left">
                          <div className="flex items-center gap-2">
                            <span className="font-display font-bold text-sm text-white">{step.label}</span>
                            {isPassed && !isFailed && (
                              <span className="text-[10px] font-mono text-green-400 font-semibold">PASSED</span>
                            )}
                            {isFailed && (
                              <span className="text-[10px] font-mono text-red-400 font-semibold">BLOCKED</span>
                            )}
                            {isHoneyRedirect && idx === 6 && (
                              <span className="text-[10px] font-mono text-purple-400 font-semibold">HONEY DETECTED</span>
                            )}
                          </div>
                          <p className="text-xs text-slate-400">{step.details}</p>
                        </div>

                        {/* Interactive dynamic tracer or checks */}
                        <div className="text-right font-mono text-[10px]">
                          {isCurrent && (
                            <span className="text-cyan-400 animate-pulse font-bold uppercase">PROCESSING...</span>
                          )}
                          {isPassed && !isFailed && (
                            <CheckCircle className="w-5 h-5 text-green-400" />
                          )}
                          {isFailed && (
                            <XCircle className="w-5 h-5 text-red-500" />
                          )}
                          {isHoneyRedirect && idx === 6 && (
                            <AlertTriangle className="w-5 h-5 text-purple-400" />
                          )}
                        </div>

                      </div>
                    </div>
                  );
                })}

              </div>

              {/* Status Outcome Banner */}
              <AnimatePresence>
                {simStatus === "completed" && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`mt-6 p-4 rounded-xl border text-xs font-semibold ${
                      currentScenario.theme === "success" 
                        ? "bg-green-950/20 border-green-500/30 text-green-400"
                        : currentScenario.theme === "warning"
                        ? "bg-purple-950/20 border-purple-500/30 text-purple-400"
                        : "bg-red-950/20 border-red-500/30 text-red-400"
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      {currentScenario.theme === "success" && <CheckCircle className="w-5 h-5" />}
                      {currentScenario.theme === "warning" && <AlertTriangle className="w-5 h-5" />}
                      {currentScenario.theme === "danger" && <XCircle className="w-5 h-5" />}
                      <span>{currentScenario.resultMessage}</span>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

            </div>

            {/* Live Terminal Log Stream console */}
            <div className="p-5 rounded-xl bg-slate-950 border border-white/10 font-mono text-xs space-y-3">
              <div className="flex items-center justify-between border-b border-white/5 pb-2 text-slate-500 text-[10px]">
                <span className="flex items-center gap-1"><Terminal className="w-3.5 h-3.5" /> SECURE HANDSHAKE LOG STREAM</span>
                <span className="text-cyan-400 font-semibold animate-pulse">● LIVE</span>
              </div>
              
              <div className="space-y-1.5 max-h-48 overflow-y-auto min-h-24 text-left">
                {simulationLogs.length === 0 ? (
                  <div className="text-slate-600">No active transaction telemetry. Press "Run Simulation" above to begin.</div>
                ) : (
                  simulationLogs.map((log, index) => (
                    <div 
                      key={index} 
                      className={
                        log.includes("[SUCCESS]") ? "text-emerald-400" :
                        log.includes("[CRITICAL]") ? "text-red-400 font-semibold" :
                        log.includes("[WARNING]") || log.includes("[DECEPTION]") ? "text-purple-400" :
                        "text-slate-300"
                      }
                    >
                      {log}
                    </div>
                  ))
                )}
              </div>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Send, 
  Bot, 
  User, 
  Terminal, 
  CheckCircle, 
  Key, 
  ShieldCheck, 
  Cpu, 
  Database,
  ArrowRight,
  Sparkles,
  Lock
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

interface ChatMessage {
  sender: "user" | "bot";
  text: string;
  timestamp: string;
  pipeline?: {
    reasoning: string;
    toolCall: string;
    validation: string;
    token: string;
    response: string;
  };
}

export default function Assistant() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: "bot",
      text: "Welcome to RAG-Sec Standalone secure portal assistant. You can request enterprise queries here. My actions will undergo real-time Zero-Trust attestation validation.",
      timestamp: "13:10:00"
    }
  ]);
  const [input, setInput] = useState("");
  const [activeStage, setActiveStage] = useState<number>(-1);
  const [thinking, setThinking] = useState(false);

  // Pre-configured secure pipeline answers based on queries
  const pipelinePresets: Record<string, any> = {
    "retrieve account balance": {
      reasoning: "User is asking for sensitive customer financial logs. Need to execute 'read_balance' tool on finance records database.",
      toolCall: JSON.stringify({
        tool: "finance_records_query",
        arguments: {
          table: "ledger_balances",
          account_id: "ACC-84291",
          fields: ["balance", "currency"]
        }
      }, null, 2),
      validation: "JSON Schema match: OK. No secondary injections or unauthorized commands parsed.",
      token: "HMAC_SHA256_HASH(SecretHSMKey + 'ACC-84291' + 'analyst_role') = \n7b82f02cb932ae9e984fa5...",
      response: JSON.stringify({
        status: "SUCCESS",
        account_id: "ACC-84291",
        balance: "$124,592.80",
        currency: "USD"
      }, null, 2)
    },
    "check system logs": {
      reasoning: "User is checking core cluster node health. Inquiring on system logs table.",
      toolCall: JSON.stringify({
        tool: "ops_system_logs",
        arguments: {
          node: "PROXY-MAIN-01",
          level: "WARNING",
          limit: 2
        }
      }, null, 2),
      validation: "JSON Schema match: OK. Query targets legitimate operations logs table.",
      token: "HMAC_SHA256_HASH(SecretHSMKey + 'PROXY-MAIN-01' + 'ops_role') = \na89b3f2982dcb908a8e801...",
      response: JSON.stringify({
        status: "SUCCESS",
        node: "PROXY-MAIN-01",
        incidents_recorded: 0,
        handshaking: "VERIFIED"
      }, null, 2)
    },
    "update user emails": {
      reasoning: "Request to modify user profile table details via write command.",
      toolCall: JSON.stringify({
        tool: "write_user_profile",
        arguments: {
          action: "UPDATE",
          target_user: "alex_vane",
          new_email: "alex@ragsec.standalone"
        }
      }, null, 2),
      validation: "JSON Schema match: OK. Paramaterized query parameters authorized.",
      token: "HMAC_SHA256_HASH(SecretHSMKey + 'alex_vane' + 'admin_role') = \n92cdbe828a8d7d91e84a22...",
      response: JSON.stringify({
        status: "SUCCESS",
        target_user: "alex_vane",
        action: "UPDATE",
        rows_affected: 1
      }, null, 2)
    }
  };

  const handleSendPreset = (queryText: string) => {
    if (thinking) return;
    triggerChat(queryText);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || thinking) return;
    triggerChat(input);
    setInput("");
  };

  const triggerChat = (queryText: string) => {
    const formattedQuery = queryText.toLowerCase().trim();
    const newUserMessage: ChatMessage = {
      sender: "user",
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    };

    setMessages(prev => [...prev, newUserMessage]);
    setThinking(true);
    setActiveStage(0);

    const preset = pipelinePresets[formattedQuery] || {
      reasoning: "Analyzing user inquiry. Query does not map to explicit predefined tool paths.",
      toolCall: JSON.stringify({
        tool: "fallback_semantic_engine",
        arguments: { raw_text: queryText }
      }, null, 2),
      validation: "WARNING: Query does not match parameterized structures. Dispatched for deep inspections.",
      token: "HMAC_SHA256_HASH(SecretKey + 'fallback') = \nPENDING_AUTHORIZATION",
      response: JSON.stringify({
        status: "BLOCKED",
        reason: "Generic un-parameterized inquiries blocked. Please formulate structured requests."
      }, null, 2)
    };

    // Sequentially step through the animation stages to simulate the backend RAG-Sec validation pipeline
    let stage = 0;
    const interval = setInterval(() => {
      stage += 1;
      setActiveStage(stage);
      if (stage >= 5) {
        clearInterval(interval);
        setThinking(false);
        setActiveStage(-1);
        
        // Final assistant response message
        const finalBotMessage: ChatMessage = {
          sender: "bot",
          text: preset.status === "BLOCKED" 
            ? "Your request was blocked at verification. For cybersecurity reasons, only structured registered actions can be verified."
            : `I have completed the query successfully. The zero-trust attestation returned: ${JSON.parse(preset.response).balance || JSON.parse(preset.response).status}.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
          pipeline: preset
        };
        setMessages(prev => [...prev, finalBotMessage]);
      }
    }, 1500);
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400 animate-pulse">
            <Sparkles className="w-3.5 h-3.5" /> SECURE NATURAL LANGUAGE GATE
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            AI Assistant Demo
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
            Witness how RAG-Sec validates natural language queries by transforming them into signed structured tool calls.
          </p>
        </div>

        {/* Suggestion presets panel */}
        <div className="flex flex-wrap items-center justify-center gap-3 max-w-2xl mx-auto">
          <span className="text-xs text-slate-500 uppercase tracking-widest font-mono">Sample Queries:</span>
          <button 
            onClick={() => handleSendPreset("Retrieve account balance")}
            disabled={thinking}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-white/5 hover:border-cyan-400 text-xs font-mono text-cyan-300 cursor-pointer"
          >
            "Retrieve account balance"
          </button>
          <button 
            onClick={() => handleSendPreset("Check system logs")}
            disabled={thinking}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-white/5 hover:border-cyan-400 text-xs font-mono text-purple-300 cursor-pointer"
          >
            "Check system logs"
          </button>
          <button 
            onClick={() => handleSendPreset("Update user emails")}
            disabled={thinking}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-white/5 hover:border-cyan-400 text-xs font-mono text-green-300 cursor-pointer"
          >
            "Update user emails"
          </button>
        </div>

        {/* Chat UI Grid split */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* Chat Window Column */}
          <div className="lg:col-span-6 flex flex-col h-[580px] rounded-2xl bg-cyber-card border border-white/5 shadow-lg overflow-hidden">
            
            {/* Window header */}
            <div className="p-4 bg-slate-950 border-b border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-cyan-400" />
                <div>
                  <h3 className="font-display font-bold text-sm text-white">RAG-Sec Secure Shell</h3>
                  <span className="text-[10px] font-mono text-green-400 flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse inline-block" />
                    ATTESTATION ACTIVE
                  </span>
                </div>
              </div>
              <span className="text-[10px] font-mono text-slate-500 uppercase">SYS: ACTIVE</span>
            </div>

            {/* Chat message streams */}
            <div className="flex-1 p-4 overflow-y-auto space-y-4">
              {messages.map((m, idx) => (
                <div 
                  key={idx} 
                  className={`flex gap-3 max-w-[85%] ${m.sender === "user" ? "ml-auto flex-row-reverse" : ""}`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border ${
                    m.sender === "bot" 
                      ? "bg-slate-950 text-cyan-400 border-cyan-400/25" 
                      : "bg-slate-900 text-purple-400 border-purple-500/25"
                  }`}>
                    {m.sender === "bot" ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                  </div>

                  <div className={`p-3 rounded-xl border text-sm text-left ${
                    m.sender === "bot" 
                      ? "bg-slate-900/60 border-white/5 text-slate-100" 
                      : "bg-cyan-500/10 border-cyan-400/20 text-slate-100 shadow-[0_0_10px_rgba(0,229,255,0.05)]"
                  }`}>
                    <p className="leading-relaxed">{m.text}</p>
                    <span className="block text-[9px] text-slate-500 text-right mt-1.5 font-mono">{m.timestamp}</span>

                    {/* Mini code block for successful answers showing pipeline response */}
                    {m.pipeline && (
                      <div className="mt-3 p-2 bg-slate-950 rounded-lg border border-white/5 font-mono text-[10px] text-cyan-300">
                        <span className="text-slate-500 block border-b border-white/5 pb-1 mb-1 font-semibold uppercase">DB Attested Response:</span>
                        <pre className="overflow-x-auto">{m.pipeline.response}</pre>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {thinking && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-lg bg-slate-950 text-cyan-400 border border-cyan-400/25 flex items-center justify-center shrink-0">
                    <Bot className="w-4 h-4 animate-spin" />
                  </div>
                  <div className="p-3.5 rounded-xl border border-white/5 bg-slate-900/40 text-xs text-slate-400 font-mono">
                    <span className="animate-pulse">Interceptor parsing tool requirements...</span>
                  </div>
                </div>
              )}
            </div>

            {/* Chat Input form */}
            <form onSubmit={handleSubmit} className="p-4 bg-slate-950 border-t border-white/10 flex gap-2">
              <input 
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type 'Retrieve account balance'..."
                className="flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-white/10 focus:border-cyan-400/50 outline-none text-sm text-white font-sans"
              />
              <button 
                type="submit"
                className="p-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold transition duration-200 cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>

          </div>

          {/* Validation Pipeline Stages Details Column */}
          <div className="lg:col-span-6 flex flex-col justify-between p-6 sm:p-8 rounded-2xl bg-cyber-card border border-white/5 shadow-lg text-left">
            
            <div className="space-y-4">
              <h3 className="font-display font-bold text-sm text-white border-b border-white/5 pb-3 uppercase tracking-wider flex items-center gap-2">
                <Lock className="w-4.5 h-4.5 text-cyan-400" />
                Active Transaction Pipeline State
              </h3>

              <div className="space-y-4">
                
                {/* Stage 1 */}
                <div className={`p-4 rounded-xl border transition-all duration-300 ${
                  activeStage === 1 ? "bg-slate-900 border-cyan-400 shadow-[0_0_15px_rgba(0,229,255,0.1)]" : "bg-transparent border-transparent opacity-45"
                }`}>
                  <div className="flex items-center gap-2 font-display font-semibold text-xs text-white uppercase mb-1">
                    <Cpu className="w-4 h-4 text-cyan-400" />
                    Stage 1: AI Reasoning & Tool Formulate
                  </div>
                  <p className="text-[11px] text-slate-400">LLM parses chat parameters and formats structural tool calling JSON.</p>
                </div>

                {/* Stage 2 */}
                <div className={`p-4 rounded-xl border transition-all duration-300 ${
                  activeStage === 2 ? "bg-slate-900 border-cyan-400 shadow-[0_0_15px_rgba(0,229,255,0.1)]" : "bg-transparent border-transparent opacity-45"
                }`}>
                  <div className="flex items-center gap-2 font-display font-semibold text-xs text-white uppercase mb-1">
                    <ShieldCheck className="w-4 h-4 text-purple-400" />
                    Stage 2: Schema Interceptor Scan
                  </div>
                  <p className="text-[11px] text-slate-400">Compares SQL schemas and blocks nested exfiltration strings instantly.</p>
                </div>

                {/* Stage 3 */}
                <div className={`p-4 rounded-xl border transition-all duration-300 ${
                  activeStage === 3 ? "bg-slate-900 border-cyan-400 shadow-[0_0_15px_rgba(0,229,255,0.1)]" : "bg-transparent border-transparent opacity-45"
                }`}>
                  <div className="flex items-center gap-2 font-display font-semibold text-xs text-white uppercase mb-1">
                    <Key className="w-4 h-4 text-green-400" />
                    Stage 3: Cryptographic Token Minting
                  </div>
                  <p className="text-[11px] text-slate-400">Creates ephemeral HMAC security signature containing current session parameters.</p>
                </div>

                {/* Stage 4 */}
                <div className={`p-4 rounded-xl border transition-all duration-300 ${
                  activeStage === 4 ? "bg-slate-900 border-cyan-400 shadow-[0_0_15px_rgba(0,229,255,0.1)]" : "bg-transparent border-transparent opacity-45"
                }`}>
                  <div className="flex items-center gap-2 font-display font-semibold text-xs text-white uppercase mb-1">
                    <Database className="w-4 h-4 text-pink-400" />
                    Stage 4: Database Decoupled Handshake
                  </div>
                  <p className="text-[11px] text-slate-400">Unlocks SQL transaction tables with verified cryptokey, returning payload safely.</p>
                </div>

              </div>
            </div>

            {/* Micro logging board inside pipeline details */}
            <div className="mt-4 p-4 bg-slate-950 rounded-xl border border-white/5 font-mono text-[10px] text-slate-400">
              <div className="text-slate-500 font-semibold mb-1 uppercase tracking-wider">Active Pipeline Core:</div>
              {thinking ? (
                <div className="space-y-1 text-cyan-300">
                  <div>&gt; Attesting request context...</div>
                  <div>&gt; Token validation handshake pending...</div>
                </div>
              ) : (
                <div className="text-slate-500">&gt; Node idling. Ready to intercept transaction queries.</div>
              )}
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}

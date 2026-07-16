import React from "react";
import { motion } from "motion/react";
import { 
  AlertTriangle, 
  CheckCircle, 
  Lightbulb, 
  Briefcase, 
  TrendingUp, 
  ShieldCheck, 
  Terminal,
  Database,
  Search,
  Lock
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

export default function About() {
  const problemPoints = [
    {
      title: "SQL Injection via Prompts",
      desc: "Users manipulate LLMs via malicious prompts to generate dangerous SQL queries (e.g. 'OR 1=1' or 'DROP TABLE') that standard firewalls pass because the request comes from an authorized application server."
    },
    {
      title: "Agent Privilege Escalation",
      desc: "AI agents granted direct DB access can dynamically browse databases, access restricted HR payroll systems, or lateral-move across other unauthorized tables without centralized logging."
    },
    {
      title: "Data Exfiltration Loops",
      desc: "Compromised assistants can scrape entire database schemas, package sensitive clients information, and leak them in their conversational text stream back to malicious users."
    }
  ];

  const innovationPoints = [
    {
      title: "Transient Attestation Handshaking",
      desc: "Instead of direct DB logins, each agent query requires a single-use token minted on the fly by the interceptor. No token = instant database denial of service.",
      icon: Lock,
      color: "text-cyan-400"
    },
    {
      title: "Honey Table Traps",
      desc: "Deploy bait databases to instantly identify and record exfiltration sweeps. Serves synthetic data while preserving secure records.",
      icon: Database,
      color: "text-purple-400"
    },
    {
      title: "Cognitive Interception",
      desc: "Real-time semantic parse of incoming queries. Checks parameters against precise schema rules at microsecond speeds before execution.",
      icon: Search,
      color: "text-emerald-400"
    }
  ];

  const targetIndustries = [
    { name: "Banking & Fintech", spec: "Protects consumer transactions and accounts data.", active: true },
    { name: "Healthcare & HIPAA", spec: "Secures sensitive clinical records and patient data.", active: true },
    { name: "Defense & Government", spec: "Ensures military-grade authorization filters for AI logs.", active: true },
    { name: "Enterprise SaaS Platforms", spec: "Enables secure multi-tenant dataset workspace protection.", active: true }
  ];

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400">
            <ShieldCheck className="w-3.5 h-3.5" /> THE RAG-SEC MANIFESTO
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            About RAG-Sec Standalone
          </h1>
          <p className="text-slate-400 max-w-3xl mx-auto text-base">
            Securing the gap between cognitive AI reasoning systems and transactional business storage.
          </p>
        </div>

        {/* Problem vs Solution Matrix */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Problem Card */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-8 rounded-2xl bg-slate-900/60 border border-red-500/20 backdrop-blur-md relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 rounded-full blur-3xl" />
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/30 flex items-center justify-center text-red-400">
                <AlertTriangle className="w-5.5 h-5.5" />
              </div>
              <h2 className="font-display font-bold text-xl text-white">The Threat: Unsecured AI Access</h2>
            </div>
            
            <div className="space-y-6">
              {problemPoints.map((pt, i) => (
                <div key={i} className="border-l-2 border-red-500/30 pl-4 space-y-1">
                  <h4 className="font-semibold text-white text-sm">{pt.title}</h4>
                  <p className="text-xs text-slate-400 leading-relaxed">{pt.desc}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Solution Card */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="p-8 rounded-2xl bg-slate-900/60 border border-green-500/20 backdrop-blur-md relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/5 rounded-full blur-3xl" />
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-lg bg-green-500/10 border border-green-500/30 flex items-center justify-center text-green-400">
                <CheckCircle className="w-5.5 h-5.5" />
              </div>
              <h2 className="font-display font-bold text-xl text-white">The Shield: Zero-Trust Runtime Interceptor</h2>
            </div>
            
            <p className="text-xs text-slate-300 leading-relaxed mb-6">
              RAG-Sec stands as a virtual firewall. AI systems possess zero permanent connection keys. When an action is demanded, the Interceptor parses the structured tool, verifies database permissions, matches with the user context, and only then mints an ephemeral connection string valid for just 30 seconds.
            </p>

            <div className="space-y-4 text-xs font-mono text-green-400 bg-slate-950/70 p-4 rounded-xl border border-green-500/10">
              <div>[SECURE STATUS] Cognitive Interception: ACTIVE</div>
              <div>[SECURE STATUS] HMAC Key Rollover: SYNCED</div>
              <div>[SECURE STATUS] Unauthorized schemas blocked: 1,428</div>
            </div>
          </motion.div>

        </div>

        {/* Technological Innovations */}
        <div className="space-y-8">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-cyan-400" />
            <h2 className="font-display font-bold text-2xl text-white">Key Innovation Highlights</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {innovationPoints.map((item, index) => {
              const Icon = item.icon;
              return (
                <motion.div
                  key={index}
                  whileHover={{ y: -5 }}
                  className="p-6 rounded-xl bg-cyber-card border border-white/5 space-y-4 relative"
                >
                  <div className={`w-10 h-10 rounded-lg bg-slate-900 flex items-center justify-center ${item.color} border border-white/10`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-display font-semibold text-white">{item.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Target Industries & Expected Impact */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Industries */}
          <div className="lg:col-span-6 space-y-6">
            <div className="flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-purple-400" />
              <h2 className="font-display font-bold text-2xl text-white">Target Verticals</h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {targetIndustries.map((ind, i) => (
                <div key={i} className="p-4 rounded-xl bg-slate-900/40 border border-white/5 space-y-1 hover:border-cyan-400/20 transition">
                  <div className="font-semibold text-xs text-white flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    {ind.name}
                  </div>
                  <p className="text-[11px] text-slate-400">{ind.spec}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Expected Impact */}
          <div className="lg:col-span-6 space-y-6">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-cyan-400" />
              <h2 className="font-display font-bold text-2xl text-white">Expected Operational Impact</h2>
            </div>
            <div className="p-6 rounded-xl bg-slate-900/40 border border-white/5 space-y-4">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="space-y-1">
                  <div className="text-[20px] font-display font-bold text-green-400">100%</div>
                  <p className="text-[9px] text-slate-400 tracking-wider">Prompt Injection Immunity</p>
                </div>
                <div className="space-y-1">
                  <div className="text-[20px] font-display font-bold text-cyan-400">&lt;3ms</div>
                  <p className="text-[9px] text-slate-400 tracking-wider">Verification Overhead</p>
                </div>
                <div className="space-y-1">
                  <div className="text-[20px] font-display font-bold text-purple-400">0%</div>
                  <p className="text-[9px] text-slate-400 tracking-wider">Production Database Leaks</p>
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                RAG-Sec secures compliance for sensitive data queries. It serves as an audit trail, keeping database logs clear of generic machine requests and recording each action back to a real authenticated user.
              </p>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

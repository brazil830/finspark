import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "motion/react";
import { 
  Shield, 
  Database, 
  Cpu, 
  Lock, 
  AlertOctagon, 
  Terminal, 
  ArrowRight, 
  Activity, 
  Zap,
  RefreshCw
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

// Custom light-weight animated counter for premium design
function AnimatedCounter({ end, suffix = "", duration = 1500 }: { end: number; suffix?: string; duration?: number }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTimestamp: number | null = null;
    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      setCount(Math.floor(progress * end));
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  }, [end, duration]);

  return (
    <span className="font-display font-bold text-3xl sm:text-4xl text-white tracking-tight">
      {count.toLocaleString()}{suffix}
    </span>
  );
}

export default function Landing() {
  const [activeTab, setActiveTab] = useState<"cognitive" | "execution" | "deception">("cognitive");

  const pillars = [
    {
      id: "cognitive",
      title: "Cognitive Plane Interception",
      description: "Intercepts and schema-validates outgoing AI tool-calls in micro-milliseconds before execution.",
      icon: Cpu,
      color: "from-cyan-400 to-blue-500",
      accent: "text-cyan-400"
    },
    {
      id: "execution",
      title: "Cryptographic Attestation",
      description: "Mints single-use transient HMAC-SHA256 tokens to prove session authenticity and user context.",
      icon: Lock,
      color: "from-purple-500 to-indigo-600",
      accent: "text-purple-400"
    },
    {
      id: "deception",
      title: "Honey Table Deception",
      description: "Traps data scraping bots by transparently redirecting malicious queries to realistic sandbox databases.",
      icon: Database,
      color: "from-red-400 to-pink-500",
      accent: "text-red-400"
    }
  ];

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col">
      <ParticleBackground />

      {/* Hero Section */}
      <section className="relative z-10 pt-20 pb-16 md:pt-32 md:pb-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Hero Content */}
          <div className="lg:col-span-7 space-y-8 text-left">
            
            {/* Tagline Badge */}
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-3  py-1.5 rounded-full bg-cyan-400/10 border border-cyan-400/20 text-xs text-cyan-400 font-mono tracking-wide"
            >
              <Zap className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
              <span>HACKATHON STANDALONE PROTOTYPE</span>
            </motion.div>

            {/* Main Headline */}
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="font-display font-extrabold text-4xl sm:text-5xl lg:text-6xl text-white tracking-tight leading-none"
            >
              Zero-Trust <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-cyan-400 bg-300% animate-gradient">
                Runtime Security
              </span> <br />
              for AI Agents.
            </motion.h1>

            {/* Description */}
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed font-sans"
            >
              Protect enterprise databases from autonomous LLM subversion. RAG-Sec Standalone sits transparently between the 
              <strong> Cognitive Plane</strong> (AI reasoning) and <strong>Execution Plane</strong> (Databases), validating structured 
              tool calls, minting transient HMAC attestation tokens, and deploying honey-table honeytraps.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 pt-2"
            >
              <Link 
                to="/simulation" 
                className="group relative flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 text-slate-950 font-bold transition-all duration-300 shadow-[0_0_20px_rgba(0,229,255,0.4)] hover:shadow-[0_0_30px_rgba(0,229,255,0.6)]"
              >
                Launch Attack Simulator
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <Link 
                to="/dashboard" 
                className="flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-white/10 hover:border-cyan-400/50 text-white font-medium transition-all duration-300"
              >
                <Activity className="w-4 h-4 text-cyan-400" />
                View SOC Dashboard
              </Link>
            </motion.div>

            {/* Secured DB Micro Badges */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="pt-4 flex flex-wrap items-center gap-4 text-slate-500 text-xs font-mono"
            >
              <span>SUPPORTED ENGINES:</span>
              <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900/50 px-2 py-1 rounded border border-white/5">
                <Database className="w-3.5 h-3.5" /> PostgreSQL
              </div>
              <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900/50 px-2 py-1 rounded border border-white/5">
                <Database className="w-3.5 h-3.5" /> Google Spanner
              </div>
              <div className="flex items-center gap-1.5 text-slate-400 bg-slate-900/50 px-2 py-1 rounded border border-white/5">
                <Database className="w-3.5 h-3.5" /> BigQuery
              </div>
            </motion.div>

          </div>

          {/* Right Hero Visualization */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-5 relative flex justify-center"
          >
            {/* Dynamic Glass Shield Visualization */}
            <div className="w-full max-w-[420px] aspect-square rounded-3xl relative flex items-center justify-center border border-cyan-400/20 bg-slate-950/40 backdrop-blur-md shadow-[0_0_50px_rgba(0,229,255,0.05)] overflow-hidden">
              
              {/* Spinning cyber locks */}
              <div className="absolute inset-4 rounded-full border border-dashed border-cyan-400/10 animate-[spin_50s_linear_infinite]" />
              <div className="absolute inset-10 rounded-full border border-dashed border-purple-500/10 animate-[spin_30s_linear_infinite_reverse]" />
              <div className="absolute inset-16 rounded-full border border-cyan-400/20" />

              {/* Central Glowing Shield */}
              <div className="relative z-10 flex flex-col items-center text-center p-6 space-y-4">
                <div className="w-20 h-20 rounded-2xl bg-cyan-500/15 border border-cyan-400/40 flex items-center justify-center text-cyan-400 shadow-[0_0_30px_rgba(0,229,255,0.2)] animate-pulse">
                  <Shield className="w-10 h-10" />
                </div>
                <div>
                  <h3 className="font-display font-semibold text-lg text-white">RAG-Sec Core Core</h3>
                  <p className="text-[11px] text-slate-400 font-mono tracking-wider mt-1">mTLS SECURE NODE: STANDALONE</p>
                </div>
                
                {/* Micro console log */}
                <div className="w-full bg-slate-950 p-3 rounded-lg border border-white/5 text-left font-mono text-[10px] space-y-1 text-cyan-300">
                  <div className="flex justify-between text-slate-500">
                    <span>[SYS STATE]</span>
                    <span>13:15:42</span>
                  </div>
                  <div className="text-emerald-400">✓ Cognitive schema loaded</div>
                  <div className="text-purple-400">✓ Ephemeral crypto key generated</div>
                  <div className="text-slate-400">○ Monitoring 18 databases...</div>
                </div>
              </div>

              {/* Animated Floating Badges */}
              <div className="absolute top-8 left-8 p-2 rounded-lg bg-slate-900/90 border border-red-500/30 text-red-400 flex items-center gap-1.5 text-[10px] font-mono animate-bounce">
                <AlertOctagon className="w-3.5 h-3.5" />
                <span>INJECTION BLOCKED</span>
              </div>

              <div className="absolute bottom-10 right-6 p-2 rounded-lg bg-slate-900/90 border border-green-500/30 text-green-400 flex items-center gap-1.5 text-[10px] font-mono animate-pulse">
                <Lock className="w-3.5 h-3.5" />
                <span>TOKEN VERIFIED</span>
              </div>

            </div>
          </motion.div>

        </div>
      </section>

      {/* Statistics Counter Ribbon */}
      <section className="relative z-10 border-y border-white/10 bg-slate-950/80 backdrop-blur-sm py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-1">
              <div className="text-[11px] font-mono text-cyan-400 tracking-widest uppercase">Threats Blocked</div>
              <div className="text-3xl font-display font-extrabold text-white">
                <AnimatedCounter end={14285} suffix="+" />
              </div>
              <p className="text-[10px] text-slate-400">99.98% Real-Time Defense</p>
            </div>
            <div className="space-y-1">
              <div className="text-[11px] font-mono text-purple-400 tracking-widest uppercase">Secure Agents Connected</div>
              <div className="text-3xl font-display font-extrabold text-white">
                <AnimatedCounter end={248} />
              </div>
              <p className="text-[10px] text-slate-400">Cognitive Plane Enrolled</p>
            </div>
            <div className="space-y-1">
              <div className="text-[11px] font-mono text-green-400 tracking-widest uppercase">Verified DB Queries</div>
              <div className="text-3xl font-display font-extrabold text-white">
                <AnimatedCounter end={842930} suffix="+" />
              </div>
              <p className="text-[10px] text-slate-400">Latency &lt; 2.5ms Avg</p>
            </div>
            <div className="space-y-1">
              <div className="text-[11px] font-mono text-pink-400 tracking-widest uppercase">Deception Honeytables</div>
              <div className="text-3xl font-display font-extrabold text-white">
                <AnimatedCounter end={32} />
              </div>
              <p className="text-[10px] text-slate-400">Active Deception Decoys</p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Technology Pillars */}
      <section className="relative z-10 py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-4 mb-16">
          <h2 className="font-display font-bold text-3xl sm:text-4xl text-white">
            Comprehensive Agent Database Interception
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm">
            RAG-Sec injects a deep zero-trust security state between the LLM and your data infrastructure.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {pillars.map((p, index) => {
            const IconComponent = p.icon;
            return (
              <motion.div
                key={p.id}
                whileHover={{ y: -6, borderColor: "rgba(0, 229, 255, 0.3)" }}
                transition={{ duration: 0.3 }}
                className="p-8 rounded-2xl bg-cyber-card border border-white/5 relative overflow-hidden group shadow-lg"
              >
                {/* Gradient Accent Background glow */}
                <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/10 transition-colors" />
                
                <div className="space-y-6 relative z-10">
                  <div className={`w-12 h-12 rounded-xl bg-slate-900 border border-white/10 flex items-center justify-center ${p.accent}`}>
                    <IconComponent className="w-6 h-6" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="font-display font-bold text-lg text-white group-hover:text-cyan-400 transition-colors">
                      {p.title}
                    </h3>
                    <p className="text-sm text-slate-400 leading-relaxed">
                      {p.description}
                    </p>
                  </div>
                  <div className="pt-2">
                    <span className={`text-xs font-mono font-semibold tracking-wider flex items-center gap-1 ${p.accent}`}>
                      DEPLOYED STATE <span className="inline-block w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                    </span>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Deception Pipeline Demonstration Highlight */}
      <section className="relative z-10 py-16 bg-slate-950/40 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="p-8 md:p-12 rounded-3xl border border-cyan-400/10 bg-slate-900/40 backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-[-30%] right-[-10%] w-[350px] h-[350px] rounded-full bg-purple-500/5 blur-[120px] pointer-events-none" />
            
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-7 space-y-6">
                <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-purple-500/10 border border-purple-500/30 text-[10px] font-mono text-purple-400">
                  <Terminal className="w-3.5 h-3.5" /> DECEPTION HONEY-SYSTEM ACTIVE
                </div>
                <h2 className="font-display font-bold text-2xl sm:text-3xl text-white">
                  Trap Rogue Agents and Insiders Alike
                </h2>
                <p className="text-slate-300 text-sm leading-relaxed">
                  RAG-Sec automatically synthesizes mock schemas on the fly. When a compromised assistant or malicious administrator initiates a scan of forbidden client tables, they are immediately redirected to a virtual sandbox database containing highly realistic mock corporate data. The system alerts the Security Operations Center (SOC) immediately while the attacker wastes time parsing honey-tokens.
                </p>
                <div className="flex gap-4">
                  <Link 
                    to="/simulation" 
                    className="inline-flex items-center gap-2 text-xs font-mono text-cyan-400 hover:text-cyan-300 font-bold tracking-wide group"
                  >
                    TEST DECEPTION SIMULATOR 
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </div>
              <div className="lg:col-span-5 bg-slate-950 p-6 rounded-2xl border border-white/5 font-mono text-xs text-slate-300 space-y-3">
                <div className="text-slate-500 flex justify-between border-b border-white/5 pb-2">
                  <span>SANDBOX DECEPTION CONTROLLER</span>
                  <span className="text-cyan-400">ONLINE</span>
                </div>
                <div className="space-y-1.5">
                  <div className="text-yellow-500 font-bold">[WARN] Query target identified as Decoy Table</div>
                  <div className="text-slate-400">&gt; Target: <span className="text-white font-semibold">company_client_global_dump_2026</span></div>
                  <div className="text-purple-400">&gt; Status: Swapping connection strings to Sandbox DB</div>
                  <div className="text-green-400">&gt; Serving 500 fake synthetic records dynamically</div>
                  <div className="text-red-400 font-semibold">&gt; CRITICAL SOC ALERT PROVOKED</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}

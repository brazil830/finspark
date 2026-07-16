import React from "react";
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  LineChart, 
  Line, 
  Legend 
} from "recharts";
import { 
  ShieldCheck, 
  TrendingUp, 
  PieChart as PieIcon, 
  BarChart2, 
  Activity, 
  Lock, 
  Sliders, 
  ArrowRight 
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

// Analytics datasets
const threatDistributionData = [
  { day: "07/10", Injection: 15, Exfiltration: 5, SchemaBypass: 12 },
  { day: "07/11", Injection: 22, Exfiltration: 8, SchemaBypass: 19 },
  { day: "07/12", Injection: 30, Exfiltration: 14, SchemaBypass: 15 },
  { day: "07/13", Injection: 25, Exfiltration: 10, SchemaBypass: 22 },
  { day: "07/14", Injection: 45, Exfiltration: 24, SchemaBypass: 32 },
  { day: "07/15", Injection: 35, Exfiltration: 18, SchemaBypass: 28 },
  { day: "07/16", Injection: 40, Exfiltration: 21, SchemaBypass: 30 }
];

const topAttacksData = [
  { name: "SQL Prompt Inject", count: 485, severity: "CRITICAL" },
  { name: "Schema Traversal", count: 320, severity: "HIGH" },
  { name: "Honey Table Scan", count: 245, severity: "CRITICAL" },
  { name: "Unauthenticated API", count: 180, severity: "MEDIUM" },
  { name: "Privilege Escalate", count: 95, severity: "HIGH" }
];

const tokenUsageData = [
  { name: "Verified & Executed", value: 12400, color: "#22C55E" },
  { name: "Expired & Dropped", value: 850, color: "#7C3AED" },
  { name: "Invalid Signature", value: 340, color: "#FF4D4F" }
];

const requestVolumeData = [
  { hour: "00:00", Queries: 1200, Latency: 1.8 },
  { hour: "04:00", Queries: 850, Latency: 1.6 },
  { hour: "08:00", Queries: 2400, Latency: 2.3 },
  { hour: "12:00", Queries: 3100, Latency: 2.1 },
  { hour: "16:00", Queries: 2800, Latency: 1.9 },
  { hour: "20:00", Queries: 1900, Latency: 1.7 }
];

export default function Analytics() {
  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400 animate-pulse">
            <Sliders className="w-3.5 h-3.5" /> SECURE AUDIT ANALYTICS ENGINE
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            Security Analytics
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm">
            Deep forensic telemetry dashboards summarizing agent transaction volume, threat distribution curves, and cryptographic token verification rates.
          </p>
        </div>

        {/* 4-Chart Bento Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* Area Chart: Threat Distribution Over Time */}
          <div className="lg:col-span-8 p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-4 text-left shadow-lg">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white flex items-center gap-2">
                <TrendingUp className="w-4.5 h-4.5 text-cyan-400" />
                Intercepted Threat Distribution Over Time
              </h3>
              <span className="text-[10px] font-mono text-slate-500">7 DAY TELEMETRY</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={threatDistributionData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="inj" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FF4D4F" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#FF4D4F" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="exf" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#7C3AED" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="sb" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#00E5FF" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="day" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis stroke="#64748B" style={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Area type="monotone" dataKey="Injection" stroke="#FF4D4F" fillOpacity={1} fill="url(#inj)" />
                  <Area type="monotone" dataKey="Exfiltration" stroke="#7C3AED" fillOpacity={1} fill="url(#exf)" />
                  <Area type="monotone" dataKey="SchemaBypass" stroke="#00E5FF" fillOpacity={1} fill="url(#sb)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Pie Chart: Token Verification Success */}
          <div className="lg:col-span-4 p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-4 flex flex-col justify-between text-left shadow-lg">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white flex items-center gap-2">
                <PieIcon className="w-4.5 h-4.5 text-purple-400" />
                Token Attestation Success Mix
              </h3>
            </div>

            <div className="h-48 w-full relative flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={tokenUsageData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {tokenUsageData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-lg font-display font-bold text-white">13.5K</span>
                <span className="text-[9px] text-slate-500 font-mono">TOTAL TOKENS</span>
              </div>
            </div>

            <div className="space-y-1.5 font-mono text-[10px] text-slate-400">
              <div className="flex justify-between">
                <span className="text-green-400">● Verified & Executed:</span>
                <span className="text-white font-bold">12,400 (91.2%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-400">● Expired & Dropped:</span>
                <span className="text-white font-bold">850 (6.3%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-red-400">● Invalid Signature:</span>
                <span className="text-white font-bold">340 (2.5%)</span>
              </div>
            </div>
          </div>

          {/* Bar Chart: Top Attacks Blocked */}
          <div className="lg:col-span-6 p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-4 text-left shadow-lg">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white flex items-center gap-2">
                <BarChart2 className="w-4.5 h-4.5 text-red-400" />
                Top Attack Vectors Prevented
              </h3>
              <span className="text-[10px] font-mono text-red-400">THREAT INCIDENTS</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={topAttacksData} layout="vertical" margin={{ top: 10, right: 10, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis type="number" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis dataKey="name" type="category" stroke="#64748B" style={{ fontSize: 9 }} width={110} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Bar dataKey="count" fill="#FF4D4F" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Line Chart: Request Volume vs Latency */}
          <div className="lg:col-span-6 p-6 rounded-2xl bg-cyber-card border border-white/5 space-y-4 text-left shadow-lg">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white flex items-center gap-2">
                <Activity className="w-4.5 h-4.5 text-green-400" />
                Proxy Request Volume & Latency Scale
              </h3>
              <span className="text-[10px] font-mono text-green-400">mTLS CHANNELS</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={requestVolumeData} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="hour" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis stroke="#64748B" style={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Line type="monotone" dataKey="Queries" stroke="#00E5FF" strokeWidth={2} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="Latency" stroke="#22C55E" strokeWidth={1.5} strokeDasharray="4 4" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>

        {/* Dynamic score summary block */}
        <div className="p-6 rounded-2xl bg-slate-900/50 border border-cyan-400/10 flex flex-col md:flex-row items-center justify-between gap-6 max-w-4xl mx-auto text-left">
          <div className="space-y-1">
            <h4 className="font-display font-semibold text-white flex items-center gap-1.5 uppercase">
              <Lock className="w-4 h-4 text-cyan-400 animate-pulse" /> mTLS Compliance Health Factor
            </h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              Based on single-use key rotations, schema structural parameters compliance, and sandbox threat isolation ratings, RAG-Sec Standalone is score-rated at <strong>99.8% defensive efficiency</strong>.
            </p>
          </div>
          <div className="shrink-0 text-center">
            <span className="text-3xl font-display font-extrabold text-cyan-400 block">A+</span>
            <span className="text-[9px] font-mono text-slate-500 uppercase">OWASP LLM SECURE</span>
          </div>
        </div>

      </div>
    </div>
  );
}

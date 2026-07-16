import React, { useState, useEffect } from "react";
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  PieChart, 
  Pie, 
  Cell, 
  BarChart, 
  Bar, 
  LineChart, 
  Line, 
  Legend 
} from "recharts";
import { 
  ShieldAlert, 
  Cpu, 
  Key, 
  Activity, 
  Database, 
  Heart, 
  Terminal, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  AlertTriangle 
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";
import { SECURITY_LOGS } from "../constants";

// Dummy datasets for Recharts
const attackTimelineData = [
  { time: "08:00", Injection: 12, Exfiltration: 4, Unauth: 8 },
  { time: "09:00", Injection: 19, Exfiltration: 2, Unauth: 14 },
  { time: "10:00", Injection: 15, Exfiltration: 9, Unauth: 5 },
  { time: "11:00", Injection: 34, Exfiltration: 15, Unauth: 22 },
  { time: "12:00", Injection: 22, Exfiltration: 6, Unauth: 11 },
  { time: "13:00", Injection: 45, Exfiltration: 28, Unauth: 19 },
];

const trendData = [
  { day: "Mon", Threats: 120, Tokens: 450, Queries: 1200 },
  { day: "Tue", Threats: 150, Tokens: 510, Queries: 1400 },
  { day: "Wed", Threats: 190, Tokens: 620, Queries: 1850 },
  { day: "Thu", Threats: 230, Tokens: 590, Queries: 1600 },
  { day: "Fri", Threats: 170, Tokens: 680, Queries: 2100 },
  { day: "Sat", Threats: 110, Tokens: 320, Queries: 950 },
  { day: "Sun", Threats: 95, Tokens: 380, Queries: 1100 },
];

const requestStatusData = [
  { name: "Allowed Queries", value: 720 },
  { name: "Blocked (Schema)", value: 140 },
  { name: "Redirected (Honey)", value: 85 },
];

const databaseActivityData = [
  { hour: "10am", ProdQueries: 140, SandboxQueries: 15 },
  { hour: "11am", ProdQueries: 230, SandboxQueries: 48 },
  { hour: "12pm", ProdQueries: 180, SandboxQueries: 22 },
  { hour: "1pm", ProdQueries: 310, SandboxQueries: 75 },
  { hour: "2pm", ProdQueries: 260, SandboxQueries: 41 },
];

const COLORS = ["#22C55E", "#FF4D4F", "#7C3AED"];

export default function Dashboard() {
  const [threatCount, setThreatCount] = useState(14285);
  const [activeTokens, setActiveTokens] = useState(18);
  const [activeLogs, setActiveLogs] = useState(SECURITY_LOGS);
  const [loading, setLoading] = useState(false);

  // Dynamic state simulation
  useEffect(() => {
    const timer = setInterval(() => {
      // Fluctuate threat blocks
      setThreatCount(prev => prev + (Math.random() > 0.6 ? 1 : 0));
      // Fluctuate tokens
      setActiveTokens(prev => Math.max(10, prev + (Math.random() > 0.5 ? 1 : -1)));
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  const refreshTelemetry = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 800);
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-12">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        
        {/* SOC Title Banner */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/30 text-xs font-mono text-red-400">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse inline-block"></span>
              SEC-OPS LIVE TELEMETRY STREAM
            </div>
            <h1 className="font-display font-extrabold text-4xl text-white tracking-tight mt-1.5">
              Security Operations Center
            </h1>
            <p className="text-slate-400 text-sm">
              Real-time cryptographic verification, cognitive agent traffic interception, and deception statistics.
            </p>
          </div>

          <button 
            onClick={refreshTelemetry}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-white/10 hover:border-cyan-400 text-xs font-mono text-slate-300 hover:text-white transition cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 text-cyan-400 ${loading ? "animate-spin" : ""}`} />
            <span>{loading ? "SYNCING TELEMETRY..." : "FORCE REFRESH"}</span>
          </button>
        </div>

        {/* SOC Overview Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
          
          {/* Card 1 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-red-500/20 shadow-lg relative overflow-hidden">
            <div className="absolute top-2 right-2 text-red-500/40"><ShieldAlert className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-red-400 uppercase tracking-wider">Threats Blocked</p>
            <p className="text-2xl font-display font-bold text-white mt-1">{threatCount.toLocaleString()}</p>
            <p className="text-[9px] text-slate-400 mt-2">○ 100% agent isolation</p>
          </div>

          {/* Card 2 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-white/5 shadow-lg relative overflow-hidden">
            <div className="absolute top-2 right-2 text-blue-500/40"><Cpu className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-blue-400 uppercase tracking-wider">Active Agents</p>
            <p className="text-2xl font-display font-bold text-white mt-1">248</p>
            <p className="text-[9px] text-slate-400 mt-2">● Enforcing zero-trust</p>
          </div>

          {/* Card 3 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-purple-500/20 shadow-lg relative overflow-hidden">
            <div className="absolute top-2 right-2 text-purple-500/40"><Key className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-purple-400 uppercase tracking-wider">Active Tokens</p>
            <p className="text-2xl font-display font-bold text-white mt-1">{activeTokens}</p>
            <p className="text-[9px] text-slate-400 mt-2">○ Rotate key: 284s</p>
          </div>

          {/* Card 4 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-white/5 shadow-lg relative overflow-hidden">
            <div className="absolute top-2 right-2 text-cyan-400/40"><Activity className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider">API Requests</p>
            <p className="text-2xl font-display font-bold text-white mt-1">14,892</p>
            <p className="text-[9px] text-slate-400 mt-2">○ Latency: &lt;2.1ms</p>
          </div>

          {/* Card 5 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-white/5 shadow-lg relative overflow-hidden">
            <div className="absolute top-2 right-2 text-green-500/40"><Database className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-green-400 uppercase tracking-wider">DB Queries</p>
            <p className="text-2xl font-display font-bold text-white mt-1">842.9K</p>
            <p className="text-[9px] text-slate-400 mt-2">○ Allowed: 98.4%</p>
          </div>

          {/* Card 6 */}
          <div className="p-5 rounded-2xl bg-cyber-card border border-cyan-400/30 shadow-lg relative overflow-hidden shadow-[0_0_15px_rgba(0,229,255,0.05)]">
            <div className="absolute top-2 right-2 text-cyan-400/60"><Heart className="w-5 h-5" /></div>
            <p className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider">Security Score</p>
            <p className="text-2xl font-display font-bold text-cyan-400 mt-1">99.8%</p>
            <p className="text-[9px] text-slate-400 mt-2">● HEALTHY STATUS</p>
          </div>

        </div>

        {/* Charts Grid - Bento-style layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Chart 1: Attack Timeline Area Chart */}
          <div className="lg:col-span-8 p-6 rounded-2xl bg-cyber-card border border-white/5 shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white flex items-center gap-2">
                <ShieldAlert className="w-4.5 h-4.5 text-red-400 animate-pulse" />
                Live Attack Interception Timeline
              </h3>
              <span className="text-[10px] font-mono text-slate-400">INTERVAL: 1 HOUR</span>
            </div>
            
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={attackTimelineData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="injGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FF4D4F" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#FF4D4F" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="exfGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#7C3AED" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="unauthGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#00E5FF" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="time" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis stroke="#64748B" style={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Area type="monotone" dataKey="Injection" stroke="#FF4D4F" fillOpacity={1} fill="url(#injGrad)" />
                  <Area type="monotone" dataKey="Exfiltration" stroke="#7C3AED" fillOpacity={1} fill="url(#exfGrad)" />
                  <Area type="monotone" dataKey="Unauth" stroke="#00E5FF" fillOpacity={1} fill="url(#unauthGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2: Blocked vs Allowed Request Status (Pie Chart) */}
          <div className="lg:col-span-4 p-6 rounded-2xl bg-cyber-card border border-white/5 shadow-lg space-y-4 flex flex-col justify-between">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white">
                Request Validation Mix
              </h3>
            </div>

            <div className="h-56 w-full relative flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={requestStatusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {requestStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                </PieChart>
              </ResponsiveContainer>
              {/* Inner percentage score label */}
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-xl font-display font-extrabold text-white">99.8%</span>
                <span className="text-[9px] text-slate-400 font-mono">SEAL RATIO</span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-1 text-center text-[10px] font-mono mt-2">
              <div className="text-green-400">
                <div className="w-2 h-2 rounded-full bg-green-500 inline-block mr-1"></div>
                Allowed (75.5%)
              </div>
              <div className="text-red-400">
                <div className="w-2 h-2 rounded-full bg-red-500 inline-block mr-1"></div>
                Blocked (14.6%)
              </div>
              <div className="text-purple-400">
                <div className="w-2 h-2 rounded-full bg-purple-500 inline-block mr-1"></div>
                Decept (9.9%)
              </div>
            </div>
          </div>

          {/* Chart 3: Threat Trend Line Chart */}
          <div className="lg:col-span-6 p-6 rounded-2xl bg-cyber-card border border-white/5 shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white">
                Threat Trend vs. Handshakes
              </h3>
              <span className="text-[10px] font-mono text-purple-400">7 DAY RECURSION</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="day" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis stroke="#64748B" style={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Line type="monotone" dataKey="Threats" stroke="#FF4D4F" strokeWidth={2} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="Tokens" stroke="#7C3AED" strokeWidth={2} />
                  <Line type="monotone" dataKey="Queries" stroke="#00E5FF" strokeWidth={1.5} strokeDasharray="3 3" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 4: Database Activity Bar Chart */}
          <div className="lg:col-span-6 p-6 rounded-2xl bg-cyber-card border border-white/5 shadow-lg space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <h3 className="font-display font-bold text-sm text-white">
                Production DB Access vs. Sandbox Deception
              </h3>
              <span className="text-[10px] font-mono text-cyan-400">REALTIME ROUTE</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={databaseActivityData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis dataKey="hour" stroke="#64748B" style={{ fontSize: 10 }} />
                  <YAxis stroke="#64748B" style={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ backgroundColor: "#0F172A", borderColor: "rgba(255,255,255,0.1)", color: "#fff" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Bar dataKey="ProdQueries" fill="#22C55E" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="SandboxQueries" fill="#7C3AED" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>

        {/* Real-time Security Incident Logs console stream */}
        <div className="p-6 rounded-2xl bg-slate-950 border border-red-500/20 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-white/10 pb-3">
            <div className="flex items-center gap-2">
              <Terminal className="w-5 h-5 text-red-400 animate-pulse" />
              <h3 className="font-display font-bold text-sm text-white">
                Live Intercepted Security Incident Logs
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-white/5 uppercase">
              Stream Node: PROXY-01
            </span>
          </div>

          <div className="space-y-3 font-mono text-xs overflow-x-auto max-h-72">
            {activeLogs.map((log) => (
              <div 
                key={log.id} 
                className={`p-3.5 rounded-lg border flex flex-col md:flex-row items-start md:items-center justify-between gap-3 ${
                  log.status === "BLOCKED" 
                    ? "bg-red-950/20 border-red-500/20 text-red-300"
                    : log.status === "REDIRECTED"
                    ? "bg-purple-950/20 border-purple-500/20 text-purple-300"
                    : "bg-slate-900/40 border-white/5 text-slate-300"
                }`}
              >
                <div className="space-y-1 text-left">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-[10px] text-slate-500">{log.timestamp}</span>
                    <span className="px-1.5 py-0.2 rounded bg-slate-950 font-bold text-[9px] border border-white/10">{log.id}</span>
                    <span className="text-[11px] text-white font-semibold">{log.agentId}</span>
                    <span className={`px-1.5 py-0.2 rounded text-[9px] font-bold ${
                      log.status === "BLOCKED" ? "bg-red-500/10 border border-red-500/30 text-red-400" :
                      log.status === "REDIRECTED" ? "bg-purple-500/10 border border-purple-500/30 text-purple-400" :
                      "bg-green-500/10 border border-green-500/30 text-green-400"
                    }`}>
                      {log.status}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1">Query: <code className="text-white bg-slate-950 px-1 py-0.5 rounded">{log.query}</code></p>
                  <p className="text-[11px] text-slate-500">{log.message}</p>
                </div>

                <div className="text-right shrink-0">
                  <span className="text-[10px] text-slate-500 block uppercase">Risk Factor</span>
                  <span className={`text-sm font-bold font-display ${
                    log.riskScore > 80 ? "text-red-400" : log.riskScore > 40 ? "text-purple-400" : "text-green-400"
                  }`}>
                    {log.riskScore}/100
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

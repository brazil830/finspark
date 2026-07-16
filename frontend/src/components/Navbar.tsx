import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Shield, Radio, Menu, X, Cpu, AlertTriangle } from "lucide-react";

export default function Navbar() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState("");
  const [alertCount, setAlertCount] = useState(1);

  // Live system time updates in UTC, fitting cybersecurity Operations center standards
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toISOString().replace("T", " ").substring(0, 19) + " UTC");
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Periodic alert count fluctuation to look alive
  useEffect(() => {
    const interval = setInterval(() => {
      setAlertCount((prev) => (Math.random() > 0.7 ? (prev === 0 ? 1 : 0) : prev));
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { name: "Home", path: "/" },
    { name: "About", path: "/about" },
    { name: "Architecture", path: "/architecture" },
    { name: "SOC Dashboard", path: "/dashboard" },
    { name: "Attack Simulator", path: "/simulation" },
    { name: "AI Assistant", path: "/assistant" },
    { name: "Token Minting", path: "/token" },
    { name: "Honey Table", path: "/honey-table" },
    { name: "Analytics", path: "/analytics" },
    { name: "Documentation", path: "/documentation" },
    { name: "Team", path: "/team" },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 glass-morphic border-b border-white/10 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo Brand */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative flex items-center justify-center w-11 h-11 rounded-lg bg-cyan-500/10 border border-cyan-400/30 group-hover:border-cyan-400 transition-all duration-300 shadow-[0_0_15px_rgba(0,229,255,0.1)] group-hover:shadow-[0_0_20px_rgba(0,229,255,0.3)]">
              <Shield className="w-6 h-6 text-cyan-400 group-hover:scale-110 transition-transform" />
              <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
              </span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-display font-bold text-lg tracking-wider text-white">RAG-Sec</span>
                <span className="px-1.5 py-0.5 rounded text-[9px] font-mono tracking-widest bg-cyan-400/15 text-cyan-400 font-semibold border border-cyan-400/20 uppercase">Standalone</span>
              </div>
              <div className="text-[10px] text-slate-400 tracking-tight font-mono">Zero-Trust Agent Proxy</div>
            </div>
          </Link>

          {/* Desktop Navigation links */}
          <div className="hidden xl:flex items-center gap-1.5">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-1.5 rounded-md text-[13px] font-medium tracking-wide transition-all duration-200 ${
                  isActive(item.path)
                    ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_10px_rgba(0,229,255,0.1)]"
                    : "text-slate-300 hover:text-white hover:bg-white/5 border border-transparent"
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Right Action Center */}
          <div className="hidden lg:flex items-center gap-4">
            {/* System Status Indicators */}
            <div className="flex flex-col items-end text-right">
              <span className="text-[10px] text-slate-400 font-mono tracking-wider">{currentTime}</span>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                <span className="text-[10px] font-mono text-green-400 tracking-wider">SYSTEM ACTIVE</span>
              </div>
            </div>

            {/* Quick threat badge */}
            <Link
              to="/dashboard"
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 transition-all text-xs font-mono"
            >
              <AlertTriangle className="w-3.5 h-3.5 animate-bounce" />
              <span>SOC MONITOR</span>
              {alertCount > 0 && (
                <span className="bg-red-500 text-white rounded-full px-1.5 py-0.2 text-[9px] font-bold animate-pulse">
                  {alertCount}
                </span>
              )}
            </Link>
          </div>

          {/* Mobile hamburger menu trigger */}
          <div className="xl:hidden flex items-center gap-3">
            {/* Real-time system status on mobile */}
            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-slate-900 border border-white/10 text-[10px] font-mono text-green-400">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
              <span>LIVE</span>
            </div>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-300 hover:text-white focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Menu Panel */}
      {mobileMenuOpen && (
        <div className="xl:hidden glass-morphic border-b border-white/10 px-4 py-4 space-y-2 max-h-[80vh] overflow-y-auto">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setMobileMenuOpen(false)}
              className={`block px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                isActive(item.path)
                  ? "bg-cyan-500/10 text-cyan-400 border-l-4 border-l-cyan-400"
                  : "text-slate-300 hover:text-white hover:bg-white/5"
              }`}
            >
              {item.name}
            </Link>
          ))}
          <div className="pt-4 border-t border-white/10 flex flex-col gap-3">
            <div className="text-xs text-slate-400 font-mono flex items-center justify-between">
              <span>SYSTEM STATE:</span>
              <span className="text-green-400 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span>
                ACTIVE
              </span>
            </div>
            <Link
              to="/dashboard"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 font-mono text-xs"
            >
              <AlertTriangle className="w-4 h-4" />
              SOC SYSTEM DISPATCH
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}

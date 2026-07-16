import React from "react";
import { Shield, HardDrive, Cpu, Lock, Terminal } from "lucide-react";

export default function Footer() {
  return (
    <footer className="relative z-10 glass-morphic border-t border-white/10 py-12 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          
          {/* Brand Info */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-cyan-400" />
              <span className="font-display font-bold text-white tracking-wider">RAG-Sec Standalone</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed max-w-sm">
              An enterprise-ready Zero-Trust Runtime Interceptor and Attestation Proxy protecting corporate data lakes from malicious AI agent subversion, schema exfiltration, and lateral prompt injections.
            </p>
            <div className="flex items-center gap-3 text-slate-500 font-mono text-[10px]">
              <span className="flex items-center gap-1"><Terminal className="w-3 h-3" /> v1.0.4</span>
              <span className="text-slate-700">|</span>
              <span className="text-green-500 flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-green-500 inline-block animate-ping"></span> SECURE STATE</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-display text-white text-xs font-semibold uppercase tracking-widest mb-4">Secured Planes</h3>
            <ul className="space-y-2.5 text-xs text-slate-400">
              <li><span className="hover:text-cyan-400 transition cursor-pointer">Cognitive Interception Plane</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">Execution Validation Plane</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">Transient Cryptographic Attestation</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">Honey Table Deception Modules</span></li>
            </ul>
          </div>

          {/* Infrastructure Specs */}
          <div>
            <h3 className="font-display text-white text-xs font-semibold uppercase tracking-widest mb-4">Architecture Compliance</h3>
            <ul className="space-y-2.5 text-xs text-slate-400">
              <li><span className="hover:text-cyan-400 transition cursor-pointer">mTLS Inter-Node Handshaking</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">AES-256 HSM Cryptography</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">SOC2 Compliance Model</span></li>
              <li><span className="hover:text-cyan-400 transition cursor-pointer">OWASP Top 10 for LLM Protected</span></li>
            </ul>
          </div>

          {/* Cyber Status Card */}
          <div className="p-4 rounded-xl bg-slate-900/50 border border-cyan-500/10 hover:border-cyan-500/25 transition duration-300">
            <h3 className="font-display text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5" /> Core Status Block
            </h3>
            <div className="space-y-1.5 text-[10px] font-mono text-slate-400">
              <div className="flex justify-between">
                <span>Proxy Handshake:</span>
                <span className="text-green-400">VERIFIED</span>
              </div>
              <div className="flex justify-between">
                <span>Crypt Key Rotate:</span>
                <span className="text-cyan-400">284s remaining</span>
              </div>
              <div className="flex justify-between">
                <span>Active Sandboxes:</span>
                <span className="text-purple-400">03 isolated</span>
              </div>
              <div className="flex justify-between">
                <span>Threat Level:</span>
                <span className="text-yellow-400 font-bold">STABLE</span>
              </div>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left">
          <p className="text-[11px] text-slate-500">
            &copy; {new Date().getFullYear()} RAG-Sec Standalone. Developed for Hackathon 2026. All Systems Encrypted.
          </p>
          <div className="flex items-center gap-6 text-[11px] text-slate-400">
            <span className="hover:text-white transition cursor-pointer">Privacy Policy</span>
            <span className="hover:text-white transition cursor-pointer">Terms of Service</span>
            <span className="hover:text-white transition cursor-pointer">System Manifest</span>
          </div>
        </div>

      </div>
    </footer>
  );
}

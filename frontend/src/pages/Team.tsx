import React from "react";
import { motion } from "motion/react";
import { 
  Github, 
  Linkedin, 
  Terminal, 
  ShieldCheck, 
  Cpu, 
  Code2,
  Users
} from "lucide-react";
import { TEAM_MEMBERS } from "../constants";
import ParticleBackground from "../components/ParticleBackground";

export default function Team() {
  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400">
            <Users className="w-3.5 h-3.5" /> SECURE DECODE TEAM
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            Meet the Core Team
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm">
            The security researchers, cryptographers, and frontend architects behind RAG-Sec Standalone.
          </p>
        </div>

        {/* Team cards list layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {TEAM_MEMBERS.map((member, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -6, borderColor: "rgba(0, 229, 255, 0.25)" }}
              transition={{ duration: 0.3 }}
              className="p-6 rounded-2xl bg-cyber-card border border-white/5 relative overflow-hidden text-center flex flex-col items-center justify-between shadow-lg"
            >
              {/* Corner decor details */}
              <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-2xl" />

              <div className="space-y-4 relative z-10 w-full flex flex-col items-center">
                
                {/* Profile Photo Avatar Frame */}
                <div className="relative w-28 h-28 rounded-full p-1 border-2 border-dashed border-cyan-400/40 hover:border-cyan-400 transition-colors duration-300">
                  <img 
                    src={member.photoUrl} 
                    alt={member.name} 
                    referrerPolicy="no-referrer"
                    className="w-full h-full rounded-full object-cover grayscale hover:grayscale-0 transition-all duration-300"
                  />
                  {/* Miniature verify icon */}
                  <span className="absolute bottom-1 right-1 bg-cyan-500 text-slate-950 p-1 rounded-full border-2 border-slate-950">
                    <ShieldCheck className="w-3.5 h-3.5" />
                  </span>
                </div>

                {/* Info Text */}
                <div className="space-y-1">
                  <h3 className="font-display font-bold text-lg text-white">{member.name}</h3>
                  <p className="text-xs font-mono text-cyan-400 font-semibold tracking-wide uppercase">
                    {member.role}
                  </p>
                </div>

                {/* Bio text block */}
                <p className="text-xs text-slate-400 leading-relaxed font-sans max-w-xs">
                  {member.bio}
                </p>

              </div>

              {/* Social Anchors */}
              <div className="flex items-center gap-4 pt-6 border-t border-white/5 w-full justify-center relative z-10 mt-6 text-slate-400">
                <a 
                  href={`https://${member.github}`}
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white hover:scale-110 transition duration-150 flex items-center gap-1.5 text-xs font-mono"
                >
                  <Github className="w-4 h-4 text-cyan-400" />
                  <span>GitHub</span>
                </a>
                <span className="text-slate-800">|</span>
                <a 
                  href={`https://${member.linkedin}`}
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-white hover:scale-110 transition duration-150 flex items-center gap-1.5 text-xs font-mono"
                >
                  <Linkedin className="w-4 h-4 text-purple-400" />
                  <span>LinkedIn</span>
                </a>
              </div>

            </motion.div>
          ))}
        </div>

        {/* Compliance Footer callout inside Team */}
        <div className="p-4 rounded-xl bg-slate-950 border border-white/5 font-mono text-[10px] text-slate-500 max-w-lg mx-auto">
          &gt; ALL PROJECT CONTRIBUTORS VERIFIED THROUGH CRYPTOGRAPHIC SECURE SHELL HANDSHAKES.
        </div>

      </div>
    </div>
  );
}

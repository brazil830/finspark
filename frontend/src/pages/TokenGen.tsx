import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  Key, 
  Cpu, 
  Fingerprint, 
  FileCode, 
  CheckCircle, 
  ShieldCheck, 
  RefreshCw, 
  Lock,
  ArrowRight
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

export default function TokenGen() {
  const [hsmSecretKey, setHsmSecretKey] = useState("K_ragsec_hsm_9a3f2b828cd...");
  const [currentTimeStamp, setCurrentTimeStamp] = useState("");
  const [isRotating, setIsRotating] = useState(false);
  const [activeStep, setActiveStep] = useState<number>(0);

  // Mock payload parameters
  const payloadData = {
    agent_id: "FinBot-Alpha",
    client_session_user: "sathish.balaji1907@gmail.com",
    user_authorized_role: "Fin_Analyst_L3",
    targeted_tables: ["ledger_balances", "accounts_receivable"],
    timestamp: "2026-07-16T13:21:42Z"
  };

  const payloadString = JSON.stringify(payloadData, null, 2);
  const calculatedHash = "d576a892f232eb9c08abcfef459cda82fb9d01248a39a82cd8b0124a9e29a3f2";
  const hmacSignature = "RAGSEC_ATTEST_v1_7b82f02cb932ae9e984fa51c89f210d32eb9c028dfa32b012d929a";

  useEffect(() => {
    setCurrentTimeStamp(new Date().toISOString());
  }, []);

  const rotateHSMKeys = () => {
    setIsRotating(true);
    setTimeout(() => {
      const randomHex = Math.random().toString(16).substring(2, 10);
      setHsmSecretKey(`K_ragsec_hsm_${randomHex}8cd...`);
      setIsRotating(false);
      // Restart step animation sequence
      setActiveStep(0);
    }, 1000);
  };

  // Automatically cycle through steps for demo purposes
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev < 4 ? prev + 1 : 0));
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400">
            <Lock className="w-3.5 h-3.5 animate-bounce" /> HSM SECURE TRANSIENT ENVELOPE
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            Cryptographic Token Minting
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm">
            RAG-Sec requires an authenticated single-use HMAC token before granting connection permissions. Watch the live payload minting pipeline.
          </p>
        </div>

        {/* Action ribbon for key rotation */}
        <div className="p-4 rounded-xl bg-slate-900 border border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded bg-purple-500/10 text-purple-400 border border-purple-500/30">
              <Key className="w-4 h-4" />
            </div>
            <div className="text-left font-mono text-xs">
              <span className="text-slate-500">HSM Secret Rotating Key:</span>
              <p className="text-white font-semibold">{hsmSecretKey}</p>
            </div>
          </div>
          
          <button 
            onClick={rotateHSMKeys}
            disabled={isRotating}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-mono text-xs cursor-pointer transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRotating ? "animate-spin" : ""}`} />
            <span>ROTATE HSM KEY</span>
          </button>
        </div>

        {/* Cryptographic Step Board layout */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 max-w-6xl mx-auto">
          
          {/* Step 1: JSON Payload */}
          <div className={`p-5 rounded-2xl bg-cyber-card border transition-all duration-300 flex flex-col justify-between h-96 ${
            activeStep === 0 ? "border-cyan-400 shadow-[0_0_20px_rgba(0,229,255,0.15)] scale-[1.02]" : "border-white/5 opacity-50"
          }`}>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                <span>01. JSON Payload</span>
                <FileCode className="w-4 h-4" />
              </div>
              <h3 className="font-display font-bold text-sm text-white text-left">Session Context</h3>
              <pre className="text-[10px] text-slate-300 font-mono bg-slate-950 p-3 rounded-lg border border-white/5 h-56 overflow-y-auto text-left whitespace-pre-wrap">
                {payloadString}
              </pre>
            </div>
            <div className="text-left text-[10px] text-slate-500 font-mono">
              ○ Binds user & agent identity
            </div>
          </div>

          {/* Step 2: SHA256 Hash Digest */}
          <div className={`p-5 rounded-2xl bg-cyber-card border transition-all duration-300 flex flex-col justify-between h-96 ${
            activeStep === 1 ? "border-cyan-400 shadow-[0_0_20px_rgba(0,229,255,0.15)] scale-[1.02]" : "border-white/5 opacity-50"
          }`}>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                <span>02. SHA-256 Digest</span>
                <Fingerprint className="w-4 h-4" />
              </div>
              <h3 className="font-display font-bold text-sm text-white text-left">Payload Hashing</h3>
              <p className="text-xs text-slate-400 text-left">The JSON payload is hashed through a cryptographic SHA-256 pipeline, forming an immutable, unique signature string representing this database transaction.</p>
              
              <div className="p-3 bg-slate-950 rounded-lg border border-white/5 font-mono text-[9px] text-yellow-300 break-all text-left">
                {calculatedHash}
              </div>
            </div>
            <div className="text-left text-[10px] text-slate-500 font-mono">
              ○ Secures payload integrity
            </div>
          </div>

          {/* Step 3: HMAC Sealed Key combining */}
          <div className={`p-5 rounded-2xl bg-cyber-card border transition-all duration-300 flex flex-col justify-between h-96 ${
            activeStep === 2 ? "border-cyan-400 shadow-[0_0_20px_rgba(0,229,255,0.15)] scale-[1.02]" : "border-white/5 opacity-50"
          }`}>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                <span>03. HMAC Signature</span>
                <Cpu className="w-4 h-4" />
              </div>
              <h3 className="font-display font-bold text-sm text-white text-left">Sealing Secret</h3>
              <p className="text-xs text-slate-400 text-left">Combines the SHA-256 digest with the active HSM hardware key to guarantee authenticity, preventing replay requests.</p>
              
              <div className="p-3 bg-slate-950 rounded-lg border border-white/5 font-mono text-[9px] text-purple-300 break-all text-left">
                HMAC_SHA256(HSM_Key, Digest)
              </div>
            </div>
            <div className="text-left text-[10px] text-slate-500 font-mono">
              ○ Rotary key signature verification
            </div>
          </div>

          {/* Step 4: Transient Attestation Token */}
          <div className={`p-5 rounded-2xl bg-cyber-card border transition-all duration-300 flex flex-col justify-between h-96 ${
            activeStep === 3 ? "border-cyan-400 shadow-[0_0_20px_rgba(0,229,255,0.15)] scale-[1.02]" : "border-white/5 opacity-50"
          }`}>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                <span>04. Transient Token</span>
                <Key className="w-4 h-4" />
              </div>
              <h3 className="font-display font-bold text-sm text-white text-left">Minted Seal</h3>
              <p className="text-xs text-slate-400 text-left">A temporary, cryptographically sealed access token is successfully minted with an embedded expiry timer of exactly 30 seconds.</p>
              
              <div className="p-3 bg-slate-950 rounded-lg border border-purple-500/30 font-mono text-[9px] text-cyan-300 break-all text-left shadow-[0_0_10px_rgba(0,229,255,0.1)]">
                {hmacSignature}
              </div>
            </div>
            <div className="text-left text-[10px] text-slate-500 font-mono">
              ○ Ephemeral, valid for 30 seconds
            </div>
          </div>

          {/* Step 5: Verification Handshake */}
          <div className={`p-5 rounded-2xl bg-cyber-card border transition-all duration-300 flex flex-col justify-between h-96 ${
            activeStep === 4 ? "border-cyan-400 shadow-[0_0_20px_rgba(0,229,255,0.15)] scale-[1.02]" : "border-white/5 opacity-50"
          }`}>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                <span>05. Verification</span>
                <ShieldCheck className="w-4 h-4" />
              </div>
              <h3 className="font-display font-bold text-sm text-white text-left">DB Handshake</h3>
              <p className="text-xs text-slate-400 text-left">The database connection pool parses the transient token, decrypts the session context variables, confirms authorization parameters, and executes the SQL query.</p>
              
              <div className="flex items-center gap-2 p-3 bg-slate-950 rounded-lg border border-green-500/30 text-green-400 font-mono text-[10px] text-left">
                <CheckCircle className="w-4.5 h-4.5 shrink-0" />
                <span>HANDSHAKE VERIFIED. ACCESS GRANTED.</span>
              </div>
            </div>
            <div className="text-left text-[10px] text-slate-500 font-mono">
              ○ Direct database pool validation
            </div>
          </div>

        </div>

        {/* Hashing flow diagram connecting arrows for visual high fidelity */}
        <div className="hidden md:flex justify-around max-w-4xl mx-auto py-4 text-slate-500 font-mono text-xs">
          <span>Payload Extract</span>
          <ArrowRight className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span>Digest Compute</span>
          <ArrowRight className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span>HMAC Sign</span>
          <ArrowRight className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span>Sealed Token</span>
          <ArrowRight className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span>DB Connect</span>
        </div>

      </div>
    </div>
  );
}

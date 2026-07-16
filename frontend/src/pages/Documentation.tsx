import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { 
  BookOpen, 
  Search, 
  Code2, 
  Database, 
  Terminal, 
  Cpu, 
  Lock, 
  ChevronDown, 
  ChevronUp, 
  Layers,
  Sparkles
} from "lucide-react";
import ParticleBackground from "../components/ParticleBackground";

interface DocTopic {
  id: string;
  category: "Overview" | "Technical" | "Implementation";
  title: string;
  summary: string;
  content: string;
  codeSnippet?: string;
  endpoints?: Array<{ method: string; path: string; desc: string }>;
}

export default function Documentation() {
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedTopic, setExpandedTopic] = useState<string | null>("executive-summary");

  const docTopics: DocTopic[] = [
    {
      id: "executive-summary",
      category: "Overview",
      title: "Executive Summary",
      summary: "Understand the core threat model of LLM-to-Database tool calling.",
      content: "RAG-Sec Standalone is a next-generation security gateway for AI Agent tool execution. Traditional enterprise networks grant AI clusters permanent connection secrets. When an LLM executes database queries via tool call triggers, malicious prompts can bypass outer web application firewalls entirely. RAG-Sec introduces an in-memory runtime interception proxy. By decoupling AI reasoning (Cognitive Plane) from transactional database queries (Execution Plane), RAG-Sec enforces strict JSON parameter schemas, mints transient attestation tokens, and isolates database connections, achieving 100% defense against autonomous agent exploitation."
    },
    {
      id: "architecture",
      category: "Overview",
      title: "Architecture Model",
      summary: "Explore the mTLS Zero-Trust decoupled plane architecture.",
      content: "The system is structured across three primary layers:\n1. The Cognitive Plane: The external or internal AI LLM agent (e.g. GPT-4, Claude).\n2. The Interceptor Proxy: A containerized gateway managing session parameters, cryptography keys, and deception routers.\n3. The Execution Plane: Secure database resources (Cloud SQL, Spanner, BigQuery) locked behind credential signature pools.\nCommunication is secured using mutual TLS (mTLS), ensuring zero persistent database connection keys ever leak to cognitive client clusters."
    },
    {
      id: "workflow",
      category: "Overview",
      title: "Secure Verification Workflow",
      summary: "Step-by-step description of the 7-stage validation pipeline.",
      content: "Every query transaction progresses sequentially through 7 validation states:\n1. AI Initiator Formulate: AI agent outputs structured tool-calling JSON.\n2. Structural Schema Check: Proxy compares parameters against precise JSON Schema guidelines to prevent nested query statements.\n3. Session Attestation extract: Binds original client session context (User, Role).\n4. Token Generation: Mints single-use HMAC-SHA256 tokens.\n5. Context Check: Analyzes semantic compliance of database request with active task goal.\n6. Honey Table Check: Examines target metadata for honeypot decoys.\n7. Destination Router: Directs queries to Production DB or Deception Sandbox Database.",
      codeSnippet: `// Standard 7-stage gate sequence
const validatePipeline = async (request) => {
  const isSchemaValid = await checkSchema(request.toolCall);
  if (!isSchemaValid) return REJECT_MALFORMED;
  
  const token = await mintAttestationToken(request.userSession);
  const isContextValid = await checkSemanticContext(request, token);
  if (!isContextValid) return REJECT_UNAUTHORIZED;
  
  const isHoney = await checkHoneyTable(request.query);
  if (isHoney) return REDIRECT_DECEPTION_SANDBOX;
  
  return ALLOW_PRODUCTION_DB;
};`
    },
    {
      id: "modules",
      category: "Technical",
      title: "System Modules",
      summary: "Breakdown of the containerized secure microservices.",
      content: "• Schema Interceptor Module: High-performance Rust-based structural parser. Runs schema checks in <2ms.\n• Attestation Engine: Integrates with hardware security modules (HSM) for ephemeral key generation and validation.\n• Honey Table Deception Module: Deploys virtual bait schemas that intercept scraper exploration requests.\n• Database Connection Pool: A locked proxy pool that drops database sockets if transient HMAC keys are omitted."
    },
    {
      id: "api",
      category: "Technical",
      title: "Proxy API Reference",
      summary: "API endpoints provided by the RAG-Sec Standalone gateway.",
      content: "All AI tool calls must be proxies through these endpoints. The proxy parses the natural text, executes verification, and triggers DB connections safely.",
      endpoints: [
        { method: "POST", path: "/api/v1/intercept", desc: "Intercepts raw LLM tool calls. Validates schema structures and context." },
        { method: "POST", path: "/api/v1/token/validate", desc: "Validates incoming transient attestation token against current rotatory keys." },
        { method: "GET", path: "/api/v1/deception/telemetry", desc: "Retrieves logs of intercepted honey-table exfiltration attempts." }
      ]
    },
    {
      id: "database",
      category: "Technical",
      title: "Database Protection Schema",
      summary: "Row-level policies and isolation parameters.",
      content: "RAG-Sec enforces strict database abstraction. Direct access to relational tables is denied. Database tables are segmented into: \n• Monitored tables (Regular production tables checked for semantic column access).\n• Honey Tables (Bait tables, e.g. company_client_global_dump_2026, hr_payroll_confidential, completely isolated from real production records). Accessing honey tables reroutes queries instantly to Sandbox databases."
    },
    {
      id: "algorithms",
      category: "Implementation",
      title: "Deception & Key Algorithms",
      summary: "Review key algorithms for token cryptography and routing.",
      content: "The HMAC attestation is calculated dynamically using SHA-256 bound to a secret rotation key, rotated every 5 minutes. The Honey-Table detection parses SQL structures using a regex parser to identify decoy table sequences on targeted SELECT scripts.",
      codeSnippet: `// Transient HMAC Verification Formula
HMAC_Attestation = HMAC_SHA256(
  Secret_HSM_Key,
  Agent_ID + User_Role + Target_Tables + Timestamp
)`
    },
    {
      id: "security",
      category: "Implementation",
      title: "Security & HSM Key Rotation",
      summary: "Hardware-security key standards and compliance details.",
      content: "Secret attestation keys are stored strictly in secure HSM (FIPS 140-2 Level 3 compliant) structures. Key material is stored only in ephemeral memory with automated 5-minute rotation cycles. Replay attacks are stopped as token timestamps must match database receipt timestamps within a 30-second window."
    },
    {
      id: "future-scope",
      category: "Implementation",
      title: "Future Scope & AI Extensions",
      summary: "Planned integrations for Spanner, OAuth, and reinforcement loops.",
      content: "Future versions of RAG-Sec Standalone will support:\n1. Multi-Agent session authorization profiles via OAuth2.\n2. Live Vector database retrieval augmentation guardrails (semantic embeddings distance checking to prevent indirect injections).\n3. Hardware-accelerated SGX Enclave decryption pools for high-throughput relational analytics."
    }
  ];

  const filteredTopics = docTopics.filter(topic => 
    topic.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
    topic.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleTopic = (id: string) => {
    setExpandedTopic(expandedTopic === id ? null : id);
  };

  return (
    <div className="relative min-h-screen bg-cyber-bg overflow-hidden flex flex-col py-16">
      <ParticleBackground />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        
        {/* Page Header */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-400/10 border border-cyan-400/30 text-xs font-mono text-cyan-400 animate-pulse">
            <BookOpen className="w-3.5 h-3.5" /> DEVELOPER MANUAL
          </div>
          <h1 className="font-display font-extrabold text-4xl sm:text-5xl text-white tracking-tight">
            System Documentation
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-sm leading-relaxed">
            Developer guidelines, system architecture details, algorithms, database schematics, and API definitions for the RAG-Sec Standalone framework.
          </p>
        </div>

        {/* Search & Layout grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Sidebar categories / Search */}
          <div className="lg:col-span-4 space-y-4 text-left">
            
            {/* Search Input bar */}
            <div className="p-4 rounded-xl bg-cyber-card border border-white/5 flex items-center gap-2">
              <Search className="w-4 h-4 text-slate-500" />
              <input 
                type="text"
                placeholder="Search doc articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-transparent border-none outline-none text-xs text-white placeholder-slate-500 w-full font-sans"
              />
            </div>

            {/* Topic Quick Navigation categories */}
            <div className="p-5 rounded-2xl bg-cyber-card border border-white/5 space-y-4">
              <h3 className="font-display font-bold text-xs text-slate-400 uppercase tracking-wider">
                Doc Sections
              </h3>

              <div className="space-y-1.5 font-sans">
                {filteredTopics.map((topic) => (
                  <button
                    key={topic.id}
                    onClick={() => toggleTopic(topic.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition duration-150 flex items-center justify-between ${
                      expandedTopic === topic.id
                        ? "bg-cyan-500/10 text-cyan-400 font-semibold"
                        : "text-slate-400 hover:text-white hover:bg-white/5"
                    }`}
                  >
                    <span>{topic.title}</span>
                    <span className="text-[10px] font-mono text-slate-600 uppercase">{topic.category}</span>
                  </button>
                ))}
              </div>
            </div>

          </div>

          {/* Accordion List Column */}
          <div className="lg:col-span-8 space-y-4 text-left">
            
            {filteredTopics.length === 0 ? (
              <div className="p-12 rounded-2xl bg-cyber-card border border-white/5 text-center text-slate-500 text-sm">
                No documentation topics matches your query. Try searching for 'token', 'honey', or 'mTLS'.
              </div>
            ) : (
              filteredTopics.map((topic) => {
                const isOpen = expandedTopic === topic.id;
                return (
                  <div 
                    key={topic.id}
                    className="rounded-2xl bg-cyber-card border border-white/5 overflow-hidden transition-all duration-300"
                  >
                    {/* Header trigger button */}
                    <button
                      onClick={() => toggleTopic(topic.id)}
                      className="w-full p-5 flex items-center justify-between hover:bg-white/5 transition duration-200"
                    >
                      <div className="space-y-1 text-left">
                        <div className="flex items-center gap-2">
                          <span className="px-2 py-0.5 rounded bg-slate-900 text-[10px] font-mono text-cyan-400 uppercase border border-cyan-400/20">
                            {topic.category}
                          </span>
                          <h3 className="font-display font-bold text-base text-white">{topic.title}</h3>
                        </div>
                        <p className="text-xs text-slate-400 leading-normal">{topic.summary}</p>
                      </div>
                      
                      {isOpen ? (
                        <ChevronUp className="w-5 h-5 text-cyan-400" />
                      ) : (
                        <ChevronDown className="w-5 h-5 text-slate-500" />
                      )}
                    </button>

                    {/* Open Content drawer */}
                    <AnimatePresence>
                      {isOpen && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.25 }}
                          className="border-t border-white/5 bg-slate-950/40"
                        >
                          <div className="p-6 space-y-6 text-sm text-slate-300 leading-relaxed whitespace-pre-line font-sans">
                            <p>{topic.content}</p>

                            {/* Endpoints display widget */}
                            {topic.endpoints && (
                              <div className="space-y-3 pt-2">
                                <h4 className="font-display font-bold text-xs text-white uppercase tracking-wider flex items-center gap-1.5">
                                  <Terminal className="w-4 h-4 text-cyan-400" /> Endpoints Specification
                                </h4>
                                <div className="space-y-2 font-mono text-xs">
                                  {topic.endpoints.map((ep, i) => (
                                    <div key={i} className="p-3 bg-slate-950 rounded-lg border border-white/5 flex flex-col sm:flex-row items-start sm:items-center gap-3">
                                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                        ep.method === "POST" ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20" : "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                                      }`}>
                                        {ep.method}
                                      </span>
                                      <span className="text-white font-semibold">{ep.path}</span>
                                      <span className="text-slate-500 text-[11px] sm:ml-auto">{ep.desc}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {/* Code Snippet widget */}
                            {topic.codeSnippet && (
                              <div className="space-y-2 pt-2">
                                <h4 className="font-display font-bold text-xs text-white uppercase tracking-wider flex items-center gap-1.5">
                                  <Code2 className="w-4 h-4 text-purple-400" /> Implementation Blueprint
                                </h4>
                                <pre className="p-4 rounded-xl bg-slate-950 border border-white/5 font-mono text-xs text-purple-300 overflow-x-auto text-left whitespace-pre">
                                  {topic.codeSnippet}
                                </pre>
                              </div>
                            )}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>

                  </div>
                );
              })
            )}

          </div>

        </div>

      </div>
    </div>
  );
}

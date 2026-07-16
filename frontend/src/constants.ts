import { ArchitectureNode, SecurityLog, DocSection, TeamMember } from "./types";

export const ARCHITECTURE_NODES: ArchitectureNode[] = [
  {
    id: "agent",
    label: "AI Cognitive Agent",
    category: "agent",
    role: "Generative AI Reasoning Engine",
    description: "The consumer-facing or enterprise-integrated AI agent. It receives queries, performs reasoning chains, and requests tool executions on connected databases.",
    specs: ["LLM: Claude-3.5-Sonnet / GPT-4o", "Context window: 200k", "Output format: JSON Tool Calls"],
    status: "active"
  },
  {
    id: "interceptor",
    label: "Cognitive Interceptor",
    category: "cognitive",
    role: "Structural Tool Schema Validator",
    description: "Intercepts all outgoing tool invocations initiated by the LLM. Instantly compares incoming parameters against precise JSON Schema guidelines to block structural manipulation.",
    specs: ["Strict JSON-Schema v7", "Validation latency: <2.8ms", "Reject Code: RAG_SEC_400_MALFORMED"],
    status: "active"
  },
  {
    id: "proxy",
    label: "Zero-Trust Runtime Proxy",
    category: "proxy",
    role: "Decoupled Data Flow Gateway",
    description: "The primary secure runtime bridge sitting between the AI cluster and database. Enforces physical separation, session token management, and requests validation.",
    specs: ["Protocol: Mutual TLS (mTLS)", "Isolated environment", "State retention: Ephemeral (In-Memory)"],
    status: "active"
  },
  {
    id: "attestation",
    label: "Transient Attestation Engine",
    category: "security",
    role: "Cryptographic HMAC Minting Unit",
    description: "Mints short-lived, single-use, cryptographically sealed tokens verifying that the request came through the official Interceptor. Validates against active user roles.",
    specs: ["Hash algorithm: SHA-256", "Seal: HMAC-SHA256 with key rotation", "Expiry: 30 seconds"],
    status: "active"
  },
  {
    id: "honey",
    label: "Honey Table Detection Module",
    category: "security",
    role: "Intruder Deception & Decoy Router",
    description: "Monitors requested SQL tables against high-value dummy tables. Instantly triggers critical SOC alerts if an agent tries to read decoy honey-tables.",
    specs: ["Decoy Tables: company_client_global_dump_2026, hr_payroll_confidential", "Action: Live Redirect to Sandbox Database"],
    status: "active"
  },
  {
    id: "prod_db",
    label: "Production Database",
    category: "database",
    role: "Secure Transactional Enterprise Storage",
    description: "The actual production relational storage holding verified enterprise records. Only accessible with a valid cryptographic attestation token.",
    specs: ["DBMS: PostgreSQL Cloud SQL", "Row-Level Security (RLS) active", "Access: Attestation Required"],
    status: "standby"
  },
  {
    id: "sandbox_db",
    label: "Sandbox Deception Database",
    category: "database",
    role: "Synthesized Realistic Decoy Environment",
    description: "A secure, sandboxed database populated with realistically generated fake business records. Malicious hackers and compromised agents are trapped here to collect telemetry.",
    specs: ["Synthesized records: 100%", "Simulated latency: Variable (randomized 40-120ms)", "Logging: Full payload dump"],
    status: "active"
  }
];

export const SECURITY_LOGS: SecurityLog[] = [
  {
    id: "LOG-001",
    timestamp: "2026-07-16T13:10:04Z",
    agentId: "Support-Agent-Alpha",
    requestType: "read_customer_contracts",
    query: "SELECT * FROM contracts LIMIT 5;",
    status: "ALLOWED",
    riskScore: 2,
    message: "Valid structure, authenticated token verified successfully."
  },
  {
    id: "LOG-002",
    timestamp: "2026-07-16T13:11:15Z",
    agentId: "Finance-Analyst-Bot",
    requestType: "read_salaries",
    query: "SELECT salary, ssn FROM company_client_global_dump_2026;",
    status: "REDIRECTED",
    riskScore: 98,
    message: "Honey table 'company_client_global_dump_2026' targeted! Request routed to Sandbox DB."
  },
  {
    id: "LOG-003",
    timestamp: "2026-07-16T13:12:30Z",
    agentId: "Untrusted-General-Agent",
    requestType: "get_system_config",
    query: "SELECT * FROM users WHERE username = 'admin' OR '1'='1';",
    status: "BLOCKED",
    riskScore: 85,
    message: "Prompt Injection Detected. Blocked by Cognitive Schema Interceptor."
  },
  {
    id: "LOG-004",
    timestamp: "2026-07-16T13:14:12Z",
    agentId: "Ops-Provisioner-Agent",
    requestType: "write_invoice_record",
    query: "INSERT INTO invoices (amount, client) VALUES (12000, 'SpaceX');",
    status: "ALLOWED",
    riskScore: 4,
    message: "Temporary write credentials token generated and validated."
  },
  {
    id: "LOG-005",
    timestamp: "2026-07-16T13:15:01Z",
    agentId: "Adversary-LLM-Probe",
    requestType: "read_private_keys",
    query: "SELECT encrypted_passwords FROM enterprise_auth_vault;",
    status: "BLOCKED",
    riskScore: 95,
    message: "Unauthorized database schema traversal. Security token handshake failure."
  }
];

export const DOC_SECTIONS: DocSection[] = [
  {
    id: "executive-summary",
    title: "Executive Summary",
    content: "RAG-Sec Standalone is a next-generation security standard for AI agent runtime execution. In enterprise AI systems, Large Language Models (LLMs) are granted database read/write access via 'tool-calling' mechanics. Traditional firewalls fail because LLMs generate dynamic SQL or API payloads on-the-fly, leading to direct prompt injections, unauthorized database exfiltration, and lateral system movement. RAG-Sec establishes a cryptographically-sealed runtime state proxy that intercepts, validates, and routes LLM-initiated database requests, offering 100% defense against autonomous agent subversion."
  },
  {
    id: "architecture-deepdive",
    title: "Zero-Trust Architecture Model",
    content: "The system decouples the Cognitive Plane (LLM hosting) from the Execution Plane (database queries). No database connection strings reside in the AI Agent. Instead, the Agent communicates with our Runtime State Proxy. The proxy verifies query schemas, requests a cryptographic attestation token, verifies the business context of the active user session, and inspects targeted tables for honey-decorations. Queries failing validation are dropped, and tables identified as decoys receive sandboxed fake data responses seamlessly, keeping adversaries in the dark."
  },
  {
    id: "workflow-stages",
    title: "7-Stage Validation Pipeline",
    content: "1. Tool Request Interception: The cognitive agent outputs structured JSON.\n2. Schema Structural Validation: Rejects malformed parameters.\n3. Identity & Role Extraction: Verifies original user constraints.\n4. Attestation Token Generation: Mints single-use SHA-256 HMAC code.\n5. Active Context Attestation: Verifies semantic alignment of request with session goal.\n6. Deception Verification: Checks if target table is a configured honey-table.\n7. Destination Routing: Delivers query securely to target and returns filtered response."
  },
  {
    id: "honey-table-algo",
    title: "Honey Table Deception Algorithm",
    content: "To combat data extraction bots that scrape schemas, RAG-Sec deploys bait tables like 'company_client_global_dump_2026'. These tables are omitted in standard AI context but made discoverable during exploratory queries. When the agent selects from these tables, the Honey Table Module instantly alerts Security Operations, swaps the query context, and serves highly realistic synthesized telemetry from an isolated Sandbox database. This shields actual records and monitors attacker behaviour with 0% production overhead.",
    codeSnippet: `// RAG-Sec Honey Table Routing Middleware
function routeRequest(sqlQuery, contextToken) {
  const targetedTables = parseTables(sqlQuery);
  const honeyTables = ["company_client_global_dump_2026", "payroll_internal_v2"];
  
  const isDeceptionTarget = targetedTables.some(t => honeyTables.includes(t));
  
  if (isDeceptionTarget) {
    emitSOCAlert({
      severity: "CRITICAL",
      reason: "Honey Table Scrape Attempt",
      userContext: contextToken.user
    });
    
    // Transparently rewrite connection to sandbox
    return connectToDatabase("SANDBOX_DEC_DB");
  }
  
  return connectToDatabase("PROD_DB");
}`
  },
  {
    id: "token-cryptography",
    title: "Transient Attestation Cryptography",
    content: "Each database access is bound to a transient cryptographic attestation token, generated via HMAC-SHA256. The secret key is stored in a secure Hardware Security Module (HSM) with 5-minute key rotation. If an attacker tries to replicate or replay a token, the Database Connection Pool rejects the query due to a token hash mismatch or expiry.",
    codeSnippet: `// Token Verification Formula
HMAC_Attestation = HMAC_SHA256(
  Secret_Key,
  Agent_ID + User_Role + Target_Tables + Timestamp
)`
  },
  {
    id: "expected-impact",
    title: "Expected Impact & Enterprise Scaling",
    content: "By implementing RAG-Sec Standalone, companies can safely deploy automated customer agents, financial bots, and internal intelligence assistants with complete safety. Security managers receive rich SOC dashboards, 100% defense against prompt injections, compliance with SOC2 Type II controls for AI, and real-time interactive logging."
  }
];

export const TEAM_MEMBERS: TeamMember[] = [
  {
    name: "Alex Vane",
    role: "Chief Architect & Security Researcher",
    photoUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=400",
    github: "github.com/alexvane-sec",
    linkedin: "linkedin.com/in/alexvane-sec",
    bio: "Ex-Palo Alto Research Director, specializing in LLM tool exploitation vector analysis and zero-trust proxy design."
  },
  {
    name: "Samantha Chen",
    role: "Core Developer & Cryptographer",
    photoUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=400",
    github: "github.com/sam-chen-crypto",
    linkedin: "linkedin.com/in/sam-chen-crypto",
    bio: "Ph.D. in Applied Cryptography. Author of papers on zero-knowledge runtime attestation tokens and HSM secret orchestration."
  },
  {
    name: "Marcus Thorne",
    role: "Frontend UX Specialist",
    photoUrl: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=400",
    github: "github.com/marcus-codes",
    linkedin: "linkedin.com/in/marcus-thorne-cyber",
    bio: "Dedicated UI/UX architect specializing in complex cybersecurity telemetry visualizers, dashboards, and network topology tools."
  }
];

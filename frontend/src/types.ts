export interface AttackScenario {
  id: string;
  name: string;
  description: string;
  query: string;
  steps: SimulationStep[];
  status: "safe" | "blocked" | "redirected";
  logs: string[];
}

export interface SimulationStep {
  id: string;
  label: string;
  status: "pending" | "success" | "failed" | "warning";
  details: string;
}

export interface ArchitectureNode {
  id: string;
  label: string;
  category: "cognitive" | "proxy" | "security" | "database" | "agent";
  description: string;
  role: string;
  specs: string[];
  status: "active" | "standby" | "alerting";
}

export interface SecurityLog {
  id: string;
  timestamp: string;
  agentId: string;
  requestType: string;
  query: string;
  status: "ALLOWED" | "BLOCKED" | "REDIRECTED";
  riskScore: number;
  message: string;
}

export interface DocSection {
  id: string;
  title: string;
  content: string;
  codeSnippet?: string;
}

export interface TeamMember {
  name: string;
  role: string;
  photoUrl: string;
  github: string;
  linkedin: string;
  bio: string;
}

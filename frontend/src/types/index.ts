export interface Role {
  id: string
  name: string
  description: string | null
  permissions: string[]
}

export interface User {
  id: string
  email: string
  full_name: string
  department: string | null
  is_active: boolean
  is_superuser: boolean
  auth_provider: string
  roles: Role[]
  created_at: string
  updated_at: string
}

export interface Control {
  id: string
  clause: string
  title: string
  description: string
  theme: string
  implementation_guidance: string | null
  status: string
  owner_id: string | null
  owner: User | null
  review_date: string | null
  created_at: string
  updated_at: string
}

export interface ClauseRequirement {
  id: string
  clause: string
  title: string
  section: string
  clause_number: number
  requirement: string
  documented_info: string | null
  conformity_status: string
  implementation_notes: string | null
  owner_id: string | null
  owner: User | null
  review_date: string | null
  created_at: string
  updated_at: string
}

export interface Risk {
  id: string
  ref_id: string
  title: string
  description: string
  category: string
  likelihood: number
  impact: number
  inherent_risk_level: string
  treatment: string
  treatment_plan: string | null
  residual_likelihood: number | null
  residual_impact: number | null
  residual_risk_level: string | null
  owner_id: string | null
  owner: User | null
  status: string
  review_date: string | null
  created_at: string
  updated_at: string
}

export interface SoAEntry {
  id: string
  control_id: string
  applicable: boolean
  justification: string | null
  implementation_status: string
  implementation_evidence: string | null
  responsible_id: string | null
  responsible: User | null
  notes: string | null
  control: Control
  created_at: string
  updated_at: string
}

export interface Evidence {
  id: string
  title: string
  description: string | null
  file_name: string
  file_path: string
  file_type: string | null
  file_size: number | null
  uploaded_by: string | null
  uploader: User | null
  control_id: string | null
  risk_id: string | null
  audit_id: string | null
  policy_id: string | null
  created_at: string
}

export interface AuditFinding {
  id: string
  ref_id: string
  audit_id: string
  control_id: string | null
  control: Control | null
  finding_type: string
  description: string
  severity: string
  corrective_action: string | null
  due_date: string | null
  status: string
  assigned_to: string | null
  assignee: User | null
  closed_at: string | null
  created_at: string
  updated_at: string
}

export interface Audit {
  id: string
  ref_id: string
  title: string
  description: string | null
  audit_type: string
  status: string
  lead_auditor_id: string | null
  lead_auditor: User | null
  start_date: string | null
  end_date: string | null
  scope: string | null
  conclusion: string | null
  findings: AuditFinding[]
  created_at: string
  updated_at: string
}

export interface PolicyAck {
  id: string
  user: User
  acknowledged_at: string
}

export interface Policy {
  id: string
  ref_id: string
  title: string
  description: string | null
  version: string
  status: string
  category: string
  owner_id: string | null
  owner: User | null
  approved_by: string | null
  approver: User | null
  approved_at: string | null
  effective_date: string | null
  review_date: string | null
  next_review_date: string | null
  content: string | null
  acknowledgments: PolicyAck[]
  created_at: string
  updated_at: string
}

export interface Asset {
  id: string
  ref_id: string
  name: string
  description: string | null
  asset_type: string
  classification: string
  owner_id: string | null
  owner: User | null
  department: string | null
  location: string | null
  status: string
  criticality: string
  created_at: string
  updated_at: string
}

export interface DocumentedInformation {
  id: string
  ref_id: string
  title: string
  description: string | null
  doc_type: string
  clause_ref: string | null
  mandatory: boolean
  version: string
  status: string
  classification: string
  location: string | null
  owner_id: string | null
  owner: User | null
  approver_id: string | null
  approver: User | null
  approved_at: string | null
  review_date: string | null
  next_review_date: string | null
  created_at: string
  updated_at: string
}

export interface InterestedParty {
  id: string
  ref_id: string
  name: string
  party_type: string
  category: string
  requirements: string | null
  addressed_in_isms: boolean
  notes: string | null
  owner_id: string | null
  owner: User | null
  created_at: string
  updated_at: string
}

export interface Metric {
  id: string
  ref_id: string
  name: string
  description: string | null
  metric_type: string
  clause_ref: string
  objective_id: string | null
  target_value: number | null
  current_value: number | null
  unit: string | null
  direction: string
  frequency: string | null
  rag: string
  owner_id: string | null
  owner: User | null
  last_measured: string | null
  created_at: string
  updated_at: string
}

export interface Objective {
  id: string
  ref_id: string
  title: string
  description: string | null
  clause_ref: string
  measure: string | null
  target_value: string | null
  current_value: string | null
  unit: string | null
  status: string
  owner_id: string | null
  owner: User | null
  due_date: string | null
  review_date: string | null
  metrics: Metric[]
  created_at: string
  updated_at: string
}

export interface DashboardStats {
  total_controls: number
  implemented_controls: number
  total_risks: number
  open_risks: number
  critical_risks: number
  total_audits: number
  open_findings: number
  total_policies: number
  total_assets: number
  compliance_score: number
  risk_posture: Record<string, number>
  controls_by_status: Record<string, number>
  controls_by_theme: Record<string, number>
  total_clauses: number
  conformant_clauses: number
  isms_conformity_score: number
  clauses_by_status: Record<string, number>
  clauses_by_section: Record<string, number>
  total_documents: number
  mandatory_documents: number
  approved_mandatory_documents: number
  document_readiness_score: number
  documents_by_status: Record<string, number>
  total_interested_parties: number
  total_objectives: number
  achieved_objectives: number
  objectives_by_status: Record<string, number>
  total_metrics: number
  on_target_metrics: number
  metrics_by_rag: Record<string, number>
  metrics_by_type: Record<string, number>
}

export interface ActivityEntry {
  id: string
  user_id: string | null
  action: string
  resource_type: string
  resource_id: string | null
  details: Record<string, unknown> | null
  created_at: string | null
}

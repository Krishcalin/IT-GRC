import axios from 'axios'
import type { User, Control, ClauseRequirement, DocumentedInformation, InterestedParty, Objective, Metric, MetricMeasurement, Supplier, Incident, TrainingCampaign, TrainingRecord, RemindersResult, Task, RiskHeatmap, PostureSnapshot, MyWork, Risk, SoAEntry, Evidence, Audit, AuditFinding, Policy, Asset, DashboardStats, ActivityEntry } from '../types'

const api = axios.create({ baseURL: '/api/v1' })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      if (window.location.pathname !== '/login') window.location.href = '/login'
    }
    return Promise.reject(err)
  },
)

// Auth
export const login = (email: string, password: string) =>
  api.post<{ access_token: string }>('/auth/login', new URLSearchParams({ username: email, password }))
export const getMe = () => api.get<User>('/auth/me')
export const getUsers = () => api.get<User[]>('/auth/users')

// Tasks & Workflow
export const getTasks = (params?: Record<string, string>) => api.get<Task[]>('/tasks', { params })
export const getTask = (id: string) => api.get<Task>(`/tasks/${id}`)
export const createTask = (data: Record<string, unknown>) => api.post<Task>('/tasks', data)
export const updateTask = (id: string, data: Partial<Task>) => api.put<Task>(`/tasks/${id}`, data)
export const decideTask = (id: string, data: { decision: string; decision_comment?: string }) => api.post<Task>(`/tasks/${id}/decision`, data)
export const deleteTask = (id: string) => api.delete(`/tasks/${id}`)

// Controls
export const getControls = (params?: Record<string, string>) => api.get<Control[]>('/controls', { params })
export const getControl = (id: string) => api.get<Control>(`/controls/${id}`)
export const updateControl = (id: string, data: Partial<Control>) => api.put<Control>(`/controls/${id}`, data)

// ISMS Clauses (4–10)
export const getClauses = (params?: Record<string, string>) => api.get<ClauseRequirement[]>('/clauses', { params })
export const getClause = (id: string) => api.get<ClauseRequirement>(`/clauses/${id}`)
export const updateClause = (id: string, data: Partial<ClauseRequirement>) => api.put<ClauseRequirement>(`/clauses/${id}`, data)

// Documented Information (Clause 7.5)
export const getDocuments = (params?: Record<string, string>) => api.get<DocumentedInformation[]>('/documents', { params })
export const getDocument = (id: string) => api.get<DocumentedInformation>(`/documents/${id}`)
export const createDocument = (data: Record<string, unknown>) => api.post<DocumentedInformation>('/documents', data)
export const updateDocument = (id: string, data: Partial<DocumentedInformation>) => api.put<DocumentedInformation>(`/documents/${id}`, data)
export const deleteDocument = (id: string) => api.delete(`/documents/${id}`)

// Interested Parties (Clause 4.2)
export const getInterestedParties = (params?: Record<string, string>) => api.get<InterestedParty[]>('/interested-parties', { params })
export const createInterestedParty = (data: Record<string, unknown>) => api.post<InterestedParty>('/interested-parties', data)
export const updateInterestedParty = (id: string, data: Partial<InterestedParty>) => api.put<InterestedParty>(`/interested-parties/${id}`, data)
export const deleteInterestedParty = (id: string) => api.delete(`/interested-parties/${id}`)

// IS Objectives (Clause 6.2)
export const getObjectives = (params?: Record<string, string>) => api.get<Objective[]>('/objectives', { params })
export const getObjective = (id: string) => api.get<Objective>(`/objectives/${id}`)
export const createObjective = (data: Record<string, unknown>) => api.post<Objective>('/objectives', data)
export const updateObjective = (id: string, data: Partial<Objective>) => api.put<Objective>(`/objectives/${id}`, data)
export const deleteObjective = (id: string) => api.delete(`/objectives/${id}`)

// Metrics — KPI/KRI/KCI (Clause 9.1)
export const getMetrics = (params?: Record<string, string>) => api.get<Metric[]>('/metrics', { params })
export const getMetric = (id: string) => api.get<Metric>(`/metrics/${id}`)
export const createMetric = (data: Record<string, unknown>) => api.post<Metric>('/metrics', data)
export const updateMetric = (id: string, data: Record<string, unknown>) => api.put<Metric>(`/metrics/${id}`, data)
export const deleteMetric = (id: string) => api.delete(`/metrics/${id}`)
export const getMetricHistory = (id: string) => api.get<MetricMeasurement[]>(`/metrics/${id}/history`)
export const addMeasurement = (id: string, data: { value: number; note?: string; captured_at?: string }) => api.post<MetricMeasurement>(`/metrics/${id}/measurements`, data)

// Analytics
export const getRiskHeatmap = (basis = 'inherent') => api.get<RiskHeatmap>('/analytics/risk-heatmap', { params: { basis } })
export const getPostureTrend = (days = 180) => api.get<PostureSnapshot[]>('/analytics/posture-trend', { params: { days } })
export const captureSnapshot = () => api.post<PostureSnapshot>('/analytics/snapshot')
export const getMyWork = () => api.get<MyWork>('/analytics/my-work')

// Suppliers / third parties (Clauses 5.19–5.23)
export const getSuppliers = (params?: Record<string, string>) => api.get<Supplier[]>('/suppliers', { params })
export const getSupplier = (id: string) => api.get<Supplier>(`/suppliers/${id}`)
export const createSupplier = (data: Record<string, unknown>) => api.post<Supplier>('/suppliers', data)
export const updateSupplier = (id: string, data: Partial<Supplier>) => api.put<Supplier>(`/suppliers/${id}`, data)
export const deleteSupplier = (id: string) => api.delete(`/suppliers/${id}`)

// Incidents (Clauses 5.24–5.28)
export const getIncidents = (params?: Record<string, string>) => api.get<Incident[]>('/incidents', { params })
export const getIncident = (id: string) => api.get<Incident>(`/incidents/${id}`)
export const createIncident = (data: Record<string, unknown>) => api.post<Incident>('/incidents', data)
export const updateIncident = (id: string, data: Partial<Incident>) => api.put<Incident>(`/incidents/${id}`, data)
export const deleteIncident = (id: string) => api.delete(`/incidents/${id}`)

// Awareness & Training (Clauses 7.2/7.3)
export const getCampaigns = (params?: Record<string, string>) => api.get<TrainingCampaign[]>('/training', { params })
export const getCampaign = (id: string) => api.get<TrainingCampaign>(`/training/${id}`)
export const createCampaign = (data: Record<string, unknown>) => api.post<TrainingCampaign>('/training', data)
export const updateCampaign = (id: string, data: Partial<TrainingCampaign>) => api.put<TrainingCampaign>(`/training/${id}`, data)
export const deleteCampaign = (id: string) => api.delete(`/training/${id}`)
export const addTrainingRecord = (campaignId: string, data: Record<string, unknown>) => api.post<TrainingRecord>(`/training/${campaignId}/records`, data)
export const updateTrainingRecord = (recordId: string, data: Record<string, unknown>) => api.put<TrainingRecord>(`/training/records/${recordId}`, data)
export const deleteTrainingRecord = (recordId: string) => api.delete(`/training/records/${recordId}`)

// Reports & export
export const downloadReport = (path: string) => api.get(`/reports/${path}`, { responseType: 'blob' })

// Reminders / notifications
export const getReminders = (params?: Record<string, string>) => api.get<RemindersResult>('/reminders', { params })

// Risks
export const getRisks = (params?: Record<string, string>) => api.get<Risk[]>('/risks', { params })
export const createRisk = (data: Record<string, unknown>) => api.post<Risk>('/risks', data)
export const getRisk = (id: string) => api.get<Risk>(`/risks/${id}`)
export const updateRisk = (id: string, data: Record<string, unknown>) => api.put<Risk>(`/risks/${id}`, data)
export const deleteRisk = (id: string) => api.delete(`/risks/${id}`)
export const linkRiskControl = (riskId: string, controlId: string) => api.post(`/risks/${riskId}/controls/${controlId}`)
export const unlinkRiskControl = (riskId: string, controlId: string) => api.delete(`/risks/${riskId}/controls/${controlId}`)

// SoA
export const getSoaEntries = (params?: Record<string, string>) => api.get<SoAEntry[]>('/soa', { params })
export const createSoaEntry = (data: Record<string, unknown>) => api.post<SoAEntry>('/soa', data)
export const updateSoaEntry = (id: string, data: Record<string, unknown>) => api.put<SoAEntry>(`/soa/${id}`, data)

// Evidence
export const getEvidenceList = (params?: Record<string, string>) => api.get<Evidence[]>('/evidence', { params })
export const uploadEvidence = (formData: FormData) => api.post<Evidence>('/evidence/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
export const downloadEvidence = (id: string) => api.get(`/evidence/${id}/download`, { responseType: 'blob' })

// Audits
export const getAudits = (params?: Record<string, string>) => api.get<Audit[]>('/audits', { params })
export const createAudit = (data: Record<string, unknown>) => api.post<Audit>('/audits', data)
export const getAudit = (id: string) => api.get<Audit>(`/audits/${id}`)
export const updateAudit = (id: string, data: Record<string, unknown>) => api.put<Audit>(`/audits/${id}`, data)
export const createFinding = (auditId: string, data: Record<string, unknown>) => api.post<AuditFinding>(`/audits/${auditId}/findings`, data)
export const updateFinding = (findingId: string, data: Record<string, unknown>) => api.put<AuditFinding>(`/audits/findings/${findingId}`, data)

// Policies
export const getPolicies = (params?: Record<string, string>) => api.get<Policy[]>('/policies', { params })
export const createPolicy = (data: Record<string, unknown>) => api.post<Policy>('/policies', data)
export const getPolicy = (id: string) => api.get<Policy>(`/policies/${id}`)
export const updatePolicy = (id: string, data: Record<string, unknown>) => api.put<Policy>(`/policies/${id}`, data)
export const acknowledgePolicy = (id: string) => api.post(`/policies/${id}/acknowledge`)

// Assets
export const getAssets = (params?: Record<string, string>) => api.get<Asset[]>('/assets', { params })
export const createAsset = (data: Record<string, unknown>) => api.post<Asset>('/assets', data)
export const getAsset = (id: string) => api.get<Asset>(`/assets/${id}`)
export const updateAsset = (id: string, data: Record<string, unknown>) => api.put<Asset>(`/assets/${id}`, data)
export const deleteAsset = (id: string) => api.delete(`/assets/${id}`)

// Dashboard
export const getDashboardStats = () => api.get<DashboardStats>('/dashboard/stats')
export const getActivityLog = () => api.get<ActivityEntry[]>('/dashboard/activity')

export default api

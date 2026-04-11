import axios from 'axios'
import type { User, Control, Risk, SoAEntry, Evidence, Audit, AuditFinding, Policy, Asset, DashboardStats, ActivityEntry } from '../types'

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

// Controls
export const getControls = (params?: Record<string, string>) => api.get<Control[]>('/controls', { params })
export const getControl = (id: string) => api.get<Control>(`/controls/${id}`)
export const updateControl = (id: string, data: Partial<Control>) => api.put<Control>(`/controls/${id}`, data)

// Risks
export const getRisks = (params?: Record<string, string>) => api.get<Risk[]>('/risks', { params })
export const createRisk = (data: Record<string, unknown>) => api.post<Risk>('/risks', data)
export const getRisk = (id: string) => api.get<Risk>(`/risks/${id}`)
export const updateRisk = (id: string, data: Record<string, unknown>) => api.put<Risk>(`/risks/${id}`, data)
export const deleteRisk = (id: string) => api.delete(`/risks/${id}`)

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

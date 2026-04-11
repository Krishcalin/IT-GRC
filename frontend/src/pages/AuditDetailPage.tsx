import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getAudit, createFinding, updateAudit } from '../services/api'
import type { Audit } from '../types'
import StatusBadge from '../components/StatusBadge'

const AuditDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [audit, setAudit] = useState<Audit | null>(null)
  const [showFindingForm, setShowFindingForm] = useState(false)
  const [form, setForm] = useState({ finding_type: 'Minor NC', description: '', severity: 'Medium', corrective_action: '' })

  const load = () => { if (id) getAudit(id).then((r) => setAudit(r.data)).catch(() => navigate('/audits')) }
  useEffect(load, [id, navigate])

  const handleAddFinding = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!id) return
    await createFinding(id, form)
    setShowFindingForm(false)
    setForm({ finding_type: 'Minor NC', description: '', severity: 'Medium', corrective_action: '' })
    load()
  }

  const handleStatusChange = async (status: string) => {
    if (!id) return
    await updateAudit(id, { status })
    load()
  }

  if (!audit) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/audits')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Audits
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div>
            <span className="text-sm font-mono font-semibold text-gray-500">{audit.ref_id}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{audit.title}</h1>
            <div className="flex gap-2 mt-2"><StatusBadge value={audit.audit_type} /><StatusBadge value={audit.status} /></div>
          </div>
          <select className="select-field" value={audit.status} onChange={(e) => handleStatusChange(e.target.value)}>
            <option>Planned</option><option>In Progress</option><option>Completed</option><option>Cancelled</option>
          </select>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div><span className="text-gray-500">Lead Auditor</span><p className="font-medium">{audit.lead_auditor?.full_name || '—'}</p></div>
          <div><span className="text-gray-500">Start Date</span><p className="font-medium">{audit.start_date || '—'}</p></div>
          <div><span className="text-gray-500">End Date</span><p className="font-medium">{audit.end_date || '—'}</p></div>
          <div><span className="text-gray-500">Findings</span><p className="font-medium">{audit.findings?.length || 0}</p></div>
        </div>
        {audit.scope && <div className="mt-4"><span className="text-sm text-gray-500">Scope</span><p className="text-sm mt-1">{audit.scope}</p></div>}
      </div>

      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-gray-900">Findings</h2>
        <button className="btn-primary text-sm" onClick={() => setShowFindingForm(!showFindingForm)}>{showFindingForm ? 'Cancel' : '+ Add Finding'}</button>
      </div>

      {showFindingForm && (
        <form onSubmit={handleAddFinding} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.finding_type} onChange={(e) => setForm({ ...form, finding_type: e.target.value })}>
                <option>Major NC</option><option>Minor NC</option><option>Observation</option><option>OFI</option>
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Severity</label>
              <select className="select-field w-full" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
                <option>Critical</option><option>High</option><option>Medium</option><option>Low</option>
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea required className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Corrective Action</label><textarea className="input-field h-16" value={form.corrective_action} onChange={(e) => setForm({ ...form, corrective_action: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Add Finding</button>
        </form>
      )}

      <div className="card p-0 overflow-hidden">
        <table className="w-full">
          <thead><tr className="bg-gray-50 border-b border-gray-200">
            <th className="table-header">Ref ID</th>
            <th className="table-header">Type</th>
            <th className="table-header">Description</th>
            <th className="table-header">Severity</th>
            <th className="table-header">Status</th>
          </tr></thead>
          <tbody>
            {(audit.findings || []).map((f) => (
              <tr key={f.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="table-cell font-mono font-semibold">{f.ref_id}</td>
                <td className="table-cell"><StatusBadge value={f.finding_type} /></td>
                <td className="table-cell max-w-md truncate">{f.description}</td>
                <td className="table-cell"><StatusBadge value={f.severity} /></td>
                <td className="table-cell"><StatusBadge value={f.status} /></td>
              </tr>
            ))}
            {(!audit.findings || audit.findings.length === 0) && <tr><td colSpan={5} className="table-cell text-center text-gray-400 py-8">No findings recorded</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AuditDetailPage

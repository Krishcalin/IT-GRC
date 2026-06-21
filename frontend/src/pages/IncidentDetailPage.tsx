import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getIncident, updateIncident } from '../services/api'
import type { Incident } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['Malware', 'Phishing', 'Unauthorized Access', 'Data Breach', 'DoS', 'Misconfiguration', 'Lost/Stolen Device', 'Insider', 'Other']
const SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
const STATUSES = ['New', 'Triaged', 'In Progress', 'Resolved', 'Closed']

const Section: React.FC<{ title: string; value: string | null }> = ({ title, value }) =>
  value ? <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">{title}</h3><p className="text-gray-700 whitespace-pre-wrap">{value}</p></div> : null

const IncidentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [inc, setInc] = useState<Incident | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({
    category: '', severity: '', status: '', reporter: '', affected_assets: '', description: '',
    containment_actions: '', root_cause: '', lessons_learned: '', evidence_notes: '', data_breach: false,
  })

  useEffect(() => {
    if (!id) return
    getIncident(id).then((r) => {
      const d = r.data
      setInc(d)
      setForm({
        category: d.category, severity: d.severity, status: d.status, reporter: d.reporter || '',
        affected_assets: d.affected_assets || '', description: d.description || '',
        containment_actions: d.containment_actions || '', root_cause: d.root_cause || '',
        lessons_learned: d.lessons_learned || '', evidence_notes: d.evidence_notes || '', data_breach: d.data_breach,
      })
    }).catch(() => navigate('/incidents'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const payload: Partial<Incident> = { ...form }
      // Stamp resolution time when the incident is first resolved/closed.
      const closing = form.status === 'Resolved' || form.status === 'Closed'
      const wasClosing = inc?.status === 'Resolved' || inc?.status === 'Closed'
      if (closing && !wasClosing && !inc?.resolved_at) payload.resolved_at = new Date().toISOString()
      const res = await updateIncident(id, payload)
      setInc(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!inc) return <div className="p-8 text-gray-400">Loading...</div>
  const fmt = (d: string | null) => (d ? new Date(d).toLocaleString() : '—')

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/incidents')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Incidents
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{inc.ref_id} · {inc.category}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{inc.title}</h1>
            <div className="flex items-center flex-wrap gap-2 mt-2">
              <StatusBadge value={inc.severity} />
              <StatusBadge value={inc.status} />
              {inc.data_breach && <StatusBadge value="Critical" className="!bg-red-100 !text-red-800" />}
              {inc.data_breach && <span className="text-xs font-semibold text-red-700">Data breach</span>}
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          <Section title="Description" value={inc.description} />

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>{CATEGORIES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Severity</label>
                  <select className="select-field w-full" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>{SEVERITIES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>{STATUSES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Reporter</label><input className="input-field" value={form.reporter} onChange={(e) => setForm({ ...form, reporter: e.target.value })} /></div>
                <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Affected Assets</label><input className="input-field" value={form.affected_assets} onChange={(e) => setForm({ ...form, affected_assets: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Containment / Response (5.26)</label><textarea className="input-field h-20" value={form.containment_actions} onChange={(e) => setForm({ ...form, containment_actions: e.target.value })} /></div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Root Cause (5.27)</label><textarea className="input-field h-20" value={form.root_cause} onChange={(e) => setForm({ ...form, root_cause: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Lessons Learned (5.27)</label><textarea className="input-field h-20" value={form.lessons_learned} onChange={(e) => setForm({ ...form, lessons_learned: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Evidence Notes (5.28)</label><textarea className="input-field h-20" value={form.evidence_notes} onChange={(e) => setForm({ ...form, evidence_notes: e.target.value })} /></div>
              <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.data_breach} onChange={(e) => setForm({ ...form, data_breach: e.target.checked })} /> Involves personal data / reportable breach</label>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <>
              <Section title="Containment / Response (5.26)" value={inc.containment_actions} />
              <Section title="Root Cause (5.27)" value={inc.root_cause} />
              <Section title="Lessons Learned (5.27)" value={inc.lessons_learned} />
              <Section title="Evidence Notes (5.28)" value={inc.evidence_notes} />
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t pt-6">
                <div><span className="text-sm text-gray-500">Reporter</span><p className="font-medium">{inc.reporter || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{inc.owner?.full_name || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Reported</span><p className="font-medium">{fmt(inc.reported_at)}</p></div>
                <div><span className="text-sm text-gray-500">Resolved</span><p className="font-medium">{fmt(inc.resolved_at)}</p></div>
                <div className="col-span-2 md:col-span-4"><span className="text-sm text-gray-500">Affected Assets</span><p className="font-medium">{inc.affected_assets || '—'}</p></div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default IncidentDetailPage

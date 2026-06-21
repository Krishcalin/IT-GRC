import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getCampaign, updateCampaign, addTrainingRecord, updateTrainingRecord, deleteTrainingRecord } from '../services/api'
import type { TrainingCampaign } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['Awareness Campaign', 'Onboarding', 'Role-based Training', 'Phishing Simulation', 'Policy Acknowledgment', 'Other']
const STATUSES = ['Planned', 'In Progress', 'Completed', 'Cancelled']
const REC_STATUSES = ['Assigned', 'Completed', 'Overdue', 'Exempt']

const CampaignDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [c, setC] = useState<TrainingCampaign | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ training_type: '', topic: '', status: '', audience: '', materials_link: '', description: '', start_date: '', end_date: '' })
  const [newParticipant, setNewParticipant] = useState('')

  const reload = () => { if (id) getCampaign(id).then((r) => setC(r.data)).catch(() => navigate('/training')) }

  useEffect(() => {
    if (!id) return
    getCampaign(id).then((r) => {
      const d = r.data
      setC(d)
      setForm({
        training_type: d.training_type, topic: d.topic || '', status: d.status, audience: d.audience || '',
        materials_link: d.materials_link || '', description: d.description || '',
        start_date: d.start_date || '', end_date: d.end_date || '',
      })
    }).catch(() => navigate('/training'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const res = await updateCampaign(id, form)
      setC(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  const addRecord = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!id || !newParticipant.trim()) return
    await addTrainingRecord(id, { participant: newParticipant.trim(), status: 'Assigned' })
    setNewParticipant('')
    reload()
  }

  const markComplete = async (recordId: string) => {
    await updateTrainingRecord(recordId, { status: 'Completed', completed_at: new Date().toISOString().slice(0, 10) })
    reload()
  }

  const setRecordStatus = async (recordId: string, status: string) => {
    await updateTrainingRecord(recordId, { status })
    reload()
  }

  const removeRecord = async (recordId: string) => {
    if (!confirm('Remove this participation record?')) return
    await deleteTrainingRecord(recordId)
    reload()
  }

  if (!c) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/training')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Awareness &amp; Training
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{c.ref_id} · {c.training_type}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{c.title}</h1>
            <div className="flex items-center gap-2 mt-2">
              <StatusBadge value={c.status} />
              {c.topic && <span className="text-xs text-gray-500">{c.topic}</span>}
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        {/* Completion summary */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm font-semibold text-gray-700">Completion</span>
            <span className="text-sm text-gray-500">{c.completion_rate}% · {c.completed_participants}/{c.total_participants} completed</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className="bg-indigo-500 h-3 rounded-full" style={{ width: `${c.completion_rate}%` }} />
          </div>
        </div>

        {c.description && <div className="mb-4"><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3><p className="text-gray-700 whitespace-pre-wrap">{c.description}</p></div>}

        {editing ? (
          <div className="space-y-4 border-t pt-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                <select className="select-field w-full" value={form.training_type} onChange={(e) => setForm({ ...form, training_type: e.target.value })}>{TYPES.map((t) => <option key={t}>{t}</option>)}</select></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>{STATUSES.map((s) => <option key={s}>{s}</option>)}</select></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Topic</label><input className="input-field" value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Audience</label><input className="input-field" value={form.audience} onChange={(e) => setForm({ ...form, audience: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label><input type="date" className="input-field" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">End Date</label><input type="date" className="input-field" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} /></div>
              <div className="md:col-span-3"><label className="block text-sm font-medium text-gray-700 mb-1">Materials Link</label><input className="input-field" value={form.materials_link} onChange={(e) => setForm({ ...form, materials_link: e.target.value })} /></div>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-24" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
            <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t pt-6">
            <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{c.owner?.full_name || '—'}</p></div>
            <div><span className="text-sm text-gray-500">Audience</span><p className="font-medium">{c.audience || '—'}</p></div>
            <div><span className="text-sm text-gray-500">Period</span><p className="font-medium">{c.start_date || '—'} → {c.end_date || '—'}</p></div>
            <div><span className="text-sm text-gray-500">Materials</span><p className="font-medium break-all">{c.materials_link ? <a href={c.materials_link} target="_blank" rel="noreferrer" className="text-indigo-600 hover:underline">link</a> : '—'}</p></div>
          </div>
        )}
      </div>

      {/* Participation records */}
      <div className="card p-0 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-700">Participation Records (evidence of competence)</h3>
        </div>
        <form onSubmit={addRecord} className="px-6 py-3 border-b border-gray-100 flex gap-2">
          <input className="input-field max-w-xs" placeholder="Participant name" value={newParticipant} onChange={(e) => setNewParticipant(e.target.value)} />
          <button type="submit" className="btn-secondary">+ Add participant</button>
        </form>
        <table className="w-full">
          <thead><tr className="bg-gray-50 border-b border-gray-200">
            <th className="table-header">Ref</th>
            <th className="table-header">Participant</th>
            <th className="table-header">Status</th>
            <th className="table-header">Score</th>
            <th className="table-header">Completed</th>
            <th className="table-header">Actions</th>
          </tr></thead>
          <tbody>
            {c.records?.map((r) => (
              <tr key={r.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="table-cell font-mono text-gray-500">{r.ref_id}</td>
                <td className="table-cell">{r.participant}</td>
                <td className="table-cell">
                  <select value={r.status} onChange={(e) => setRecordStatus(r.id, e.target.value)} className="text-xs border border-gray-200 rounded px-1.5 py-0.5">
                    {REC_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </td>
                <td className="table-cell text-gray-600">{r.score ?? '—'}</td>
                <td className="table-cell text-gray-400">{r.completed_at || '—'}</td>
                <td className="table-cell">
                  <div className="flex gap-3">
                    {r.status !== 'Completed' && <button onClick={() => markComplete(r.id)} className="text-emerald-600 hover:text-emerald-800 text-xs">Mark complete</button>}
                    <button onClick={() => removeRecord(r.id)} className="text-red-500 hover:text-red-700 text-xs">Remove</button>
                  </div>
                </td>
              </tr>
            ))}
            {(!c.records || c.records.length === 0) && <tr><td colSpan={6} className="table-cell text-center text-gray-400 py-8">No participants yet — add one above.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CampaignDetailPage

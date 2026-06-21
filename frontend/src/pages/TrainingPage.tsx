import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCampaigns, createCampaign } from '../services/api'
import type { TrainingCampaign } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['Awareness Campaign', 'Onboarding', 'Role-based Training', 'Phishing Simulation', 'Policy Acknowledgment', 'Other']
const STATUSES = ['Planned', 'In Progress', 'Completed', 'Cancelled']

const emptyForm = { title: '', training_type: 'Awareness Campaign', topic: '', status: 'Planned', audience: '', materials_link: '', description: '' }

const TrainingPage: React.FC = () => {
  const navigate = useNavigate()
  const [campaigns, setCampaigns] = useState<TrainingCampaign[]>([])
  const [loading, setLoading] = useState(true)
  const [trainingType, setTrainingType] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (trainingType) params.training_type = trainingType
    if (status) params.status = status
    if (search) params.search = search
    getCampaigns(params).then((r) => setCampaigns(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [trainingType, status, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createCampaign(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Awareness &amp; Training</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{campaigns.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Campaign'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Awareness campaigns and training programmes (ISO/IEC 27001:2022 Clauses 7.2/7.3). Participation records are the evidence of competence.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.training_type} onChange={(e) => setForm({ ...form, training_type: e.target.value })}>
                {TYPES.map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {STATUSES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Topic</label><input className="input-field" value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Audience</label><input className="input-field" value={form.audience} onChange={(e) => setForm({ ...form, audience: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Materials Link</label><input className="input-field" value={form.materials_link} onChange={(e) => setForm({ ...form, materials_link: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Campaign</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={trainingType} onChange={(e) => setTrainingType(e.target.value)}>
          <option value="">All Types</option>
          {TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <input className="input-field max-w-xs" placeholder="Search ref or title..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Title</th>
              <th className="table-header">Type</th>
              <th className="table-header">Topic</th>
              <th className="table-header">Completion</th>
              <th className="table-header">Status</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {campaigns.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/training/${c.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{c.ref_id}</td>
                  <td className="table-cell">{c.title}</td>
                  <td className="table-cell text-gray-500">{c.training_type}</td>
                  <td className="table-cell text-gray-500">{c.topic || '—'}</td>
                  <td className="table-cell">
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div className="bg-indigo-500 h-2 rounded-full" style={{ width: `${c.completion_rate}%` }} />
                      </div>
                      <span className="text-xs text-gray-500">{c.completion_rate}% ({c.completed_participants}/{c.total_participants})</span>
                    </div>
                  </td>
                  <td className="table-cell"><StatusBadge value={c.status} /></td>
                  <td className="table-cell text-gray-400">{c.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {campaigns.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No training campaigns yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default TrainingPage

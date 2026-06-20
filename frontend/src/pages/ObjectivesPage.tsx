import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getObjectives, createObjective } from '../services/api'
import type { Objective } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Not Started', 'On Track', 'At Risk', 'Achieved', 'Missed']

const emptyForm = { title: '', description: '', measure: '', target_value: '', unit: '%', status: 'Not Started' }

const ObjectivesPage: React.FC = () => {
  const navigate = useNavigate()
  const [objectives, setObjectives] = useState<Objective[]>([])
  const [loading, setLoading] = useState(true)
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (status) params.status = status
    if (search) params.search = search
    getObjectives(params).then((r) => setObjectives(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [status, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createObjective(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Information Security Objectives</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{objectives.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Objective'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Measurable ISMS objectives (ISO/IEC 27001:2022 Clause 6.2). Track each against its target and link KPIs/KRIs/KCIs that measure it.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {STATUSES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Measure</label><input className="input-field" placeholder="How achievement is measured" value={form.measure} onChange={(e) => setForm({ ...form, measure: e.target.value })} /></div>
            <div className="grid grid-cols-2 gap-2">
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Target</label><input className="input-field" placeholder="e.g. <= 5%" value={form.target_value} onChange={(e) => setForm({ ...form, target_value: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Unit</label><input className="input-field" value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} /></div>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Objective</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
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
              <th className="table-header">Measure</th>
              <th className="table-header">Target</th>
              <th className="table-header">KxIs</th>
              <th className="table-header">Status</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {objectives.map((o) => (
                <tr key={o.id} onClick={() => navigate(`/objectives/${o.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{o.ref_id}</td>
                  <td className="table-cell">{o.title}</td>
                  <td className="table-cell text-gray-500 max-w-xs truncate" title={o.measure || ''}>{o.measure || '—'}</td>
                  <td className="table-cell text-gray-600">{o.target_value || '—'}</td>
                  <td className="table-cell text-gray-400">{o.metrics?.length || 0}</td>
                  <td className="table-cell"><StatusBadge value={o.status} /></td>
                  <td className="table-cell text-gray-400">{o.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {objectives.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No objectives yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default ObjectivesPage

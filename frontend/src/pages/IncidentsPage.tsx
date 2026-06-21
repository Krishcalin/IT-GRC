import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getIncidents, createIncident } from '../services/api'
import type { Incident } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['Malware', 'Phishing', 'Unauthorized Access', 'Data Breach', 'DoS', 'Misconfiguration', 'Lost/Stolen Device', 'Insider', 'Other']
const SEVERITIES = ['Low', 'Medium', 'High', 'Critical']
const STATUSES = ['New', 'Triaged', 'In Progress', 'Resolved', 'Closed']

const emptyForm = { title: '', category: 'Other', severity: 'Medium', status: 'New', reporter: '', affected_assets: '', description: '', data_breach: false }

const IncidentsPage: React.FC = () => {
  const navigate = useNavigate()
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [severity, setSeverity] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (category) params.category = category
    if (severity) params.severity = severity
    if (status) params.status = status
    if (search) params.search = search
    getIncidents(params).then((r) => setIncidents(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [category, severity, status, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createIncident(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  const fmt = (d: string | null) => (d ? new Date(d).toLocaleDateString() : '—')

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Security Incidents</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{incidents.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Report Incident'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Information security incident register (ISO/IEC 27001:2022 Clauses 5.24–5.28): assess, respond, learn, and preserve evidence.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Severity</label>
              <select className="select-field w-full" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })}>
                {SEVERITIES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {STATUSES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Reporter</label><input className="input-field" value={form.reporter} onChange={(e) => setForm({ ...form, reporter: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Affected Assets</label><input className="input-field" value={form.affected_assets} onChange={(e) => setForm({ ...form, affected_assets: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.data_breach} onChange={(e) => setForm({ ...form, data_breach: e.target.checked })} /> Involves personal data / reportable breach</label>
          <button type="submit" className="btn-primary">Report Incident</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select className="select-field" value={severity} onChange={(e) => setSeverity(e.target.value)}>
          <option value="">All Severity</option>
          {SEVERITIES.map((s) => <option key={s} value={s}>{s}</option>)}
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
              <th className="table-header">Category</th>
              <th className="table-header">Severity</th>
              <th className="table-header">Status</th>
              <th className="table-header">Reported</th>
              <th className="table-header">Breach</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {incidents.map((i) => (
                <tr key={i.id} onClick={() => navigate(`/incidents/${i.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{i.ref_id}</td>
                  <td className="table-cell">{i.title}</td>
                  <td className="table-cell text-gray-500">{i.category}</td>
                  <td className="table-cell"><StatusBadge value={i.severity} /></td>
                  <td className="table-cell"><StatusBadge value={i.status} /></td>
                  <td className="table-cell text-gray-400">{fmt(i.reported_at)}</td>
                  <td className="table-cell">{i.data_breach ? <span className="text-xs font-semibold text-red-700">Yes</span> : <span className="text-xs text-gray-400">No</span>}</td>
                  <td className="table-cell text-gray-400">{i.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {incidents.length === 0 && <tr><td colSpan={8} className="table-cell text-center text-gray-400 py-12">No incidents recorded</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default IncidentsPage

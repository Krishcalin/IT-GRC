import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAudits, createAudit } from '../services/api'
import type { Audit } from '../types'
import StatusBadge from '../components/StatusBadge'

const AuditsPage: React.FC = () => {
  const navigate = useNavigate()
  const [audits, setAudits] = useState<Audit[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', audit_type: 'Internal', description: '', start_date: '', end_date: '', scope: '' })

  const load = () => { setLoading(true); getAudits().then((r) => setAudits(r.data)).catch(() => {}).finally(() => setLoading(false)) }
  useEffect(load, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    const data: Record<string, unknown> = { ...form }
    if (!data.start_date) delete data.start_date
    if (!data.end_date) delete data.end_date
    await createAudit(data)
    setShowForm(false)
    setForm({ title: '', audit_type: 'Internal', description: '', start_date: '', end_date: '', scope: '' })
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Audits</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Audit'}</button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.audit_type} onChange={(e) => setForm({ ...form, audit_type: e.target.value })}>
                <option>Internal</option><option>External</option><option>Surveillance</option>
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label><input type="date" className="input-field" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">End Date</label><input type="date" className="input-field" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Scope</label><textarea className="input-field h-20" value={form.scope} onChange={(e) => setForm({ ...form, scope: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Audit</button>
        </form>
      )}

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Title</th>
              <th className="table-header">Type</th>
              <th className="table-header">Status</th>
              <th className="table-header">Start</th>
              <th className="table-header">End</th>
              <th className="table-header">Findings</th>
            </tr></thead>
            <tbody>
              {audits.map((a) => (
                <tr key={a.id} onClick={() => navigate(`/audits/${a.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold">{a.ref_id}</td>
                  <td className="table-cell">{a.title}</td>
                  <td className="table-cell">{a.audit_type}</td>
                  <td className="table-cell"><StatusBadge value={a.status} /></td>
                  <td className="table-cell text-sm text-gray-400">{a.start_date || '—'}</td>
                  <td className="table-cell text-sm text-gray-400">{a.end_date || '—'}</td>
                  <td className="table-cell text-center">{a.findings?.length || 0}</td>
                </tr>
              ))}
              {audits.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No audits yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default AuditsPage

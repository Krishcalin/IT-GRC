import React, { useEffect, useState } from 'react'
import { getPolicies, createPolicy, acknowledgePolicy } from '../services/api'
import type { Policy } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['Information Security', 'Access Control', 'Data Protection', 'Incident Response', 'Business Continuity', 'Acceptable Use', 'Risk Management', 'Other']

const PoliciesPage: React.FC = () => {
  const [policies, setPolicies] = useState<Policy[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', category: 'Information Security', description: '', content: '' })
  const [expanded, setExpanded] = useState<string | null>(null)

  const load = () => { setLoading(true); getPolicies().then((r) => setPolicies(r.data)).catch(() => {}).finally(() => setLoading(false)) }
  useEffect(load, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createPolicy(form)
    setShowForm(false)
    setForm({ title: '', category: 'Information Security', description: '', content: '' })
    load()
  }

  const handleAck = async (id: string) => {
    try { await acknowledgePolicy(id); load() } catch { /* already acked */ }
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Policies</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Policy'}</button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Content (Markdown)</label><textarea className="input-field h-32 font-mono text-sm" value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Policy</button>
        </form>
      )}

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Title</th>
              <th className="table-header">Category</th>
              <th className="table-header">Version</th>
              <th className="table-header">Status</th>
              <th className="table-header">Acks</th>
              <th className="table-header">Actions</th>
            </tr></thead>
            <tbody>
              {policies.map((p) => (
                <React.Fragment key={p.id}>
                  <tr className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer" onClick={() => setExpanded(expanded === p.id ? null : p.id)}>
                    <td className="table-cell font-mono font-semibold">{p.ref_id}</td>
                    <td className="table-cell">{p.title}</td>
                    <td className="table-cell text-sm">{p.category}</td>
                    <td className="table-cell text-center">{p.version}</td>
                    <td className="table-cell"><StatusBadge value={p.status} /></td>
                    <td className="table-cell text-center">{p.acknowledgments?.length || 0}</td>
                    <td className="table-cell"><button onClick={(e) => { e.stopPropagation(); handleAck(p.id) }} className="text-indigo-600 hover:text-indigo-800 text-xs font-medium">Acknowledge</button></td>
                  </tr>
                  {expanded === p.id && p.content && (
                    <tr><td colSpan={7} className="px-6 py-4 bg-gray-50 text-sm whitespace-pre-wrap">{p.content}</td></tr>
                  )}
                </React.Fragment>
              ))}
              {policies.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No policies yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default PoliciesPage

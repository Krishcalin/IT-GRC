import React, { useEffect, useState } from 'react'
import { getRisks, createRisk, deleteRisk } from '../services/api'
import type { Risk } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['', 'Strategic', 'Operational', 'Financial', 'Compliance', 'Technical', 'Reputational']
const RISK_STATUSES = ['', 'Open', 'In Treatment', 'Closed', 'Accepted']

const RisksPage: React.FC = () => {
  const [risks, setRisks] = useState<Risk[]>([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [status, setStatus] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', description: '', category: 'Technical', likelihood: 3, impact: 3, treatment: 'Mitigate', treatment_plan: '' })

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (category) params.category = category
    if (status) params.status = status
    getRisks(params).then((r) => setRisks(r.data)).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(load, [category, status])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createRisk(form)
    setShowForm(false)
    setForm({ title: '', description: '', category: 'Technical', likelihood: 3, impact: 3, treatment: 'Mitigate', treatment_plan: '' })
    load()
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this risk?')) return
    await deleteRisk(id)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Risk Register</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ Add Risk'}</button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.filter(Boolean).map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Likelihood (1-5)</label>
              <input type="number" min={1} max={5} className="input-field" value={form.likelihood} onChange={(e) => setForm({ ...form, likelihood: +e.target.value })} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Impact (1-5)</label>
              <input type="number" min={1} max={5} className="input-field" value={form.impact} onChange={(e) => setForm({ ...form, impact: +e.target.value })} />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea required className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </div>
          <button type="submit" className="btn-primary">Create Risk</button>
        </form>
      )}

      <div className="flex gap-3">
        <select className="select-field" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          {CATEGORIES.filter(Boolean).map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {RISK_STATUSES.filter(Boolean).map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Title</th>
              <th className="table-header">Category</th>
              <th className="table-header">L x I</th>
              <th className="table-header">Risk Level</th>
              <th className="table-header">Treatment</th>
              <th className="table-header">Status</th>
              <th className="table-header">Actions</th>
            </tr></thead>
            <tbody>
              {risks.map((r) => (
                <tr key={r.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="table-cell font-mono font-semibold">{r.ref_id}</td>
                  <td className="table-cell">{r.title}</td>
                  <td className="table-cell">{r.category}</td>
                  <td className="table-cell text-center">{r.likelihood} x {r.impact}</td>
                  <td className="table-cell"><StatusBadge value={r.inherent_risk_level} /></td>
                  <td className="table-cell"><StatusBadge value={r.treatment} /></td>
                  <td className="table-cell"><StatusBadge value={r.status} /></td>
                  <td className="table-cell"><button onClick={() => handleDelete(r.id)} className="text-red-500 hover:text-red-700 text-xs">Delete</button></td>
                </tr>
              ))}
              {risks.length === 0 && <tr><td colSpan={8} className="table-cell text-center text-gray-400 py-12">No risks found</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default RisksPage

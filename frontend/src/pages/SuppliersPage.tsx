import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getSuppliers, createSupplier } from '../services/api'
import type { Supplier } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['Product', 'Service', 'ICT Supply Chain', 'Cloud Service']
const CRITICALITIES = ['Low', 'Medium', 'High', 'Critical']
const CLASSIFICATIONS = ['Public', 'Internal', 'Confidential', 'Restricted']
const STATUSES = ['Active', 'Onboarding', 'Under Review', 'Offboarded']

const emptyForm = {
  name: '', category: 'Service', criticality: 'Medium', data_classification: 'Internal', status: 'Active',
  service_description: '', certifications: '', description: '',
  is_requirements_agreed: false, right_to_audit: false, processes_pii: false,
}

const SuppliersPage: React.FC = () => {
  const navigate = useNavigate()
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [criticality, setCriticality] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (category) params.category = category
    if (criticality) params.criticality = criticality
    if (status) params.status = status
    if (search) params.search = search
    getSuppliers(params).then((r) => setSuppliers(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [category, criticality, status, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createSupplier(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Suppliers &amp; Third Parties</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{suppliers.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Supplier'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Supplier relationships and their information security expectations (ISO/IEC 27001:2022 Clauses 5.19–5.23).
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Name</label><input required className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Criticality</label>
              <select className="select-field w-full" value={form.criticality} onChange={(e) => setForm({ ...form, criticality: e.target.value })}>
                {CRITICALITIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Data Classification</label>
              <select className="select-field w-full" value={form.data_classification} onChange={(e) => setForm({ ...form, data_classification: e.target.value })}>
                {CLASSIFICATIONS.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                {STATUSES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Certifications</label><input className="input-field" placeholder="ISO 27001, SOC 2..." value={form.certifications} onChange={(e) => setForm({ ...form, certifications: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Service Description</label><input className="input-field" value={form.service_description} onChange={(e) => setForm({ ...form, service_description: e.target.value })} /></div>
          <div className="flex flex-wrap gap-6">
            <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.is_requirements_agreed} onChange={(e) => setForm({ ...form, is_requirements_agreed: e.target.checked })} /> IS requirements agreed (5.20)</label>
            <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.right_to_audit} onChange={(e) => setForm({ ...form, right_to_audit: e.target.checked })} /> Right to audit</label>
            <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.processes_pii} onChange={(e) => setForm({ ...form, processes_pii: e.target.checked })} /> Processes PII</label>
          </div>
          <button type="submit" className="btn-primary">Create Supplier</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select className="select-field" value={criticality} onChange={(e) => setCriticality(e.target.value)}>
          <option value="">All Criticality</option>
          {CRITICALITIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <input className="input-field max-w-xs" placeholder="Search ref or name..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Name</th>
              <th className="table-header">Category</th>
              <th className="table-header">Criticality</th>
              <th className="table-header">Data Class</th>
              <th className="table-header">Audit</th>
              <th className="table-header">Status</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {suppliers.map((s) => (
                <tr key={s.id} onClick={() => navigate(`/suppliers/${s.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{s.ref_id}</td>
                  <td className="table-cell">{s.name}</td>
                  <td className="table-cell text-gray-500">{s.category}</td>
                  <td className="table-cell"><StatusBadge value={s.criticality} /></td>
                  <td className="table-cell"><StatusBadge value={s.data_classification} /></td>
                  <td className="table-cell">{s.right_to_audit ? <span className="text-xs font-semibold text-emerald-700">Yes</span> : <span className="text-xs text-gray-400">No</span>}</td>
                  <td className="table-cell"><StatusBadge value={s.status} /></td>
                  <td className="table-cell text-gray-400">{s.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {suppliers.length === 0 && <tr><td colSpan={8} className="table-cell text-center text-gray-400 py-12">No suppliers yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default SuppliersPage

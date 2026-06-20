import React, { useEffect, useState } from 'react'
import { getInterestedParties, createInterestedParty, updateInterestedParty, deleteInterestedParty } from '../services/api'
import type { InterestedParty } from '../types'
import StatusBadge from '../components/StatusBadge'

const PARTY_TYPES = ['Internal', 'External']
const CATEGORIES = ['Customer', 'Regulator', 'Employee', 'Supplier', 'Partner', 'Owner', 'Other']

const emptyForm = { name: '', party_type: 'External', category: 'Customer', requirements: '', addressed_in_isms: false, notes: '' }

const InterestedPartiesPage: React.FC = () => {
  const [parties, setParties] = useState<InterestedParty[]>([])
  const [loading, setLoading] = useState(true)
  const [partyType, setPartyType] = useState('')
  const [category, setCategory] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (partyType) params.party_type = partyType
    if (category) params.category = category
    if (search) params.search = search
    getInterestedParties(params).then((r) => setParties(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [partyType, category, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createInterestedParty(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  const toggleAddressed = async (p: InterestedParty) => {
    await updateInterestedParty(p.id, { addressed_in_isms: !p.addressed_in_isms })
    load()
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this interested party?')) return
    await deleteInterestedParty(id)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Interested Parties</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{parties.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Party'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Parties relevant to the ISMS and their requirements (ISO/IEC 27001:2022 Clause 4.2). Mark whether each requirement is addressed by the ISMS (4.2c).
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Name</label><input required className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.party_type} onChange={(e) => setForm({ ...form, party_type: e.target.value })}>
                {PARTY_TYPES.map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Requirements / Expectations</label><textarea className="input-field h-20" value={form.requirements} onChange={(e) => setForm({ ...form, requirements: e.target.value })} /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Notes</label><input className="input-field" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></div>
          <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.addressed_in_isms} onChange={(e) => setForm({ ...form, addressed_in_isms: e.target.checked })} /> Requirements addressed by the ISMS (4.2c)</label>
          <button type="submit" className="btn-primary">Create Party</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={partyType} onChange={(e) => setPartyType(e.target.value)}>
          <option value="">All Types</option>
          {PARTY_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="select-field" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All Categories</option>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <input className="input-field max-w-xs" placeholder="Search ref or name..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Name</th>
              <th className="table-header">Type</th>
              <th className="table-header">Category</th>
              <th className="table-header">Requirements</th>
              <th className="table-header">Addressed</th>
              <th className="table-header">Actions</th>
            </tr></thead>
            <tbody>
              {parties.map((p) => (
                <tr key={p.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="table-cell font-mono font-semibold">{p.ref_id}</td>
                  <td className="table-cell">{p.name}</td>
                  <td className="table-cell text-gray-500">{p.party_type}</td>
                  <td className="table-cell"><StatusBadge value={p.category} /></td>
                  <td className="table-cell text-gray-600 max-w-md truncate" title={p.requirements || ''}>{p.requirements || '—'}</td>
                  <td className="table-cell">
                    <button onClick={() => toggleAddressed(p)} className={`text-xs font-semibold px-2 py-0.5 rounded-full ${p.addressed_in_isms ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-600'}`}>
                      {p.addressed_in_isms ? 'Yes' : 'No'}
                    </button>
                  </td>
                  <td className="table-cell"><button onClick={() => handleDelete(p.id)} className="text-red-500 hover:text-red-700 text-xs">Delete</button></td>
                </tr>
              ))}
              {parties.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No interested parties yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default InterestedPartiesPage

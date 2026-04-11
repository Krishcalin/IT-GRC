import React, { useEffect, useState } from 'react'
import { getAssets, createAsset, deleteAsset } from '../services/api'
import type { Asset } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['', 'Hardware', 'Software', 'Data', 'Service', 'People', 'Facility']
const CLASSIFICATIONS = ['', 'Public', 'Internal', 'Confidential', 'Restricted']

const AssetsPage: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([])
  const [loading, setLoading] = useState(true)
  const [assetType, setAssetType] = useState('')
  const [classification, setClassification] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', description: '', asset_type: 'Software', classification: 'Internal', department: '', location: '', criticality: 'Medium' })

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (assetType) params.asset_type = assetType
    if (classification) params.classification = classification
    getAssets(params).then((r) => setAssets(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [assetType, classification])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createAsset(form)
    setShowForm(false)
    setForm({ name: '', description: '', asset_type: 'Software', classification: 'Internal', department: '', location: '', criticality: 'Medium' })
    load()
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this asset?')) return
    await deleteAsset(id)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Asset Inventory</h1>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Asset'}</button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Name</label><input required className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.asset_type} onChange={(e) => setForm({ ...form, asset_type: e.target.value })}>
                {TYPES.filter(Boolean).map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Classification</label>
              <select className="select-field w-full" value={form.classification} onChange={(e) => setForm({ ...form, classification: e.target.value })}>
                {CLASSIFICATIONS.filter(Boolean).map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Department</label><input className="input-field" value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Location</label><input className="input-field" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Criticality</label>
              <select className="select-field w-full" value={form.criticality} onChange={(e) => setForm({ ...form, criticality: e.target.value })}>
                <option>Low</option><option>Medium</option><option>High</option><option>Critical</option>
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Asset</button>
        </form>
      )}

      <div className="flex gap-3">
        <select className="select-field" value={assetType} onChange={(e) => setAssetType(e.target.value)}>
          <option value="">All Types</option>
          {TYPES.filter(Boolean).map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="select-field" value={classification} onChange={(e) => setClassification(e.target.value)}>
          <option value="">All Classifications</option>
          {CLASSIFICATIONS.filter(Boolean).map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Name</th>
              <th className="table-header">Type</th>
              <th className="table-header">Classification</th>
              <th className="table-header">Criticality</th>
              <th className="table-header">Status</th>
              <th className="table-header">Actions</th>
            </tr></thead>
            <tbody>
              {assets.map((a) => (
                <tr key={a.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="table-cell font-mono font-semibold">{a.ref_id}</td>
                  <td className="table-cell">{a.name}</td>
                  <td className="table-cell">{a.asset_type}</td>
                  <td className="table-cell"><StatusBadge value={a.classification} /></td>
                  <td className="table-cell"><StatusBadge value={a.criticality} /></td>
                  <td className="table-cell"><StatusBadge value={a.status} /></td>
                  <td className="table-cell"><button onClick={() => handleDelete(a.id)} className="text-red-500 hover:text-red-700 text-xs">Delete</button></td>
                </tr>
              ))}
              {assets.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No assets yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default AssetsPage

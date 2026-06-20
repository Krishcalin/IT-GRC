import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getDocuments, createDocument } from '../services/api'
import type { DocumentedInformation } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['Policy', 'Process', 'Procedure', 'Plan', 'Register', 'Record', 'Statement', 'Guideline']
const STATUSES = ['Draft', 'Under Review', 'Approved', 'Retired']
const CLASSIFICATIONS = ['Public', 'Internal', 'Confidential', 'Restricted']

const emptyForm = { title: '', doc_type: 'Policy', clause_ref: '', mandatory: false, version: '0.1', classification: 'Internal', location: '', description: '' }

const DocumentsPage: React.FC = () => {
  const navigate = useNavigate()
  const [docs, setDocs] = useState<DocumentedInformation[]>([])
  const [loading, setLoading] = useState(true)
  const [docType, setDocType] = useState('')
  const [status, setStatus] = useState('')
  const [mandatoryOnly, setMandatoryOnly] = useState(false)
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (docType) params.doc_type = docType
    if (status) params.status = status
    if (mandatoryOnly) params.mandatory = 'true'
    if (search) params.search = search
    getDocuments(params).then((r) => setDocs(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [docType, status, mandatoryOnly, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    await createDocument(form)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  const total = docs.length
  const approved = docs.filter((d) => d.status === 'Approved').length

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Documented Information</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{total}</span>
          {total > 0 && <span className="text-xs text-gray-500">{approved}/{total} approved</span>}
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Document'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        ISMS documents and records (ISO/IEC 27001:2022 Clause 7.5). The mandatory documented information required by Clauses 4–10 is pre-loaded.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.doc_type} onChange={(e) => setForm({ ...form, doc_type: e.target.value })}>
                {TYPES.map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Clause Ref</label><input className="input-field" placeholder="e.g. 6.1.3 / A.5.1" value={form.clause_ref} onChange={(e) => setForm({ ...form, clause_ref: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Version</label><input className="input-field" value={form.version} onChange={(e) => setForm({ ...form, version: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Classification</label>
              <select className="select-field w-full" value={form.classification} onChange={(e) => setForm({ ...form, classification: e.target.value })}>
                {CLASSIFICATIONS.map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Location / Link</label><input className="input-field" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.mandatory} onChange={(e) => setForm({ ...form, mandatory: e.target.checked })} /> Mandatory documented information</label>
          <button type="submit" className="btn-primary">Create Document</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3 items-center">
        <select className="select-field" value={docType} onChange={(e) => setDocType(e.target.value)}>
          <option value="">All Types</option>
          {TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <label className="flex items-center gap-2 text-sm text-gray-600"><input type="checkbox" checked={mandatoryOnly} onChange={(e) => setMandatoryOnly(e.target.checked)} /> Mandatory only</label>
        <input className="input-field max-w-xs" placeholder="Search ref or title..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref ID</th>
              <th className="table-header">Title</th>
              <th className="table-header">Type</th>
              <th className="table-header">Clause</th>
              <th className="table-header">Version</th>
              <th className="table-header">Status</th>
              <th className="table-header">Mandatory</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {docs.map((d) => (
                <tr key={d.id} onClick={() => navigate(`/documents/${d.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{d.ref_id}</td>
                  <td className="table-cell">{d.title}</td>
                  <td className="table-cell text-gray-500">{d.doc_type}</td>
                  <td className="table-cell font-mono text-gray-500">{d.clause_ref || '—'}</td>
                  <td className="table-cell text-gray-500">{d.version}</td>
                  <td className="table-cell"><StatusBadge value={d.status} /></td>
                  <td className="table-cell">{d.mandatory ? <span className="text-xs font-semibold text-indigo-700">Required</span> : <span className="text-xs text-gray-400">—</span>}</td>
                  <td className="table-cell text-gray-400">{d.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {docs.length === 0 && <tr><td colSpan={8} className="table-cell text-center text-gray-400 py-12">No documents found</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default DocumentsPage

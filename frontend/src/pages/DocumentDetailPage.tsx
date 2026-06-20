import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getDocument, updateDocument } from '../services/api'
import type { DocumentedInformation } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Draft', 'Under Review', 'Approved', 'Retired']
const CLASSIFICATIONS = ['Public', 'Internal', 'Confidential', 'Restricted']

const DocumentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [doc, setDoc] = useState<DocumentedInformation | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ status: '', version: '', classification: '', location: '', description: '', review_date: '', next_review_date: '' })

  useEffect(() => {
    if (!id) return
    getDocument(id).then((r) => {
      setDoc(r.data)
      setForm({
        status: r.data.status, version: r.data.version, classification: r.data.classification,
        location: r.data.location || '', description: r.data.description || '',
        review_date: r.data.review_date || '', next_review_date: r.data.next_review_date || '',
      })
    }).catch(() => navigate('/documents'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const payload: Partial<DocumentedInformation> = { ...form }
      // Stamp approval time when a document is approved.
      if (form.status === 'Approved' && doc?.status !== 'Approved') payload.approved_at = new Date().toISOString()
      const res = await updateDocument(id, payload)
      setDoc(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!doc) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/documents')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Documents
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{doc.ref_id} · {doc.doc_type}{doc.clause_ref ? ` · Clause ${doc.clause_ref}` : ''}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{doc.title}</h1>
            <div className="flex items-center gap-2 mt-2">
              <StatusBadge value={doc.status} />
              <StatusBadge value={doc.classification} />
              <span className="text-xs text-gray-500">v{doc.version}</span>
              {doc.mandatory && <span className="text-xs font-semibold text-indigo-700">Mandatory</span>}
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          {doc.description && (
            <div>
              <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3>
              <p className="text-gray-700 whitespace-pre-wrap">{doc.description}</p>
            </div>
          )}

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                    {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Version</label><input className="input-field" value={form.version} onChange={(e) => setForm({ ...form, version: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Classification</label>
                  <select className="select-field w-full" value={form.classification} onChange={(e) => setForm({ ...form, classification: e.target.value })}>
                    {CLASSIFICATIONS.map((c) => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Review Date</label><input type="date" className="input-field" value={form.review_date} onChange={(e) => setForm({ ...form, review_date: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Next Review Date</label><input type="date" className="input-field" value={form.next_review_date} onChange={(e) => setForm({ ...form, next_review_date: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Location / Link</label><input className="input-field" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-24" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 border-t pt-6">
              <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{doc.owner?.full_name || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Approver</span><p className="font-medium">{doc.approver?.full_name || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Approved</span><p className="font-medium">{doc.approved_at ? new Date(doc.approved_at).toLocaleDateString() : '—'}</p></div>
              <div><span className="text-sm text-gray-500">Review Date</span><p className="font-medium">{doc.review_date || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Next Review</span><p className="font-medium">{doc.next_review_date || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Location</span><p className="font-medium break-all">{doc.location || '—'}</p></div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DocumentDetailPage

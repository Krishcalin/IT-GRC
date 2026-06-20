import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getClause, updateClause } from '../services/api'
import type { ClauseRequirement } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Not Assessed', 'In Progress', 'Partially Conformant', 'Conformant', 'Nonconformant']

const ClauseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [clause, setClause] = useState<ClauseRequirement | null>(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ conformity_status: '', implementation_notes: '', review_date: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!id) return
    getClause(id).then((r) => {
      setClause(r.data)
      setForm({ conformity_status: r.data.conformity_status, implementation_notes: r.data.implementation_notes || '', review_date: r.data.review_date || '' })
    }).catch(() => navigate('/clauses'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const res = await updateClause(id, form)
      setClause(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!clause) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/clauses')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to ISMS Clauses
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">Clause {clause.clause}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{clause.title}</h1>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs text-gray-500">{clause.section}</span>
              <StatusBadge value={clause.conformity_status} />
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Requirement</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{clause.requirement}</p>
          </div>

          {clause.documented_info && (
            <div className="rounded-lg bg-indigo-50 border border-indigo-100 p-4">
              <h3 className="text-sm font-semibold text-indigo-700 mb-1 flex items-center gap-1.5">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}><path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                Mandatory documented information
              </h3>
              <p className="text-sm text-indigo-900">{clause.documented_info}</p>
            </div>
          )}

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Conformity Status</label>
                <select className="select-field" value={form.conformity_status} onChange={(e) => setForm({ ...form, conformity_status: e.target.value })}>
                  {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Implementation Notes</label>
                <textarea className="input-field h-32" value={form.implementation_notes} onChange={(e) => setForm({ ...form, implementation_notes: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Review Date</label>
                <input type="date" className="input-field max-w-xs" value={form.review_date} onChange={(e) => setForm({ ...form, review_date: e.target.value })} />
              </div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <>
              {clause.implementation_notes && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Implementation Notes</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{clause.implementation_notes}</p>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4 border-t pt-6">
                <div>
                  <span className="text-sm text-gray-500">Owner</span>
                  <p className="font-medium">{clause.owner?.full_name || '—'}</p>
                </div>
                <div>
                  <span className="text-sm text-gray-500">Review Date</span>
                  <p className="font-medium">{clause.review_date || '—'}</p>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ClauseDetailPage

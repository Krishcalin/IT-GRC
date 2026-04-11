import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getControl, updateControl } from '../services/api'
import type { Control } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Not Started', 'In Progress', 'Implemented', 'Not Applicable']

const ControlDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [control, setControl] = useState<Control | null>(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ status: '', implementation_guidance: '', review_date: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!id) return
    getControl(id).then((r) => {
      setControl(r.data)
      setForm({ status: r.data.status, implementation_guidance: r.data.implementation_guidance || '', review_date: r.data.review_date || '' })
    }).catch(() => navigate('/controls'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const res = await updateControl(id, form)
      setControl(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!control) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/controls')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Controls
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{control.clause}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{control.title}</h1>
            <div className="flex gap-2 mt-2">
              <StatusBadge value={control.theme} />
              <StatusBadge value={control.status} />
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3>
            <p className="text-gray-700">{control.description}</p>
          </div>

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select className="select-field" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Implementation Guidance</label>
                <textarea className="input-field h-32" value={form.implementation_guidance} onChange={(e) => setForm({ ...form, implementation_guidance: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Review Date</label>
                <input type="date" className="input-field max-w-xs" value={form.review_date} onChange={(e) => setForm({ ...form, review_date: e.target.value })} />
              </div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <>
              {control.implementation_guidance && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Implementation Guidance</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{control.implementation_guidance}</p>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4 border-t pt-6">
                <div>
                  <span className="text-sm text-gray-500">Owner</span>
                  <p className="font-medium">{control.owner?.full_name || '—'}</p>
                </div>
                <div>
                  <span className="text-sm text-gray-500">Review Date</span>
                  <p className="font-medium">{control.review_date || '—'}</p>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default ControlDetailPage

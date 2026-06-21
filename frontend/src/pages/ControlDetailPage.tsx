import React, { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getControl, updateControl, getControls, getControlMappings, addControlMapping, deleteControlMapping } from '../services/api'
import type { Control, ControlMappingItem } from '../types'
import StatusBadge from '../components/StatusBadge'

const RELATIONSHIPS = ['equivalent', 'related', 'broader', 'narrower']

const STATUSES = ['Not Started', 'In Progress', 'Implemented', 'Not Applicable']

const ControlDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [control, setControl] = useState<Control | null>(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ status: '', implementation_guidance: '', review_date: '' })
  const [saving, setSaving] = useState(false)
  const [mappings, setMappings] = useState<ControlMappingItem[]>([])
  const [allControls, setAllControls] = useState<Control[]>([])
  const [pickFramework, setPickFramework] = useState('')
  const [pickTarget, setPickTarget] = useState('')
  const [pickRel, setPickRel] = useState('related')

  const loadMappings = useCallback(() => {
    if (!id) return
    getControlMappings(id).then((r) => setMappings(r.data)).catch(() => {})
  }, [id])

  useEffect(() => {
    if (!id) return
    getControl(id).then((r) => {
      setControl(r.data)
      setForm({ status: r.data.status, implementation_guidance: r.data.implementation_guidance || '', review_date: r.data.review_date || '' })
    }).catch(() => navigate('/controls'))
    loadMappings()
    getControls().then((r) => setAllControls(r.data)).catch(() => {})
  }, [id, navigate, loadMappings])

  const addMapping = async () => {
    if (!id || !pickTarget) return
    try { await addControlMapping(id, { target_control_id: pickTarget, relationship_type: pickRel }) } catch { /* dup/ignore */ }
    setPickTarget('')
    loadMappings()
  }
  const removeMapping = async (mappingId: string) => {
    if (!id) return
    await deleteControlMapping(id, mappingId)
    loadMappings()
  }

  const frameworkOptions = Array.from(new Set(allControls.map((c) => c.framework))).filter((f) => f !== control?.framework)
  const mappedIds = new Set(mappings.map((m) => m.control.id))
  const targetOptions = allControls.filter((c) => c.id !== id && !mappedIds.has(c.id) && (!pickFramework || c.framework === pickFramework))

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
            <div className="flex items-center gap-2">
              <span className="text-sm font-mono font-semibold text-indigo-600">{control.clause}</span>
              <span className="text-xs text-gray-400">·</span>
              <span className="text-xs font-medium text-gray-500">{control.framework}</span>
            </div>
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

      {/* Cross-framework crosswalk */}
      <div className="card">
        <h3 className="text-sm font-semibold text-gray-700 mb-1">Framework Crosswalk</h3>
        <p className="text-xs text-gray-400 mb-4">Map this control to equivalent controls in other frameworks — satisfy multiple frameworks from one control set.</p>

        {mappings.length > 0 ? (
          <table className="w-full mb-4">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Framework</th>
              <th className="table-header">Clause</th>
              <th className="table-header">Title</th>
              <th className="table-header">Relationship</th>
              <th className="table-header"></th>
            </tr></thead>
            <tbody>
              {mappings.map((m) => (
                <tr key={m.id} className="border-b border-gray-100">
                  <td className="table-cell text-xs text-gray-500">{m.control.framework}</td>
                  <td className="table-cell font-mono text-indigo-600 cursor-pointer hover:underline" onClick={() => navigate(`/controls/${m.control.id}`)}>{m.control.clause}</td>
                  <td className="table-cell">{m.control.title}</td>
                  <td className="table-cell"><span className="text-xs capitalize bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full">{m.relationship_type}</span></td>
                  <td className="table-cell text-right"><button onClick={() => removeMapping(m.id)} className="text-xs text-gray-400 hover:text-red-600">Remove</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p className="text-sm text-gray-400 mb-4">No cross-framework mappings yet.</p>}

        <div className="flex flex-wrap items-end gap-3 border-t pt-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Framework</label>
            <select className="select-field" value={pickFramework} onChange={(e) => { setPickFramework(e.target.value); setPickTarget('') }}>
              <option value="">All frameworks</option>
              {frameworkOptions.map((f) => <option key={f} value={f}>{f}</option>)}
            </select>
          </div>
          <div className="flex-1 min-w-[16rem]">
            <label className="block text-xs font-medium text-gray-600 mb-1">Control</label>
            <select className="select-field w-full" value={pickTarget} onChange={(e) => setPickTarget(e.target.value)}>
              <option value="">Select a control…</option>
              {targetOptions.map((c) => <option key={c.id} value={c.id}>{c.framework} · {c.clause} — {c.title}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Relationship</label>
            <select className="select-field capitalize" value={pickRel} onChange={(e) => setPickRel(e.target.value)}>
              {RELATIONSHIPS.map((r) => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <button onClick={addMapping} disabled={!pickTarget} className="btn-primary disabled:opacity-50">Add Mapping</button>
        </div>
      </div>
    </div>
  )
}

export default ControlDetailPage

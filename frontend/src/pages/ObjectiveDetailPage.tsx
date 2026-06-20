import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getObjective, updateObjective } from '../services/api'
import type { Objective } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Not Started', 'On Track', 'At Risk', 'Achieved', 'Missed']

const ObjectiveDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [obj, setObj] = useState<Objective | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ status: '', measure: '', target_value: '', current_value: '', unit: '', description: '', due_date: '', review_date: '' })

  useEffect(() => {
    if (!id) return
    getObjective(id).then((r) => {
      setObj(r.data)
      setForm({
        status: r.data.status, measure: r.data.measure || '', target_value: r.data.target_value || '',
        current_value: r.data.current_value || '', unit: r.data.unit || '', description: r.data.description || '',
        due_date: r.data.due_date || '', review_date: r.data.review_date || '',
      })
    }).catch(() => navigate('/objectives'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const res = await updateObjective(id, form)
      setObj(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!obj) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/objectives')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Objectives
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{obj.ref_id} · Clause {obj.clause_ref}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{obj.title}</h1>
            <div className="flex items-center gap-2 mt-2">
              <StatusBadge value={obj.status} />
              {obj.target_value && <span className="text-xs text-gray-500">Target: {obj.target_value}</span>}
              {obj.current_value && <span className="text-xs text-gray-500">Current: {obj.current_value}</span>}
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          {obj.description && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3><p className="text-gray-700 whitespace-pre-wrap">{obj.description}</p></div>}
          {obj.measure && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Measure</h3><p className="text-gray-700">{obj.measure}</p></div>}

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                    {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Target</label><input className="input-field" value={form.target_value} onChange={(e) => setForm({ ...form, target_value: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Current</label><input className="input-field" value={form.current_value} onChange={(e) => setForm({ ...form, current_value: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label><input type="date" className="input-field" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Review Date</label><input type="date" className="input-field" value={form.review_date} onChange={(e) => setForm({ ...form, review_date: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Measure</label><input className="input-field" value={form.measure} onChange={(e) => setForm({ ...form, measure: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-24" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t pt-6">
              <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{obj.owner?.full_name || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Due Date</span><p className="font-medium">{obj.due_date || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Review Date</span><p className="font-medium">{obj.review_date || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Unit</span><p className="font-medium">{obj.unit || '—'}</p></div>
            </div>
          )}
        </div>
      </div>

      {/* Linked metrics */}
      <div className="card p-0 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100"><h3 className="text-sm font-semibold text-gray-700">Linked Metrics (KPI / KRI / KCI)</h3></div>
        <table className="w-full">
          <thead><tr className="bg-gray-50 border-b border-gray-200">
            <th className="table-header">Ref</th>
            <th className="table-header">Name</th>
            <th className="table-header">Type</th>
            <th className="table-header">Target</th>
            <th className="table-header">Current</th>
            <th className="table-header">Status</th>
          </tr></thead>
          <tbody>
            {obj.metrics?.map((m) => (
              <tr key={m.id} onClick={() => navigate(`/metrics/${m.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer">
                <td className="table-cell font-mono font-semibold text-indigo-600">{m.ref_id}</td>
                <td className="table-cell">{m.name}</td>
                <td className="table-cell text-gray-500">{m.metric_type}</td>
                <td className="table-cell text-gray-600">{m.target_value ?? '—'}{m.unit ? ` ${m.unit}` : ''}</td>
                <td className="table-cell text-gray-600">{m.current_value ?? '—'}{m.unit ? ` ${m.unit}` : ''}</td>
                <td className="table-cell"><StatusBadge value={m.rag} /></td>
              </tr>
            ))}
            {(!obj.metrics || obj.metrics.length === 0) && <tr><td colSpan={6} className="table-cell text-center text-gray-400 py-8">No metrics linked yet — add one in the Metrics page and set its objective.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default ObjectiveDetailPage

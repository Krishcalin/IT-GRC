import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getMetric, updateMetric } from '../services/api'
import type { Metric } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['KPI', 'KRI', 'KCI']
const DIRECTIONS = [
  { value: 'higher_is_better', label: 'Higher is better' },
  { value: 'lower_is_better', label: 'Lower is better' },
]
const FREQUENCIES = ['Monthly', 'Quarterly', 'Annual', 'Continuous']

const MetricDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [metric, setMetric] = useState<Metric | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({ name: '', description: '', metric_type: 'KPI', target_value: '', current_value: '', unit: '', direction: 'higher_is_better', frequency: '', last_measured: '' })

  useEffect(() => {
    if (!id) return
    getMetric(id).then((r) => {
      setMetric(r.data)
      setForm({
        name: r.data.name, description: r.data.description || '', metric_type: r.data.metric_type,
        target_value: r.data.target_value?.toString() ?? '', current_value: r.data.current_value?.toString() ?? '',
        unit: r.data.unit || '', direction: r.data.direction, frequency: r.data.frequency || '',
        last_measured: r.data.last_measured || '',
      })
    }).catch(() => navigate('/metrics'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const payload: Record<string, unknown> = {
        name: form.name, description: form.description, metric_type: form.metric_type,
        unit: form.unit, direction: form.direction, frequency: form.frequency,
        target_value: form.target_value === '' ? null : Number(form.target_value),
        current_value: form.current_value === '' ? null : Number(form.current_value),
        last_measured: form.last_measured || null,
      }
      const res = await updateMetric(id, payload)
      setMetric(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!metric) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/metrics')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Metrics
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{metric.ref_id} · {metric.metric_type} · Clause {metric.clause_ref}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{metric.name}</h1>
            <div className="flex items-center gap-2 mt-2">
              <StatusBadge value={metric.rag} />
              <span className="text-xs text-gray-500">
                Target {metric.target_value ?? '—'}{metric.unit ? ` ${metric.unit}` : ''} · Current {metric.current_value ?? '—'}{metric.unit ? ` ${metric.unit}` : ''}
              </span>
              <span className="text-xs text-gray-400">({metric.direction === 'lower_is_better' ? 'lower is better' : 'higher is better'})</span>
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          {metric.description && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3><p className="text-gray-700 whitespace-pre-wrap">{metric.description}</p></div>}

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Name</label><input className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                  <select className="select-field w-full" value={form.metric_type} onChange={(e) => setForm({ ...form, metric_type: e.target.value })}>
                    {TYPES.map((t) => <option key={t}>{t}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Unit</label><input className="input-field" value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Target</label><input type="number" step="any" className="input-field" value={form.target_value} onChange={(e) => setForm({ ...form, target_value: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Current</label><input type="number" step="any" className="input-field" value={form.current_value} onChange={(e) => setForm({ ...form, current_value: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Direction</label>
                  <select className="select-field w-full" value={form.direction} onChange={(e) => setForm({ ...form, direction: e.target.value })}>
                    {DIRECTIONS.map((d) => <option key={d.value} value={d.value}>{d.label}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Frequency</label>
                  <select className="select-field w-full" value={form.frequency} onChange={(e) => setForm({ ...form, frequency: e.target.value })}>
                    <option value="">—</option>
                    {FREQUENCIES.map((f) => <option key={f}>{f}</option>)}
                  </select>
                </div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Last Measured</label><input type="date" className="input-field" value={form.last_measured} onChange={(e) => setForm({ ...form, last_measured: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-24" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t pt-6">
              <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{metric.owner?.full_name || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Frequency</span><p className="font-medium">{metric.frequency || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Last Measured</span><p className="font-medium">{metric.last_measured || '—'}</p></div>
              <div><span className="text-sm text-gray-500">Linked Objective</span><p className="font-medium">{metric.objective_id ? <button onClick={() => navigate(`/objectives/${metric.objective_id}`)} className="text-indigo-600 hover:underline">view</button> : '—'}</p></div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MetricDetailPage

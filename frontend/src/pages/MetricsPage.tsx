import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getMetrics, createMetric, getObjectives } from '../services/api'
import type { Metric, Objective } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['KPI', 'KRI', 'KCI']
const DIRECTIONS = [
  { value: 'higher_is_better', label: 'Higher is better' },
  { value: 'lower_is_better', label: 'Lower is better' },
]
const FREQUENCIES = ['Monthly', 'Quarterly', 'Annual', 'Continuous']

const emptyForm = { name: '', description: '', metric_type: 'KPI', target_value: '', current_value: '', unit: '%', direction: 'higher_is_better', frequency: 'Quarterly', objective_id: '' }

const MetricsPage: React.FC = () => {
  const navigate = useNavigate()
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [objectives, setObjectives] = useState<Objective[]>([])
  const [loading, setLoading] = useState(true)
  const [metricType, setMetricType] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (metricType) params.metric_type = metricType
    if (search) params.search = search
    getMetrics(params).then((r) => setMetrics(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [metricType, search])
  useEffect(() => { getObjectives().then((r) => setObjectives(r.data)).catch(() => {}) }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload = {
      ...form,
      target_value: form.target_value === '' ? null : Number(form.target_value),
      current_value: form.current_value === '' ? null : Number(form.current_value),
      objective_id: form.objective_id || null,
    }
    await createMetric(payload)
    setShowForm(false)
    setForm(emptyForm)
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Metrics — KPI / KRI / KCI</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{metrics.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Metric'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Key Performance / Risk / Control Indicators (ISO/IEC 27001:2022 Clause 9.1). Each compares target vs. current and yields a RAG status.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Name</label><input required className="input-field" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.metric_type} onChange={(e) => setForm({ ...form, metric_type: e.target.value })}>
                {TYPES.map((t) => <option key={t}>{t}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Linked Objective</label>
              <select className="select-field w-full" value={form.objective_id} onChange={(e) => setForm({ ...form, objective_id: e.target.value })}>
                <option value="">— none —</option>
                {objectives.map((o) => <option key={o.id} value={o.id}>{o.ref_id} · {o.title}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Target</label><input type="number" step="any" className="input-field" value={form.target_value} onChange={(e) => setForm({ ...form, target_value: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Current</label><input type="number" step="any" className="input-field" value={form.current_value} onChange={(e) => setForm({ ...form, current_value: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Unit</label><input className="input-field" value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Direction</label>
              <select className="select-field w-full" value={form.direction} onChange={(e) => setForm({ ...form, direction: e.target.value })}>
                {DIRECTIONS.map((d) => <option key={d.value} value={d.value}>{d.label}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Frequency</label>
              <select className="select-field w-full" value={form.frequency} onChange={(e) => setForm({ ...form, frequency: e.target.value })}>
                {FREQUENCIES.map((f) => <option key={f}>{f}</option>)}
              </select>
            </div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><input className="input-field" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Metric</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={metricType} onChange={(e) => setMetricType(e.target.value)}>
          <option value="">All Types</option>
          {TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
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
              <th className="table-header">Target</th>
              <th className="table-header">Current</th>
              <th className="table-header">Status</th>
              <th className="table-header">Frequency</th>
            </tr></thead>
            <tbody>
              {metrics.map((m) => (
                <tr key={m.id} onClick={() => navigate(`/metrics/${m.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{m.ref_id}</td>
                  <td className="table-cell">{m.name}</td>
                  <td className="table-cell text-gray-500">{m.metric_type}</td>
                  <td className="table-cell text-gray-600">{m.target_value ?? '—'}{m.unit ? ` ${m.unit}` : ''}</td>
                  <td className="table-cell text-gray-600">{m.current_value ?? '—'}{m.unit ? ` ${m.unit}` : ''}</td>
                  <td className="table-cell"><StatusBadge value={m.rag} /></td>
                  <td className="table-cell text-gray-400">{m.frequency || '—'}</td>
                </tr>
              ))}
              {metrics.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No metrics yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default MetricsPage

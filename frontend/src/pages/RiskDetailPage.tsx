import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getRisk, updateRisk, getControls, linkRiskControl, unlinkRiskControl, getIncidents } from '../services/api'
import type { Risk, Control, Incident } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Open', 'In Treatment', 'Closed', 'Accepted']
const TREATMENTS = ['Mitigate', 'Accept', 'Transfer', 'Avoid']

const RiskDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [risk, setRisk] = useState<Risk | null>(null)
  const [allControls, setAllControls] = useState<Control[]>([])
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [addCtrl, setAddCtrl] = useState('')
  const [form, setForm] = useState({ status: '', treatment: '', treatment_plan: '', residual_likelihood: '', residual_impact: '', review_date: '' })

  const reload = () => { if (id) getRisk(id).then((r) => setRisk(r.data)).catch(() => navigate('/risks')) }

  useEffect(() => {
    if (!id) return
    getRisk(id).then((r) => {
      const d = r.data
      setRisk(d)
      setForm({
        status: d.status, treatment: d.treatment, treatment_plan: d.treatment_plan || '',
        residual_likelihood: d.residual_likelihood?.toString() ?? '', residual_impact: d.residual_impact?.toString() ?? '',
        review_date: d.review_date || '',
      })
    }).catch(() => navigate('/risks'))
    getControls().then((r) => setAllControls(r.data)).catch(() => {})
    getIncidents({ risk_id: id }).then((r) => setIncidents(r.data)).catch(() => {})
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const payload: Record<string, unknown> = {
        status: form.status, treatment: form.treatment, treatment_plan: form.treatment_plan,
        review_date: form.review_date || null,
        residual_likelihood: form.residual_likelihood === '' ? null : Number(form.residual_likelihood),
        residual_impact: form.residual_impact === '' ? null : Number(form.residual_impact),
      }
      const res = await updateRisk(id, payload)
      setRisk(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  const link = async () => {
    if (!id || !addCtrl) return
    await linkRiskControl(id, addCtrl)
    setAddCtrl('')
    reload()
  }
  const unlink = async (controlId: string) => {
    if (!id) return
    await unlinkRiskControl(id, controlId)
    reload()
  }

  if (!risk) return <div className="p-8 text-gray-400">Loading...</div>
  const linkedIds = new Set(risk.controls.map((c) => c.id))
  const available = allControls.filter((c) => !linkedIds.has(c.id))

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/risks')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Risk Register
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{risk.ref_id} · {risk.category}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{risk.title}</h1>
            <div className="flex items-center flex-wrap gap-2 mt-2">
              <StatusBadge value={risk.inherent_risk_level} />
              <StatusBadge value={risk.treatment} />
              <StatusBadge value={risk.status} />
              <span className="text-xs text-gray-500">Inherent L×I: {risk.likelihood}×{risk.impact}</span>
              {risk.residual_risk_level && <span className="text-xs text-gray-500">· Residual: {risk.residual_risk_level}</span>}
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3><p className="text-gray-700 whitespace-pre-wrap">{risk.description}</p></div>

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>{STATUSES.map((s) => <option key={s}>{s}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Treatment</label>
                  <select className="select-field w-full" value={form.treatment} onChange={(e) => setForm({ ...form, treatment: e.target.value })}>{TREATMENTS.map((t) => <option key={t}>{t}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Review Date</label><input type="date" className="input-field" value={form.review_date} onChange={(e) => setForm({ ...form, review_date: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Residual Likelihood (1-5)</label><input type="number" min={1} max={5} className="input-field" value={form.residual_likelihood} onChange={(e) => setForm({ ...form, residual_likelihood: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Residual Impact (1-5)</label><input type="number" min={1} max={5} className="input-field" value={form.residual_impact} onChange={(e) => setForm({ ...form, residual_impact: e.target.value })} /></div>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Treatment Plan</label><textarea className="input-field h-24" value={form.treatment_plan} onChange={(e) => setForm({ ...form, treatment_plan: e.target.value })} /></div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <>
              {risk.treatment_plan && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Treatment Plan</h3><p className="text-gray-700 whitespace-pre-wrap">{risk.treatment_plan}</p></div>}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 border-t pt-6">
                <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{risk.owner?.full_name || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Residual L×I</span><p className="font-medium">{risk.residual_likelihood ?? '—'}{risk.residual_impact ? ` × ${risk.residual_impact}` : ''}</p></div>
                <div><span className="text-sm text-gray-500">Review Date</span><p className="font-medium">{risk.review_date || '—'}</p></div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Mitigating controls */}
      <div className="card">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Mitigating Controls</h3>
        <div className="flex gap-2 mb-4">
          <select className="select-field flex-1" value={addCtrl} onChange={(e) => setAddCtrl(e.target.value)}>
            <option value="">Select a control to link…</option>
            {available.map((c) => <option key={c.id} value={c.id}>{c.clause} · {c.title}</option>)}
          </select>
          <button onClick={link} disabled={!addCtrl} className="btn-secondary">+ Link control</button>
        </div>
        <div className="flex flex-wrap gap-2">
          {risk.controls.map((c) => (
            <span key={c.id} className="inline-flex items-center gap-2 bg-gray-100 text-gray-700 text-xs font-medium px-2.5 py-1 rounded-full">
              <button onClick={() => navigate(`/controls/${c.id}`)} className="hover:text-indigo-600">{c.clause} · {c.title}</button>
              <button onClick={() => unlink(c.id)} className="text-gray-400 hover:text-red-600" title="Unlink">✕</button>
            </span>
          ))}
          {risk.controls.length === 0 && <span className="text-sm text-gray-400">No controls linked yet.</span>}
        </div>
      </div>

      {/* Related incidents */}
      <div className="card p-0 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100"><h3 className="text-sm font-semibold text-gray-700">Related Incidents</h3></div>
        <table className="w-full">
          <thead><tr className="bg-gray-50 border-b border-gray-200">
            <th className="table-header">Ref</th><th className="table-header">Title</th><th className="table-header">Severity</th><th className="table-header">Status</th>
          </tr></thead>
          <tbody>
            {incidents.map((i) => (
              <tr key={i.id} onClick={() => navigate(`/incidents/${i.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer">
                <td className="table-cell font-mono font-semibold text-indigo-600">{i.ref_id}</td>
                <td className="table-cell">{i.title}</td>
                <td className="table-cell"><StatusBadge value={i.severity} /></td>
                <td className="table-cell"><StatusBadge value={i.status} /></td>
              </tr>
            ))}
            {incidents.length === 0 && <tr><td colSpan={4} className="table-cell text-center text-gray-400 py-8">No incidents linked to this risk.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default RiskDetailPage

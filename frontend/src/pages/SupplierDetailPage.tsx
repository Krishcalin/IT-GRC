import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getSupplier, updateSupplier } from '../services/api'
import type { Supplier } from '../types'
import StatusBadge from '../components/StatusBadge'

const CATEGORIES = ['Product', 'Service', 'ICT Supply Chain', 'Cloud Service']
const CRITICALITIES = ['Low', 'Medium', 'High', 'Critical']
const CLASSIFICATIONS = ['Public', 'Internal', 'Confidential', 'Restricted']
const STATUSES = ['Active', 'Onboarding', 'Under Review', 'Offboarded']

const Flag: React.FC<{ on: boolean; label: string }> = ({ on, label }) => (
  <span className={`inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full ${on ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-500'}`}>
    {on ? '✓' : '—'} {label}
  </span>
)

const SupplierDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [s, setS] = useState<Supplier | null>(null)
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState({
    category: '', criticality: '', data_classification: '', status: '', certifications: '',
    service_description: '', description: '', notes: '',
    is_requirements_agreed: false, right_to_audit: false, processes_pii: false,
    contract_start: '', contract_end: '', last_review_date: '', next_review_date: '',
  })

  useEffect(() => {
    if (!id) return
    getSupplier(id).then((r) => {
      const d = r.data
      setS(d)
      setForm({
        category: d.category, criticality: d.criticality, data_classification: d.data_classification, status: d.status,
        certifications: d.certifications || '', service_description: d.service_description || '', description: d.description || '', notes: d.notes || '',
        is_requirements_agreed: d.is_requirements_agreed, right_to_audit: d.right_to_audit, processes_pii: d.processes_pii,
        contract_start: d.contract_start || '', contract_end: d.contract_end || '',
        last_review_date: d.last_review_date || '', next_review_date: d.next_review_date || '',
      })
    }).catch(() => navigate('/suppliers'))
  }, [id, navigate])

  const handleSave = async () => {
    if (!id) return
    setSaving(true)
    try {
      const res = await updateSupplier(id, form)
      setS(res.data)
      setEditing(false)
    } catch { /* ignore */ }
    setSaving(false)
  }

  if (!s) return <div className="p-8 text-gray-400">Loading...</div>

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/suppliers')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Suppliers
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{s.ref_id} · {s.category}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{s.name}</h1>
            <div className="flex items-center flex-wrap gap-2 mt-2">
              <StatusBadge value={s.status} />
              <StatusBadge value={s.criticality} />
              <StatusBadge value={s.data_classification} />
            </div>
          </div>
          <button onClick={() => setEditing(!editing)} className="btn-secondary">{editing ? 'Cancel' : 'Edit'}</button>
        </div>

        <div className="space-y-6">
          {s.service_description && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Service</h3><p className="text-gray-700">{s.service_description}</p></div>}
          {s.description && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h3><p className="text-gray-700 whitespace-pre-wrap">{s.description}</p></div>}

          {editing ? (
            <div className="space-y-4 border-t pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  <select className="select-field w-full" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>{CATEGORIES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Criticality</label>
                  <select className="select-field w-full" value={form.criticality} onChange={(e) => setForm({ ...form, criticality: e.target.value })}>{CRITICALITIES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Data Classification</label>
                  <select className="select-field w-full" value={form.data_classification} onChange={(e) => setForm({ ...form, data_classification: e.target.value })}>{CLASSIFICATIONS.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select className="select-field w-full" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>{STATUSES.map((c) => <option key={c}>{c}</option>)}</select></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Certifications</label><input className="input-field" value={form.certifications} onChange={(e) => setForm({ ...form, certifications: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Contract Start</label><input type="date" className="input-field" value={form.contract_start} onChange={(e) => setForm({ ...form, contract_start: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Contract End</label><input type="date" className="input-field" value={form.contract_end} onChange={(e) => setForm({ ...form, contract_end: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Last Review</label><input type="date" className="input-field" value={form.last_review_date} onChange={(e) => setForm({ ...form, last_review_date: e.target.value })} /></div>
                <div><label className="block text-sm font-medium text-gray-700 mb-1">Next Review</label><input type="date" className="input-field" value={form.next_review_date} onChange={(e) => setForm({ ...form, next_review_date: e.target.value })} /></div>
              </div>
              <div className="flex flex-wrap gap-6">
                <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.is_requirements_agreed} onChange={(e) => setForm({ ...form, is_requirements_agreed: e.target.checked })} /> IS requirements agreed (5.20)</label>
                <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.right_to_audit} onChange={(e) => setForm({ ...form, right_to_audit: e.target.checked })} /> Right to audit</label>
                <label className="flex items-center gap-2 text-sm text-gray-700"><input type="checkbox" checked={form.processes_pii} onChange={(e) => setForm({ ...form, processes_pii: e.target.checked })} /> Processes PII</label>
              </div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Service Description</label><input className="input-field" value={form.service_description} onChange={(e) => setForm({ ...form, service_description: e.target.value })} /></div>
              <div><label className="block text-sm font-medium text-gray-700 mb-1">Notes</label><textarea className="input-field h-24" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></div>
              <button onClick={handleSave} disabled={saving} className="btn-primary">{saving ? 'Saving...' : 'Save Changes'}</button>
            </div>
          ) : (
            <>
              <div className="flex flex-wrap gap-2 border-t pt-6">
                <Flag on={s.is_requirements_agreed} label="IS requirements agreed" />
                <Flag on={s.right_to_audit} label="Right to audit" />
                <Flag on={s.processes_pii} label="Processes PII" />
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium">{s.owner?.full_name || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Certifications</span><p className="font-medium">{s.certifications || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Contract</span><p className="font-medium">{s.contract_start || '—'} → {s.contract_end || '—'}</p></div>
                <div><span className="text-sm text-gray-500">Next Review</span><p className="font-medium">{s.next_review_date || '—'}</p></div>
              </div>
              {s.notes && <div><h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Notes</h3><p className="text-gray-700 whitespace-pre-wrap">{s.notes}</p></div>}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default SupplierDetailPage

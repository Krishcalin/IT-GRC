import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAssessments, createAssessment } from '../services/api'
import type { AssessmentSummary } from '../types'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['Control Self-Assessment', 'Maturity Assessment', 'Vendor Questionnaire']
const STATUSES = ['Draft', 'In Progress', 'Submitted', 'Reviewed', 'Closed']
const FRAMEWORKS = ['', 'ISO 27001:2022', 'ISO 27019:2024', 'NIST CSF 2.0', 'SOC 2']

const emptyForm = { title: '', assessment_type: 'Control Self-Assessment', framework: '', status: 'Draft', description: '' }

const AssessmentsPage: React.FC = () => {
  const navigate = useNavigate()
  const [rows, setRows] = useState<AssessmentSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [assessmentType, setAssessmentType] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = () => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (assessmentType) params.assessment_type = assessmentType
    if (status) params.status = status
    if (search) params.search = search
    getAssessments(params).then((r) => setRows(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [assessmentType, status, search])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload: Record<string, unknown> = { ...form }
    if (!payload.framework) delete payload.framework
    const r = await createAssessment(payload)
    setShowForm(false); setForm(emptyForm)
    navigate(`/assessments/${r.data.id}`)
  }

  const scoreColor = (s: number) => (s >= 80 ? 'text-emerald-600' : s >= 50 ? 'text-amber-600' : 'text-red-600')

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Assessments &amp; Questionnaires</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{rows.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Assessment'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Control self-assessments with CMMI maturity scoring and vendor security questionnaires — with derived scores and progress.
      </p>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.assessment_type} onChange={(e) => setForm({ ...form, assessment_type: e.target.value })}>{TYPES.map((t) => <option key={t}>{t}</option>)}</select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Framework (for control assessments)</label>
              <select className="select-field w-full" value={form.framework} onChange={(e) => setForm({ ...form, framework: e.target.value })}>
                {FRAMEWORKS.map((f) => <option key={f} value={f}>{f || '—'}</option>)}
              </select>
            </div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          </div>
          <button type="submit" className="btn-primary">Create &amp; Open</button>
        </form>
      )}

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={assessmentType} onChange={(e) => setAssessmentType(e.target.value)}><option value="">All Types</option>{TYPES.map((t) => <option key={t} value={t}>{t}</option>)}</select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}><option value="">All Statuses</option>{STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}</select>
        <input className="input-field max-w-xs" placeholder="Search ref or title..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref</th>
              <th className="table-header">Title</th>
              <th className="table-header">Type</th>
              <th className="table-header">Framework</th>
              <th className="table-header">Progress</th>
              <th className="table-header">Score</th>
              <th className="table-header">Status</th>
            </tr></thead>
            <tbody>
              {rows.map((a) => (
                <tr key={a.id} onClick={() => navigate(`/assessments/${a.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{a.ref_id}</td>
                  <td className="table-cell">{a.title}</td>
                  <td className="table-cell text-gray-500 text-sm">{a.assessment_type}</td>
                  <td className="table-cell text-gray-500 text-sm">{a.framework || '—'}</td>
                  <td className="table-cell text-gray-500 text-sm">{a.answered_count}/{a.item_count}</td>
                  <td className="table-cell"><span className={`font-semibold ${scoreColor(a.score)}`}>{a.score}%</span></td>
                  <td className="table-cell"><StatusBadge value={a.status} /></td>
                </tr>
              ))}
              {rows.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No assessments yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default AssessmentsPage

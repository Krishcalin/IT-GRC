import React, { useEffect, useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getAssessment, updateAssessment, populateAssessment, addAssessmentItem, updateAssessmentItem, deleteAssessmentItem } from '../services/api'
import type { Assessment, AssessmentItem } from '../types'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['Draft', 'In Progress', 'Submitted', 'Reviewed', 'Closed']
const MATURITY = [
  { v: '', l: '—' }, { v: '0', l: '0 · None' }, { v: '1', l: '1 · Initial' }, { v: '2', l: '2 · Managed' },
  { v: '3', l: '3 · Defined' }, { v: '4', l: '4 · Quant. Managed' }, { v: '5', l: '5 · Optimizing' },
]
const RESULTS = ['', 'Compliant', 'Partial', 'Non-Compliant', 'N/A', 'Yes', 'No']

const AssessmentDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [a, setA] = useState<Assessment | null>(null)
  const [newQuestion, setNewQuestion] = useState('')
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    if (!id) return
    getAssessment(id).then((r) => setA(r.data)).catch(() => navigate('/assessments'))
  }, [id, navigate])
  useEffect(() => { load() }, [load])

  const setStatus = async (status: string) => { if (id) { await updateAssessment(id, { status }); load() } }
  const saveItem = async (item: AssessmentItem, patch: Partial<AssessmentItem>) => {
    if (!id) return
    await updateAssessmentItem(id, item.id, patch); load()
  }
  const removeItem = async (itemId: string) => { if (id) { await deleteAssessmentItem(id, itemId); load() } }
  const addQuestion = async () => {
    if (!id || !newQuestion.trim()) return
    await addAssessmentItem(id, { question: newQuestion.trim() }); setNewQuestion(''); load()
  }
  const populate = async () => {
    if (!id) return
    setBusy(true)
    try { await populateAssessment(id) } catch { /* needs framework */ }
    setBusy(false); load()
  }

  if (!a) return <div className="p-8 text-gray-400">Loading...</div>
  const scoreColor = a.score >= 80 ? 'text-emerald-600' : a.score >= 50 ? 'text-amber-600' : 'text-red-600'
  const isQuestionnaire = a.assessment_type === 'Vendor Questionnaire'

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/assessments')} className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to Assessments
      </button>

      <div className="card">
        <div className="flex items-start justify-between">
          <div>
            <span className="text-sm font-mono font-semibold text-indigo-600">{a.ref_id} · {a.assessment_type}{a.framework ? ` · ${a.framework}` : ''}</span>
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{a.title}</h1>
            {a.description && <p className="text-gray-600 mt-1 text-sm">{a.description}</p>}
          </div>
          <select className="select-field" value={a.status} onChange={(e) => setStatus(e.target.value)}>
            {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 border-t pt-6">
          <div><span className="text-sm text-gray-500">Score</span><p className={`text-2xl font-bold ${scoreColor}`}>{a.score}%</p></div>
          <div><span className="text-sm text-gray-500">Avg Maturity</span><p className="text-2xl font-bold text-gray-700">{a.avg_maturity ?? '—'}{a.avg_maturity != null ? '/5' : ''}</p></div>
          <div><span className="text-sm text-gray-500">Progress</span><p className="text-2xl font-bold text-gray-700">{a.answered_count}/{a.item_count}</p></div>
          <div><span className="text-sm text-gray-500">Owner</span><p className="font-medium pt-1">{a.owner?.full_name || '—'}</p></div>
        </div>
      </div>

      <div className="card p-0 overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b border-gray-100">
          <h3 className="text-sm font-semibold text-gray-700">Items ({a.item_count})</h3>
          {a.framework && !isQuestionnaire && (
            <button onClick={populate} disabled={busy} className="btn-secondary text-sm">{busy ? 'Adding…' : `Populate from ${a.framework}`}</button>
          )}
        </div>
        <table className="w-full">
          <thead><tr className="bg-gray-50 border-b border-gray-200">
            <th className="table-header">{isQuestionnaire ? 'Question' : 'Control'}</th>
            {!isQuestionnaire && <th className="table-header">Maturity</th>}
            <th className="table-header">Result</th>
            <th className="table-header">Comment</th>
            <th className="table-header"></th>
          </tr></thead>
          <tbody>
            {a.items.map((it) => (
              <tr key={it.id} className="border-b border-gray-100 align-top">
                <td className="table-cell">
                  {it.control ? (
                    <span><span className="font-mono text-indigo-600 cursor-pointer hover:underline" onClick={() => navigate(`/controls/${it.control!.id}`)}>{it.control.clause}</span> <span className="text-gray-700">{it.control.title}</span></span>
                  ) : <span className="text-gray-700">{it.question}</span>}
                </td>
                {!isQuestionnaire && (
                  <td className="table-cell">
                    <select className="select-field text-xs py-1" value={it.maturity ?? ''} onChange={(e) => saveItem(it, { maturity: e.target.value === '' ? null : Number(e.target.value) })}>
                      {MATURITY.map((m) => <option key={m.v} value={m.v}>{m.l}</option>)}
                    </select>
                  </td>
                )}
                <td className="table-cell">
                  <select className="select-field text-xs py-1" value={it.result ?? ''} onChange={(e) => saveItem(it, { result: e.target.value || null })}>
                    {RESULTS.map((r) => <option key={r} value={r}>{r || '—'}</option>)}
                  </select>
                </td>
                <td className="table-cell">
                  <input className="input-field text-xs py-1 w-full" defaultValue={it.comment ?? ''} onBlur={(e) => { if (e.target.value !== (it.comment ?? '')) saveItem(it, { comment: e.target.value }) }} placeholder="Add comment…" />
                </td>
                <td className="table-cell text-right"><button onClick={() => removeItem(it.id)} className="text-xs text-gray-400 hover:text-red-600">Remove</button></td>
              </tr>
            ))}
            {a.items.length === 0 && <tr><td colSpan={isQuestionnaire ? 4 : 5} className="table-cell text-center text-gray-400 py-10">No items yet{a.framework && !isQuestionnaire ? ' — use “Populate from framework”.' : ''}</td></tr>}
          </tbody>
        </table>
        <div className="flex items-center gap-3 p-4 border-t border-gray-100">
          <input className="input-field flex-1" placeholder={isQuestionnaire ? 'Add a question…' : 'Add a custom item / question…'} value={newQuestion} onChange={(e) => setNewQuestion(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') addQuestion() }} />
          <button onClick={addQuestion} disabled={!newQuestion.trim()} className="btn-primary disabled:opacity-50">Add Item</button>
        </div>
      </div>
    </div>
  )
}

export default AssessmentDetailPage

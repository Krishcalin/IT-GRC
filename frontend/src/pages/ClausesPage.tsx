import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getClauses } from '../services/api'
import type { ClauseRequirement } from '../types'
import StatusBadge from '../components/StatusBadge'

const SECTIONS = [
  'Context of the organization',
  'Leadership',
  'Planning',
  'Support',
  'Operation',
  'Performance evaluation',
  'Improvement',
]
const STATUSES = ['Not Assessed', 'In Progress', 'Partially Conformant', 'Conformant', 'Nonconformant']

const ClausesPage: React.FC = () => {
  const navigate = useNavigate()
  const [clauses, setClauses] = useState<ClauseRequirement[]>([])
  const [loading, setLoading] = useState(true)
  const [section, setSection] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (section) params.section = section
    if (status) params.status = status
    if (search) params.search = search
    getClauses(params)
      .then((r) => setClauses(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [section, status, search])

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">ISMS Clauses (4–10)</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{clauses.length}</span>
        </div>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Mandatory ISO/IEC 27001:2022 management-system requirements. Unlike Annex A controls, these clauses cannot be excluded when claiming conformity.
      </p>

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={section} onChange={(e) => setSection(e.target.value)}>
          <option value="">All Sections</option>
          {SECTIONS.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Conformity</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <input className="input-field max-w-xs" placeholder="Search clause or title..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-400">Loading...</div>
        ) : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Clause</th>
              <th className="table-header">Title</th>
              <th className="table-header">Section</th>
              <th className="table-header">Conformity</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {clauses.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/clauses/${c.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{c.clause}</td>
                  <td className="table-cell">{c.title}</td>
                  <td className="table-cell text-gray-500">{c.section}</td>
                  <td className="table-cell"><StatusBadge value={c.conformity_status} /></td>
                  <td className="table-cell text-gray-400">{c.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {clauses.length === 0 && <tr><td colSpan={5} className="table-cell text-center text-gray-400 py-12">No clauses found</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default ClausesPage

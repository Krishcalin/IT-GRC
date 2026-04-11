import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getControls } from '../services/api'
import type { Control } from '../types'
import StatusBadge from '../components/StatusBadge'

const THEMES = ['', 'Organizational', 'People', 'Physical', 'Technological']
const STATUSES = ['', 'Not Started', 'In Progress', 'Implemented', 'Not Applicable']

const ControlsPage: React.FC = () => {
  const navigate = useNavigate()
  const [controls, setControls] = useState<Control[]>([])
  const [loading, setLoading] = useState(true)
  const [theme, setTheme] = useState('')
  const [status, setStatus] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (theme) params.theme = theme
    if (status) params.status = status
    if (search) params.search = search
    getControls(params)
      .then((r) => setControls(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [theme, status, search])

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">ISO 27001:2022 Controls</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{controls.length}</span>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        <select className="select-field" value={theme} onChange={(e) => setTheme(e.target.value)}>
          <option value="">All Themes</option>
          {THEMES.filter(Boolean).map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {STATUSES.filter(Boolean).map((s) => <option key={s} value={s}>{s}</option>)}
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
              <th className="table-header">Theme</th>
              <th className="table-header">Status</th>
              <th className="table-header">Owner</th>
            </tr></thead>
            <tbody>
              {controls.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/controls/${c.id}`)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{c.clause}</td>
                  <td className="table-cell">{c.title}</td>
                  <td className="table-cell"><StatusBadge value={c.theme} /></td>
                  <td className="table-cell"><StatusBadge value={c.status} /></td>
                  <td className="table-cell text-gray-400">{c.owner?.full_name || '—'}</td>
                </tr>
              ))}
              {controls.length === 0 && <tr><td colSpan={5} className="table-cell text-center text-gray-400 py-12">No controls found</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default ControlsPage

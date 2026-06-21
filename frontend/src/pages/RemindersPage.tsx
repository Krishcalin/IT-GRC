import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getReminders } from '../services/api'
import type { RemindersResult } from '../types'

const WINDOWS = [
  { value: '7', label: 'Next 7 days' },
  { value: '30', label: 'Next 30 days' },
  { value: '90', label: 'Next 90 days' },
]

const RemindersPage: React.FC = () => {
  const navigate = useNavigate()
  const [data, setData] = useState<RemindersResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [windowDays, setWindowDays] = useState('30')

  useEffect(() => {
    setLoading(true)
    getReminders({ window_days: windowDays })
      .then((r) => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [windowDays])

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Reminders</h1>
        <select className="select-field" value={windowDays} onChange={(e) => setWindowDays(e.target.value)}>
          {WINDOWS.map((w) => <option key={w.value} value={w.value}>{w.label}</option>)}
        </select>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Reviews and renewals that are overdue or coming due across controls, clauses, documents, suppliers, policies, risks, and objectives.
      </p>

      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="card"><p className="text-sm font-medium text-gray-500">Overdue</p><p className="text-3xl font-bold mt-1 text-red-600">{data.overdue_count}</p></div>
          <div className="card"><p className="text-sm font-medium text-gray-500">Upcoming (within window)</p><p className="text-3xl font-bold mt-1 text-amber-600">{data.upcoming_count}</p></div>
        </div>
      )}

      <div className="card p-0 overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-gray-400">Loading...</div>
        ) : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Status</th>
              <th className="table-header">Category</th>
              <th className="table-header">Ref</th>
              <th className="table-header">Title</th>
              <th className="table-header">Due Date</th>
            </tr></thead>
            <tbody>
              {(data?.items || []).map((it, idx) => (
                <tr key={idx} onClick={() => navigate(it.link)} className="border-b border-gray-100 hover:bg-indigo-50/50 cursor-pointer transition-colors">
                  <td className="table-cell">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${it.kind === 'overdue' ? 'bg-red-100 text-red-800' : 'bg-amber-100 text-amber-800'}`}>
                      {it.kind === 'overdue' ? 'Overdue' : 'Upcoming'}
                    </span>
                  </td>
                  <td className="table-cell text-gray-500">{it.category}</td>
                  <td className="table-cell font-mono font-semibold text-indigo-600">{it.ref_id}</td>
                  <td className="table-cell">{it.title}</td>
                  <td className="table-cell text-gray-600">{it.due_date}</td>
                </tr>
              ))}
              {(!data || data.items.length === 0) && <tr><td colSpan={5} className="table-cell text-center text-gray-400 py-12">Nothing due — set review dates on controls, documents, suppliers, etc. to see reminders here.</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default RemindersPage

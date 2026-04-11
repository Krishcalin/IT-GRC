import React, { useEffect, useState } from 'react'
import { getSoaEntries, getControls, createSoaEntry, updateSoaEntry } from '../services/api'
import type { SoAEntry, Control } from '../types'
import StatusBadge from '../components/StatusBadge'

const IMPL_STATUSES = ['Not Implemented', 'Partially Implemented', 'Fully Implemented', 'N/A']

const SoAPage: React.FC = () => {
  const [entries, setEntries] = useState<SoAEntry[]>([])
  const [controls, setControls] = useState<Control[]>([])
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const [s, c] = await Promise.all([getSoaEntries({ limit: '200' }), getControls({ limit: '200' })])
      setEntries(s.data)
      setControls(c.data)
    } catch { /* ignore */ }
    setLoading(false)
  }
  useEffect(() => { load() }, [])

  const mapped = new Set(entries.map((e) => e.control_id))
  const unmapped = controls.filter((c) => !mapped.has(c.id))
  const applicable = entries.filter((e) => e.applicable).length
  const fullyImpl = entries.filter((e) => e.implementation_status === 'Fully Implemented').length

  const handleInit = async (controlId: string) => {
    await createSoaEntry({ control_id: controlId, applicable: true, implementation_status: 'Not Implemented' })
    load()
  }

  const handleToggle = async (entry: SoAEntry, field: string, value: unknown) => {
    await updateSoaEntry(entry.id, { [field]: value })
    load()
  }

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Statement of Applicability</h1>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card text-center"><p className="text-sm text-gray-500">Total Entries</p><p className="text-2xl font-bold text-indigo-600">{entries.length}</p></div>
        <div className="card text-center"><p className="text-sm text-gray-500">Applicable</p><p className="text-2xl font-bold text-emerald-600">{applicable}</p></div>
        <div className="card text-center"><p className="text-sm text-gray-500">Fully Implemented</p><p className="text-2xl font-bold text-blue-600">{fullyImpl}</p></div>
      </div>

      {unmapped.length > 0 && (
        <div className="card bg-amber-50 border-amber-200">
          <p className="text-sm font-medium text-amber-800 mb-2">{unmapped.length} controls have no SoA entry</p>
          <div className="flex flex-wrap gap-2">
            {unmapped.slice(0, 10).map((c) => (
              <button key={c.id} onClick={() => handleInit(c.id)} className="text-xs bg-white border border-amber-300 rounded px-2 py-1 hover:bg-amber-100">{c.clause}</button>
            ))}
            {unmapped.length > 10 && <span className="text-xs text-amber-600 py-1">+{unmapped.length - 10} more</span>}
          </div>
        </div>
      )}

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Clause</th>
              <th className="table-header">Title</th>
              <th className="table-header">Applicable</th>
              <th className="table-header">Implementation Status</th>
              <th className="table-header">Justification</th>
            </tr></thead>
            <tbody>
              {entries.map((e) => (
                <tr key={e.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{e.control.clause}</td>
                  <td className="table-cell">{e.control.title}</td>
                  <td className="table-cell">
                    <button onClick={() => handleToggle(e, 'applicable', !e.applicable)} className={`w-5 h-5 rounded border-2 flex items-center justify-center ${e.applicable ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-gray-300'}`}>
                      {e.applicable && <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>}
                    </button>
                  </td>
                  <td className="table-cell">
                    <select className="select-field text-xs" value={e.implementation_status} onChange={(ev) => handleToggle(e, 'implementation_status', ev.target.value)}>
                      {IMPL_STATUSES.map((s) => <option key={s}>{s}</option>)}
                    </select>
                  </td>
                  <td className="table-cell text-gray-400 text-xs">{e.justification || '—'}</td>
                </tr>
              ))}
              {entries.length === 0 && <tr><td colSpan={5} className="table-cell text-center text-gray-400 py-12">No SoA entries yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default SoAPage

import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getFrameworkCoverage } from '../services/api'
import type { FrameworkCoverage } from '../types'

const FrameworksPage: React.FC = () => {
  const navigate = useNavigate()
  const [data, setData] = useState<FrameworkCoverage | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFrameworkCoverage().then((r) => setData(r.data)).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const frameworks = data?.frameworks.map((f) => f.framework) || []
  const cell = (src: string, tgt: string) => data?.matrix.find((m) => m.source === src && m.target === tgt)
  const pctColor = (p: number) => (p >= 60 ? 'text-emerald-600' : p >= 25 ? 'text-amber-600' : 'text-gray-400')
  const bgFor = (p: number) => (p >= 60 ? 'bg-emerald-50' : p >= 25 ? 'bg-amber-50' : '')

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center gap-3">
        <h1 className="text-2xl font-bold text-gray-900">Frameworks &amp; Crosswalk Coverage</h1>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Unified control framework — map one control set across multiple standards ("test once, comply many") and see cross-framework coverage.
      </p>

      {loading ? <div className="card text-center text-gray-400 py-8">Loading…</div> : !data ? null : (
        <>
          {/* Per-framework summary */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {data.frameworks.map((f) => (
              <button key={f.framework} onClick={() => navigate(`/controls?framework=${encodeURIComponent(f.framework)}`)} className="card text-left hover:bg-indigo-50/50 transition-colors">
                <p className="text-sm font-semibold text-gray-800">{f.framework}</p>
                <p className="text-3xl font-bold text-indigo-600 mt-1">{f.total}</p>
                <p className="text-xs text-gray-500 mt-1">{f.mapped_any} mapped to other frameworks ({f.coverage_pct}%)</p>
              </button>
            ))}
          </div>

          {/* Coverage matrix */}
          <div className="card p-0 overflow-x-auto">
            <div className="p-4 border-b border-gray-100">
              <h3 className="text-sm font-semibold text-gray-700">Cross-Framework Coverage Matrix</h3>
              <p className="text-xs text-gray-400 mt-1">Each cell: % (and count) of the <em>row</em> framework's controls mapped to the <em>column</em> framework.</p>
            </div>
            <table className="w-full">
              <thead><tr className="bg-gray-50 border-b border-gray-200">
                <th className="table-header">From ↓ / To →</th>
                {frameworks.map((f) => <th key={f} className="table-header">{f}</th>)}
              </tr></thead>
              <tbody>
                {frameworks.map((src) => (
                  <tr key={src} className="border-b border-gray-100">
                    <td className="table-cell font-semibold text-gray-700">{src}</td>
                    {frameworks.map((tgt) => {
                      if (src === tgt) return <td key={tgt} className="table-cell text-center text-gray-300">—</td>
                      const c = cell(src, tgt)
                      const pct = c?.coverage_pct ?? 0
                      return (
                        <td key={tgt} className={`table-cell text-center ${bgFor(pct)}`}>
                          <span className={`font-semibold ${pctColor(pct)}`}>{pct}%</span>
                          <span className="block text-[11px] text-gray-400">{c?.mapped ?? 0}/{c?.total ?? 0}</span>
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-xs text-gray-400">Add or edit mappings from any control's detail page (Framework Crosswalk section).</p>
        </>
      )}
    </div>
  )
}

export default FrameworksPage

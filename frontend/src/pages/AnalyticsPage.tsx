import React, { useEffect, useState, useCallback } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts'
import { getRiskHeatmap, getPostureTrend, captureSnapshot } from '../services/api'
import type { RiskHeatmap, PostureSnapshot } from '../types'

const LEVEL_BG: Record<string, string> = {
  Critical: 'bg-red-500 text-white',
  High: 'bg-orange-400 text-white',
  Medium: 'bg-amber-300 text-amber-900',
  Low: 'bg-emerald-300 text-emerald-900',
}

const AnalyticsPage: React.FC = () => {
  const [basis, setBasis] = useState<'inherent' | 'residual'>('inherent')
  const [heatmap, setHeatmap] = useState<RiskHeatmap | null>(null)
  const [days, setDays] = useState(180)
  const [trend, setTrend] = useState<PostureSnapshot[]>([])
  const [loading, setLoading] = useState(true)

  const loadHeat = useCallback(() => {
    getRiskHeatmap(basis).then((r) => setHeatmap(r.data)).catch(() => {})
  }, [basis])
  const loadTrend = useCallback(() => {
    getPostureTrend(days).then((r) => setTrend(r.data)).catch(() => {})
  }, [days])

  useEffect(() => { loadHeat() }, [loadHeat])
  useEffect(() => { Promise.resolve(loadTrend()).finally(() => setLoading(false)) }, [loadTrend])

  const snapshotNow = async () => { await captureSnapshot(); loadTrend() }

  const cellAt = (likelihood: number, impact: number) =>
    heatmap?.cells.find((c) => c.likelihood === likelihood && c.impact === impact)

  const trendData = trend.map((s) => ({
    date: s.snapshot_date.slice(5), // MM-DD
    Compliance: s.compliance_score,
    Conformity: s.isms_conformity_score,
    'Doc Readiness': s.document_readiness_score,
    Training: s.training_completion_rate,
  }))

  return (
    <div className="p-8 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <button onClick={snapshotNow} className="btn-secondary text-sm">Capture posture snapshot</button>
      </div>
      <p className="text-sm text-gray-500 -mt-4">Risk heat map and ISMS posture trends for management reporting.</p>

      {/* Risk heat map */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-700">Risk Heat Map (5×5)</h3>
          <div className="flex rounded-lg border border-gray-200 overflow-hidden text-sm">
            {(['inherent', 'residual'] as const).map((b) => (
              <button key={b} onClick={() => setBasis(b)} className={`px-3 py-1.5 capitalize ${basis === b ? 'bg-indigo-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}>{b}</button>
            ))}
          </div>
        </div>
        <div className="flex">
          {/* Y axis label */}
          <div className="flex flex-col justify-center mr-2">
            <span className="text-xs font-semibold text-gray-500 -rotate-90 whitespace-nowrap">Impact →</span>
          </div>
          <div className="flex-1">
            <table className="w-full border-collapse">
              <tbody>
                {[5, 4, 3, 2, 1].map((impact) => (
                  <tr key={impact}>
                    <td className="text-xs font-semibold text-gray-500 pr-2 text-right w-8">{impact}</td>
                    {[1, 2, 3, 4, 5].map((likelihood) => {
                      const cell = cellAt(likelihood, impact)
                      const lvl = cell?.level || 'Low'
                      return (
                        <td key={likelihood} className="p-1">
                          <div className={`rounded-md h-14 flex flex-col items-center justify-center ${LEVEL_BG[lvl]} ${cell && cell.count > 0 ? 'ring-2 ring-gray-800/30' : 'opacity-70'}`}>
                            <span className="text-lg font-bold leading-none">{cell?.count ?? 0}</span>
                            <span className="text-[10px] opacity-80">{lvl}</span>
                          </div>
                        </td>
                      )
                    })}
                  </tr>
                ))}
                <tr>
                  <td></td>
                  {[1, 2, 3, 4, 5].map((l) => <td key={l} className="text-xs font-semibold text-gray-500 text-center pt-1">{l}</td>)}
                </tr>
              </tbody>
            </table>
            <div className="text-xs font-semibold text-gray-500 text-center mt-1">Likelihood →</div>
          </div>
        </div>
        <p className="text-xs text-gray-400 mt-3">
          {heatmap ? `${heatmap.total} risk(s) plotted on a ${basis} basis.` : 'Loading…'} Cell colour = risk level (likelihood × impact); number = risks in that cell.
        </p>
      </div>

      {/* Posture trend */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-700">ISMS Posture Trend</h3>
          <select className="select-field text-sm" value={days} onChange={(e) => setDays(Number(e.target.value))}>
            <option value={90}>Last 90 days</option>
            <option value={180}>Last 180 days</option>
            <option value={365}>Last 365 days</option>
          </select>
        </div>
        {loading ? <p className="text-sm text-gray-400 py-12 text-center">Loading…</p> : trendData.length > 0 ? (
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={trendData} margin={{ top: 8, right: 16, bottom: 0, left: -8 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="Compliance" stroke="#6366f1" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Conformity" stroke="#10b981" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Doc Readiness" stroke="#f59e0b" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="Training" stroke="#0ea5e9" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        ) : <p className="text-sm text-gray-400 py-12 text-center">No snapshots yet — view the dashboard to record today's posture, or capture one above.</p>}
        <p className="text-xs text-gray-400 mt-3">Scores are captured once per day (automatically when the dashboard loads). Trend shows compliance, ISMS conformity, document readiness, and training completion.</p>
      </div>
    </div>
  )
}

export default AnalyticsPage

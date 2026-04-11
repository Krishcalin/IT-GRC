import React, { useEffect, useState } from 'react'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { getDashboardStats, getActivityLog } from '../services/api'
import type { DashboardStats, ActivityEntry } from '../types'

const COLORS = ['#6366f1', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6']

const StatCard: React.FC<{ label: string; value: string | number; color: string }> = ({ label, value, color }) => (
  <div className="card">
    <p className="text-sm font-medium text-gray-500">{label}</p>
    <p className={`text-3xl font-bold mt-1 ${color}`}>{value}</p>
  </div>
)

const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [activity, setActivity] = useState<ActivityEntry[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getDashboardStats(), getActivityLog()])
      .then(([s, a]) => { setStats(s.data); setActivity(a.data.slice(0, 10)) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading || !stats) return <div className="p-8"><div className="animate-pulse space-y-6"><div className="grid grid-cols-4 gap-6">{[1,2,3,4].map(i => <div key={i} className="h-24 bg-gray-200 rounded-xl" />)}</div></div></div>

  const statusData = Object.entries(stats.controls_by_status).map(([name, value]) => ({ name, value }))
  const themeData = Object.entries(stats.controls_by_theme).map(([name, value]) => ({ name, value }))
  const scoreColor = stats.compliance_score >= 80 ? 'text-emerald-600' : stats.compliance_score >= 50 ? 'text-amber-600' : 'text-red-600'

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      {/* Stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="Total Controls" value={stats.total_controls} color="text-indigo-600" />
        <StatCard label="Open Risks" value={stats.open_risks} color="text-amber-600" />
        <StatCard label="Open Findings" value={stats.open_findings} color="text-red-600" />
        <StatCard label="Compliance Score" value={`${stats.compliance_score}%`} color={scoreColor} />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Controls by Status</h3>
          {statusData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={statusData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                  {statusData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
        </div>
        <div className="card">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Controls by Theme</h3>
          {themeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={themeData}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
        </div>
      </div>

      {/* Second row stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard label="Implemented Controls" value={stats.implemented_controls} color="text-emerald-600" />
        <StatCard label="Critical Risks" value={stats.critical_risks} color="text-red-600" />
        <StatCard label="Total Policies" value={stats.total_policies} color="text-blue-600" />
        <StatCard label="Total Assets" value={stats.total_assets} color="text-gray-700" />
      </div>

      {/* Recent activity */}
      <div className="card">
        <h3 className="text-sm font-semibold text-gray-700 mb-4">Recent Activity</h3>
        {activity.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead><tr className="border-b border-gray-200">
                <th className="table-header">Action</th>
                <th className="table-header">Resource</th>
                <th className="table-header">Time</th>
              </tr></thead>
              <tbody>
                {activity.map((a) => (
                  <tr key={a.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="table-cell font-medium">{a.action}</td>
                    <td className="table-cell">{a.resource_type} {a.resource_id?.slice(0, 8)}</td>
                    <td className="table-cell text-gray-400">{a.created_at ? new Date(a.created_at).toLocaleString() : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : <p className="text-sm text-gray-400 text-center py-4">No activity yet</p>}
      </div>
    </div>
  )
}

export default DashboardPage

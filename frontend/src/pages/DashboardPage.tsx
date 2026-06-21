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
  const clauseStatusData = Object.entries(stats.clauses_by_status || {}).map(([name, value]) => ({ name, value }))
  const clauseSectionData = Object.entries(stats.clauses_by_section || {}).map(([name, value]) => ({ name, value }))
  const scoreColor = stats.compliance_score >= 80 ? 'text-emerald-600' : stats.compliance_score >= 50 ? 'text-amber-600' : 'text-red-600'
  const ismsColor = stats.isms_conformity_score >= 80 ? 'text-emerald-600' : stats.isms_conformity_score >= 50 ? 'text-amber-600' : 'text-red-600'
  const docColor = stats.document_readiness_score >= 80 ? 'text-emerald-600' : stats.document_readiness_score >= 50 ? 'text-amber-600' : 'text-red-600'
  const objectiveStatusData = Object.entries(stats.objectives_by_status || {}).map(([name, value]) => ({ name, value }))
  const metricRagData = Object.entries(stats.metrics_by_rag || {}).map(([name, value]) => ({ name, value }))
  const RAG_COLORS: Record<string, string> = { 'On Target': '#10b981', 'Near Target': '#f59e0b', 'Off Target': '#ef4444', 'No Data': '#9ca3af' }
  const supplierCriticalityData = Object.entries(stats.suppliers_by_criticality || {}).map(([name, value]) => ({ name, value }))
  const supplierCategoryData = Object.entries(stats.suppliers_by_category || {}).map(([name, value]) => ({ name, value }))

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

      {/* ISMS management-system clauses (4–10) */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">ISMS Management-System Clauses (4–10)</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard label="Mandatory Clauses" value={stats.total_clauses} color="text-indigo-600" />
          <StatCard label="Conformant" value={stats.conformant_clauses} color="text-emerald-600" />
          <StatCard label="ISMS Conformity" value={`${stats.isms_conformity_score}%`} color={ismsColor} />
          <div className="card flex items-center">
            <p className="text-sm text-gray-500">Per Clause 1 (Scope), none of Clauses 4–10 may be excluded when claiming conformity.</p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Clause Conformity</h3>
            {clauseStatusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie data={clauseStatusData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {clauseStatusData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Clauses by Section</h3>
            {clauseSectionData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={clauseSectionData} layout="vertical" margin={{ left: 40 }}>
                  <XAxis type="number" allowDecimals={false} />
                  <YAxis type="category" dataKey="name" tick={{ fontSize: 11 }} width={140} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#10b981" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
        </div>
      </div>

      {/* ISMS records: documented information (7.5) + interested parties (4.2) */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">ISMS Records</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard label="Document Readiness" value={`${stats.document_readiness_score}%`} color={docColor} />
          <StatCard label="Mandatory Documents" value={stats.mandatory_documents} color="text-indigo-600" />
          <StatCard label="Approved (Mandatory)" value={stats.approved_mandatory_documents} color="text-emerald-600" />
          <StatCard label="Interested Parties" value={stats.total_interested_parties} color="text-gray-700" />
        </div>
      </div>

      {/* ISMS objectives (6.2) + metrics / KxI (9.1) */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">ISMS Objectives &amp; KPIs</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard label="IS Objectives" value={stats.total_objectives} color="text-indigo-600" />
          <StatCard label="Achieved" value={stats.achieved_objectives} color="text-emerald-600" />
          <StatCard label="Metrics (KPI/KRI/KCI)" value={stats.total_metrics} color="text-gray-700" />
          <StatCard label="On-Target Metrics" value={stats.on_target_metrics} color="text-emerald-600" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Objectives by Status</h3>
            {objectiveStatusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={objectiveStatusData}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#6366f1" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Metric RAG Status</h3>
            {metricRagData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie data={metricRagData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {metricRagData.map((d, i) => <Cell key={i} fill={RAG_COLORS[d.name] || COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
        </div>
      </div>

      {/* Suppliers / third parties (5.19–5.23) */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Suppliers &amp; Third Parties</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard label="Total Suppliers" value={stats.total_suppliers} color="text-indigo-600" />
          <StatCard label="High / Critical" value={stats.critical_suppliers} color="text-red-600" />
          <div className="card flex items-center lg:col-span-2">
            <p className="text-sm text-gray-500">Supplier relationships and their IS expectations (agreements, right-to-audit, certifications, periodic review) per Clauses 5.19–5.23.</p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Suppliers by Criticality</h3>
            {supplierCriticalityData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={supplierCriticalityData}>
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#6366f1" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">Suppliers by Category</h3>
            {supplierCategoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie data={supplierCategoryData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                    {supplierCategoryData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <p className="text-sm text-gray-400 py-12 text-center">No data</p>}
          </div>
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

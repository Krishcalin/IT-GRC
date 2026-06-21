import React, { useEffect, useState, useCallback } from 'react'
import { getTasks, createTask, updateTask, decideTask, deleteTask, getUsers } from '../services/api'
import type { Task, User } from '../types'
import { useAuth } from '../hooks/useAuth'
import StatusBadge from '../components/StatusBadge'

const TYPES = ['Action', 'Approval', 'Review', 'Remediation']
const PRIORITIES = ['Low', 'Medium', 'High', 'Critical']
const STATUSES = ['Open', 'In Progress', 'Blocked', 'Done', 'Cancelled']
const RESOURCE_TYPES = ['', 'control', 'risk', 'finding', 'incident', 'document', 'supplier', 'policy', 'assessment', 'objective', 'other']

const emptyForm = {
  title: '', task_type: 'Action', priority: 'Medium', status: 'Open',
  assignee_id: '', due_date: '', description: '', resource_type: '', resource_label: '',
}

const TasksPage: React.FC = () => {
  const { user } = useAuth()
  const [tasks, setTasks] = useState<Task[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<'mine' | 'all'>('mine')
  const [status, setStatus] = useState('')
  const [taskType, setTaskType] = useState('')
  const [priority, setPriority] = useState('')
  const [search, setSearch] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(emptyForm)

  const load = useCallback(() => {
    setLoading(true)
    const params: Record<string, string> = {}
    if (tab === 'mine' && user) params.assignee_id = user.id
    if (status) params.status = status
    if (taskType) params.task_type = taskType
    if (priority) params.priority = priority
    if (search) params.search = search
    getTasks(params).then((r) => setTasks(r.data)).catch(() => {}).finally(() => setLoading(false))
  }, [tab, user, status, taskType, priority, search])

  useEffect(() => { load() }, [load])
  useEffect(() => { getUsers().then((r) => setUsers(r.data)).catch(() => {}) }, [])

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    const payload: Record<string, unknown> = { ...form }
    if (!payload.assignee_id) delete payload.assignee_id
    if (!payload.due_date) delete payload.due_date
    if (!payload.resource_type) { delete payload.resource_type; delete payload.resource_label }
    await createTask(payload)
    setShowForm(false); setForm(emptyForm); load()
  }

  const changeStatus = async (t: Task, newStatus: string) => {
    await updateTask(t.id, { status: newStatus }); load()
  }
  const decide = async (t: Task, decision: 'Approved' | 'Rejected') => {
    const comment = window.prompt(`${decision} — add an optional comment:`) || undefined
    await decideTask(t.id, { decision, decision_comment: comment }); load()
  }
  const remove = async (t: Task) => {
    if (window.confirm(`Delete ${t.ref_id}?`)) { await deleteTask(t.id); load() }
  }

  const fmt = (d: string | null) => (d ? new Date(d).toLocaleDateString() : '—')
  const openCount = tasks.filter((t) => ['Open', 'In Progress', 'Blocked'].includes(t.status)).length
  const overdueCount = tasks.filter((t) => t.overdue).length
  const approvalCount = tasks.filter((t) => t.task_type === 'Approval' && ['Open', 'In Progress', 'Blocked'].includes(t.status)).length

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900">Tasks & Workflow</h1>
          <span className="bg-indigo-100 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">{tasks.length}</span>
        </div>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>{showForm ? 'Cancel' : '+ New Task'}</button>
      </div>
      <p className="text-sm text-gray-500 -mt-3">
        Assign, track, and sign off work across every module — actions, reviews, remediation, and approvals with due dates and an audit trail.
      </p>

      {/* Summary chips */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div className="card"><div className="text-2xl font-bold text-indigo-600">{openCount}</div><div className="text-sm text-gray-500">Open</div></div>
        <div className="card"><div className="text-2xl font-bold text-red-600">{overdueCount}</div><div className="text-sm text-gray-500">Overdue</div></div>
        <div className="card"><div className="text-2xl font-bold text-amber-600">{approvalCount}</div><div className="text-sm text-gray-500">Pending Approvals</div></div>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-3"><label className="block text-sm font-medium text-gray-700 mb-1">Title</label><input required className="input-field" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select className="select-field w-full" value={form.task_type} onChange={(e) => setForm({ ...form, task_type: e.target.value })}>{TYPES.map((t) => <option key={t}>{t}</option>)}</select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
              <select className="select-field w-full" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>{PRIORITIES.map((p) => <option key={p}>{p}</option>)}</select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Assignee</label>
              <select className="select-field w-full" value={form.assignee_id} onChange={(e) => setForm({ ...form, assignee_id: e.target.value })}>
                <option value="">Unassigned</option>
                {users.map((u) => <option key={u.id} value={u.id}>{u.full_name}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label><input type="date" className="input-field" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Related To</label>
              <select className="select-field w-full" value={form.resource_type} onChange={(e) => setForm({ ...form, resource_type: e.target.value })}>
                {RESOURCE_TYPES.map((r) => <option key={r} value={r}>{r || '—'}</option>)}
              </select>
            </div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Related Label</label><input className="input-field" placeholder="e.g. A.5.18 Access rights" value={form.resource_label} onChange={(e) => setForm({ ...form, resource_label: e.target.value })} /></div>
          </div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Description</label><textarea className="input-field h-20" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></div>
          <button type="submit" className="btn-primary">Create Task</button>
        </form>
      )}

      {/* Tabs + filters */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex rounded-lg border border-gray-200 overflow-hidden">
          <button onClick={() => setTab('mine')} className={`px-4 py-2 text-sm font-medium ${tab === 'mine' ? 'bg-indigo-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}>My Tasks</button>
          <button onClick={() => setTab('all')} className={`px-4 py-2 text-sm font-medium ${tab === 'all' ? 'bg-indigo-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}>All Tasks</button>
        </div>
        <select className="select-field" value={status} onChange={(e) => setStatus(e.target.value)}><option value="">All Statuses</option>{STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}</select>
        <select className="select-field" value={taskType} onChange={(e) => setTaskType(e.target.value)}><option value="">All Types</option>{TYPES.map((t) => <option key={t} value={t}>{t}</option>)}</select>
        <select className="select-field" value={priority} onChange={(e) => setPriority(e.target.value)}><option value="">All Priorities</option>{PRIORITIES.map((p) => <option key={p} value={p}>{p}</option>)}</select>
        <input className="input-field max-w-xs" placeholder="Search ref or title..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Ref</th>
              <th className="table-header">Title</th>
              <th className="table-header">Type</th>
              <th className="table-header">Priority</th>
              <th className="table-header">Assignee</th>
              <th className="table-header">Due</th>
              <th className="table-header">Status</th>
              <th className="table-header">Actions</th>
            </tr></thead>
            <tbody>
              {tasks.map((t) => (
                <tr key={t.id} className="border-b border-gray-100 hover:bg-indigo-50/40 transition-colors">
                  <td className="table-cell font-mono font-semibold text-indigo-600">{t.ref_id}</td>
                  <td className="table-cell">
                    <div className="font-medium text-gray-800">{t.title}</div>
                    {t.resource_label && <div className="text-xs text-gray-400">{t.resource_type}: {t.resource_label}</div>}
                    {t.decision && <div className={`text-xs font-semibold ${t.decision === 'Approved' ? 'text-green-700' : 'text-red-700'}`}>{t.decision}{t.decided_by ? ` by ${t.decided_by.full_name}` : ''}</div>}
                  </td>
                  <td className="table-cell text-gray-500">{t.task_type}</td>
                  <td className="table-cell"><StatusBadge value={t.priority} /></td>
                  <td className="table-cell text-gray-500">{t.assignee?.full_name || '—'}</td>
                  <td className={`table-cell ${t.overdue ? 'text-red-600 font-semibold' : 'text-gray-400'}`}>{fmt(t.due_date)}{t.overdue ? ' ⚠' : ''}</td>
                  <td className="table-cell">
                    <select className="select-field text-xs py-1" value={t.status} onChange={(e) => changeStatus(t, e.target.value)}>
                      {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </td>
                  <td className="table-cell">
                    <div className="flex items-center gap-2">
                      {t.task_type === 'Approval' && !t.decision && (
                        <>
                          <button onClick={() => decide(t, 'Approved')} className="text-xs font-semibold text-green-700 hover:underline">Approve</button>
                          <button onClick={() => decide(t, 'Rejected')} className="text-xs font-semibold text-red-700 hover:underline">Reject</button>
                        </>
                      )}
                      <button onClick={() => remove(t)} className="text-xs text-gray-400 hover:text-red-600">Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
              {tasks.length === 0 && <tr><td colSpan={8} className="table-cell text-center text-gray-400 py-12">No tasks{tab === 'mine' ? ' assigned to you' : ''}</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default TasksPage

import React from 'react'

const colors: Record<string, string> = {
  // green
  Implemented: 'bg-emerald-100 text-emerald-800',
  'Fully Implemented': 'bg-emerald-100 text-emerald-800',
  Pass: 'bg-emerald-100 text-emerald-800',
  Resolved: 'bg-emerald-100 text-emerald-800',
  Approved: 'bg-emerald-100 text-emerald-800',
  Active: 'bg-emerald-100 text-emerald-800',
  Verified: 'bg-emerald-100 text-emerald-800',
  Completed: 'bg-emerald-100 text-emerald-800',
  // yellow
  'In Progress': 'bg-amber-100 text-amber-800',
  'Partially Implemented': 'bg-amber-100 text-amber-800',
  'Under Review': 'bg-amber-100 text-amber-800',
  'In Treatment': 'bg-amber-100 text-amber-800',
  Medium: 'bg-amber-100 text-amber-800',
  // gray
  'Not Started': 'bg-gray-100 text-gray-600',
  'Not Implemented': 'bg-gray-100 text-gray-600',
  Open: 'bg-gray-100 text-gray-600',
  Draft: 'bg-gray-100 text-gray-600',
  Planned: 'bg-gray-100 text-gray-600',
  // red
  Critical: 'bg-red-100 text-red-800',
  Overdue: 'bg-red-100 text-red-800',
  Failed: 'bg-red-100 text-red-800',
  Cancelled: 'bg-red-100 text-red-800',
  // orange
  High: 'bg-orange-100 text-orange-800',
  // teal
  Low: 'bg-teal-100 text-teal-800',
  // blue misc
  Mitigate: 'bg-blue-100 text-blue-800',
  Accept: 'bg-purple-100 text-purple-800',
  Transfer: 'bg-sky-100 text-sky-800',
  Avoid: 'bg-rose-100 text-rose-800',
}

interface Props {
  value: string
  className?: string
}

const StatusBadge: React.FC<Props> = ({ value, className = '' }) => {
  const color = colors[value] || 'bg-gray-100 text-gray-600'
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color} ${className}`}>
      {value}
    </span>
  )
}

export default StatusBadge

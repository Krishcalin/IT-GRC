import React, { useState } from 'react'
import { downloadReport } from '../services/api'

interface ReportDef {
  key: string
  path: string
  filename?: string
  title: string
  description: string
  kind: 'csv' | 'html'
}

const REPORTS: ReportDef[] = [
  { key: 'soa', path: 'soa.csv', filename: 'statement_of_applicability.csv', title: 'Statement of Applicability (SoA)', description: 'Every control with applicability, implementation status, justification, and responsible owner.', kind: 'csv' },
  { key: 'risks', path: 'risks.csv', filename: 'risk_register.csv', title: 'Risk Register', description: 'Full risk register with likelihood × impact scoring, treatment, residual level, and status.', kind: 'csv' },
  { key: 'controls', path: 'controls.csv', filename: 'controls.csv', title: 'Controls Catalogue', description: 'All controls (ISO 27001:2022 Annex A + ISO 27019:2024 energy sector) with framework, theme, status, owner, and review date.', kind: 'csv' },
  { key: 'board', path: 'board-pack.html', title: 'Board Pack (printable)', description: 'One-page executive summary — compliance, conformity, risks, incidents, training — ready to print or save as PDF.', kind: 'html' },
]

const ReportsPage: React.FC = () => {
  const [busy, setBusy] = useState<string | null>(null)

  const run = async (r: ReportDef) => {
    setBusy(r.key)
    try {
      const res = await downloadReport(r.path)
      const url = URL.createObjectURL(res.data as Blob)
      if (r.kind === 'html') {
        window.open(url, '_blank')
        setTimeout(() => URL.revokeObjectURL(url), 60000)
      } else {
        const a = document.createElement('a')
        a.href = url
        a.download = r.filename || r.path
        document.body.appendChild(a)
        a.click()
        a.remove()
        URL.revokeObjectURL(url)
      }
    } catch { /* ignore */ }
    setBusy(null)
  }

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Reports &amp; Export</h1>
      <p className="text-sm text-gray-500 -mt-3">
        Export audit-ready evidence as CSV, or generate a printable management board pack.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {REPORTS.map((r) => (
          <div key={r.key} className="card flex flex-col">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{r.title}</h3>
                <span className={`inline-block mt-1 text-xs font-semibold px-2 py-0.5 rounded-full ${r.kind === 'html' ? 'bg-indigo-100 text-indigo-700' : 'bg-emerald-100 text-emerald-700'}`}>
                  {r.kind === 'html' ? 'Printable HTML / PDF' : 'CSV'}
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-3 flex-1">{r.description}</p>
            <button onClick={() => run(r)} disabled={busy === r.key} className="btn-primary mt-4 self-start">
              {busy === r.key ? 'Preparing…' : r.kind === 'html' ? 'Open Board Pack' : 'Download CSV'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ReportsPage

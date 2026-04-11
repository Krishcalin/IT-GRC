import React, { useEffect, useState } from 'react'
import { getEvidenceList, uploadEvidence, downloadEvidence } from '../services/api'
import type { Evidence } from '../types'

const EvidencePage: React.FC = () => {
  const [items, setItems] = useState<Evidence[]>([])
  const [loading, setLoading] = useState(true)
  const [showUpload, setShowUpload] = useState(false)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [file, setFile] = useState<File | null>(null)

  const load = () => {
    setLoading(true)
    getEvidenceList().then((r) => setItems(r.data)).catch(() => {}).finally(() => setLoading(false))
  }
  useEffect(load, [])

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    const fd = new FormData()
    fd.append('title', title)
    fd.append('description', description)
    fd.append('file', file)
    await uploadEvidence(fd)
    setShowUpload(false)
    setTitle('')
    setDescription('')
    setFile(null)
    load()
  }

  const handleDownload = async (ev: Evidence) => {
    const res = await downloadEvidence(ev.id)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = ev.file_name
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const fmtSize = (bytes: number | null) => {
    if (!bytes) return '—'
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / 1048576).toFixed(1)} MB`
  }

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Evidence Library</h1>
        <button className="btn-primary" onClick={() => setShowUpload(!showUpload)}>{showUpload ? 'Cancel' : '+ Upload'}</button>
      </div>

      {showUpload && (
        <form onSubmit={handleUpload} className="card space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input required className="input-field" value={title} onChange={(e) => setTitle(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <input className="input-field" value={description} onChange={(e) => setDescription(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">File</label>
            <input type="file" required onChange={(e) => setFile(e.target.files?.[0] || null)} className="text-sm" />
          </div>
          <button type="submit" className="btn-primary">Upload</button>
        </form>
      )}

      <div className="card p-0 overflow-hidden">
        {loading ? <div className="p-8 text-center text-gray-400">Loading...</div> : (
          <table className="w-full">
            <thead><tr className="bg-gray-50 border-b border-gray-200">
              <th className="table-header">Title</th>
              <th className="table-header">File</th>
              <th className="table-header">Type</th>
              <th className="table-header">Size</th>
              <th className="table-header">Uploaded By</th>
              <th className="table-header">Date</th>
              <th className="table-header">Action</th>
            </tr></thead>
            <tbody>
              {items.map((ev) => (
                <tr key={ev.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="table-cell font-medium">{ev.title}</td>
                  <td className="table-cell text-sm text-gray-500">{ev.file_name}</td>
                  <td className="table-cell text-xs text-gray-400">{ev.file_type || '—'}</td>
                  <td className="table-cell text-xs">{fmtSize(ev.file_size)}</td>
                  <td className="table-cell text-sm">{ev.uploader?.full_name || '—'}</td>
                  <td className="table-cell text-xs text-gray-400">{new Date(ev.created_at).toLocaleDateString()}</td>
                  <td className="table-cell"><button onClick={() => handleDownload(ev)} className="text-indigo-600 hover:text-indigo-800 text-xs font-medium">Download</button></td>
                </tr>
              ))}
              {items.length === 0 && <tr><td colSpan={7} className="table-cell text-center text-gray-400 py-12">No evidence uploaded yet</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default EvidencePage

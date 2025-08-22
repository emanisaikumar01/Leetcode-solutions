import { useState } from 'react'
import axios from 'axios'

const MAX_FILE_MB = 5

export default function UploadForm({ onSuccess }) {
	const [file, setFile] = useState(null)
	const [jd, setJd] = useState('')
	const [error, setError] = useState('')
	const [loading, setLoading] = useState(false)

	function handleFileChange(e) {
		const f = e.target.files?.[0]
		setError('')
		if (!f) {
			setFile(null)
			return
		}
		const valid = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
		if (!valid.includes(f.type) && !/\.(pdf|docx)$/i.test(f.name)) {
			setError('Only .pdf and .docx files are allowed.')
			setFile(null)
			return
		}
		if (f.size > MAX_FILE_MB * 1024 * 1024) {
			setError(`File exceeds ${MAX_FILE_MB}MB limit.`)
			setFile(null)
			return
		}
		setFile(f)
	}

	async function handleSubmit(e) {
		e.preventDefault()
		setError('')
		if (!file) {
			setError('Please select a resume file (.pdf/.docx).')
			return
		}
		if (!jd || jd.trim().length < 30) {
			setError('Please paste a detailed job description (at least 30 characters).')
			return
		}
		try {
			setLoading(true)
			const form = new FormData()
			form.append('file', file)
			form.append('job_description', jd)
			const res = await axios.post('/api/analyze', form, { headers: { 'Content-Type': 'multipart/form-data' } })
			onSuccess(res.data)
		} catch (err) {
			const msg = err?.response?.data?.detail || 'Failed to analyze resume.'
			setError(msg)
		} finally {
			setLoading(false)
		}
	}

	return (
		<form onSubmit={handleSubmit} className="space-y-6 bg-slate-900/50 rounded-xl p-6 border border-slate-800">
			<div>
				<label className="block text-sm font-medium mb-2">Upload Resume (.pdf or .docx)</label>
				<input type="file" accept=".pdf,.docx" onChange={handleFileChange} className="block w-full text-sm bg-slate-800 file:bg-slate-700 file:text-slate-100 file:border-0 file:px-4 file:py-2 file:mr-4 rounded" />
				<p className="text-xs text-slate-400 mt-1">Max {MAX_FILE_MB}MB. Strict validation enforced.</p>
			</div>
			<div>
				<label className="block text-sm font-medium mb-2">Job Description</label>
				<textarea value={jd} onChange={e => setJd(e.target.value)} rows={8} placeholder="Paste the job description here..." className="w-full rounded bg-slate-800 border border-slate-700 p-3"></textarea>
			</div>
			{error && <div className="text-red-400 text-sm">{error}</div>}
			<button type="submit" disabled={loading} className="inline-flex items-center bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-5 py-2 rounded">
				{loading ? 'Analyzing…' : 'Analyze Resume'}
			</button>
		</form>
	)
}
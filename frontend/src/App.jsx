import { useState } from 'react'
import UploadForm from './components/UploadForm'
import Results from './components/Results'

function App() {
	const [result, setResult] = useState(null)

	return (
		<div className="min-h-screen p-6 md:p-10">
			<header className="max-w-5xl mx-auto">
				<h1 className="text-2xl md:text-4xl font-bold tracking-tight">DPR – AI Resume Analyzer</h1>
				<p className="text-slate-400 mt-2">Upload your resume and a job description to get an ATS score, skill gaps, and course recommendations.</p>
			</header>

			<main className="max-w-5xl mx-auto mt-8">
				{!result ? (
					<UploadForm onSuccess={setResult} />
				) : (
					<Results data={result} onReset={() => setResult(null)} />
				)}
			</main>
		</div>
	)
}

export default App
import ScoreMeter from './ScoreMeter'

export default function Results({ data, onReset }) {
	return (
		<div className="space-y-6">
			<div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
				<h2 className="text-xl font-semibold">ATS Score</h2>
				<div className="mt-4">
					<ScoreMeter score={data.ats_score} />
					<p className="text-slate-400 mt-2">Higher is better. Aim for 75+.</p>
				</div>
			</div>

			<div className="grid md:grid-cols-2 gap-6">
				<div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
					<h3 className="font-semibold">Missing Skills</h3>
					<ul className="mt-3 list-disc list-inside text-red-300">
						{data.missing_skills.length === 0 ? (
							<li className="text-slate-400">No critical gaps detected.</li>
						) : data.missing_skills.map(s => <li key={s}>{s}</li>)}
					</ul>
				</div>
				<div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
					<h3 className="font-semibold">Matched Skills</h3>
					<ul className="mt-3 list-disc list-inside text-emerald-300">
						{data.matched_skills.length === 0 ? (
							<li className="text-slate-400">No matches yet.</li>
						) : data.matched_skills.map(s => <li key={s}>{s}</li>)}
					</ul>
				</div>
			</div>

			<div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
				<h3 className="font-semibold">Suggested Courses</h3>
				<div className="mt-3 grid md:grid-cols-2 gap-4">
					{data.course_recommendations.length === 0 ? (
						<p className="text-slate-400">No course recommendations at this time.</p>
					) : data.course_recommendations.map(c => (
						<div key={c.skill} className="bg-slate-800 rounded p-3 border border-slate-700">
							<div className="font-medium">{c.skill}</div>
							<div className="text-sm mt-1 space-x-3">
								<a className="text-indigo-300 hover:underline" href={c.coursera} target="_blank" rel="noreferrer">Coursera</a>
								<a className="text-indigo-300 hover:underline" href={c.udemy} target="_blank" rel="noreferrer">Udemy</a>
								<a className="text-indigo-300 hover:underline" href={c.nptel} target="_blank" rel="noreferrer">NPTEL</a>
							</div>
						</div>
					))}
				</div>
			</div>

			<div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800">
				<h3 className="font-semibold">Suggestions</h3>
				<ul className="mt-3 list-disc list-inside text-slate-300">
					{data.suggestions.map((s, idx) => <li key={idx}>{s}</li>)}
				</ul>
			</div>

			<button onClick={onReset} className="inline-flex items-center bg-slate-700 hover:bg-slate-600 px-5 py-2 rounded">Analyse Another Resume</button>
		</div>
	)
}
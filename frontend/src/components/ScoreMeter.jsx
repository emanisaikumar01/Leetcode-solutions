import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'

export default function ScoreMeter({ score }) {
	const data = [{ name: 'Score', value: score, fill: score >= 75 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444' }]
	return (
		<div className="flex items-center gap-6">
			<RadialBarChart width={200} height={200} innerRadius="80%" outerRadius="100%" data={data} startAngle={180} endAngle={-180}>
				<PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
				<RadialBar dataKey="value" background cornerRadius={10} />
			</RadialBarChart>
			<div>
				<div className="text-5xl font-bold">{score}</div>
				<div className="text-slate-400">/ 100</div>
			</div>
		</div>
	)
}
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { chartAxisStyle, chartTooltipStyle } from '@/lib/chart-theme'
import type { EngagementPoint } from '@/types/dashboard'

interface EngagementLineChartProps {
  data: EngagementPoint[]
  height?: number
}

export function EngagementLineChart({ data, height = 300 }: EngagementLineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="0" stroke="rgba(217,217,217,0.1)" horizontal vertical={false} />
        <XAxis dataKey="month" stroke="#D9D9D9" axisLine={false} tickLine={false} style={chartAxisStyle} />
        <YAxis stroke="#D9D9D9" axisLine={false} tickLine={false} style={chartAxisStyle} />
        <Tooltip contentStyle={chartTooltipStyle} />
        <Line
          type="monotone"
          dataKey="atRisk"
          stroke="#FE981E"
          strokeWidth={3}
          name="At-Risk"
          dot={{ fill: '#FE981E', r: 5, strokeWidth: 2, stroke: '#252025' }}
        />
        <Line
          type="monotone"
          dataKey="onTrack"
          stroke="#60A5FA"
          strokeWidth={3}
          name="On-Track"
          dot={{ fill: '#60A5FA', r: 5, strokeWidth: 2, stroke: '#252025' }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'
import { chartAxisStyle, chartTooltipStyle } from '@/lib/chart-theme'
import type { RadarPoint } from '@/types/dashboard'

interface ClusterRadarChartProps {
  data: RadarPoint[]
  height?: number
}

export function ClusterRadarChart({ data, height = 400 }: ClusterRadarChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data}>
        <PolarGrid stroke="rgba(217,217,217,0.1)" />
        <PolarAngleAxis dataKey="subject" stroke="#D9D9D9" style={chartAxisStyle} />
        <PolarRadiusAxis stroke="#D9D9D9" />
        <Radar
          name="Last-Minute"
          dataKey="lastMinute"
          stroke="#FE981E"
          fill="#FE981E"
          fillOpacity={0.3}
        />
        <Radar
          name="Struggling"
          dataKey="struggling"
          stroke="#F87171"
          fill="#F87171"
          fillOpacity={0.3}
        />
        <Radar
          name="Disengaged"
          dataKey="disengaged"
          stroke="#6B7280"
          fill="#6B7280"
          fillOpacity={0.3}
        />
        <Tooltip contentStyle={chartTooltipStyle} />
      </RadarChart>
    </ResponsiveContainer>
  )
}

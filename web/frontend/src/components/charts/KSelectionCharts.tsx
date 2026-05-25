import type { ReactNode } from 'react'
import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { chartAxisStyle, chartTooltipStyle } from '@/lib/chart-theme'
import type { KSelectionPoint } from '@/types/mlLab'

interface KSelectionChartsProps {
  data: KSelectionPoint[]
  recommendedK: number
}

export function KSelectionCharts({ data, recommendedK }: KSelectionChartsProps) {
  const normalized = data.map((d) => ({
    ...d,
    inertiaNorm: d.inertia / data[0].inertia,
  }))

  return (
    <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
      <ChartCard title="Elbow (Inertia)" subtitle="Lower is better — look for the knee">
        <ResponsiveContainer width="100%" height={280}>
          <ComposedChart data={normalized}>
            <CartesianGrid stroke="rgba(217,217,217,0.1)" vertical={false} />
            <XAxis dataKey="k" stroke="#D9D9D9" axisLine={false} tickLine={false} style={chartAxisStyle} />
            <YAxis stroke="#D9D9D9" axisLine={false} tickLine={false} style={chartAxisStyle} />
            <Tooltip contentStyle={chartTooltipStyle} />
            <Line
              type="monotone"
              dataKey="inertia"
              stroke="#60A5FA"
              strokeWidth={3}
              dot={({ cx, cy, payload }) =>
                cx != null && cy != null ? (
                  <circle
                    cx={cx}
                    cy={cy}
                    r={payload?.k === recommendedK ? 7 : 5}
                    fill={payload?.k === recommendedK ? '#FE981E' : '#60A5FA'}
                    stroke="#252025"
                    strokeWidth={2}
                  />
                ) : (
                  <g />
                )
              }
              name="Inertia"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard title="Silhouette & Davies–Bouldin" subtitle="Silhouette ↑ better · DB ↓ better">
        <ResponsiveContainer width="100%" height={280}>
          <ComposedChart data={data}>
            <CartesianGrid stroke="rgba(217,217,217,0.1)" vertical={false} />
            <XAxis dataKey="k" stroke="#D9D9D9" axisLine={false} tickLine={false} style={chartAxisStyle} />
            <YAxis yAxisId="left" stroke="#34D399" axisLine={false} tickLine={false} style={chartAxisStyle} />
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#F87171"
              axisLine={false}
              tickLine={false}
              style={chartAxisStyle}
            />
            <Tooltip contentStyle={chartTooltipStyle} />
            <Legend />
            <Bar yAxisId="left" dataKey="silhouette" fill="#34D399" name="Silhouette" radius={[4, 4, 0, 0]} />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="daviesBouldin"
              stroke="#F87171"
              strokeWidth={2}
              name="Davies–Bouldin"
              dot={{ r: 4 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}

function ChartCard({
  title,
  subtitle,
  children,
}: {
  title: string
  subtitle: string
  children: ReactNode
}) {
  return (
    <div className="rounded-xl border border-white/[0.06] bg-[#252025] p-4 sm:p-6">
      <h4 className="text-base font-bold text-white sm:text-lg">{title}</h4>
      <p className="mb-4 text-xs text-[#D9D9D9]/60 sm:text-sm">{subtitle}</p>
      {children}
    </div>
  )
}

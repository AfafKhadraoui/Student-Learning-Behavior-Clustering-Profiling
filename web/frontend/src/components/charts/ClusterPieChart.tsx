import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import { chartTooltipStyle } from '@/lib/chart-theme'
import { TOTAL_STUDENTS } from '@/constants/design'
import type { ClusterSummary } from '@/types/dashboard'

interface ClusterPieChartProps {
  data: ClusterSummary[]
  total?: number
}

export function ClusterPieChart({ data, total = TOTAL_STUDENTS }: ClusterPieChartProps) {
  return (
    <div className="relative mx-auto w-full max-w-[240px]">
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={70}
            outerRadius={100}
            paddingAngle={3}
            dataKey="value"
          >
            {data.map((entry) => (
              <Cell key={entry.name} fill={entry.color} stroke="none" />
            ))}
          </Pie>
          <Tooltip contentStyle={chartTooltipStyle} />
        </PieChart>
      </ResponsiveContainer>
      <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl font-black text-white sm:text-3xl">{total}</div>
          <div className="text-xs text-[#D9D9D9]/60">Students</div>
        </div>
      </div>
    </div>
  )
}

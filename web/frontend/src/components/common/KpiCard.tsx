import { TrendingDown, TrendingUp, type LucideIcon } from 'lucide-react'
import { DashboardCard } from '@/components/common/DashboardCard'
import { CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { KpiMetric } from '@/types/dashboard'
import { cn } from '@/lib/utils'

interface KpiCardProps {
  metric: KpiMetric
  icon: LucideIcon
  trendPositiveIsGood?: boolean
  onClick?: () => void
}

export function KpiCard({
  metric,
  icon: Icon,
  trendPositiveIsGood = true,
  onClick,
}: KpiCardProps) {
  const trendColor =
    metric.trendUp === trendPositiveIsGood ? 'text-[#34D399]' : 'text-[#F87171]'
  const TrendIcon = metric.trendUp ? TrendingUp : TrendingDown

  return (
    <DashboardCard
      hoverAccent
      className={`group ${onClick ? 'cursor-pointer' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                onClick()
              }
            }
          : undefined
      }
    >
      <CardHeader className="flex flex-row items-center justify-between pb-3">
        <CardTitle className="text-sm font-medium text-[#9A9099]">{metric.label}</CardTitle>
        <div className="rounded-xl bg-white/5 p-2.5 transition-all group-hover:bg-[#FE981E]/10">
          <Icon className="size-5 text-[#9A9099] transition-colors group-hover:text-[#FE981E]" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="mb-2 text-2xl font-black text-white sm:text-3xl">{metric.value}</div>
        <div className="flex flex-wrap items-center gap-1.5 text-sm">
          <div className={cn('flex items-center gap-1', trendColor)}>
            <TrendIcon className="size-4" />
            <span className="font-medium">{metric.trend}</span>
          </div>
          <span className="text-[#D9D9D9]/60">{metric.trendLabel}</span>
        </div>
      </CardContent>
    </DashboardCard>
  )
}

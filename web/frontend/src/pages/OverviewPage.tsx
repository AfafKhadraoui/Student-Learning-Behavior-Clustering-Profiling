import { AlertTriangle, BarChart3, CheckCircle2, ChevronDown, Users } from 'lucide-react'
import { ClusterPieChart } from '@/components/charts/ClusterPieChart'
import { EngagementLineChart } from '@/components/charts/EngagementLineChart'
import { DashboardCard } from '@/components/common/DashboardCard'
import { KpiCard } from '@/components/common/KpiCard'
import { LoadingState } from '@/components/common/LoadingState'
import { StudentTable } from '@/components/tables/StudentTable'
import { CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useApp } from '@/context/AppContext'
import { useDashboardOverview } from '@/hooks/useDashboardData'
import type { KpiMetric } from '@/types/dashboard'

const KPI_ICONS = [Users, AlertTriangle, CheckCircle2, BarChart3] as const

export function OverviewPage() {
  const { data, loading, error } = useDashboardOverview()
  const { navigateToStudents, navigateToModels, setSelectedStudent } = useApp()

  if (loading) return <LoadingState label="Loading dashboard..." />
  if (error || !data) {
    return (
      <p className="text-sm text-[#F87171]" role="alert">
        {error ?? 'Failed to load dashboard'}
      </p>
    )
  }

  const kpiActions: Record<string, () => void> = {
    'total-students': () => navigateToStudents(),
    'at-risk': () => navigateToStudents('Struggling Students'),
    interventions: () => navigateToStudents(),
    silhouette: () => navigateToModels(),
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6 xl:grid-cols-4">
        {data.kpis.map((metric: KpiMetric, index) => (
          <KpiCard
            key={metric.id}
            metric={metric}
            icon={KPI_ICONS[index] ?? Users}
            trendPositiveIsGood={metric.id !== 'at-risk'}
            onClick={kpiActions[metric.id]}
          />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <DashboardCard className="xl:col-span-2">
          <CardHeader className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <CardTitle className="text-lg text-white sm:text-xl">Engagement Over Time</CardTitle>
              <CardDescription className="text-[#D9D9D9]/60">
                Student activity trends
              </CardDescription>
            </div>
            <div className="flex flex-wrap items-center gap-3 sm:gap-4">
              <LegendDot color="#FE981E" label="At-Risk" />
              <LegendDot color="#60A5FA" label="On-Track" />
              <button
                type="button"
                className="flex items-center gap-1 rounded-lg bg-white/5 px-3 py-1.5 text-xs text-[#D9D9D9] hover:bg-white/10"
              >
                Monthly
                <ChevronDown className="size-3" aria-hidden />
              </button>
            </div>
          </CardHeader>
          <CardContent className="min-h-[260px] sm:min-h-[300px]">
            <EngagementLineChart data={data.engagement} />
          </CardContent>
        </DashboardCard>

        <DashboardCard>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-lg text-white sm:text-xl">Cluster Distribution</CardTitle>
            <button
              type="button"
              onClick={() => navigateToModels()}
              className="text-xs text-[#FE981E] hover:underline"
            >
              ML Lab →
            </button>
          </CardHeader>
          <CardContent className="flex flex-col items-center">
            <ClusterPieChart data={data.clusters} />
            <ul className="mt-6 w-full space-y-2">
              {data.clusters.map((cluster) => (
                <li key={cluster.name}>
                  <button
                    type="button"
                    onClick={() => navigateToStudents(cluster.name)}
                    className="flex w-full items-center justify-between gap-2 rounded-lg px-2 py-1.5 transition-colors hover:bg-white/5"
                  >
                    <div className="flex min-w-0 items-center gap-2">
                      <span
                        className="size-2 shrink-0 rounded-full"
                        style={{ backgroundColor: cluster.color }}
                      />
                      <span className="truncate text-left text-xs text-[#D9D9D9]">{cluster.name}</span>
                    </div>
                    <span className="shrink-0 text-sm font-medium text-white">{cluster.value}</span>
                  </button>
                </li>
              ))}
            </ul>
          </CardContent>
        </DashboardCard>
      </div>

      <DashboardCard>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="text-lg text-white sm:text-xl">Recent Student Activity</CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              Click a row for details
            </CardDescription>
          </div>
          <button
            type="button"
            onClick={() => navigateToStudents()}
            className="text-sm text-[#FE981E] hover:underline"
          >
            View all →
          </button>
        </CardHeader>
        <CardContent>
          <StudentTable
            students={data.recentStudents}
            compact
            onSelectStudent={setSelectedStudent}
          />
        </CardContent>
      </DashboardCard>
    </div>
  )
}

function LegendDot({ color, label }: { color: string; label: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="size-2 rounded-full" style={{ backgroundColor: color }} />
      <span className="text-xs text-[#D9D9D9]">{label}</span>
    </div>
  )
}

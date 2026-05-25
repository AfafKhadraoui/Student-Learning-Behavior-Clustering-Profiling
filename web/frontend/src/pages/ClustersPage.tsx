import { useState } from 'react'
import { ExternalLink } from 'lucide-react'
import { ClusterRadarChart } from '@/components/charts/ClusterRadarChart'
import { DashboardCard } from '@/components/common/DashboardCard'
import { LoadingState } from '@/components/common/LoadingState'
import { PageHeader } from '@/components/common/PageHeader'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { TOTAL_STUDENTS } from '@/constants/design'
import { useApp } from '@/context/AppContext'
import { useClusterAnalysis } from '@/hooks/useDashboardData'
import { fetchMlLabData } from '@/services/mlLabService'
import type { ClusterProfile } from '@/types/mlLab'
import { useEffect } from 'react'

export function ClustersPage() {
  const { data, loading, error } = useClusterAnalysis()
  const { navigateToStudents, navigateToModels } = useApp()
  const [profiles, setProfiles] = useState<ClusterProfile[]>([])
  const [expandedId, setExpandedId] = useState<number | null>(null)

  useEffect(() => {
    fetchMlLabData().then((d) => setProfiles(d.clusterProfiles))
  }, [])

  if (loading) return <LoadingState label="Loading cluster analysis..." />
  if (error || !data) {
    return (
      <p className="text-sm text-[#F87171]" role="alert">
        {error ?? 'Failed to load clusters'}
      </p>
    )
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Cluster Analysis"
        description="ENSIA k=3 profiles from notebook 03 — Peach et al. behavioral archetypes"
        action={
          <Button
            variant="ghost"
            className="text-[#FE981E] hover:bg-[#FE981E]/10"
            onClick={() => navigateToModels()}
          >
            Open ML Lab
            <ExternalLink className="ml-2 size-4" />
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {data.clusters.map((cluster) => {
          const profile = profiles.find((p) => p.name === cluster.name)
          const isExpanded = expandedId === profile?.id
          return (
            <button
              key={cluster.name}
              type="button"
              onClick={() => {
                if (profile) setExpandedId(isExpanded ? null : profile.id)
              }}
              className="text-left"
            >
              <DashboardCard hoverAccent className="h-full overflow-hidden p-0 gap-0">
                <div className="h-2" style={{ backgroundColor: cluster.color }} />
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm text-white">{cluster.name}</CardTitle>
                  {profile && (
                    <Badge className="mt-1 w-fit border-white/10 bg-white/5 text-[#D9D9D9]">
                      Risk: {profile.riskLevel}
                    </Badge>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="mb-2 text-2xl font-black text-white sm:text-3xl">
                    {cluster.value.toLocaleString()}
                  </div>
                  <p className="text-xs text-[#D9D9D9]/60">
                    {((cluster.value / TOTAL_STUDENTS) * 100).toFixed(1)}% of cohort
                  </p>
                  {isExpanded && profile?.interpretation && (
                    <p className="mt-3 text-xs leading-relaxed text-[#D9D9D9]/80">
                      {profile.interpretation}
                    </p>
                  )}
                  <Button
                    size="sm"
                    variant="ghost"
                    className="mt-3 text-[#FE981E] hover:bg-[#FE981E]/10"
                    onClick={(e) => {
                      e.stopPropagation()
                      navigateToStudents(cluster.name)
                    }}
                  >
                    View students →
                  </Button>
                </CardContent>
              </DashboardCard>
            </button>
          )
        })}
      </div>

      <DashboardCard>
        <CardHeader>
          <CardTitle className="text-lg text-white sm:text-xl">Feature Profile Comparison</CardTitle>
          <CardDescription className="text-[#D9D9D9]/60">
            Normalized behavioral metrics (20 engineered features → key dimensions)
          </CardDescription>
        </CardHeader>
        <CardContent className="min-h-[320px] sm:min-h-[400px]">
          <ClusterRadarChart data={data.radar} />
        </CardContent>
      </DashboardCard>
    </div>
  )
}

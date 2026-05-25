import { useState } from 'react'
import {
  CheckCircle2,
  Clock,
  ExternalLink,
  FileCode2,
  Layers,
  Sparkles,
} from 'lucide-react'
import { KSelectionCharts } from '@/components/charts/KSelectionCharts'
import { DashboardCard } from '@/components/common/DashboardCard'
import { LoadingState } from '@/components/common/LoadingState'
import { PageHeader } from '@/components/common/PageHeader'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useApp } from '@/context/AppContext'
import { useMlLab } from '@/hooks/useMlLab'
import type { ClusteringAlgorithm, ModelComparisonRow } from '@/types/mlLab'
import { cn } from '@/lib/utils'

export function ModelLabPage() {
  const { data, loading, error } = useMlLab()
  const { navigateToStudents } = useApp()
  const [selectedAlgo, setSelectedAlgo] = useState<string>('kmeans')

  if (loading) return <LoadingState label="Loading ML pipeline..." />
  if (error || !data) {
    return <p className="text-sm text-[#F87171]" role="alert">{error ?? 'Failed to load ML Lab'}</p>
  }

  const activeAlgo = data.algorithms.find((a) => a.id === selectedAlgo) ?? data.algorithms[0]

  return (
    <div className="space-y-6">
      <PageHeader
        title="ML Lab"
        description="K-selection, clustering algorithms, and model comparison — aligned with notebooks 03–07"
        action={
          <Badge className="bg-[#FE981E]/15 text-[#FE981E] border-[#FE981E]/30">
            Primary: K-Means · k={data.kSelection.recommendedK}
          </Badge>
        }
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-4">
        {data.pipeline.map((step) => (
          <button
            key={step.id}
            type="button"
            className={cn(
              'rounded-xl border p-3 text-left transition-all hover:border-[#FE981E]/40',
              step.status === 'complete'
                ? 'border-[#34D399]/30 bg-[#34D399]/5'
                : 'border-white/10 bg-white/5',
            )}
          >
            <div className="mb-2 flex items-center justify-between gap-2">
              <span className="text-xs font-medium text-[#9A9099]">NB {step.id}</span>
              {step.status === 'complete' ? (
                <CheckCircle2 className="size-4 text-[#34D399]" />
              ) : (
                <Clock className="size-4 text-[#D9D9D9]/40" />
              )}
            </div>
            <p className="text-sm font-semibold text-white">{step.name}</p>
            <p className="mt-1 truncate text-xs text-[#D9D9D9]/50">{step.output}</p>
          </button>
        ))}
      </div>

      <Tabs defaultValue="k-selection">
        <TabsList>
          <TabsTrigger value="k-selection">K Selection</TabsTrigger>
          <TabsTrigger value="algorithms">Algorithms</TabsTrigger>
          <TabsTrigger value="comparison">Comparison</TabsTrigger>
          <TabsTrigger value="profiles">ENSIA Profiles</TabsTrigger>
        </TabsList>

        <TabsContent value="k-selection" className="space-y-4">
          <DashboardCard>
            <CardHeader>
              <CardTitle className="text-white">Recommended k = {data.kSelection.recommendedK}</CardTitle>
              <CardDescription className="text-[#D9D9D9]/60">{data.kSelection.reason}</CardDescription>
            </CardHeader>
          </DashboardCard>
          <KSelectionCharts data={data.kSelection.metrics} recommendedK={data.kSelection.recommendedK} />
          <DashboardCard>
            <CardHeader>
              <CardTitle className="text-white">Distance Metric Sweep</CardTitle>
              <CardDescription className="text-[#D9D9D9]/60">Notebook 03 — Euclidean (k-selection) vs Manhattan (final) vs Mahalanobis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                {data.kSelection.distanceMetrics.map((m) => (
                  <button
                    key={m.metric}
                    type="button"
                    className={cn(
                      'rounded-xl border p-4 text-left transition-all',
                      m.selected
                        ? 'border-[#FE981E] bg-[#FE981E]/10'
                        : 'border-white/10 bg-white/5 hover:border-white/20',
                    )}
                  >
                    <p className="text-sm font-bold capitalize text-white">{m.metric}</p>
                    <p className="mt-1 text-2xl font-black text-[#FE981E]">{m.silhouette.toFixed(2)}</p>
                    <p className="text-xs text-[#D9D9D9]/60">Silhouette @ k=3</p>
                    {m.selected && (
                      <Badge className="mt-2 bg-[#FE981E] text-white">Selected</Badge>
                    )}
                  </button>
                ))}
              </div>
            </CardContent>
          </DashboardCard>
        </TabsContent>

        <TabsContent value="algorithms" className="space-y-4">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {data.algorithms.map((algo) => (
              <AlgorithmCard
                key={algo.id}
                algo={algo}
                selected={selectedAlgo === algo.id}
                onSelect={() => setSelectedAlgo(algo.id)}
              />
            ))}
          </div>
          {activeAlgo && (
            <DashboardCard>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-white">
                  <FileCode2 className="size-5 text-[#FE981E]" />
                  {activeAlgo.name} — Detail
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-[#D9D9D9]/80">
                <p>{activeAlgo.description}</p>
                <p>
                  <span className="text-[#9A9099]">Notebook:</span>{' '}
                  <code className="rounded bg-white/5 px-2 py-0.5 text-[#FE981E]">{activeAlgo.notebook}.ipynb</code>
                </p>
                <p>
                  <span className="text-[#9A9099]">Artifact:</span>{' '}
                  <code className="rounded bg-white/5 px-2 py-0.5">{activeAlgo.artifact}</code>
                </p>
                {activeAlgo.status === 'active' && (
                  <Button
                    className="bg-[#FE981E] text-white hover:bg-[#E08918]"
                    onClick={() => navigateToStudents()}
                  >
                    View clustered students
                    <ExternalLink className="ml-2 size-4" />
                  </Button>
                )}
              </CardContent>
            </DashboardCard>
          )}
        </TabsContent>

        <TabsContent value="comparison">
          <DashboardCard>
            <CardHeader>
              <CardTitle className="text-white">Model Comparison Matrix</CardTitle>
              <CardDescription className="text-[#D9D9D9]/60">
                Notebook 07 — ARI vs K-Means baseline when additional models are trained
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[640px] text-sm">
                  <thead>
                    <tr className="border-b border-white/10 text-left text-[#9A9099]">
                      {['Algorithm', 'Status', 'k', 'Silhouette', 'Davies–Bouldin', 'ARI vs K-Means', 'Notes'].map(
                        (h) => (
                          <th key={h} className="px-3 py-3 font-medium">
                            {h}
                          </th>
                        ),
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {data.comparison.map((row) => (
                      <ComparisonRow key={row.algorithm} row={row} />
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </DashboardCard>
        </TabsContent>

        <TabsContent value="profiles" className="space-y-4">
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
            {data.clusterProfiles.map((profile) => (
              <button
                key={profile.id}
                type="button"
                onClick={() => navigateToStudents(profile.name)}
                className="overflow-hidden rounded-xl border border-white/[0.06] bg-[#252025] text-left transition-all hover:border-[#FE981E]/50"
              >
                <div className="h-2" style={{ backgroundColor: profile.color }} />
                <div className="p-5">
                  <h4 className="font-bold text-white">{profile.shortName}</h4>
                  <p className="mt-1 text-xs text-[#D9D9D9]/60">{profile.name}</p>
                  <p className="mt-3 text-2xl font-black text-white">
                    {profile.value.toLocaleString()}
                    <span className="ml-1 text-sm font-normal text-[#9A9099]">students</span>
                  </p>
                  <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                    <div className="rounded-lg bg-white/5 p-2">
                      <p className="text-[#9A9099]">Pass</p>
                      <p className="font-bold text-[#34D399]">{profile.pctPass}%</p>
                    </div>
                    <div className="rounded-lg bg-white/5 p-2">
                      <p className="text-[#9A9099]">Fail+Withdrawn</p>
                      <p className="font-bold text-[#F87171]">{profile.pctFailWithdrawn}%</p>
                    </div>
                  </div>
                  <Badge className="mt-3 border-white/10 bg-white/5 text-[#D9D9D9]">
                    Risk: {profile.riskLevel}
                  </Badge>
                </div>
              </button>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function AlgorithmCard({
  algo,
  selected,
  onSelect,
}: {
  algo: ClusteringAlgorithm
  selected: boolean
  onSelect: () => void
}) {
  const isActive = algo.status === 'active'
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        'rounded-xl border p-5 text-left transition-all',
        selected ? 'border-[#FE981E] ring-1 ring-[#FE981E]/30' : 'border-white/[0.06]',
        isActive ? 'bg-[#252025] hover:border-[#FE981E]/50' : 'bg-[#252025]/60 opacity-90',
      )}
    >
      <div className="mb-3 flex items-start justify-between">
        <div className="flex items-center gap-2">
          <Layers className="size-5 text-[#FE981E]" />
          <h4 className="font-bold text-white">{algo.name}</h4>
        </div>
        <Badge
          className={cn(
            isActive ? 'bg-[#34D399]/15 text-[#34D399]' : 'bg-white/10 text-[#D9D9D9]',
          )}
        >
          {isActive ? 'Active' : 'Coming soon'}
        </Badge>
      </div>
      <p className="text-sm text-[#D9D9D9]/70">{algo.description}</p>
      {!isActive && (
        <p className="mt-3 flex items-center gap-1 text-xs text-[#FE981E]">
          <Sparkles className="size-3" />
          Backend hook: {algo.notebook}
        </p>
      )}
    </button>
  )
}

function ComparisonRow({ row }: { row: ModelComparisonRow }) {
  const fmt = (v: number | null, digits = 2) =>
    v == null ? '—' : typeof v === 'number' ? v.toFixed(digits) : v
  return (
    <tr className="border-b border-white/5 hover:bg-white/5">
      <td className="px-3 py-3 font-medium text-white">{row.algorithm}</td>
      <td className="px-3 py-3">
        <Badge
          className={cn(
            row.status === 'active'
              ? 'bg-[#34D399]/15 text-[#34D399]'
              : 'bg-white/10 text-[#D9D9D9]',
          )}
        >
          {row.status}
        </Badge>
      </td>
      <td className="px-3 py-3 text-[#D9D9D9]">{row.k ?? '—'}</td>
      <td className="px-3 py-3 text-[#D9D9D9]">{fmt(row.silhouette)}</td>
      <td className="px-3 py-3 text-[#D9D9D9]">{fmt(row.daviesBouldin)}</td>
      <td className="px-3 py-3 text-[#D9D9D9]">{fmt(row.ariVsKmeans)}</td>
      <td className="px-3 py-3 text-xs text-[#9A9099]">{row.notes}</td>
    </tr>
  )
}

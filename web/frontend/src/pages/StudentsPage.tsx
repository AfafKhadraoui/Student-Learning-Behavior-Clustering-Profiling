import { useEffect, useState } from 'react'
import { Filter } from 'lucide-react'
import { DashboardCard } from '@/components/common/DashboardCard'
import { LoadingState } from '@/components/common/LoadingState'
import { PageHeader } from '@/components/common/PageHeader'
import { StudentTable } from '@/components/tables/StudentTable'
import { CardContent } from '@/components/ui/card'
import { useApp } from '@/context/AppContext'
import { useStudents } from '@/hooks/useStudents'
import type { RiskLevel } from '@/types/dashboard'

const CLUSTER_OPTIONS = [
  { value: 'all', label: 'All Clusters' },
  { value: 'Engaged Last-Minute Learners', label: 'Last-Minute (On-Track)' },
  { value: 'Struggling Students', label: 'Struggling' },
  { value: 'Disengaged / Withdrawn', label: 'Disengaged' },
]

export function StudentsPage() {
  const { setSelectedStudent, searchQuery, clusterFilter, setClusterFilter } = useApp()
  const [filterCluster, setFilterCluster] = useState(clusterFilter === 'all' ? 'all' : clusterFilter)
  const [filterRisk, setFilterRisk] = useState<RiskLevel | 'all'>('all')

  useEffect(() => {
    if (clusterFilter !== 'all') setFilterCluster(clusterFilter)
  }, [clusterFilter])

  const { students, loading, error } = useStudents({
    cluster: filterCluster === 'all' ? 'all' : (filterCluster as never),
    risk: filterRisk,
    search: searchQuery,
  })

  return (
    <div className="space-y-6">
      <PageHeader
        title="Student Table"
        description="Full searchable and filterable student list — click any row for details"
        action={
          <>
            <FilterSelect
              label="Cluster filter"
              value={filterCluster}
              onChange={(v) => {
                setFilterCluster(v)
                setClusterFilter(v)
              }}
              options={CLUSTER_OPTIONS}
            />
            <FilterSelect
              label="Risk filter"
              value={filterRisk}
              onChange={(v) => setFilterRisk(v as RiskLevel | 'all')}
              options={[
                { value: 'all', label: 'All Risk Levels' },
                { value: 'Low', label: 'Low' },
                { value: 'Moderate', label: 'Moderate' },
                { value: 'High', label: 'High' },
                { value: 'Critical', label: 'Critical' },
              ]}
            />
          </>
        }
      />

      <DashboardCard>
        <CardContent className="p-0">
          {loading ? (
            <LoadingState label="Loading students..." />
          ) : error ? (
            <p className="p-6 text-sm text-[#F87171]" role="alert">
              {error}
            </p>
          ) : students.length === 0 ? (
            <p className="p-6 text-sm text-[#D9D9D9]/60">No students match your filters.</p>
          ) : (
            <StudentTable
              students={students}
              showActions
              onSelectStudent={setSelectedStudent}
            />
          )}
        </CardContent>
      </DashboardCard>
    </div>
  )
}

function FilterSelect({
  label,
  value,
  onChange,
  options,
}: {
  label: string
  value: string
  onChange: (value: string) => void
  options: { value: string; label: string }[]
}) {
  return (
    <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-3 py-2">
      <Filter className="size-4 shrink-0 text-[#D9D9D9]/50" aria-hidden />
      <select
        aria-label={label}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="max-w-[160px] bg-transparent text-sm text-white outline-none sm:max-w-none"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} className="bg-[#252025]">
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
}

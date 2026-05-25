import { X } from 'lucide-react'
import { ClusterBadge } from '@/components/common/ClusterBadge'
import { RiskBadge } from '@/components/common/RiskBadge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import type { Student } from '@/types/dashboard'

interface StudentDetailPanelProps {
  student: Student
  onClose: () => void
}

export function StudentDetailPanel({ student, onClose }: StudentDetailPanelProps) {
  return (
    <>
      <button
        type="button"
        className="fixed inset-0 z-40 bg-black/50 lg:bg-black/30"
        aria-label="Close student details"
        onClick={onClose}
      />
      <aside
        className="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col overflow-auto border-l border-white/10 bg-[#1C1718] p-4 shadow-2xl sm:p-6"
        aria-label="Student details"
      >
        <div className="mb-6 flex items-center justify-between">
          <h3 className="text-lg font-bold text-white sm:text-xl">Student Details</h3>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-1 text-[#D9D9D9]/50 hover:bg-white/5 hover:text-white"
            aria-label="Close panel"
          >
            <X className="size-5" />
          </button>
        </div>

        <div className="space-y-6">
          <DetailField label="Student ID" value={student.id} />
          <DetailField label="Name" value={student.name} />
          <div>
            <p className="mb-1 text-sm text-[#D9D9D9]/60">Cluster</p>
            <ClusterBadge cluster={student.cluster} />
          </div>
          <div>
            <p className="mb-1 text-sm text-[#D9D9D9]/60">Risk Level</p>
            <RiskBadge risk={student.risk} showRange />
          </div>
          <div>
            <p className="mb-2 text-sm text-[#D9D9D9]/60">Engagement Score</p>
            <div className="flex items-center gap-3">
              <Progress value={(student.score / 10) * 100} className="flex-1" />
              <span className="font-medium text-white">{student.score}/10</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <StatBox label="Active Days" value={String(student.activeDays)} />
            <StatBox label="Submissions" value={String(student.submissions)} />
          </div>
          <StatBox label="Average Grade" value={`${student.avgGrade}%`} fullWidth />
          <Button className="w-full bg-[#FE981E] font-bold text-white hover:bg-[#E08918]">
            Send Intervention Email
          </Button>
        </div>
      </aside>
    </>
  )
}

function DetailField({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="mb-1 text-sm text-[#D9D9D9]/60">{label}</p>
      <p className="font-medium text-white">{value}</p>
    </div>
  )
}

function StatBox({
  label,
  value,
  fullWidth,
}: {
  label: string
  value: string
  fullWidth?: boolean
}) {
  return (
    <div
      className={`rounded-xl border border-white/5 bg-white/5 p-4 ${fullWidth ? 'col-span-2' : ''}`}
    >
      <p className="mb-1 text-sm text-[#D9D9D9]/60">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  )
}

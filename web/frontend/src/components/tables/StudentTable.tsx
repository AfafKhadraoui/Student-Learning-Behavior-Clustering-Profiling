import { Button } from '@/components/ui/button'
import { ClusterBadge } from '@/components/common/ClusterBadge'
import { RiskBadge } from '@/components/common/RiskBadge'
import { getClusterColor } from '@/utils/cluster'
import type { Student } from '@/types/dashboard'

interface StudentTableProps {
  students: Student[]
  onSelectStudent?: (student: Student) => void
  showActions?: boolean
  compact?: boolean
}

export function StudentTable({
  students,
  onSelectStudent,
  showActions = false,
  compact = false,
}: StudentTableProps) {
  const cellPy = compact ? 'py-3' : 'py-4'

  return (
    <div className="overflow-x-auto -mx-1 px-1">
      <table className="w-full min-w-[640px]">
        <thead>
          <tr className="border-b border-white/10">
            {['Student ID', 'Name', 'Cluster', 'Score', 'Active Days', ...(showActions ? ['Submissions', 'Risk Level', 'Action'] : ['Risk Level'])].map(
              (header) => (
                <th
                  key={header}
                  scope="col"
                  className="text-left px-3 py-3 text-xs font-medium text-[#9A9099] first:pl-4 last:pr-4"
                >
                  {header}
                </th>
              ),
            )}
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr
              key={student.id}
              onClick={() => onSelectStudent?.(student)}
              className={`border-b border-white/5 transition-colors ${onSelectStudent ? 'cursor-pointer hover:bg-white/5' : ''}`}
            >
              <td className={`${cellPy} px-3 pl-4 text-xs font-medium text-white`}>{student.id}</td>
              <td className={`${cellPy} px-3 text-xs text-[#D9D9D9]`}>{student.name}</td>
              <td className={`${cellPy} px-3`}>
                {compact ? (
                  <div className="flex items-center gap-1.5">
                    <span
                      className="size-2 rounded-full"
                      style={{ backgroundColor: getClusterColor(student.cluster) }}
                    />
                    <span className="text-xs text-[#D9D9D9]">{student.cluster}</span>
                  </div>
                ) : (
                  <ClusterBadge cluster={student.cluster} />
                )}
              </td>
              <td className={`${cellPy} px-3`}>
                {showActions ? (
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-20 overflow-hidden rounded-full bg-white/10">
                      <div
                        className="h-full bg-[#FE981E]"
                        style={{ width: `${(student.score / 10) * 100}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium text-white">{student.score}</span>
                  </div>
                ) : (
                  <span className="text-xs font-medium text-white">{student.score}</span>
                )}
              </td>
              <td className={`${cellPy} px-3 text-xs text-[#D9D9D9]`}>{student.activeDays}</td>
              {showActions && (
                <td className={`${cellPy} px-3 text-xs text-[#D9D9D9]`}>{student.submissions}</td>
              )}
              <td className={`${cellPy} px-3`}>
                <RiskBadge risk={student.risk} showRange={!showActions} />
              </td>
              {showActions && (
                <td className={`${cellPy} px-3 pr-4`}>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="text-[#FE981E] hover:bg-[#FE981E]/10 hover:text-[#E08918]"
                    onClick={(e) => {
                      e.stopPropagation()
                      onSelectStudent?.(student)
                    }}
                  >
                    View
                  </Button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

import { Badge } from '@/components/ui/badge'
import { getRiskBadgeClass, getRiskScoreRange } from '@/utils/cluster'
import type { RiskLevel } from '@/types/dashboard'
import { cn } from '@/lib/utils'

interface RiskBadgeProps {
  risk: RiskLevel
  showRange?: boolean
}

export function RiskBadge({ risk, showRange = false }: RiskBadgeProps) {
  return (
    <Badge variant="outline" className={cn('text-xs px-2 py-0.5 border', getRiskBadgeClass(risk))}>
      {risk}
      {showRange && ` · ${getRiskScoreRange(risk)}`}
    </Badge>
  )
}

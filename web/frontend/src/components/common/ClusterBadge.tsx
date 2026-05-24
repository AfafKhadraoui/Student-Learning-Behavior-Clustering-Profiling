import { Badge } from '@/components/ui/badge'
import { getClusterColor } from '@/utils/cluster'

interface ClusterBadgeProps {
  cluster: string
  showDot?: boolean
}

export function ClusterBadge({ cluster, showDot = false }: ClusterBadgeProps) {
  const color = getClusterColor(cluster)
  return (
    <div className="flex items-center gap-1.5">
      {showDot && (
        <span className="size-2 shrink-0 rounded-full" style={{ backgroundColor: color }} />
      )}
      <Badge
        variant="outline"
        className="border text-xs"
        style={{
          backgroundColor: `${color}20`,
          borderColor: `${color}40`,
          color,
        }}
      >
        {cluster}
      </Badge>
    </div>
  )
}

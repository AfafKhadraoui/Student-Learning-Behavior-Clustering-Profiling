import { CLUSTER_COLORS } from '@/constants/design'
import type { ClusterName, RiskLevel } from '@/types/dashboard'

export function getClusterColor(cluster: string): string {
  return CLUSTER_COLORS[cluster] ?? '#6B7280'
}

export function getRiskBadgeClass(risk: RiskLevel): string {
  switch (risk) {
    case 'Low':
      return 'bg-[rgba(52,211,153,0.12)] text-[#34D399] border-[#34D399]/20'
    case 'Moderate':
      return 'bg-[rgba(254,152,30,0.12)] text-[#FE981E] border-[#FE981E]/20'
    case 'High':
      return 'bg-[rgba(248,113,113,0.12)] text-[#F87171] border-[#F87171]/20'
    case 'Critical':
      return 'bg-[rgba(239,68,68,0.15)] text-[#EF4444] border-[#EF4444]/20'
    default:
      return 'bg-[#6B7280]/10 text-[#6B7280] border-[#6B7280]/20'
  }
}

export function getRiskScoreRange(risk: RiskLevel): string {
  switch (risk) {
    case 'Low':
      return '0-2'
    case 'Moderate':
      return '3-4'
    case 'High':
      return '5-7'
    case 'Critical':
      return '8-10'
    default:
      return '0'
  }
}

export function getCsvStatusClass(status: string): string {
  switch (status) {
    case 'ready':
      return 'bg-[rgba(52,211,153,0.12)] text-[#34D399] border-[#34D399]/20'
    case 'processing':
      return 'bg-[rgba(254,152,30,0.12)] text-[#FE981E] border-[#FE981E]/20'
    default:
      return 'bg-[rgba(248,113,113,0.12)] text-[#F87171] border-[#F87171]/20'
  }
}

export function isClusterName(value: string): value is ClusterName {
  return value in CLUSTER_COLORS
}

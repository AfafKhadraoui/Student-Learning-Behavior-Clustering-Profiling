export type RiskLevel = 'Low' | 'Moderate' | 'High' | 'Critical'

export type ClusterName =
  | 'Engaged Last-Minute Learners'
  | 'Struggling Students'
  | 'Disengaged / Withdrawn'

export interface Student {
  id: string
  name: string
  cluster: ClusterName | string
  risk: RiskLevel
  score: number
  activeDays: number
  submissions: number
  avgGrade: number
}

export interface ClusterSummary {
  name: string
  value: number
  color: string
}

export interface EngagementPoint {
  month: string
  atRisk: number
  onTrack: number
}

export interface RadarPoint {
  subject: string
  highPerformer: number
  consistentLearner: number
  lastMinute: number
  struggling: number
  disengaged: number
}

export interface KpiMetric {
  id: string
  label: string
  value: string | number
  trend: number
  trendLabel: string
  trendUp: boolean
}

export type CsvFileStatus = 'ready' | 'processing' | 'missing'

export interface CsvFile {
  name: string
  status: CsvFileStatus
  size: string
}

export interface DashboardOverview {
  kpis: KpiMetric[]
  engagement: EngagementPoint[]
  clusters: ClusterSummary[]
  recentStudents: Student[]
}

export interface ClusterAnalysis {
  clusters: ClusterSummary[]
  radar: RadarPoint[]
}

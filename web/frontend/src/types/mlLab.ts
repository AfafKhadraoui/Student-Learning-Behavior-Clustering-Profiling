export type AlgorithmStatus = 'active' | 'planned'

export interface KSelectionPoint {
  k: number
  inertia: number
  silhouette: number
  daviesBouldin: number
  calinskiHarabasz: number
}

export interface DistanceMetricResult {
  metric: string
  silhouette: number
  selected: boolean
}

export interface KSelectionResult {
  recommendedK: number
  reason: string
  metrics: KSelectionPoint[]
  distanceMetrics: DistanceMetricResult[]
}

export interface ClusteringAlgorithm {
  id: string
  name: string
  notebook: string
  status: AlgorithmStatus
  description: string
  artifact: string
  features: number
  selectedK: number | null
}

export interface ModelComparisonRow {
  algorithm: string
  status: AlgorithmStatus | 'planned'
  k: number | null
  silhouette: number | null
  daviesBouldin: number | null
  ariVsKmeans: number | null
  noisePct: number | null
  notes: string
}

export interface PipelineStep {
  id: string
  name: string
  notebook: string
  status: 'complete' | 'planned' | 'in_progress'
  output: string
}

export interface ClusterProfile {
  id: number
  name: string
  shortName: string
  value: number
  color: string
  riskLevel: string
  pctPass: number
  pctFailWithdrawn: number
  interpretation?: string
  intervention?: string
}

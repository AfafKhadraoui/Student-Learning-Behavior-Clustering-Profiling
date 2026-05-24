import clustersData from '@/data/mock/clusters.json'
import engagementData from '@/data/mock/engagement.json'
import kpisData from '@/data/mock/kpis.json'
import radarData from '@/data/mock/radar.json'
import studentsData from '@/data/mock/students.json'
import { apiGet, USE_MOCK_API } from '@/services/api/client'
import type {
  ClusterAnalysis,
  ClusterSummary,
  DashboardOverview,
  EngagementPoint,
  KpiMetric,
  RadarPoint,
  Student,
} from '@/types/dashboard'

function loadMockOverview(): DashboardOverview {
  return {
    kpis: kpisData as KpiMetric[],
    engagement: engagementData as EngagementPoint[],
    clusters: clustersData as ClusterSummary[],
    recentStudents: (studentsData as Student[]).slice(0, 5),
  }
}

function loadMockClusterAnalysis(): ClusterAnalysis {
  return {
    clusters: clustersData as ClusterSummary[],
    radar: radarData as RadarPoint[],
  }
}

export async function fetchDashboardOverview(): Promise<DashboardOverview> {
  if (USE_MOCK_API) {
    return Promise.resolve(loadMockOverview())
  }
  return apiGet<DashboardOverview>('/dashboard/overview')
}

export async function fetchClusterAnalysis(): Promise<ClusterAnalysis> {
  if (USE_MOCK_API) {
    return Promise.resolve(loadMockClusterAnalysis())
  }
  return apiGet<ClusterAnalysis>('/clusters/analysis')
}

export { loadMockOverview, loadMockClusterAnalysis }

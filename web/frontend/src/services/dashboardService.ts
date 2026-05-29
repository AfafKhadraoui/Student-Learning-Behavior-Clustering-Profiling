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
  try {
    return await apiGet<DashboardOverview>('/dashboard/overview')
  } catch (error) {
    console.warn('Falling back to mock dashboard data:', error)
    return loadMockOverview()
  }
}

export async function fetchClusterAnalysis(): Promise<ClusterAnalysis> {
  if (USE_MOCK_API) {
    return Promise.resolve(loadMockClusterAnalysis())
  }
  try {
    return await apiGet<ClusterAnalysis>('/clusters/analysis')
  } catch (error) {
    console.warn('Falling back to mock cluster analysis:', error)
    return loadMockClusterAnalysis()
  }
}

export { loadMockOverview, loadMockClusterAnalysis }

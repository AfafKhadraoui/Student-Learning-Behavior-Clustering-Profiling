import algorithmsData from '@/data/mock/algorithms.json'
import clustersData from '@/data/mock/clusters.json'
import kSelectionData from '@/data/mock/k-selection.json'
import modelComparisonData from '@/data/mock/model-comparison.json'
import pipelineData from '@/data/mock/pipeline.json'
import { apiGet, USE_MOCK_API } from '@/services/api/client'
import type {
  ClusteringAlgorithm,
  ClusterProfile,
  KSelectionResult,
  ModelComparisonRow,
  PipelineStep,
} from '@/types/mlLab'

export interface MlLabBundle {
  kSelection: KSelectionResult
  algorithms: ClusteringAlgorithm[]
  comparison: ModelComparisonRow[]
  pipeline: PipelineStep[]
  clusterProfiles: ClusterProfile[]
}

function loadMock(): MlLabBundle {
  return {
    kSelection: kSelectionData as KSelectionResult,
    algorithms: algorithmsData as ClusteringAlgorithm[],
    comparison: modelComparisonData as ModelComparisonRow[],
    pipeline: pipelineData as PipelineStep[],
    clusterProfiles: clustersData as ClusterProfile[],
  }
}

export async function fetchMlLabData(): Promise<MlLabBundle> {
  if (USE_MOCK_API) return Promise.resolve(loadMock())
  return apiGet<MlLabBundle>('/ml-lab')
}

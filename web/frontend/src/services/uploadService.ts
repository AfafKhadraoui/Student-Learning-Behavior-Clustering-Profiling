import csvFilesData from '@/data/mock/csv-files.json'
import { apiGet, apiPost, USE_MOCK_API } from '@/services/api/client'
import type { CsvFile } from '@/types/dashboard'

export async function fetchCsvFileStatus(): Promise<CsvFile[]> {
  if (USE_MOCK_API) {
    return Promise.resolve(csvFilesData as CsvFile[])
  }
  try {
    return await apiGet<CsvFile[]>('/upload/status')
  } catch (error) {
    console.warn('Falling back to mock upload status:', error)
    return csvFilesData as CsvFile[]
  }
}

export async function processUploadedFiles(): Promise<{ jobId: string }> {
  if (USE_MOCK_API) {
    return Promise.resolve({ jobId: 'mock-job-1' })
  }
  try {
    return await apiPost<{ jobId: string }>('/upload/process')
  } catch (error) {
    console.warn('Falling back to mock upload processing:', error)
    return { jobId: 'mock-job-1' }
  }
}

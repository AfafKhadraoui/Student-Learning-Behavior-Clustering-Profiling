import csvFilesData from '@/data/mock/csv-files.json'
import { apiGet, USE_MOCK_API } from '@/services/api/client'
import type { CsvFile } from '@/types/dashboard'

export async function fetchCsvFileStatus(): Promise<CsvFile[]> {
  if (USE_MOCK_API) {
    return Promise.resolve(csvFilesData as CsvFile[])
  }
  return apiGet<CsvFile[]>('/upload/status')
}

export async function processUploadedFiles(): Promise<{ jobId: string }> {
  if (USE_MOCK_API) {
    return Promise.resolve({ jobId: 'mock-job-1' })
  }
  const response = await fetch('/api/upload/process', { method: 'POST' })
  if (!response.ok) throw new Error('Failed to start processing')
  return response.json() as Promise<{ jobId: string }>
}

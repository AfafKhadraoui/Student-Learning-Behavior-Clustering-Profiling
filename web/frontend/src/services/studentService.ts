import studentsData from '@/data/mock/students.json'
import { apiGet, USE_MOCK_API } from '@/services/api/client'
import type { ClusterName, RiskLevel, Student } from '@/types/dashboard'

export interface StudentFilters {
  cluster?: ClusterName | 'all'
  risk?: RiskLevel | 'all'
  search?: string
}

export async function fetchStudents(filters?: StudentFilters): Promise<Student[]> {
  if (USE_MOCK_API) {
    return Promise.resolve(filterStudents(studentsData as Student[], filters))
  }
  const params = new URLSearchParams()
  if (filters?.cluster && filters.cluster !== 'all') params.set('cluster', filters.cluster)
  if (filters?.risk && filters.risk !== 'all') params.set('risk', filters.risk)
  if (filters?.search) params.set('q', filters.search)
  const query = params.toString()
  return apiGet<Student[]>(`/students${query ? `?${query}` : ''}`)
}

export function filterStudents(students: Student[], filters?: StudentFilters): Student[] {
  return students.filter((student) => {
    const clusterMatch =
      !filters?.cluster ||
      filters.cluster === 'all' ||
      student.cluster === filters.cluster ||
      student.cluster.includes(filters.cluster) ||
      filters.cluster.includes(student.cluster)
    const riskMatch = !filters?.risk || filters.risk === 'all' || student.risk === filters.risk
    const search = filters?.search?.trim().toLowerCase()
    const searchMatch =
      !search ||
      student.name.toLowerCase().includes(search) ||
      student.id.toLowerCase().includes(search)
    return clusterMatch && riskMatch && searchMatch
  })
}

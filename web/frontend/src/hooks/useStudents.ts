import { useEffect, useMemo, useState } from 'react'
import { fetchStudents } from '@/services/studentService'
import type { ClusterName, RiskLevel, Student } from '@/types/dashboard'

export interface UseStudentsOptions {
  cluster?: ClusterName | 'all'
  risk?: RiskLevel | 'all'
  search?: string
}

export function useStudents(options: UseStudentsOptions = {}) {
  const [students, setStudents] = useState<Student[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const filterKey = useMemo(
    () => JSON.stringify(options),
    [options.cluster, options.risk, options.search],
  )

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    fetchStudents(options)
      .then((data) => {
        if (!cancelled) {
          setStudents(data)
          setError(null)
          setLoading(false)
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setStudents([])
          setError(err.message)
          setLoading(false)
        }
      })
    return () => {
      cancelled = true
    }
  }, [filterKey])

  return { students, loading, error }
}

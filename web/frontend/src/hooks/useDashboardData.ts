import { useEffect, useState } from 'react'
import {
  fetchClusterAnalysis,
  fetchDashboardOverview,
} from '@/services/dashboardService'
import type { ClusterAnalysis, DashboardOverview } from '@/types/dashboard'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useDashboardOverview() {
  const [state, setState] = useState<AsyncState<DashboardOverview>>({
    data: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    let cancelled = false
    fetchDashboardOverview()
      .then((data) => {
        if (!cancelled) setState({ data, loading: false, error: null })
      })
      .catch((err: Error) => {
        if (!cancelled) setState({ data: null, loading: false, error: err.message })
      })
    return () => {
      cancelled = true
    }
  }, [])

  return state
}

export function useClusterAnalysis() {
  const [state, setState] = useState<AsyncState<ClusterAnalysis>>({
    data: null,
    loading: true,
    error: null,
  })

  useEffect(() => {
    let cancelled = false
    fetchClusterAnalysis()
      .then((data) => {
        if (!cancelled) setState({ data, loading: false, error: null })
      })
      .catch((err: Error) => {
        if (!cancelled) setState({ data: null, loading: false, error: err.message })
      })
    return () => {
      cancelled = true
    }
  }, [])

  return state
}

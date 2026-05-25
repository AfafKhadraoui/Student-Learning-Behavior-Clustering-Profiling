import { useEffect, useState } from 'react'
import { fetchMlLabData } from '@/services/mlLabService'
import type { MlLabBundle } from '@/services/mlLabService'

export function useMlLab() {
  const [data, setData] = useState<MlLabBundle | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    fetchMlLabData()
      .then((bundle) => {
        if (!cancelled) {
          setData(bundle)
          setError(null)
          setLoading(false)
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setData(null)
          setError(err.message)
          setLoading(false)
        }
      })
    return () => {
      cancelled = true
    }
  }, [])

  return { data, loading, error }
}

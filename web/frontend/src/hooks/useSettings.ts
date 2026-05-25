import { useCallback, useEffect, useState } from 'react'

const STORAGE_KEY = 'ensia-insight-settings'

export interface AppSettings {
  emailNotifications: boolean
  autoRefresh: boolean
  refreshIntervalMin: number
  useMockApi: boolean
  apiBaseUrl: string
  defaultAlgorithm: string
  compactTables: boolean
  showPipelineHints: boolean
}

const DEFAULT_SETTINGS: AppSettings = {
  emailNotifications: true,
  autoRefresh: false,
  refreshIntervalMin: 5,
  useMockApi: true,
  apiBaseUrl: '/api',
  defaultAlgorithm: 'kmeans',
  compactTables: false,
  showPipelineHints: true,
}

function loadSettings(): AppSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return DEFAULT_SETTINGS
    return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) }
  } catch {
    return DEFAULT_SETTINGS
  }
}

export function useSettings() {
  const [settings, setSettings] = useState<AppSettings>(loadSettings)

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
  }, [settings])

  const update = useCallback(<K extends keyof AppSettings>(key: K, value: AppSettings[K]) => {
    setSettings((prev) => ({ ...prev, [key]: value }))
  }, [])

  const reset = useCallback(() => setSettings(DEFAULT_SETTINGS), [])

  return { settings, update, reset }
}

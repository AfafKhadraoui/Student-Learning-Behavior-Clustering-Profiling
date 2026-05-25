import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { NavId } from '@/constants/navigation'
import type { Student } from '@/types/dashboard'

interface AppContextValue {
  showWelcome: boolean
  setShowWelcome: (value: boolean) => void
  selectedNav: NavId
  setSelectedNav: (id: NavId) => void
  selectedStudent: Student | null
  setSelectedStudent: (student: Student | null) => void
  mobileNavOpen: boolean
  setMobileNavOpen: (open: boolean) => void
  searchQuery: string
  setSearchQuery: (query: string) => void
  clusterFilter: string
  setClusterFilter: (cluster: string) => void
  dismissWelcome: () => void
  navigate: (id: NavId) => void
  navigateToStudents: (cluster?: string) => void
  navigateToModels: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const [showWelcome, setShowWelcome] = useState(true)
  const [selectedNav, setSelectedNav] = useState<NavId>('overview')
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null)
  const [mobileNavOpen, setMobileNavOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [clusterFilter, setClusterFilter] = useState('all')

  const dismissWelcome = useCallback(() => setShowWelcome(false), [])

  const navigate = useCallback((id: NavId) => {
    setSelectedNav(id)
    setMobileNavOpen(false)
    if (id !== 'students') setSelectedStudent(null)
  }, [])

  const navigateToStudents = useCallback((cluster?: string) => {
    if (cluster) setClusterFilter(cluster)
    setSelectedNav('students')
    setMobileNavOpen(false)
  }, [])

  const navigateToModels = useCallback(() => {
    setSelectedNav('models')
    setMobileNavOpen(false)
  }, [])

  const value = useMemo(
    () => ({
      showWelcome,
      setShowWelcome,
      selectedNav,
      setSelectedNav: navigate,
      selectedStudent,
      setSelectedStudent,
      mobileNavOpen,
      setMobileNavOpen,
      searchQuery,
      setSearchQuery,
      clusterFilter,
      setClusterFilter,
      dismissWelcome,
      navigate,
      navigateToStudents,
      navigateToModels,
    }),
    [
      showWelcome,
      selectedNav,
      selectedStudent,
      mobileNavOpen,
      searchQuery,
      clusterFilter,
      dismissWelcome,
      navigate,
      navigateToStudents,
      navigateToModels,
    ],
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}

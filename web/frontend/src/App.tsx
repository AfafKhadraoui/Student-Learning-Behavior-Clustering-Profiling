import { AppProvider, useApp } from '@/context/AppContext'
import { DashboardRouter } from '@/pages/DashboardRouter'
import { WelcomePage } from '@/pages/WelcomePage'

function AppContent() {
  const { showWelcome } = useApp()
  if (showWelcome) return <WelcomePage />
  return <DashboardRouter />
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  )
}

import { AppShell } from '@/components/layout/AppShell'
import { ClustersPage } from '@/pages/ClustersPage'
import { ModelLabPage } from '@/pages/ModelLabPage'
import { OverviewPage } from '@/pages/OverviewPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { StudentsPage } from '@/pages/StudentsPage'
import { UploadPage } from '@/pages/UploadPage'
import { useApp } from '@/context/AppContext'

export function DashboardRouter() {
  const { selectedNav } = useApp()

  const page = (() => {
    switch (selectedNav) {
      case 'overview':
        return <OverviewPage />
      case 'clusters':
        return <ClustersPage />
      case 'students':
        return <StudentsPage />
      case 'models':
        return <ModelLabPage />
      case 'upload':
        return <UploadPage />
      case 'settings':
        return <SettingsPage />
      default:
        return <OverviewPage />
    }
  })()

  return <AppShell>{page}</AppShell>
}

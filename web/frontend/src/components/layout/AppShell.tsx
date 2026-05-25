import { useState, type ReactNode } from 'react'
import { DashboardHeader } from '@/components/layout/DashboardHeader'
import { HelpPanel } from '@/components/layout/HelpPanel'
import { MobileNavDrawer } from '@/components/layout/MobileNavDrawer'
import { Sidebar } from '@/components/layout/Sidebar'
import { StudentDetailPanel } from '@/components/layout/StudentDetailPanel'
import { useApp } from '@/context/AppContext'

interface AppShellProps {
  children: ReactNode
}

export function AppShell({ children }: AppShellProps) {
  const { selectedStudent, setSelectedStudent } = useApp()
  const [helpOpen, setHelpOpen] = useState(false)

  return (
    <div className="flex h-dvh min-h-0 overflow-hidden bg-[#1C1718]">
      <Sidebar className="hidden lg:flex" onHelpOpen={() => setHelpOpen(true)} />
      <MobileNavDrawer onHelpOpen={() => setHelpOpen(true)} />

      <main className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
        <DashboardHeader />
        <div className="custom-scrollbar min-h-0 flex-1 overflow-y-auto overflow-x-hidden px-4 pb-6 pt-4 sm:px-6 sm:pb-8 sm:pt-6 lg:px-8">
          {children}
        </div>
      </main>

      {selectedStudent && (
        <StudentDetailPanel
          student={selectedStudent}
          onClose={() => setSelectedStudent(null)}
        />
      )}

      <HelpPanel open={helpOpen} onClose={() => setHelpOpen(false)} />
    </div>
  )
}

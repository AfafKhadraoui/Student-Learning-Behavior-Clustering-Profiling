import { X } from 'lucide-react'
import { Sidebar } from '@/components/layout/Sidebar'
import { useApp } from '@/context/AppContext'

interface MobileNavDrawerProps {
  onHelpOpen?: () => void
}

export function MobileNavDrawer({ onHelpOpen }: MobileNavDrawerProps) {
  const { mobileNavOpen, setMobileNavOpen } = useApp()

  if (!mobileNavOpen) return null

  return (
    <div className="fixed inset-0 z-50 lg:hidden" role="dialog" aria-modal="true" aria-label="Navigation">
      <button
        type="button"
        className="absolute inset-0 bg-black/60"
        aria-label="Close navigation"
        onClick={() => setMobileNavOpen(false)}
      />
      <div className="relative flex h-full w-[76px] max-w-[80vw] flex-col bg-[#0F123F] shadow-2xl">
        <button
          type="button"
          className="absolute right-0 top-4 z-10 translate-x-full rounded-r-lg bg-[#0F123F] p-2 text-white"
          aria-label="Close menu"
          onClick={() => setMobileNavOpen(false)}
        >
          <X className="size-4" />
        </button>
        <Sidebar
          className="h-full w-full border-r-0"
          onNavigate={() => setMobileNavOpen(false)}
          onHelpOpen={() => {
            setMobileNavOpen(false)
            onHelpOpen?.()
          }}
        />
      </div>
    </div>
  )
}

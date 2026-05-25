import { BookOpen, HelpCircle, LogOut } from 'lucide-react'
import { NAV_ITEMS } from '@/constants/navigation'
import { useApp } from '@/context/AppContext'
import { cn } from '@/lib/utils'

interface SidebarProps {
  className?: string
  onNavigate?: () => void
  onHelpOpen?: () => void
}

export function Sidebar({ className, onNavigate, onHelpOpen }: SidebarProps) {
  const { selectedNav, navigate } = useApp()

  const handleNav = (id: (typeof NAV_ITEMS)[number]['id']) => {
    navigate(id)
    onNavigate?.()
  }

  return (
    <aside
      className={cn(
        'flex h-full w-[76px] shrink-0 flex-col items-center border-r border-white/[0.06] bg-[#0F123F]/95 py-5 backdrop-blur-xl',
        className,
      )}
      aria-label="Main navigation"
    >
      <div className="mb-6">
        <div className="flex size-11 items-center justify-center rounded-2xl bg-gradient-to-br from-[#FE981E] to-[#E08918] shadow-lg shadow-[#FE981E]/20">
          <BookOpen className="size-5 text-white" aria-hidden />
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1.5 px-2" aria-label="Dashboard sections">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon
          const isActive = selectedNav === item.id
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => handleNav(item.id)}
              aria-label={item.label}
              aria-current={isActive ? 'page' : undefined}
              title={item.label}
              className={cn(
                'group relative flex size-11 items-center justify-center rounded-xl transition-all duration-200',
                isActive
                  ? 'bg-[#FE981E] text-white shadow-md shadow-[#FE981E]/25'
                  : 'text-[#D9D9D9]/45 hover:bg-white/[0.06] hover:text-white',
              )}
            >
              <Icon className="size-[22px]" aria-hidden />
              <span className="pointer-events-none absolute left-full ml-3 hidden whitespace-nowrap rounded-lg bg-[#252025] px-2.5 py-1.5 text-xs font-medium text-white opacity-0 shadow-lg transition-opacity group-hover:opacity-100 lg:block">
                {item.label}
              </span>
            </button>
          )
        })}
      </nav>

      <div className="mt-auto flex w-full flex-col gap-1.5 border-t border-white/[0.06] px-2 pt-4">
        <button
          type="button"
          aria-label="Help and support"
          title="Help"
          onClick={() => {
            onHelpOpen?.()
            onNavigate?.()
          }}
          className="flex size-11 items-center justify-center rounded-xl text-[#D9D9D9]/45 transition-all hover:bg-white/[0.06] hover:text-[#FE981E]"
        >
          <HelpCircle className="size-[22px]" aria-hidden />
        </button>
        <button
          type="button"
          aria-label="Log out"
          title="Log out"
          className="flex size-11 items-center justify-center rounded-xl text-[#FE981E]/70 transition-all hover:bg-[#FE981E]/10 hover:text-[#FE981E]"
        >
          <LogOut className="size-[22px]" aria-hidden />
        </button>
      </div>
    </aside>
  )
}

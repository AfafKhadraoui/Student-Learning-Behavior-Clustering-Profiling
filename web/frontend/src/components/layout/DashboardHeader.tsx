import { useState } from 'react'
import { Bell, ChevronDown, Menu, Search } from 'lucide-react'
import { NotificationsPanel } from '@/components/layout/NotificationsPanel'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import { useApp } from '@/context/AppContext'
import { cn } from '@/lib/utils'

export function DashboardHeader() {
  const { searchQuery, setSearchQuery, setMobileNavOpen } = useApp()
  const [notificationsOpen, setNotificationsOpen] = useState(false)

  return (
    <header className="relative z-20 flex shrink-0 flex-col gap-4 border-b border-white/5 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8 lg:py-6">
      <div className="flex min-w-0 items-start gap-3">
        <button
          type="button"
          className="mt-1 rounded-xl p-2 text-[#D9D9D9] hover:bg-white/5 lg:hidden"
          aria-label="Open navigation menu"
          onClick={() => setMobileNavOpen(true)}
        >
          <Menu className="size-5" />
        </button>
        <div className="min-w-0">
          <h2 className="truncate text-xl font-black text-white sm:text-2xl lg:text-3xl">
            <span>Welcome Back, </span>
            <span className="text-[#FE981E]">Professor</span>
          </h2>
          <p className="text-xs text-[#D9D9D9]/60 sm:text-sm">
            Here&apos;s what&apos;s happening with your students today
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2 sm:gap-4">
        <div className="relative min-w-0 flex-1 sm:flex-none">
          <Search
            className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-[#D9D9D9]/50"
            aria-hidden
          />
          <Input
            type="search"
            placeholder="Search students..."
            aria-label="Search students"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-11 w-full min-w-0 rounded-xl border-white/10 bg-white/5 pl-10 text-white placeholder:text-[#D9D9D9]/30 focus:border-[#FE981E] sm:w-64 lg:w-80"
          />
        </div>

        <div className="relative">
          <button
            type="button"
            aria-label="Notifications"
            aria-expanded={notificationsOpen}
            onClick={() => setNotificationsOpen((v) => !v)}
            className={cn(
              'relative shrink-0 rounded-xl p-3 transition-all',
              notificationsOpen
                ? 'bg-[#FE981E]/15 text-[#FE981E]'
                : 'bg-white/5 text-[#D9D9D9] hover:bg-white/10',
            )}
          >
            <Bell className="size-5" />
            <span className="absolute top-2 right-2 size-2 rounded-full bg-[#FE981E] ring-2 ring-[#1C1718]" />
          </button>
          <NotificationsPanel open={notificationsOpen} onClose={() => setNotificationsOpen(false)} />
        </div>

        <button
          type="button"
          className="flex min-w-0 items-center gap-2 rounded-xl bg-white/5 px-3 py-2 transition-all hover:bg-white/10 sm:gap-3 sm:px-4"
          aria-label="User menu"
        >
          <Avatar className="size-8 shrink-0">
            <AvatarFallback className="bg-gradient-to-br from-[#FE981E] to-[#E08918] text-sm font-bold text-white">
              PR
            </AvatarFallback>
          </Avatar>
          <span className="hidden text-sm font-medium text-white sm:inline">Professor</span>
          <ChevronDown className="size-4 shrink-0 text-[#D9D9D9]/50" aria-hidden />
        </button>
      </div>
    </header>
  )
}

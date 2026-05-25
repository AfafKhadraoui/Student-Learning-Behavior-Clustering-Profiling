import { useEffect, useRef } from 'react'
import { AlertTriangle, Bell, CheckCircle2, Info, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import notificationsData from '@/data/mock/notifications.json'
import { useApp } from '@/context/AppContext'
import type { AppNotification, NotificationType } from '@/types/notifications'
import { cn } from '@/lib/utils'

interface NotificationsPanelProps {
  open: boolean
  onClose: () => void
}

export function NotificationsPanel({ open, onClose }: NotificationsPanelProps) {
  const panelRef = useRef<HTMLDivElement>(null)
  const { navigate, navigateToStudents } = useApp()
  const notifications = notificationsData as AppNotification[]
  const unread = notifications.filter((n) => !n.read).length

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    const onClick = (e: MouseEvent) => {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) onClose()
    }
    window.addEventListener('keydown', onKey)
    document.addEventListener('mousedown', onClick)
    return () => {
      window.removeEventListener('keydown', onKey)
      document.removeEventListener('mousedown', onClick)
    }
  }, [open, onClose])

  if (!open) return null

  const handleAction = (n: AppNotification) => {
    onClose()
    if (n.actionNav === 'students') navigateToStudents()
    else if (n.actionNav) navigate(n.actionNav)
  }

  return (
    <div
      ref={panelRef}
      className="absolute right-0 top-full z-50 mt-2 w-[min(calc(100vw-2rem),380px)] overflow-hidden rounded-2xl border border-white/10 bg-[#252025] shadow-2xl shadow-black/40"
      role="dialog"
      aria-label="Notifications"
    >
      <div className="flex items-center justify-between border-b border-white/5 px-4 py-3">
        <div className="flex items-center gap-2">
          <Bell className="size-4 text-[#FE981E]" />
          <h3 className="font-bold text-white">Notifications</h3>
          {unread > 0 && (
            <span className="rounded-full bg-[#FE981E] px-2 py-0.5 text-xs font-bold text-white">
              {unread}
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={onClose}
          className="rounded-lg p-1 text-[#D9D9D9]/50 hover:bg-white/5 hover:text-white"
          aria-label="Close notifications"
        >
          <X className="size-4" />
        </button>
      </div>

      <ul className="custom-scrollbar max-h-[min(70vh,420px)] overflow-y-auto">
        {notifications.map((n) => (
          <li
            key={n.id}
            className={cn(
              'border-b border-white/5 px-4 py-3 transition-colors hover:bg-white/[0.03]',
              !n.read && 'bg-[#FE981E]/[0.04]',
            )}
          >
            <div className="flex gap-3">
              <NotifIcon type={n.type} />
              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-2">
                  <p className="text-sm font-semibold text-white">{n.title}</p>
                  {!n.read && (
                    <span className="mt-1 size-2 shrink-0 rounded-full bg-[#FE981E]" />
                  )}
                </div>
                <p className="mt-0.5 text-xs leading-relaxed text-[#D9D9D9]/70">{n.message}</p>
                <p className="mt-1.5 text-[10px] text-[#9A9099]">{n.time}</p>
                {n.actionLabel && (
                  <button
                    type="button"
                    onClick={() => handleAction(n)}
                    className="mt-2 text-xs font-medium text-[#FE981E] hover:underline"
                  >
                    {n.actionLabel} →
                  </button>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>

      <div className="border-t border-white/5 p-3">
        <Button
          variant="ghost"
          className="w-full text-sm text-[#D9D9D9] hover:bg-white/5 hover:text-white"
          onClick={onClose}
        >
          Mark all as read
        </Button>
      </div>
    </div>
  )
}

function NotifIcon({ type }: { type: NotificationType }) {
  const config = {
    alert: { Icon: AlertTriangle, className: 'bg-[#F87171]/15 text-[#F87171]' },
    info: { Icon: Info, className: 'bg-[#60A5FA]/15 text-[#60A5FA]' },
    success: { Icon: CheckCircle2, className: 'bg-[#34D399]/15 text-[#34D399]' },
  }[type]
  const { Icon, className } = config
  return (
    <div className={cn('flex size-8 shrink-0 items-center justify-center rounded-xl', className)}>
      <Icon className="size-4" />
    </div>
  )
}

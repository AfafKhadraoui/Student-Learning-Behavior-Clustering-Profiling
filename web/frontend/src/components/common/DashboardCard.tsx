import type { ComponentProps, ReactNode } from 'react'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface DashboardCardProps extends ComponentProps<'div'> {
  children: ReactNode
  hoverAccent?: boolean
}

export function DashboardCard({
  children,
  className,
  hoverAccent = false,
  ...props
}: DashboardCardProps) {
  return (
    <Card
      className={cn(
        'bg-[#252025] border border-white/[0.06]',
        hoverAccent && 'hover:border-[#FE981E]/50 transition-all',
        className,
      )}
      {...props}
    >
      {children}
    </Card>
  )
}

import * as React from 'react'
import { cn } from '@/lib/utils'

function Input({ className, type, ...props }: React.ComponentProps<'input'>) {
  return (
    <input
      type={type}
      className={cn(
        'flex h-9 w-full min-w-0 rounded-md border px-3 py-1 text-base transition-colors outline-none disabled:opacity-50 md:text-sm',
        'focus-visible:ring-2 focus-visible:ring-[#FE981E]/50',
        className,
      )}
      {...props}
    />
  )
}

export { Input }

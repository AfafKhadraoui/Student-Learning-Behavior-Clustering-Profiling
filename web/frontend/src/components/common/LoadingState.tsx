export function LoadingState({ label = 'Loading...' }: { label?: string }) {
  return (
    <div className="flex min-h-[200px] items-center justify-center text-[#D9D9D9]/60">
      <span className="animate-pulse text-sm">{label}</span>
    </div>
  )
}

import { useEffect } from 'react'
import { BookOpen, HelpCircle, Keyboard, Mail, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useApp } from '@/context/AppContext'

const FAQ = [
  {
    q: 'How do I explore student clusters?',
    a: 'Open Clusters for ENSIA profiles, or ML Lab for k-selection charts. Click any cluster card to filter the student table.',
  },
  {
    q: 'What does at-risk mean?',
    a: 'Risk combines cluster assignment with engagement metrics from notebook 08. High and Critical levels suggest intervention.',
  },
  {
    q: 'How is k selected?',
    a: 'Notebook 03 runs elbow, silhouette, and Davies–Bouldin sweeps. The dashboard recommends k=3 for interpretable ENSIA archetypes.',
  },
  {
    q: 'When will other algorithms appear?',
    a: 'Hierarchical, DBSCAN, and GMM slots are in ML Lab — connect the FastAPI backend when notebooks 04–06 are complete.',
  },
]

interface HelpPanelProps {
  open: boolean
  onClose: () => void
}

export function HelpPanel({ open, onClose }: HelpPanelProps) {
  const { navigate, navigateToModels } = useApp()

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  return (
    <>
      <button
        type="button"
        className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm"
        aria-label="Close help"
        onClick={onClose}
      />
      <aside
        className="fixed inset-y-0 right-0 z-[70] flex w-full max-w-md flex-col border-l border-white/10 bg-[#1C1718] shadow-2xl"
        role="dialog"
        aria-label="Help and support"
      >
        <div className="flex items-center justify-between border-b border-white/5 px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-[#FE981E]/15 p-2.5">
              <HelpCircle className="size-5 text-[#FE981E]" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Help Center</h2>
              <p className="text-xs text-[#D9D9D9]/60">ENSIA·Insight dashboard guide</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-[#D9D9D9]/50 hover:bg-white/5 hover:text-white"
            aria-label="Close help panel"
          >
            <X className="size-5" />
          </button>
        </div>

        <div className="custom-scrollbar flex-1 overflow-y-auto px-6 py-5">
          <section className="mb-6">
            <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-[#FE981E]">
              <BookOpen className="size-4" />
              Quick start
            </h3>
            <p className="text-sm leading-relaxed text-[#D9D9D9]/80">
              Upload OULAD CSVs, run the ML pipeline in ML Lab, review clusters and at-risk students,
              then configure alerts in Settings.
            </p>
            <Button
              className="mt-4 bg-[#FE981E] text-white hover:bg-[#E08918]"
              onClick={() => {
                onClose()
                navigate('overview')
              }}
            >
              Go to Overview
            </Button>
          </section>

          <section className="mb-6">
            <h3 className="mb-3 text-sm font-semibold text-white">FAQ</h3>
            <ul className="space-y-3">
              {FAQ.map((item) => (
                <li
                  key={item.q}
                  className="rounded-xl border border-white/[0.06] bg-[#252025] p-4"
                >
                  <p className="text-sm font-medium text-white">{item.q}</p>
                  <p className="mt-1.5 text-xs leading-relaxed text-[#D9D9D9]/70">{item.a}</p>
                </li>
              ))}
            </ul>
          </section>

          <section className="mb-6">
            <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-white">
              <Keyboard className="size-4 text-[#9A9099]" />
              Shortcuts
            </h3>
            <ul className="space-y-2 text-xs text-[#D9D9D9]/70">
              <li className="flex justify-between rounded-lg bg-white/5 px-3 py-2">
                <span>Close panels</span>
                <kbd className="rounded bg-[#1C1718] px-2 py-0.5 text-[#FE981E]">Esc</kbd>
              </li>
            </ul>
          </section>

          <section>
            <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-white">
              <Mail className="size-4 text-[#9A9099]" />
              Support
            </h3>
            <p className="text-xs text-[#D9D9D9]/60">
              For pipeline issues, check notebooks 00–08 in the repo. For demo day, use ML Lab to
              walk through k-selection live.
            </p>
            <Button
              variant="ghost"
              className="mt-3 text-[#FE981E] hover:bg-[#FE981E]/10"
              onClick={() => {
                onClose()
                navigateToModels()
              }}
            >
              Open ML Lab →
            </Button>
          </section>
        </div>
      </aside>
    </>
  )
}

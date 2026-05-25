import { useEffect } from 'react'
import { ArrowUpRight, BookOpen } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ASSETS } from '@/constants/design'
import { useApp } from '@/context/AppContext'

export function WelcomePage() {
  const { dismissWelcome } = useApp()

  useEffect(() => {
    document.documentElement.classList.add('welcome-active')
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault()
        dismissWelcome()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => {
      document.documentElement.classList.remove('welcome-active')
      window.removeEventListener('keydown', onKey)
    }
  }, [dismissWelcome])

  return (
    <div className="welcome-screen fixed inset-0 z-[100] h-dvh w-full overflow-y-auto overflow-x-hidden bg-[#1C1718] custom-scrollbar">
      <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-20">
        <div className="h-[min(70vh,600px)] w-[min(70vh,600px)] rounded-full bg-[#FE981E] blur-[200px]" />
      </div>
      <div className="pointer-events-none fixed inset-0 flex items-center justify-center opacity-10">
        <div className="h-[min(45vh,400px)] w-[min(45vh,400px)] translate-x-24 -translate-y-24 rounded-full bg-[#D9D9D9] blur-[150px] sm:translate-x-48" />
      </div>

      <div className="relative z-10 mx-auto flex min-h-dvh w-full max-w-5xl flex-col items-center justify-center px-4 py-8 text-center sm:px-8 sm:py-10">
        <div className="mb-5 w-full max-w-[420px] shrink-0 sm:mb-6 sm:max-w-[480px]">
          <img
            src={ASSETS.welcomeHero}
            alt="Student learning"
            className="mx-auto h-auto max-h-[22vh] w-full object-contain drop-shadow-2xl sm:max-h-[28vh] md:max-h-[32vh]"
          />
        </div>

        <div className="mb-3 flex shrink-0 flex-col items-center gap-3 sm:mb-4 sm:flex-row sm:gap-4">
          <div className="rounded-[20px] bg-[#FE981E] p-3 sm:p-3.5">
            <BookOpen className="size-7 text-white sm:size-8" aria-hidden />
          </div>
          <h1 className="text-3xl font-black tracking-tight text-white sm:text-4xl md:text-5xl lg:text-6xl">
            ENSIA<span className="text-[#FE981E]">·</span>Insight
          </h1>
        </div>

        <p className="mb-2 shrink-0 text-base font-semibold text-[#D9D9D9] sm:mb-3 sm:text-xl md:text-2xl">
          ML-Powered Learning Analytics Platform
        </p>

        <p className="mb-6 max-w-2xl shrink-0 text-sm leading-relaxed text-[#D9D9D9]/80 sm:mb-8 sm:text-base md:text-lg">
          Visualize student engagement patterns, identify at-risk learners, and track behavioral
          clusters with advanced machine learning insights.
        </p>

        <Button
          type="button"
          onClick={dismissWelcome}
          className="shrink-0 rounded-xl bg-[#FE981E] px-10 py-5 text-base font-bold text-white shadow-2xl transition-all hover:scale-[1.02] hover:bg-[#E08918] sm:px-14 sm:py-6 sm:text-lg"
        >
          Start Exploring
          <ArrowUpRight className="ml-2 size-5" aria-hidden />
        </Button>

        <p className="mt-4 shrink-0 pb-2 text-xs text-[#D9D9D9]/40 sm:mt-5">Press Enter to continue</p>
      </div>
    </div>
  )
}

import {
  Bell,
  Database,
  FlaskConical,
  Monitor,
  RefreshCw,
  RotateCcw,
  Server,
} from 'lucide-react'
import { DashboardCard } from '@/components/common/DashboardCard'
import { PageHeader } from '@/components/common/PageHeader'
import { Button } from '@/components/ui/button'
import { CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { TOTAL_STUDENTS } from '@/constants/design'
import { useApp } from '@/context/AppContext'
import { useSettings } from '@/hooks/useSettings'

export function SettingsPage() {
  const { settings, update, reset } = useSettings()
  const { navigateToModels } = useApp()

  return (
    <div className="space-y-6">
      <PageHeader
        title="Settings"
        description="Dashboard preferences, API connection, and pipeline defaults"
        action={
          <Button
            variant="ghost"
            className="text-[#D9D9D9] hover:text-white"
            onClick={reset}
          >
            <RotateCcw className="mr-2 size-4" />
            Reset defaults
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <DashboardCard>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Bell className="size-5 text-[#FE981E]" />
              Notifications
            </CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              Alerts for at-risk students and pipeline jobs
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <SettingToggle
              label="Email notifications"
              description="Daily digest for high / critical risk clusters"
              checked={settings.emailNotifications}
              onCheckedChange={(v) => update('emailNotifications', v)}
            />
            <SettingToggle
              label="Auto-refresh dashboard"
              description={`Reload data every ${settings.refreshIntervalMin} minutes`}
              checked={settings.autoRefresh}
              onCheckedChange={(v) => update('autoRefresh', v)}
            />
            {settings.autoRefresh && (
              <div className="flex items-center gap-3 pl-1">
                <RefreshCw className="size-4 text-[#9A9099]" />
                <label className="text-sm text-[#D9D9D9]">
                  Interval (minutes)
                  <Input
                    type="number"
                    min={1}
                    max={60}
                    value={settings.refreshIntervalMin}
                    onChange={(e) =>
                      update('refreshIntervalMin', Number(e.target.value) || 5)
                    }
                    className="mt-1 w-24 border-white/10 bg-white/5 text-white"
                  />
                </label>
              </div>
            )}
          </CardContent>
        </DashboardCard>

        <DashboardCard>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Server className="size-5 text-[#FE981E]" />
              API & Data
            </CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              Connect to FastAPI backend when ready (see web/backend)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <SettingToggle
              label="Use mock data"
              description="Load from src/data/mock until backend is live"
              checked={settings.useMockApi}
              onCheckedChange={(v) => update('useMockApi', v)}
            />
            <div>
              <label className="text-sm font-medium text-white">API base URL</label>
              <p className="mb-2 text-xs text-[#D9D9D9]/60">
                Proxied via Vite to localhost:8000 when using /api
              </p>
              <Input
                value={settings.apiBaseUrl}
                onChange={(e) => update('apiBaseUrl', e.target.value)}
                className="border-white/10 bg-white/5 text-white"
                placeholder="/api"
              />
            </div>
            <Button
              variant="outline"
              className="w-full border-white/10 text-[#D9D9D9] hover:bg-white/5"
              onClick={() => navigateToModels()}
            >
              <FlaskConical className="mr-2 size-4" />
              View ML pipeline status
            </Button>
          </CardContent>
        </DashboardCard>

        <DashboardCard>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Database className="size-5 text-[#FE981E]" />
              Clustering defaults
            </CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              Production model from notebook 03
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label htmlFor="algo-select" className="text-sm font-medium text-white">
                Primary algorithm
              </label>
              <select
                id="algo-select"
                value={settings.defaultAlgorithm}
                onChange={(e) => update('defaultAlgorithm', e.target.value)}
                className="mt-2 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white outline-none focus:border-[#FE981E]"
              >
                <option value="kmeans" className="bg-[#252025]">
                  K-Means (active)
                </option>
                <option value="hierarchical" className="bg-[#252025]" disabled>
                  Hierarchical (coming soon)
                </option>
                <option value="dbscan" className="bg-[#252025]" disabled>
                  DBSCAN (coming soon)
                </option>
                <option value="gmm" className="bg-[#252025]" disabled>
                  GMM (coming soon)
                </option>
              </select>
            </div>
            <p className="rounded-xl bg-[#FE981E]/10 p-3 text-xs text-[#D9D9D9]">
              Selected k=<strong className="text-[#FE981E]">3</strong> · 17 features ·
              Manhattan (L1) distance · artifacts in <code className="text-[#FE981E]">models/</code>
            </p>
          </CardContent>
        </DashboardCard>

        <DashboardCard>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Monitor className="size-5 text-[#FE981E]" />
              Display
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <SettingToggle
              label="Compact tables"
              description="Denser rows on student list"
              checked={settings.compactTables}
              onCheckedChange={(v) => update('compactTables', v)}
            />
            <SettingToggle
              label="Pipeline hints"
              description="Show notebook references in ML Lab"
              checked={settings.showPipelineHints}
              onCheckedChange={(v) => update('showPipelineHints', v)}
            />
          </CardContent>
        </DashboardCard>
      </div>

      <DashboardCard className="max-w-3xl">
        <CardHeader>
          <CardTitle className="text-white">About ENSIA·Insight</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-[#D9D9D9]/70 space-y-2">
          <p>
            OULAD student learning behavior clustering — notebooks 00–08, primary K-Means model,
            ENSIA risk profiling for demo day.
          </p>
          <p className="text-xs text-[#9A9099]">
            Frontend v0.1 · Mock API {settings.useMockApi ? 'enabled' : 'disabled'} · Cohort n=
            {TOTAL_STUDENTS.toLocaleString()}
          </p>
        </CardContent>
      </DashboardCard>
    </div>
  )
}

function SettingToggle({
  label,
  description,
  checked,
  onCheckedChange,
}: {
  label: string
  description: string
  checked: boolean
  onCheckedChange: (v: boolean) => void
}) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-white/5 pb-4 last:border-0 last:pb-0">
      <div>
        <p className="font-medium text-white">{label}</p>
        <p className="text-sm text-[#D9D9D9]/60">{description}</p>
      </div>
      <Switch checked={checked} onCheckedChange={onCheckedChange} aria-label={label} />
    </div>
  )
}

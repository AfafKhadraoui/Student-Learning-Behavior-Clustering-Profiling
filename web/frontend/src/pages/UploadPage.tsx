import { useCallback, useEffect, useState } from 'react'
import { CheckCircle2, FileText, Upload, X } from 'lucide-react'
import { DashboardCard } from '@/components/common/DashboardCard'
import { LoadingState } from '@/components/common/LoadingState'
import { PageHeader } from '@/components/common/PageHeader'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useApp } from '@/context/AppContext'
import { fetchCsvFileStatus, processUploadedFiles } from '@/services/uploadService'
import type { CsvFile } from '@/types/dashboard'
import { getCsvStatusClass } from '@/utils/cluster'

const REQUIRED_FILES = [
  'studentInfo.csv',
  'studentAssessment.csv',
  'assessments.csv',
  'courses.csv',
  'studentRegistration.csv',
  'studentVle.csv',
  'vle.csv',
]

export function UploadPage() {
  const { navigateToModels } = useApp()
  const [files, setFiles] = useState<CsvFile[]>([])
  const [loading, setLoading] = useState(true)
  const [processing, setProcessing] = useState(false)
  const [uploadedNames, setUploadedNames] = useState<string[]>([])
  const [dragOver, setDragOver] = useState(false)
  const [processMessage, setProcessMessage] = useState<string | null>(null)

  useEffect(() => {
    fetchCsvFileStatus()
      .then(setFiles)
      .finally(() => setLoading(false))
  }, [])

  const handleFiles = useCallback((fileList: FileList | null) => {
    if (!fileList) return
    const names = Array.from(fileList)
      .filter((f) => f.name.endsWith('.csv'))
      .map((f) => f.name)
    if (names.length) {
      setUploadedNames((prev) => [...new Set([...prev, ...names])])
      setProcessMessage(null)
    }
  }, [])

  const handleProcess = async () => {
    setProcessing(true)
    setProcessMessage(null)
    try {
      const result = await processUploadedFiles()
      setProcessMessage(
        `Pipeline job queued (ID: ${result.jobId}). Connect backend to run notebook 00 pipeline.`,
      )
    } catch {
      setProcessMessage('Processing started in mock mode. Connect backend for real ingestion.')
    } finally {
      setProcessing(false)
    }
  }

  const readyCount = files.filter((f) => f.status === 'ready').length + uploadedNames.length

  return (
    <div className="space-y-6">
      <PageHeader
        title="Upload Data"
        description="Upload the 7 OULAD CSV files — same inputs as notebook 00_data_engineering"
        action={
          <Button
            variant="ghost"
            className="text-[#FE981E] hover:bg-[#FE981E]/10"
            onClick={() => navigateToModels()}
          >
            View pipeline →
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatPill label="Required" value={REQUIRED_FILES.length} />
        <StatPill label="Ready" value={readyCount} accent />
        <StatPill label="Missing" value={Math.max(0, REQUIRED_FILES.length - readyCount)} warn />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <DashboardCard>
          <CardHeader>
            <CardTitle className="text-lg text-white sm:text-xl">Drag & Drop Files</CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              Drop OULAD CSVs or click to browse
            </CardDescription>
          </CardHeader>
          <CardContent>
            <label className="block cursor-pointer">
              <input
                type="file"
                accept=".csv"
                multiple
                className="sr-only"
                aria-label="Upload CSV files"
                onChange={(e) => handleFiles(e.target.files)}
              />
              <div
                className={`rounded-xl border-2 border-dashed p-8 text-center transition-all sm:p-12 ${
                  dragOver
                    ? 'border-[#FE981E] bg-[#FE981E]/10'
                    : 'border-white/20 hover:border-[#FE981E] hover:bg-[#FE981E]/5'
                }`}
                onDragOver={(e) => {
                  e.preventDefault()
                  setDragOver(true)
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault()
                  setDragOver(false)
                  handleFiles(e.dataTransfer.files)
                }}
              >
                <Upload className="mx-auto mb-4 size-10 text-[#D9D9D9]/50 sm:size-12" aria-hidden />
                <p className="mb-2 font-medium text-white">Drop files here or click to browse</p>
                <p className="text-sm text-[#D9D9D9]/60">Supported: CSV only</p>
              </div>
            </label>
            {uploadedNames.length > 0 && (
              <ul className="mt-4 space-y-2">
                {uploadedNames.map((name) => (
                  <li
                    key={name}
                    className="flex items-center justify-between rounded-lg bg-[#34D399]/10 px-3 py-2 text-sm text-[#34D399]"
                  >
                    <span className="flex items-center gap-2 truncate">
                      <CheckCircle2 className="size-4 shrink-0" />
                      {name}
                    </span>
                    <button
                      type="button"
                      aria-label={`Remove ${name}`}
                      onClick={() => setUploadedNames((prev) => prev.filter((n) => n !== name))}
                      className="shrink-0 text-[#D9D9D9]/50 hover:text-white"
                    >
                      <X className="size-4" />
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </DashboardCard>

        <DashboardCard>
          <CardHeader>
            <CardTitle className="text-lg text-white sm:text-xl">File Status</CardTitle>
            <CardDescription className="text-[#D9D9D9]/60">
              7 OULAD CSV files required for master_raw.csv
            </CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <LoadingState label="Checking files..." />
            ) : (
              <>
                <ul className="space-y-3">
                  {files.map((file) => {
                    const justUploaded = uploadedNames.includes(file.name)
                    const status = justUploaded ? 'ready' : file.status
                    return (
                      <li
                        key={file.name}
                        className="flex items-center justify-between gap-3 rounded-xl border border-white/5 bg-white/5 p-3 transition-all hover:border-white/10"
                      >
                        <div className="flex min-w-0 items-center gap-3">
                          <FileText className="size-4 shrink-0 text-[#D9D9D9]/50" aria-hidden />
                          <div className="min-w-0">
                            <p className="truncate text-sm font-medium text-white">{file.name}</p>
                            <p className="text-xs text-[#D9D9D9]/60">{file.size}</p>
                          </div>
                        </div>
                        <Badge
                          variant="outline"
                          className={`shrink-0 text-xs capitalize ${getCsvStatusClass(status)}`}
                        >
                          {justUploaded ? 'uploaded' : status}
                        </Badge>
                      </li>
                    )
                  })}
                </ul>
                {processMessage && (
                  <p className="mt-4 rounded-lg bg-[#FE981E]/10 p-3 text-sm text-[#FE981E]">
                    {processMessage}
                  </p>
                )}
                <Button
                  className="mt-6 w-full bg-[#FE981E] font-bold text-white hover:bg-[#E08918]"
                  disabled={processing}
                  onClick={handleProcess}
                >
                  {processing ? 'Processing...' : 'Process Files'}
                </Button>
              </>
            )}
          </CardContent>
        </DashboardCard>
      </div>
    </div>
  )
}

function StatPill({
  label,
  value,
  accent,
  warn,
}: {
  label: string
  value: number
  accent?: boolean
  warn?: boolean
}) {
  return (
    <div className="rounded-xl border border-white/[0.06] bg-[#252025] px-4 py-3 text-center">
      <p className="text-xs text-[#9A9099]">{label}</p>
      <p
        className={`text-2xl font-black ${
          accent ? 'text-[#34D399]' : warn ? 'text-[#F87171]' : 'text-white'
        }`}
      >
        {value}
      </p>
    </div>
  )
}

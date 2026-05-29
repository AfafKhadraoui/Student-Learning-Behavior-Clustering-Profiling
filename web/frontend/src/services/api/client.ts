const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/$/, '')

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers ?? {})
  headers.set('Accept', 'application/json')

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
  })

  if (!response.ok) {
    throw new ApiError(`Request failed: ${path}`, response.status)
  }

  return response.json() as Promise<T>
}

export async function apiGet<T>(path: string): Promise<T> {
  return requestJson<T>(path)
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  return requestJson<T>(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
}

export const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true'

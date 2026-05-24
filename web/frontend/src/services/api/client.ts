const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '/api'

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { Accept: 'application/json' },
  })

  if (!response.ok) {
    throw new ApiError(`Request failed: ${path}`, response.status)
  }

  return response.json() as Promise<T>
}

export const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API !== 'false'

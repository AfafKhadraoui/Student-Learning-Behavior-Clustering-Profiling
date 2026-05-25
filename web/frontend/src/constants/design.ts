export const COLORS = {
  background: '#1C1718',
  sidebar: '#0F123F',
  card: '#252025',
  cardBorder: 'rgba(255,255,255,0.06)',
  accent: '#FE981E',
  accentHover: '#E08918',
  text: '#FFFFFF',
  textSecondary: '#D9D9D9',
  muted: '#9A9099',
  label: '#5C5760',
} as const

export const CLUSTER_COLORS: Record<string, string> = {
  'Engaged Last-Minute Learners': '#FE981E',
  'Last-Minute (On-Track)': '#FE981E',
  'Struggling Students': '#F87171',
  Struggling: '#F87171',
  'Disengaged / Withdrawn': '#6B7280',
  Disengaged: '#6B7280',
  'High Performer': '#34D399',
  'Consistent Learner': '#60A5FA',
  'Last-Minute': '#FE981E',
}

export const TOTAL_STUDENTS = 32593

export const ASSETS = {
  welcomeHero: '/images/welcome-hero.png',
} as const

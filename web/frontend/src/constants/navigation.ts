import {
  BarChart3,
  FlaskConical,
  LayoutDashboard,
  Settings,
  Upload,
  Users,
  type LucideIcon,
} from 'lucide-react'

export type NavId =
  | 'overview'
  | 'clusters'
  | 'students'
  | 'models'
  | 'upload'
  | 'settings'

export interface NavItem {
  id: NavId
  label: string
  icon: LucideIcon
}

export const NAV_ITEMS: NavItem[] = [
  { id: 'overview', icon: LayoutDashboard, label: 'Overview' },
  { id: 'clusters', icon: BarChart3, label: 'Clusters' },
  { id: 'students', icon: Users, label: 'Students' },
  { id: 'models', icon: FlaskConical, label: 'ML Lab' },
  { id: 'upload', icon: Upload, label: 'Upload' },
  { id: 'settings', icon: Settings, label: 'Settings' },
]

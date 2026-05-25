export type NotificationType = 'alert' | 'info' | 'success'

export interface AppNotification {
  id: string
  type: NotificationType
  title: string
  message: string
  time: string
  read: boolean
  actionLabel?: string
  actionNav?: 'students' | 'models' | 'clusters'
}

export interface HelpItem {
  question: string
  answer: string
}

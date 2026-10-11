import type { ReactNode } from 'react'
import { connection } from 'next/server'
import { ApiAccessProvider, loadApiSetting } from '@/api'
import { autoDirection } from '@/theme/theme'
import '@/theme/theme.css'

export const metadata = { title: 'Trading Assistant' }

export default async function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  // The API address is a runtime setting, so it is read for every request.
  await connection()
  const setting = loadApiSetting()
  return (
    <html lang="en" {...autoDirection}>
      <body>
        <ApiAccessProvider
          {...('address' in setting
            ? { baseUrl: setting.address.baseUrl }
            : { problem: setting.problem })}
        >
          {children}
        </ApiAccessProvider>
      </body>
    </html>
  )
}

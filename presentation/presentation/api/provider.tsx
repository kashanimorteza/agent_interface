'use client'

import { createContext, useContext, useMemo, type ReactNode } from 'react'
import { createApiClient, type ApiClient } from './calls.ts'

/** What Interaction Logic receives from API Access: the calls, or the reason there are none. */
export type ApiAccess =
  | { readonly status: 'ready'; readonly client: ApiClient }
  | { readonly status: 'misconfigured'; readonly problem: string }

const Context = createContext<ApiAccess | null>(null)

type ProviderProps = {
  /** The complete Base URL of the API; absent when the setting is not usable. */
  readonly baseUrl?: string
  /** Why the setting is not usable. */
  readonly problem?: string
  readonly children: ReactNode
}

export function ApiAccessProvider({
  baseUrl,
  problem,
  children,
}: ProviderProps) {
  const access = useMemo<ApiAccess>(
    () =>
      baseUrl === undefined
        ? {
            status: 'misconfigured',
            problem: problem ?? 'The API address is not set.',
          }
        : { status: 'ready', client: createApiClient({ baseUrl }) },
    [baseUrl, problem],
  )
  return <Context value={access}>{children}</Context>
}

export function useApiAccess(): ApiAccess {
  const access = useContext(Context)
  if (access === null) {
    throw new Error('API Access is used outside its provider.')
  }
  return access
}

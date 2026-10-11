import { useCallback, useRef, useState } from 'react'
import type { ApiResult } from '@/api'
import type { Failure } from './failure'

/** The call of the Endpoint that removes every record of one Entity. */
export type RemoveAllCall = () => Promise<ApiResult<unknown>>

/** Where removing every record of an Entity stands, for the interface to present. */
export type RemoveAllState =
  | { readonly status: 'idle' }
  /** Waiting for the user's confirmation; nothing has been sent. */
  | { readonly status: 'confirming'; readonly question: string }
  | { readonly status: 'working' }
  /** Every record is gone; the user sees no records. */
  | { readonly status: 'done' }
  /** The request failed as the API returned; what the user sees is unchanged. */
  | { readonly status: 'failed'; readonly failure: Failure }

export type RemoveAll = {
  readonly state: RemoveAllState
  /** Asks for confirmation; nothing is sent until `confirm`. */
  readonly request: () => void
  readonly confirm: () => void
  readonly cancel: () => void
  readonly dismiss: () => void
}

/**
 * The flow of removing every record of one Entity. It asks first, with a
 * question that names the Entity; only a confirmation calls the Endpoint; after
 * a success `onChanged` lets the owner refresh what the user sees; a failure is
 * held as returned and `onChanged` is not called.
 */
export function useRemoveAll(
  entity: string,
  call: RemoveAllCall,
  onChanged: () => void,
): RemoveAll {
  const [state, setState] = useState<RemoveAllState>({ status: 'idle' })
  const sending = useRef(false)

  const run = useCallback(async () => {
    sending.current = true
    setState({ status: 'working' })
    const result = await call().finally(() => {
      sending.current = false
    })
    if (!result.ok) {
      setState({ status: 'failed', failure: result.failure })
      return
    }
    onChanged()
    setState({ status: 'done' })
  }, [call, onChanged])

  return {
    state,
    request: () =>
      setState({
        status: 'confirming',
        question: `Remove every ${entity} record? This cannot be undone.`,
      }),
    confirm: () => {
      if (state.status === 'confirming' && !sending.current) void run()
    },
    cancel: () => {
      if (state.status === 'confirming') setState({ status: 'idle' })
    },
    dismiss: () => {
      if (state.status === 'done' || state.status === 'failed') {
        setState({ status: 'idle' })
      }
    },
  }
}

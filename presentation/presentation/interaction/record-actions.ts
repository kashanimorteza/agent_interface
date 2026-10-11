import { useCallback, useState } from 'react'
import type { ApiResult } from '@/api'
import type { FieldDescription } from './fields'
import type { Failure } from './failure'
import { recordOf, type RecordState } from './record'

export type RecordAction = 'enable' | 'disable' | 'delete'

type IdCall = (args: { id: number }) => Promise<ApiResult<unknown>>

/** The calls of the three actions on one record. */
export type RecordActionCalls = {
  readonly enable: IdCall
  readonly disable: IdCall
  readonly delete: IdCall
}

/** Where an action on a record stands, for the interface to present. */
export type ActionState =
  | { readonly status: 'idle' }
  /** A delete waits for the user's confirmation; nothing has been sent. */
  | {
      readonly status: 'confirming'
      readonly action: 'delete'
      readonly id: number
    }
  | {
      readonly status: 'working'
      readonly action: RecordAction
      readonly id: number
    }
  /** The action succeeded; an enabled or disabled record is given in its new state, a deleted one is gone. */
  | {
      readonly status: 'done'
      readonly action: RecordAction
      readonly id: number
      readonly record: RecordState
    }
  /** The action failed as the API returned; what the user sees is unchanged. */
  | {
      readonly status: 'failed'
      readonly action: RecordAction
      readonly id: number
      readonly failure: Failure
    }

export type RecordActions = {
  readonly state: ActionState
  readonly enable: (id: number) => void
  readonly disable: (id: number) => void
  /** Asks for confirmation; nothing is sent until `confirm`. */
  readonly requestDelete: (id: number) => void
  readonly confirm: () => void
  readonly cancel: () => void
  readonly dismiss: () => void
}

/**
 * The flow of enabling, disabling and deleting one record. Each action calls
 * only its own Endpoint for the chosen record; a delete waits for
 * confirmation; after a success `onChanged` lets the owner refresh what the
 * user sees; a failure is held as returned.
 */
export function useRecordActions(
  calls: RecordActionCalls,
  fields: readonly FieldDescription[],
  onChanged: () => void,
): RecordActions {
  const [state, setState] = useState<ActionState>({ status: 'idle' })

  const run = useCallback(
    async (action: RecordAction, id: number) => {
      setState({ status: 'working', action, id })
      const result = await calls[action]({ id })
      if (!result.ok) {
        setState({ status: 'failed', action, id, failure: result.failure })
        return
      }
      onChanged()
      setState({
        status: 'done',
        action,
        id,
        record:
          action === 'delete' ? { status: 'absent' } : recordOf(result, fields),
      })
    },
    [calls, fields, onChanged],
  )

  return {
    state,
    enable: (id) => void run('enable', id),
    disable: (id) => void run('disable', id),
    requestDelete: (id) =>
      setState({ status: 'confirming', action: 'delete', id }),
    confirm: () => {
      if (state.status === 'confirming') void run(state.action, state.id)
    },
    cancel: () => {
      if (state.status === 'confirming') setState({ status: 'idle' })
    },
    dismiss: () => setState({ status: 'idle' }),
  }
}

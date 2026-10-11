import { useCallback, useState } from 'react'
import {
  recordFromWire,
  TranslationError,
  type ApiResult,
  type FieldKinds,
  type RecordValues,
} from '@/api'
import { useLoaded } from './async'
import type { FieldDescription } from './fields'
import type { Failure } from './failure'

/** What the interface holds about one record it asked for. */
export type RecordState =
  | { readonly status: 'idle' }
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly record: RecordValues }
  /** The API answered that there is no such record. */
  | { readonly status: 'absent' }
  | { readonly status: 'failed'; readonly failure: Failure }

export type GetCall = (args: { id: number }) => Promise<ApiResult<unknown>>

export function kindsOf(fields: readonly FieldDescription[]): FieldKinds {
  return Object.fromEntries(fields.map((field) => [field.name, field.kind]))
}

/** Reads the record an Endpoint answered with as interface data, or says why it cannot be. */
export function recordOf(
  result: ApiResult<unknown>,
  fields: readonly FieldDescription[],
): RecordState {
  if (!result.ok) return { status: 'failed', failure: result.failure }
  if (result.value === null) return { status: 'absent' }
  try {
    return {
      status: 'loaded',
      record: recordFromWire(kindsOf(fields), result.value),
    }
  } catch (error) {
    if (error instanceof TranslationError) {
      return {
        status: 'failed',
        failure: { kind: 'untranslatable', message: error.message },
      }
    }
    throw error
  }
}

/** Requests one record by its id. */
export async function loadRecord(
  get: GetCall,
  fields: readonly FieldDescription[],
  id: number,
): Promise<RecordState> {
  return recordOf(await get({ id }), fields)
}

/** The flow of presenting one record by its id, for any Entity whose call and Field descriptions it is given. */
export function useRecord(
  get: GetCall,
  fields: readonly FieldDescription[],
  id: number | null,
): RecordState & { readonly reload: () => void } {
  const [reloads, setReloads] = useState(0)
  const reload = useCallback(() => setReloads((count) => count + 1), [])
  const loaded = useLoaded(id === null ? null : `${id}:${reloads}`, () =>
    loadRecord(get, fields, id as number),
  )
  const state: RecordState =
    loaded.status === 'ready' ? loaded.value : { status: loaded.status }
  return { ...state, reload }
}

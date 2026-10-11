import { useRef, useState } from 'react'
import type { ApiResult } from '@/api'
import type { Failure } from './failure'
import {
  isEnterable,
  type FieldDescription,
  type FieldEntry,
  type FieldValue,
  type RecordValues,
} from './fields'
import { recordOf } from './record'

/** Whether the form adds a new record or edits one that exists. */
export type FormMode =
  | { readonly kind: 'add' }
  | { readonly kind: 'edit'; readonly record: RecordValues }

/** The call of an Endpoint that stores one record. */
export type SaveCall = (args: {
  entity: RecordValues
}) => Promise<ApiResult<unknown>>

export type FormOutcome =
  | { readonly ok: true; readonly record: RecordValues }
  | {
      readonly ok: false
      /** Why a Field's entry is not acceptable, by Field name. */
      readonly problems: Readonly<Record<string, string>>
    }

type Entries = Readonly<Record<string, FieldEntry>>

function isEmpty(field: FieldDescription, entry: FieldEntry): boolean {
  return (
    entry.state === 'empty' ||
    (entry.state === 'value' && field.kind === 'string' && entry.value === '')
  )
}

/**
 * Whether an entry leaves the value the record holds as it is. A value left as
 * held is not entered again; a sensitive value is never shown, so an empty
 * entry for it keeps what the record holds.
 */
function unchanged(
  field: FieldDescription,
  entry: FieldEntry,
  held: FieldValue,
): boolean {
  if (field.sensitive === true && entry.state === 'empty') return true
  return entry.state === 'value' && entry.value === held
}

/**
 * Reads what a user entered as the record to store, or says what is wrong
 * with it. Only requirement is checked here; every application rule is the
 * API's. A Field that cannot be entered is never taken from the entries: when
 * editing, the record keeps the value it holds, which the API needs to
 * identify and store it; when adding, there is none.
 */
export function recordFromEntries(
  fields: readonly FieldDescription[],
  mode: FormMode,
  entries: Entries,
): FormOutcome {
  const record: Record<string, FieldValue> = {}
  const problems: Record<string, string> = {}
  for (const field of fields) {
    if (!isEnterable(field)) {
      const held = mode.kind === 'edit' ? mode.record[field.name] : undefined
      if (held !== undefined) record[field.name] = held
      continue
    }
    const entry = entries[field.name] ?? { state: 'empty' }
    const held = mode.kind === 'edit' ? mode.record[field.name] : undefined
    if (entry.state === 'invalid') {
      problems[field.name] = 'Enter a valid value.'
    } else if (
      held !== undefined &&
      held !== null &&
      unchanged(field, entry, held)
    ) {
      record[field.name] = held
    } else if (entry.state === 'absent') {
      record[field.name] = null
    } else if (isEmpty(field, entry)) {
      if (field.required) {
        problems[field.name] = 'Enter a value.'
      } else {
        record[field.name] = null
      }
    } else if (entry.state === 'value') {
      record[field.name] = entry.value
    }
  }
  return Object.keys(problems).length > 0
    ? { ok: false, problems }
    : { ok: true, record }
}

/** Where storing a record stands, for the interface to present. */
export type FormState =
  | { readonly status: 'idle' }
  | { readonly status: 'saving' }
  /** The API stored the record and returned it. */
  | { readonly status: 'saved'; readonly record: RecordValues }
  /** The API answered that the record to update does not exist. */
  | { readonly status: 'absent' }
  /** The request failed as the API returned; what the user entered is kept. */
  | { readonly status: 'failed'; readonly failure: Failure }

export type RecordFormFlow = {
  readonly state: FormState
  /** Why an entry cannot be sent yet, by Field name. */
  readonly problems: Readonly<Record<string, string>>
  /** Checks the entries and, when they are complete, adds or updates the record. */
  readonly submit: (entries: Entries) => void
  /** Clears a held result or failure. */
  readonly dismiss: () => void
}

/**
 * The flow of the record form, for any Entity whose calls and Field
 * descriptions it is given: it adds a new record or updates the one being
 * edited, and after the API stores it `onSaved` lets the owner refresh what
 * the user sees. The API's result or error is held as returned.
 */
export function useRecordForm(
  fields: readonly FieldDescription[],
  mode: FormMode,
  calls: { readonly add: SaveCall; readonly update: SaveCall },
  onSaved: (record: RecordValues) => void,
): RecordFormFlow {
  const [state, setState] = useState<FormState>({ status: 'idle' })
  const [problems, setProblems] = useState<Readonly<Record<string, string>>>({})
  const sending = useRef(false)

  const send = async (entity: RecordValues) => {
    sending.current = true
    setState({ status: 'saving' })
    const result = await (mode.kind === 'add' ? calls.add : calls.update)({
      entity,
    }).finally(() => {
      sending.current = false
    })
    const stored = recordOf(result, fields)
    if (stored.status === 'loaded') {
      setState({ status: 'saved', record: stored.record })
      onSaved(stored.record)
    } else if (stored.status === 'failed') {
      setState({ status: 'failed', failure: stored.failure })
    } else {
      setState({ status: 'absent' })
    }
  }

  return {
    state,
    problems,
    submit: (entries) => {
      if (sending.current) return
      const outcome = recordFromEntries(fields, mode, entries)
      if (!outcome.ok) {
        setProblems(outcome.problems)
        return
      }
      setProblems({})
      void send(outcome.record)
    },
    dismiss: () => setState({ status: 'idle' }),
  }
}

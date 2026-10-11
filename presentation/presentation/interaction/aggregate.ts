import { useRef, useState } from 'react'
import {
  queryVocabulary,
  type ApiResult,
  type FilterCondition,
  type ValueKind,
} from '@/api'
import type { Failure } from './failure'
import type { FieldDescription, FieldValue } from './fields'
import { filterOf, noFilters, type FilterDraft } from './filter'

/** A counting or aggregate operation an Adapter offers and what it takes. */
export type AggregateOperation = {
  readonly name: string
  /** Present when the operation takes a Field: the Fields it can be given. */
  readonly fields?: readonly FieldDescription[]
  readonly takesFilters: boolean
}

/** The operation a user chose with its arguments. */
export type AggregateRequest = {
  readonly operation: string
  readonly field: string | null
  readonly filters: FilterDraft
}

/** The first operation offered, with the first Field it takes. */
export function firstRequest(
  operations: readonly AggregateOperation[],
): AggregateRequest | null {
  const operation = operations[0]
  if (operation === undefined) return null
  return {
    operation: operation.name,
    field: operation.fields?.[0]?.name ?? null,
    filters: noFilters,
  }
}

/** The request after another operation was chosen: arguments the new operation does not take are dropped. */
export function changeOperation(
  request: AggregateRequest,
  operation: AggregateOperation,
): AggregateRequest {
  const field =
    operation.fields === undefined
      ? null
      : (operation.fields.find((f) => f.name === request.field)?.name ??
        operation.fields[0]?.name ??
        null)
  return {
    operation: operation.name,
    field,
    filters: operation.takesFilters ? request.filters : noFilters,
  }
}

type Query = {
  filters?: readonly FilterCondition[]
  combination?: string
}

/** The call of the Endpoint that counts the records that match. */
export type CountCall = (args: Query) => Promise<ApiResult<unknown>>

/** The call of an Endpoint that gives one value computed from a Field of the records that match. */
export type FieldCall = (
  args: Query & { field: string },
) => Promise<ApiResult<unknown>>

/** The calls of the Endpoints that count or aggregate the records of one Entity; an operation the Adapter lacks is left out. */
export type AggregateCalls = Readonly<{
  count?: CountCall
  sum?: FieldCall
  min?: FieldCall
  max?: FieldCall
}>

const NUMERIC: ReadonlySet<ValueKind> = new Set(['integer', 'float', 'decimal'])

/**
 * The operations an Adapter offers and the Fields each can be given. A total
 * is offered for numeric Fields and a smallest or largest value for any Field
 * that can be compared (not a boolean), as the API states when it refuses
 * others. A sensitive Field is never offered, because the value of one would
 * be shown.
 */
export function operationsOf(
  calls: AggregateCalls,
  fields: readonly FieldDescription[],
): AggregateOperation[] {
  const visible = fields.filter((field) => field.sensitive !== true)
  const operations: AggregateOperation[] = []
  if (calls.count !== undefined) {
    operations.push({ name: 'count', takesFilters: true })
  }
  if (calls.sum !== undefined) {
    operations.push({
      name: 'sum',
      fields: visible.filter((field) => NUMERIC.has(field.kind)),
      takesFilters: true,
    })
  }
  for (const name of ['min', 'max'] as const) {
    if (calls[name] !== undefined) {
      operations.push({
        name,
        fields: visible.filter((field) => field.kind !== 'boolean'),
        takesFilters: true,
      })
    }
  }
  return operations
}

/** Where a count or aggregate stands, for the interface to present. */
export type AggregateState =
  | { readonly status: 'idle' }
  | { readonly status: 'loading' }
  /** The single value the operation gave. */
  | { readonly status: 'ready'; readonly value: FieldValue }
  | { readonly status: 'failed'; readonly failure: Failure }

export type Aggregate = {
  readonly operations: readonly AggregateOperation[]
  /** The choices as they stand; null when the Adapter offers no operation. */
  readonly request: AggregateRequest | null
  readonly setRequest: (request: AggregateRequest) => void
  /** One entry per Filter condition: why it is not complete, or null. */
  readonly problems: readonly (string | null)[]
  readonly state: AggregateState
  /** Asks for the result of the chosen operation; nothing is sent while a choice is incomplete. */
  readonly run: () => void
}

function singleValue(value: unknown): FieldValue | undefined {
  return value === null ||
    typeof value === 'number' ||
    typeof value === 'string' ||
    typeof value === 'boolean'
    ? value
    : undefined
}

/** Starts the request of one operation; nothing starts for an operation the Adapter lacks or one that needs a Field and has none. */
function ask(
  calls: AggregateCalls,
  operation: string,
  field: string | null,
  query: Query,
): Promise<ApiResult<unknown>> | undefined {
  if (operation === 'count') return calls.count?.(query)
  if (field === null) return undefined
  const call =
    operation === 'sum'
      ? calls.sum
      : operation === 'min'
        ? calls.min
        : operation === 'max'
          ? calls.max
          : undefined
  return call?.({ ...query, field })
}

/**
 * The flow of asking for a count or an aggregate of one Entity, for any
 * Entity whose calls and Field descriptions it is given. Only an operation
 * the Adapter offers can be chosen; the request carries exactly the
 * operation, its Field where it takes one, and the Filters chosen; the single
 * result, or the error as the API returned it, is held.
 */
export function useAggregate(
  calls: AggregateCalls,
  fields: readonly FieldDescription[],
): Aggregate {
  const operations = operationsOf(calls, fields)
  const [request, setRequest] = useState(() => firstRequest(operations))
  const [problems, setProblems] = useState<readonly (string | null)[]>([])
  const [state, setState] = useState<AggregateState>({ status: 'idle' })
  const sending = useRef(false)

  const run = async () => {
    const operation = operations.find((o) => o.name === request?.operation)
    if (request === null || operation === undefined || sending.current) return
    const outcome = filterOf(request.filters, fields, queryVocabulary.operators)
    if (!outcome.ok) {
      setProblems(outcome.problems)
      return
    }
    const query: Query = {
      ...(outcome.conditions.length > 0 && { filters: outcome.conditions }),
      ...(outcome.combination !== undefined && {
        combination: outcome.combination,
      }),
    }
    const pending = ask(calls, operation.name, request.field, query)
    if (pending === undefined) return
    setProblems([])
    sending.current = true
    setState({ status: 'loading' })
    const result = await pending.finally(() => {
      sending.current = false
    })
    if (!result.ok) {
      setState({ status: 'failed', failure: result.failure })
      return
    }
    const value = singleValue(result.value)
    setState(
      value === undefined
        ? {
            status: 'failed',
            failure: {
              kind: 'untranslatable',
              message: 'The result is not a single value.',
            },
          }
        : { status: 'ready', value },
    )
  }

  return {
    operations,
    request,
    setRequest,
    problems,
    state,
    run: () => void run(),
  }
}

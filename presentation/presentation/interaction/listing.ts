import { useState } from 'react'
import {
  queryVocabulary,
  recordFromWire,
  TranslationError,
  type ApiResult,
  type FilterCondition,
  type OrderTerm,
  type QueryVocabulary,
  type RecordValues,
} from '@/api'
import { useLoaded } from './async'
import type { Failure } from './failure'
import type { FieldDescription } from './fields'
import { filterOf, noFilters, type FilterDraft } from './filter'
import { limitOf, orderTermsOf, unordered, type OrderAndLimit } from './order'
import { kindsOf } from './record'

/** What a list is asked for; a choice the user did not make is left out. */
export type ListRequest = {
  readonly filters?: readonly FilterCondition[]
  readonly combination?: string
  readonly orders?: readonly OrderTerm[]
  readonly limit?: number
}

/** The call of the Endpoint that lists the records of one Entity. */
export type ListCall = (args: ListRequest) => Promise<ApiResult<unknown>>

/** What the interface holds about the list it asked for. */
export type ListState =
  | { readonly status: 'loading' }
  | { readonly status: 'loaded'; readonly records: readonly RecordValues[] }
  | { readonly status: 'failed'; readonly failure: Failure }

/** Requests a list and reads its records as interface data, or says why it cannot be. */
export async function loadList(
  list: ListCall,
  fields: readonly FieldDescription[],
  request: ListRequest,
): Promise<Exclude<ListState, { status: 'loading' }>> {
  const result = await list(request)
  if (!result.ok) return { status: 'failed', failure: result.failure }
  try {
    if (!Array.isArray(result.value)) {
      throw new TranslationError('A list is not a list of records.')
    }
    const kinds = kindsOf(fields)
    return {
      status: 'loaded',
      records: result.value.map((item) => recordFromWire(kinds, item)),
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

/** Why the choices cannot be applied yet. */
export type ListingProblems = {
  /** One entry per Filter condition: why it is not complete, or null. */
  readonly filters: readonly (string | null)[]
  readonly limit: string | null
}

const noProblems: ListingProblems = { filters: [], limit: null }

export type Listing = {
  readonly filter: FilterDraft
  readonly setFilter: (draft: FilterDraft) => void
  readonly orderAndLimit: OrderAndLimit
  readonly setOrderAndLimit: (value: OrderAndLimit) => void
  /** The operators, combinations and directions the API names; the choices offered are exactly these. */
  readonly vocabulary: QueryVocabulary
  readonly problems: ListingProblems
  readonly state: ListState
  /** Requests the list with the choices as they stand; nothing is sent while a choice is incomplete. */
  readonly apply: () => void
  /** Requests the list again with the choices last applied. */
  readonly refresh: () => void
}

type Applied = { readonly id: number; readonly request: ListRequest }

/**
 * The flow of listing the records of one Entity, for any Entity whose call and
 * Field descriptions it is given. The list is requested when the flow starts
 * with no choices, and again whenever the user applies their choices.
 */
export function useListing(
  list: ListCall,
  fields: readonly FieldDescription[],
): Listing {
  const [filter, setFilter] = useState<FilterDraft>(noFilters)
  const [orderAndLimit, setOrderAndLimit] = useState<OrderAndLimit>(unordered)
  const [problems, setProblems] = useState<ListingProblems>(noProblems)
  const [applied, setApplied] = useState<Applied>({ id: 0, request: {} })

  const loaded = useLoaded(String(applied.id), () =>
    loadList(list, fields, applied.request),
  )

  const apply = () => {
    const outcome = filterOf(filter, fields, queryVocabulary.operators)
    const limit = limitOf(orderAndLimit.limit)
    if (!outcome.ok || limit === null) {
      setProblems({
        filters: outcome.ok ? [] : outcome.problems,
        limit: limit === null ? 'Enter a whole number.' : null,
      })
      return
    }
    setProblems(noProblems)
    const orders = orderTermsOf(orderAndLimit.order)
    setApplied((current) => ({
      id: current.id + 1,
      request: {
        ...(outcome.conditions.length > 0 && { filters: outcome.conditions }),
        ...(outcome.combination !== undefined && {
          combination: outcome.combination,
        }),
        ...(orders.length > 0 && { orders }),
        ...(limit !== undefined && { limit }),
      },
    }))
  }

  return {
    filter,
    setFilter,
    orderAndLimit,
    setOrderAndLimit,
    vocabulary: queryVocabulary,
    problems,
    state: loaded.status === 'ready' ? loaded.value : { status: 'loading' },
    apply,
    refresh: () =>
      setApplied((current) => ({
        id: current.id + 1,
        request: current.request,
      })),
  }
}

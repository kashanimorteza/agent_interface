import { noFilters, type FilterDraft } from './filter'
import type { FieldDescription } from './fields'

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

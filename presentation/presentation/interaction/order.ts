import type { OrderTerm } from '@/api'
import type { FieldEntry } from './fields'

/** The Field a list is ordered by and the direction, as a user chose them. */
export type OrderChoice = {
  readonly field: string
  readonly direction: string
}

/** How a list is ordered and limited, as a user chose it; each choice can be cleared. */
export type OrderAndLimit = {
  readonly order: OrderChoice | null
  readonly limit: FieldEntry
}

export const unordered: OrderAndLimit = {
  order: null,
  limit: { state: 'empty' },
}

/** The Order terms a choice stands for. */
export function orderTermsOf(choice: OrderChoice | null): OrderTerm[] {
  return choice === null
    ? []
    : [{ field: choice.field, direction: choice.direction }]
}

/** The limit a choice stands for: a number, nothing when cleared, or null when what was typed is not a whole number. */
export function limitOf(entry: FieldEntry): number | undefined | null {
  if (entry.state === 'value' && typeof entry.value === 'number') {
    return entry.value
  }
  return entry.state === 'empty' || entry.state === 'absent' ? undefined : null
}

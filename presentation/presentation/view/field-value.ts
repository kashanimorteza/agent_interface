import type { FieldValue } from '@/interaction/fields'

/** A stored value as it is shown: exactly what the record holds, with a boolean as Yes or No. */
export function valueText(value: FieldValue): string {
  return typeof value === 'boolean' ? (value ? 'Yes' : 'No') : String(value)
}

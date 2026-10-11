import { valueFromWire, type FieldValue, type ValueKind } from '@/api'

/** The Field of another Entity that a related Field takes its value from. */
export type FieldRelation = {
  /** The Adapter that serves the related Entity. */
  readonly entity: string
  readonly field: string
}

/** What a Field is, as its Declaration in Model states it. */
export type FieldDescription = {
  readonly name: string
  /** What the Declaration says the Field is; it names the Field to the user. Absent when the Declaration gives none. */
  readonly description?: string
  readonly kind: ValueKind
  /** A value must be supplied; an optional Field may be left unset. */
  readonly required: boolean
  /** The value the Declaration gives when none is supplied; absent when it gives none. */
  readonly default?: FieldValue
  /** The value is a credential or otherwise secret: it can be entered but is never shown. */
  readonly sensitive?: boolean
  /** The value cannot be changed by a user once the record exists. */
  readonly immutable?: boolean
  /** Model supplies the value itself, so a user never enters it. */
  readonly generated?: boolean
  /** The Field takes its value from a record of another Entity. */
  readonly relation?: FieldRelation
}

/** A user enters a Field unless it is fixed once the record exists or Model supplies its value. */
export function isEnterable(field: FieldDescription): boolean {
  return field.immutable !== true && field.generated !== true
}

/** An operator of a Filter, how many values it takes, and the kinds of Field it applies to. */
export type OperatorDescription = {
  readonly name: string
  readonly value: 'none' | 'one' | 'many'
  /** Absent when the operator applies to a Field of any kind. */
  readonly kinds?: readonly ValueKind[]
}

/** What a user has entered for one Field. */
export type FieldEntry =
  | { readonly state: 'empty' }
  /** An optional Field deliberately left without a value, which is not the same as an empty text. */
  | { readonly state: 'absent' }
  | { readonly state: 'value'; readonly value: FieldValue }
  /** Text that is not in the form of its kind. */
  | { readonly state: 'invalid'; readonly text: string }

const INTEGER = /^[+-]?\d+$/

function parsed(kind: ValueKind, candidate: unknown, text: string): FieldEntry {
  try {
    return { state: 'value', value: valueFromWire(kind, candidate) }
  } catch {
    return { state: 'invalid', text }
  }
}

/** Reads what a user typed for a Field of the given kind as a value of that kind. */
export function parseFieldText(kind: ValueKind, text: string): FieldEntry {
  const trimmed = text.trim()
  switch (kind) {
    case 'string':
      return { state: 'value', value: text }
    case 'integer':
      return INTEGER.test(trimmed)
        ? parsed(kind, Number(trimmed), text)
        : trimmed === ''
          ? { state: 'empty' }
          : { state: 'invalid', text }
    case 'float':
      return trimmed === ''
        ? { state: 'empty' }
        : parsed(kind, Number(trimmed), text)
    case 'boolean':
      return trimmed === 'true' || trimmed === 'false'
        ? { state: 'value', value: trimmed === 'true' }
        : trimmed === ''
          ? { state: 'empty' }
          : { state: 'invalid', text }
    case 'decimal':
    case 'datetime':
    case 'uuid':
      return trimmed === '' ? { state: 'empty' } : parsed(kind, trimmed, text)
  }
}

/** The text a value is shown as when it is edited. */
export function fieldText(value: FieldValue | undefined): string {
  return value === undefined || value === null ? '' : String(value)
}

export type { FieldValue, RecordValues } from '@/api'

/** The value kinds the API publishes a transport form for. */
export type ValueKind =
  'string' | 'integer' | 'float' | 'decimal' | 'boolean' | 'datetime' | 'uuid'

/**
 * A Field value as interface data. A decimal, a datetime and a uuid are held
 * as their text, which is also their transport form, so no value is rounded.
 */
export type FieldValue = string | number | boolean | null

export class TranslationError extends Error {
  override name = 'TranslationError'
}

const DECIMAL = /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/
const DATETIME =
  /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})$/
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function refuse(kind: ValueKind): never {
  throw new TranslationError(`A value is not in the form of a ${kind}.`)
}

/**
 * Checks that a value has the form of its kind and returns it unchanged. The
 * same form holds on both sides of the API, so one check serves both
 * directions. A message names the kind, never the value.
 */
function conform(kind: ValueKind, value: unknown): FieldValue {
  if (value === null) return null
  switch (kind) {
    case 'string':
      return typeof value === 'string' ? value : refuse(kind)
    case 'integer':
      return typeof value === 'number' && Number.isSafeInteger(value)
        ? value
        : refuse(kind)
    case 'float':
      return typeof value === 'number' && Number.isFinite(value)
        ? value
        : refuse(kind)
    case 'boolean':
      return typeof value === 'boolean' ? value : refuse(kind)
    case 'decimal':
      return typeof value === 'string' && DECIMAL.test(value)
        ? value
        : refuse(kind)
    case 'datetime':
      return typeof value === 'string' && DATETIME.test(value)
        ? value
        : refuse(kind)
    case 'uuid':
      return typeof value === 'string' && UUID.test(value)
        ? value
        : refuse(kind)
  }
}

/** Interface data to the form the API receives. */
export function valueToWire(kind: ValueKind, value: FieldValue): FieldValue {
  return conform(kind, value)
}

/** The form the API sent to interface data. */
export function valueFromWire(kind: ValueKind, wire: unknown): FieldValue {
  return conform(kind, wire)
}

export type FieldKinds = Readonly<Record<string, ValueKind>>
export type RecordValues = Readonly<Record<string, FieldValue>>

function translateRecord(
  kinds: FieldKinds,
  record: Readonly<Record<string, unknown>>,
  convert: (kind: ValueKind, value: unknown) => FieldValue,
): RecordValues {
  const result: Record<string, FieldValue> = {}
  for (const [name, value] of Object.entries(record)) {
    const kind = kinds[name]
    if (kind === undefined) {
      throw new TranslationError(`A Field is not described: ${name}.`)
    }
    result[name] = convert(kind, value)
  }
  return result
}

/** A record as interface data to the Entity object the API receives. */
export function recordToWire(
  kinds: FieldKinds,
  record: RecordValues,
): RecordValues {
  return translateRecord(kinds, record, conform)
}

/** An Entity object the API sent to a record as interface data. */
export function recordFromWire(kinds: FieldKinds, wire: unknown): RecordValues {
  if (wire === null || typeof wire !== 'object' || Array.isArray(wire)) {
    throw new TranslationError('A record is not an object.')
  }
  return translateRecord(kinds, wire as Record<string, unknown>, conform)
}

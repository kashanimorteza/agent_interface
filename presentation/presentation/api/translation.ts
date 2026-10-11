import {
  TranslationError,
  type FieldValue,
  type RecordValues,
} from './values.ts'

/** One condition of a Filter as interface data; the operator is a name the API publishes. */
export type FilterCondition = {
  readonly field: string
  readonly operator: string
  /** Absent when the operator takes no value; a list when it takes several. */
  readonly value?: FieldValue | readonly FieldValue[]
}

/** One term of an Order as interface data; the direction is a name the API publishes. */
export type OrderTerm = {
  readonly field: string
  readonly direction?: string
}

/** The interface-data form of every Parameter the API publishes a transport form for. */
export type ParameterForms = {
  readonly entity: RecordValues
  readonly filters: readonly FilterCondition[]
  readonly orders: readonly OrderTerm[]
  readonly combination: string
  readonly field: string
  readonly instance: string
  readonly limit: number
  readonly id: number
}

function jsonValue(value: unknown): FieldValue {
  if (value === null) return null
  if (typeof value === 'string' || typeof value === 'boolean') return value
  if (typeof value === 'number' && Number.isFinite(value)) return value
  throw new TranslationError('A value cannot travel as JSON.')
}

function name(value: unknown, what: string): string {
  if (typeof value !== 'string' || value === '') {
    throw new TranslationError(`A ${what} must be a non-empty name.`)
  }
  return value
}

export function filterToWire(
  condition: FilterCondition,
): Record<string, unknown> {
  const wire: Record<string, unknown> = {
    field: name(condition.field, 'Filter Field'),
    operator: name(condition.operator, 'Filter operator'),
  }
  const { value } = condition
  if (value !== undefined) {
    wire.value = Array.isArray(value) ? value.map(jsonValue) : jsonValue(value)
  }
  return wire
}

export function orderToWire(term: OrderTerm): Record<string, unknown> {
  const wire: Record<string, unknown> = {
    field: name(term.field, 'Order Field'),
  }
  if (term.direction !== undefined)
    wire.direction = name(term.direction, 'Order direction')
  return wire
}

function integer(value: unknown, what: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value)) {
    throw new TranslationError(`A ${what} must be an integer.`)
  }
  return value
}

function recordToJson(record: unknown): Record<string, FieldValue> {
  if (record === null || typeof record !== 'object' || Array.isArray(record)) {
    throw new TranslationError('A record must be an object.')
  }
  const wire: Record<string, FieldValue> = {}
  for (const [field, value] of Object.entries(record))
    wire[field] = jsonValue(value)
  return wire
}

/**
 * Translates the value of one Parameter from interface data to the form the
 * API receives. A Parameter without a published transport form is refused, so
 * nothing travels in a form the API did not publish.
 */
export function parameterToWire(parameter: string, value: unknown): unknown {
  switch (parameter) {
    case 'entity':
      return recordToJson(value)
    case 'filters':
      if (!Array.isArray(value))
        throw new TranslationError('Filters must be a list.')
      return value.map((condition: FilterCondition) => filterToWire(condition))
    case 'orders':
      if (!Array.isArray(value))
        throw new TranslationError('Orders must be a list.')
      return value.map((term: OrderTerm) => orderToWire(term))
    case 'combination':
    case 'field':
    case 'instance':
      return name(value, parameter)
    case 'limit':
    case 'id':
      return integer(value, parameter)
    default:
      throw new TranslationError(
        `The Parameter ${parameter} has no published transport form.`,
      )
  }
}

/** Translates every given Parameter; a Parameter given as null or left out travels as such. */
export function argumentsToWire(
  args: Readonly<Record<string, unknown>>,
): Record<string, unknown> {
  const wire: Record<string, unknown> = {}
  for (const [parameter, value] of Object.entries(args)) {
    if (value === undefined) continue
    wire[parameter] = value === null ? null : parameterToWire(parameter, value)
  }
  return wire
}

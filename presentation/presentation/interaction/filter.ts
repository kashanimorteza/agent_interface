import type { FilterCondition } from '@/api'
import type {
  FieldDescription,
  FieldEntry,
  OperatorDescription,
} from './fields'

/** One condition of a Filter as a user is building it. */
export type ConditionDraft = {
  readonly field: string
  readonly operator: string
  /** The values entered: none, one or several, as the operator takes them. */
  readonly values: readonly FieldEntry[]
}

/** A Filter as a user is building it. */
export type FilterDraft = {
  readonly conditions: readonly ConditionDraft[]
  /** How several conditions combine; absent while there is at most one. */
  readonly combination: string | null
}

export const noFilters: FilterDraft = { conditions: [], combination: null }

/** The operators that apply to a Field of the given kind, in the order given. */
export function applicableOperators(
  operators: readonly OperatorDescription[],
  field: FieldDescription,
): OperatorDescription[] {
  return operators.filter(
    (operator) =>
      operator.kinds === undefined || operator.kinds.includes(field.kind),
  )
}

function valuesFor(operator: OperatorDescription | undefined): FieldEntry[] {
  return operator === undefined || operator.value === 'none'
    ? []
    : [{ state: 'empty' }]
}

/** A new condition on the first Field with the first operator that applies to it. */
export function newCondition(
  fields: readonly FieldDescription[],
  operators: readonly OperatorDescription[],
): ConditionDraft | null {
  const field = fields[0]
  if (field === undefined) return null
  const operator = applicableOperators(operators, field)[0]
  if (operator === undefined) return null
  return {
    field: field.name,
    operator: operator.name,
    values: valuesFor(operator),
  }
}

/** The condition after its Field was changed: the operator is kept when it still applies. */
export function changeField(
  condition: ConditionDraft,
  field: FieldDescription,
  operators: readonly OperatorDescription[],
): ConditionDraft {
  const applicable = applicableOperators(operators, field)
  const operator =
    applicable.find((candidate) => candidate.name === condition.operator) ??
    applicable[0]
  return {
    field: field.name,
    operator: operator?.name ?? '',
    values: valuesFor(operator),
  }
}

/** The condition after its operator was changed: values are kept only when the number they take is unchanged. */
export function changeOperator(
  condition: ConditionDraft,
  operator: OperatorDescription,
  previous: OperatorDescription | undefined,
): ConditionDraft {
  return {
    ...condition,
    operator: operator.name,
    values:
      previous?.value === operator.value
        ? condition.values
        : valuesFor(operator),
  }
}

export type FilterOutcome =
  | {
      readonly ok: true
      readonly conditions: readonly FilterCondition[]
      readonly combination: string | undefined
    }
  | {
      /** One entry per condition: why it is not complete, or null. */
      readonly ok: false
      readonly problems: readonly (string | null)[]
    }

function valueOf(entry: FieldEntry | undefined) {
  return entry !== undefined && entry.state === 'value' && entry.value !== null
    ? entry
    : null
}

/** The conditions a draft stands for, or what is missing from the ones that are incomplete. */
export function filterOf(
  draft: FilterDraft,
  fields: readonly FieldDescription[],
  operators: readonly OperatorDescription[],
): FilterOutcome {
  const problems: (string | null)[] = []
  const conditions: FilterCondition[] = []
  for (const condition of draft.conditions) {
    const field = fields.find((candidate) => candidate.name === condition.field)
    const operator = operators.find(
      (candidate) => candidate.name === condition.operator,
    )
    if (field === undefined || operator === undefined) {
      problems.push('Choose a Field and an operator.')
      continue
    }
    if (operator.value === 'none') {
      problems.push(null)
      conditions.push({ field: field.name, operator: operator.name })
      continue
    }
    const entries = condition.values.map(valueOf)
    if (
      entries.length === 0 ||
      (operator.value === 'one' && entries.length !== 1) ||
      entries.some((entry) => entry === null)
    ) {
      problems.push('Enter a value.')
      continue
    }
    problems.push(null)
    const values = entries.map((entry) => entry!.value)
    conditions.push({
      field: field.name,
      operator: operator.name,
      value: operator.value === 'many' ? values : values[0]!,
    })
  }
  if (problems.some((problem) => problem !== null)) {
    return { ok: false, problems }
  }
  return {
    ok: true,
    conditions,
    combination:
      conditions.length > 1 ? (draft.combination ?? undefined) : undefined,
  }
}

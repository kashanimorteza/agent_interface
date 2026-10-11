import type { RecordValues } from '@/api'
import { useLoaded } from './async'
import type { Failure } from './failure'
import type { FieldDescription } from './fields'
import { declarations } from './generated/declarations'
import { loadList, type ListCall } from './listing'

/** The records of a related Entity, ready to be chosen from. */
export type RelatedChoice = {
  readonly status: 'ready'
  readonly records: readonly RecordValues[]
  /** The Field of the related Entity whose value the choice hands on. */
  readonly valueField: string
  /** Text by which a record is told apart from the others. */
  readonly describe: (record: RecordValues) => string
}

export type RelatedFailure = {
  readonly status: 'failed'
  readonly failure: Failure
}

/** What the interface holds about the choices of every related Field of a form. */
export type RelatedChoices =
  /** No Field of the form is related, so nothing is requested. */
  | { readonly status: 'none' }
  | { readonly status: 'loading' }
  | {
      readonly status: 'ready'
      /** By the name of the related Field. */
      readonly choices: Readonly<Record<string, RelatedChoice | RelatedFailure>>
    }

/** The calls that list the records of every Entity, by Adapter. */
export type EntityLists = Readonly<Record<string, { readonly list: ListCall }>>

const described: Readonly<Record<string, readonly FieldDescription[]>> =
  declarations

/**
 * Names a record by its value of the related Field and by its first text
 * Field that is not sensitive, such as "3 · Acc-1"; only the value when it has
 * no such text.
 */
export function describeRecord(
  fields: readonly FieldDescription[],
  valueField: string,
  record: RecordValues,
): string {
  const value = String(record[valueField])
  const named = fields.find(
    (field) =>
      field.kind === 'string' &&
      field.sensitive !== true &&
      field.name !== valueField,
  )
  const text = named === undefined ? null : record[named.name]
  return typeof text === 'string' && text !== '' ? `${value} · ${text}` : value
}

/** The Fields of a form that take their value from a record of another Entity, which a user chooses. */
export function relatedFieldsOf(
  fields: readonly FieldDescription[],
): FieldDescription[] {
  return fields.filter(
    (field) =>
      field.relation !== undefined &&
      field.immutable !== true &&
      field.generated !== true,
  )
}

async function loadChoice(
  lists: EntityLists,
  field: FieldDescription,
): Promise<RelatedChoice | RelatedFailure> {
  const relation = field.relation!
  const related = described[relation.entity]
  const list = lists[relation.entity]?.list
  if (related === undefined || list === undefined) {
    return {
      status: 'failed',
      failure: {
        kind: 'untranslatable',
        message: 'The related Entity is not served.',
      },
    }
  }
  const result = await loadList(list, related, {})
  if (result.status === 'failed') return result
  return {
    status: 'ready',
    records: result.records,
    valueField: relation.field,
    describe: (record) => describeRecord(related, relation.field, record),
  }
}

/**
 * The flow that supplies every related Field of a form with the records of the
 * Entity it relates to. The records are requested through API Access when the
 * form is shown and held with the loading state; a Field that is not related
 * requests nothing. The chosen record's value is handed back through the
 * form's own entries.
 */
export function useRelatedChoices(
  lists: EntityLists,
  fields: readonly FieldDescription[],
): RelatedChoices {
  const related = relatedFieldsOf(fields)
  const loaded = useLoaded(
    related.length === 0 ? null : related.map((field) => field.name).join(','),
    async () => {
      const entries = await Promise.all(
        related.map(
          async (field) =>
            [field.name, await loadChoice(lists, field)] as const,
        ),
      )
      return Object.fromEntries(entries)
    },
  )
  if (loaded.status === 'idle') return { status: 'none' }
  if (loaded.status === 'loading') return { status: 'loading' }
  return { status: 'ready', choices: loaded.value }
}

import { useApiAccess, type ApiClient } from '@/api'
import type { Failure } from './failure'
import type { FieldDescription } from './fields'
import { declarations } from './generated/declarations'
import { entities, type EntityKey } from './generated/entities'
import type { EntityLists } from './related'

export type { EntityKey }

/** What Model declares about one Entity: its name and description, and its Fields in Declaration order. */
export function entityOf(key: EntityKey): {
  readonly name: string
  readonly description: string
  readonly fields: readonly FieldDescription[]
} {
  const entity = entities.find((candidate) => candidate.adapter === key)
  if (entity === undefined) throw new Error('The Entity is not described.')
  return {
    name: entity.name,
    description: entity.description,
    fields: declarations[key],
  }
}

/** The calls of one Entity's Adapter, or the reason there are none. */
export type EntityAccess<K extends EntityKey> =
  | {
      readonly status: 'ready'
      /** One call for every Endpoint of the Adapter. */
      readonly calls: ApiClient['entity'][K]
      /** The list call of every Entity, for the records a related Field is chosen from. */
      readonly lists: EntityLists
    }
  | { readonly status: 'misconfigured'; readonly failure: Failure }

/** Gives a Section the calls of its own Adapter through API Access. */
export function useEntityAccess<K extends EntityKey>(key: K): EntityAccess<K> {
  const access = useApiAccess()
  if (access.status === 'misconfigured') {
    return {
      status: 'misconfigured',
      failure: { kind: 'untranslatable', message: access.problem },
    }
  }
  return {
    status: 'ready',
    calls: access.client.entity[key],
    lists: access.client.entity,
  }
}

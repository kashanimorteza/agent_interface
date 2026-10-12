import type { EntityMeta } from '../metadata/types';

/** The location of an Entity's page: the Entity's name in lower case, words joined by hyphens. */
export function locationOf(entity: EntityMeta): string {
  return entity.name.toLowerCase().replace(/\s+/g, '-');
}

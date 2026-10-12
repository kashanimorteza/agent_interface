import type { BaseKey } from '@refinedev/core';
import type { Row } from '../api/values';
import type { EntityMeta } from '../metadata/types';

/** The identity of a listed record, or null when the row holds none. */
export function rowIdentity(entity: EntityMeta, row: Row): BaseKey | null {
  const id = row[entity.primaryKey];
  return typeof id === 'string' || typeof id === 'number' ? id : null;
}

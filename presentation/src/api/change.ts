import type { EntityMeta } from '../metadata/types';
import { requireServed } from './adapter';
import { call } from './errors';
import { send } from './transport';
import { readRecord, type Row } from './values';

export type StateChange = 'enable' | 'disable';

export function isStateChange(value: unknown): value is StateChange {
  return value === 'enable' || value === 'disable';
}

/** Deletes a record and returns the record API deleted, or null when API had none. */
export async function deleteRecord(entity: EntityMeta, id: string | number): Promise<Row | null> {
  const adapter = requireServed(entity, 'delete');
  const deleted = await call(send('delete', `/entity/${adapter}/delete/{id}`, { path: { id } }));
  return deleted === null ? null : readRecord(entity, deleted);
}

/** Enables or disables a record and returns the record as API now holds it, or null when none. */
export async function changeRecord(
  entity: EntityMeta,
  id: string | number,
  change: StateChange,
): Promise<Row | null> {
  const adapter = requireServed(entity, change);
  const path = `/entity/${adapter}/${change}/{id}` as const;
  const changed = await call(send('patch', path, { path: { id }, body: {} }));
  return changed === null ? null : readRecord(entity, changed);
}

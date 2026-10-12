import type { EntityMeta } from '../metadata/types';
import { isServed, requireServed } from './adapter';
import { call } from './errors';
import { viewRecord } from './read';
import { send } from './transport';
import {
  fieldOf,
  readRecord,
  toApiValue,
  writeRecord,
  type InputValue,
  type Row,
  type RowValue,
} from './values';

export type FormValues = Readonly<Record<string, InputValue>>;

/** The identity of a record in the form its primary key has. */
export function identityOf(entity: EntityMeta, id: string | number): RowValue {
  return toApiValue(fieldOf(entity, entity.primaryKey), id);
}

/** Adds a new record from form values and returns the record API stored, with its identity. */
export async function addRecord(entity: EntityMeta, values: FormValues): Promise<Row> {
  const adapter = requireServed(entity, 'add');
  const stored = await call(
    send('post', `/entity/${adapter}/add`, { body: { entity: writeRecord(entity, values) } }),
  );
  return readRecord(entity, stored);
}

/**
 * Edits a stored record with form values and returns the record API stored. The generated and
 * immutable Fields are carried over from the record as API holds it.
 */
export async function editRecord(
  entity: EntityMeta,
  id: string | number,
  values: FormValues,
): Promise<Row> {
  const adapter = requireServed(entity, 'edit');
  const current = isServed(entity, 'view') ? await viewRecord(entity, id) : null;
  const base: Row = current ?? { [entity.primaryKey]: identityOf(entity, id) };
  const stored = await call(
    send('put', `/entity/${adapter}/update`, {
      body: { entity: writeRecord(entity, values, base) },
    }),
  );
  return readRecord(entity, stored);
}

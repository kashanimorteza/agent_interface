import type { HttpError } from '@refinedev/core';
import type { EntityMeta } from '../metadata/types';
import { requireServed } from './adapter';
import { call } from './errors';
import { toCountBody, toListBody, type ListQuery } from './queries';
import { send } from './transport';
import { readRecord, readRecords, RecordShapeError, type Row } from './values';

/** A record the caller asked for that API does not have. */
export class RecordMissingError extends Error implements HttpError {
  readonly statusCode = 404;

  constructor(entity: EntityMeta, id: string | number) {
    super(`API has no ${entity.name} with the identity ${id}.`);
    this.name = 'RecordMissingError';
  }
}

/** One page of a result: the records from `size * (current - 1)` on, at most `size` of them. */
export interface PageWindow {
  readonly current: number;
  readonly size: number;
}

export interface ReadQuery extends ListQuery {
  readonly window?: PageWindow;
}

export interface Page {
  readonly rows: readonly Row[];
  readonly total: number;
}

/**
 * Lists the records of an Entity for a query, with the total number of records the query
 * selects. API's list takes a limit and no offset, so a page is read as the first
 * `current * size` records of the query and cut from where the page begins.
 */
export async function listRecords(entity: EntityMeta, query: ReadQuery = {}): Promise<Page> {
  const adapter = requireServed(entity, 'list');
  const { window, ...listQuery } = query;
  const limit = window === undefined ? listQuery.limit : window.current * window.size;
  const [listed, counted] = await Promise.all([
    call(send('post', `/entity/${adapter}/list`, { body: toListBody({ ...listQuery, limit }) })),
    call(send('post', `/entity/${adapter}/count`, { body: toCountBody(listQuery) })),
  ]);
  if (typeof counted !== 'number') {
    throw new RecordShapeError(`The count of ${entity.name} records is not a number.`);
  }
  const rows = readRecords(entity, listed);
  return {
    rows: window === undefined ? rows : rows.slice((window.current - 1) * window.size),
    total: counted,
  };
}

/** Reads one record by its identity, or null when API has none. */
export async function viewRecord(entity: EntityMeta, id: string | number): Promise<Row | null> {
  const adapter = requireServed(entity, 'view');
  const found = await call(send('get', `/entity/${adapter}/get_by_id/{id}`, { path: { id } }));
  return found === null ? null : readRecord(entity, found);
}

/** Reads the records with the given identities, in a single request. */
export async function viewRecords(
  entity: EntityMeta,
  ids: readonly (string | number)[],
): Promise<readonly Row[]> {
  if (ids.length === 0) {
    return [];
  }
  const page = await listRecords(entity, {
    filters: [{ field: entity.primaryKey, operator: 'in', value: ids }],
  });
  return page.rows;
}

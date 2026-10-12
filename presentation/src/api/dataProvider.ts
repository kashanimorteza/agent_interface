import type {
  BaseRecord,
  CreateParams,
  CreateResponse,
  DataProvider,
  DeleteOneParams,
  DeleteOneResponse,
  GetListParams,
  GetListResponse,
  GetManyParams,
  GetManyResponse,
  GetOneParams,
  GetOneResponse,
  UpdateParams,
  UpdateResponse,
} from '@refinedev/core';
import { entities } from '../metadata/resources.config';
import type { EntityMeta } from '../metadata/types';
import { apiAddress } from './address';
import { OperationNotServedError } from './adapter';
import { isCombination } from './queries';
import { changeRecord, deleteRecord, isStateChange } from './change';
import { listRecords, RecordMissingError, viewRecord, viewRecords, type PageWindow } from './read';
import type { InputValue, Row } from './values';
import { addRecord, editRecord } from './write';

function entityOf(resource: string): EntityMeta {
  const entity = entities.find((candidate) => candidate.segment === resource);
  if (entity === undefined) {
    throw new OperationNotServedError(`Presentation has no Entity for the resource ${resource}.`);
  }
  return entity;
}

function asRecord(row: Row): BaseRecord {
  return row;
}

async function getList({
  resource,
  pagination,
  filters,
  sorters,
  meta,
}: GetListParams): Promise<GetListResponse> {
  const entity = entityOf(resource);
  const combination: unknown = meta?.['combination'];
  const paged = pagination?.mode === undefined || pagination.mode === 'server';
  const window: PageWindow | undefined = paged
    ? { current: pagination?.currentPage ?? 1, size: pagination?.pageSize ?? 10 }
    : undefined;
  const page = await listRecords(entity, {
    filters,
    sorters,
    combination: isCombination(combination) ? combination : undefined,
    window,
  });
  return { data: page.rows.map(asRecord), total: page.total };
}

async function getOne({ resource, id }: GetOneParams): Promise<GetOneResponse> {
  const entity = entityOf(resource);
  const row = await viewRecord(entity, id);
  if (row === null) {
    throw new RecordMissingError(entity, id);
  }
  return { data: asRecord(row) };
}

async function getMany({ resource, ids }: GetManyParams): Promise<GetManyResponse> {
  const rows = await viewRecords(entityOf(resource), ids);
  return { data: rows.map(asRecord) };
}

type Values = Readonly<Record<string, InputValue>>;

async function create({ resource, variables }: CreateParams<Values>): Promise<CreateResponse> {
  return { data: asRecord(await addRecord(entityOf(resource), variables)) };
}

/** Updates a record; the `operation` of the request meta turns it into enabling or disabling. */
async function update({
  resource,
  id,
  variables,
  meta,
}: UpdateParams<Values>): Promise<UpdateResponse> {
  const entity = entityOf(resource);
  const operation: unknown = meta?.['operation'];
  if (isStateChange(operation)) {
    const changed = await changeRecord(entity, id, operation);
    if (changed === null) {
      throw new RecordMissingError(entity, id);
    }
    return { data: asRecord(changed) };
  }
  return { data: asRecord(await editRecord(entity, id, variables)) };
}

async function deleteOne({ resource, id }: DeleteOneParams): Promise<DeleteOneResponse> {
  const entity = entityOf(resource);
  const deleted = await deleteRecord(entity, id);
  if (deleted === null) {
    throw new RecordMissingError(entity, id);
  }
  return { data: asRecord(deleted) };
}

/** The one data provider: the only way pages reach API's records. */
export const dataProvider = {
  getApiUrl: () => apiAddress(),
  getList,
  getOne,
  getMany,
  create,
  update,
  deleteOne,
} as unknown as DataProvider;

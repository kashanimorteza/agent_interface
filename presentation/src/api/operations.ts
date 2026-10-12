import type { paths } from './contract';

export type RecordOperation = 'list' | 'view' | 'add' | 'edit' | 'delete' | 'enable' | 'disable';

/** The Adapter segments of API's Entity Group, taken from the generated contract. */
export type Adapter = keyof paths extends infer K
  ? K extends `/entity/${infer A}/list`
    ? A
    : never
  : never;

export type ServedOperations = Readonly<Record<RecordOperation, boolean>>;

/** The Action of API's Entity Group that serves each record operation of a page. */
export const actionOf: Readonly<Record<RecordOperation, string>> = {
  list: 'list',
  view: 'get_by_id',
  add: 'add',
  edit: 'update',
  delete: 'delete',
  enable: 'enable',
  disable: 'disable',
};

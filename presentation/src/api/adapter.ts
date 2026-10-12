import type { EntityMeta } from '../metadata/types';
import type { Adapter, RecordOperation } from './operations';
import { servedOperations } from './served';

export class OperationNotServedError extends Error {}

/** The Adapter of API's Entity Group that serves an Entity. */
export function adapterOf(entity: EntityMeta): Adapter {
  const segment = entity.segment;
  if (!Object.hasOwn(servedOperations, segment)) {
    throw new OperationNotServedError(`API has no Adapter for ${entity.name}.`);
  }
  return segment as Adapter;
}

export function isServed(entity: EntityMeta, operation: RecordOperation): boolean {
  return servedOperations[adapterOf(entity)][operation];
}

/** Refuses an operation API does not serve for the Entity, before any request is made. */
export function requireServed(entity: EntityMeta, operation: RecordOperation): Adapter {
  const adapter = adapterOf(entity);
  if (!servedOperations[adapter][operation]) {
    throw new OperationNotServedError(`API does not serve ${operation} for ${entity.name}.`);
  }
  return adapter;
}

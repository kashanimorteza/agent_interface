import type { EntityMeta, FieldMeta } from '../metadata/types';

/** A Field is labelled by its description; a Field without one by its name. */
export function fieldLabel(field: FieldMeta): string {
  return field.description ?? field.name;
}

export function entityLabel(entity: EntityMeta): string {
  return entity.name;
}

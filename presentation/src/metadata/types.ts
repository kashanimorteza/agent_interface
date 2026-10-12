export type FieldType = 'integer' | 'float' | 'decimal' | 'string' | 'boolean' | 'datetime';

export type FieldDefault = string | number | boolean | null;

export interface FieldMeta {
  readonly name: string;
  readonly description: string | null;
  readonly type: FieldType;
  readonly nullable: boolean;
  readonly hasDefault: boolean;
  readonly default: FieldDefault;
  readonly immutable: boolean;
  readonly generated: boolean;
  readonly sensitive: boolean;
  readonly size: number | null;
}

export interface RelationMeta {
  readonly field: string;
  readonly entity: string;
  readonly targetField: string;
}

/**
 * The choices of `field` are the related records whose `via` Field equals the value
 * of the Field `on`, because the related Entity itself relates to the Entity `on` relates to.
 */
export interface DependencyMeta {
  readonly field: string;
  readonly on: string;
  readonly via: string;
}

export interface EntityMeta {
  readonly name: string;
  readonly segment: string;
  readonly description: string;
  readonly primaryKey: string;
  readonly labelField: string;
  readonly fields: readonly FieldMeta[];
  readonly relations: readonly RelationMeta[];
  readonly dependencies: readonly DependencyMeta[];
}

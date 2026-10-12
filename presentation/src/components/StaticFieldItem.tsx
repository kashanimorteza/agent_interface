import { Form } from 'antd';
import type { Row } from '../api/values';
import type { EntityMeta, FieldMeta } from '../metadata/types';
import { FieldValue } from './FieldValue';
import { fieldLabel } from './labels';
import type { FormMode } from './validation';

interface StaticFieldItemProps {
  readonly entity: EntityMeta;
  readonly field: FieldMeta;
  readonly mode: FormMode;
  /** The stored record, when editing. */
  readonly record?: Row;
}

/**
 * A generated or immutable Field in a form: its value is shown for an existing record, it can
 * never be changed, and it is not asked for when a record is added.
 */
export function StaticFieldItem({ entity, field, mode, record }: StaticFieldItemProps) {
  if (mode === 'add' || record === undefined) {
    return null;
  }
  return (
    <Form.Item label={fieldLabel(field)}>
      <FieldValue entity={entity} field={field} value={record[field.name]} />
    </Form.Item>
  );
}

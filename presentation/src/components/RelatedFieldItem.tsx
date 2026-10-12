import { Form } from 'antd';
import { useTranslation } from 'react-i18next';
import type { EntityMeta, FieldMeta, RelationMeta } from '../metadata/types';
import { fieldLabel } from './labels';
import { RelatedSelect } from './RelatedSelect';
import { validateField, type FormMode } from './validation';

interface RelatedFieldItemProps {
  readonly entity: EntityMeta;
  readonly field: FieldMeta;
  readonly relation: RelationMeta;
  readonly mode: FormMode;
  readonly disabled?: boolean;
}

/** One form item for a related Field: chosen from the records of the Entity it relates to. */
export function RelatedFieldItem({
  entity,
  field,
  relation,
  mode,
  disabled,
}: RelatedFieldItemProps) {
  const { t } = useTranslation();
  const required = !field.nullable && !(mode === 'add' && field.hasDefault);
  return (
    <Form.Item
      name={field.name}
      label={fieldLabel(field)}
      required={required}
      rules={[
        {
          validator: (_rule, value: Parameters<typeof validateField>[1]) => {
            const problem = validateField(field, value, mode);
            return problem === null
              ? Promise.resolve()
              : Promise.reject(new Error(t(`validation.${problem}`, { size: field.size ?? 0 })));
          },
        },
      ]}
    >
      <RelatedSelect entity={entity} field={field} relation={relation} disabled={disabled} />
    </Form.Item>
  );
}

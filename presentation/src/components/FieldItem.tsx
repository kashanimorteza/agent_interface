import { Form } from 'antd';
import { useTranslation } from 'react-i18next';
import type { FieldMeta } from '../metadata/types';
import { FieldInput } from './FieldInput';
import { fieldLabel } from './labels';
import { validateField, type FormMode } from './validation';

interface FieldItemProps {
  readonly field: FieldMeta;
  readonly mode: FormMode;
  readonly disabled?: boolean;
}

/** One form item for a Field: its label, its input and the rules its Declaration gives it. */
export function FieldItem({ field, mode, disabled }: FieldItemProps) {
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
      <FieldInput field={field} disabled={disabled} />
    </Form.Item>
  );
}

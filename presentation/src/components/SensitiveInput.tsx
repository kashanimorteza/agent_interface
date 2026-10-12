import { Input } from 'antd';
import type { InputValue } from '../api/values';
import type { FieldMeta } from '../metadata/types';
import { fieldLabel } from './labels';

interface SensitiveInputProps {
  readonly field: FieldMeta;
  readonly value?: InputValue;
  readonly onChange?: (value: InputValue) => void;
  readonly disabled?: boolean;
}

/** The entry of a sensitive Field: the value is typed without ever being shown. */
export function SensitiveInput({ field, value, onChange, disabled }: SensitiveInputProps) {
  return (
    <Input.Password
      aria-label={fieldLabel(field)}
      visibilityToggle={false}
      autoComplete="new-password"
      maxLength={field.size ?? undefined}
      value={typeof value === 'string' ? value : ''}
      disabled={disabled}
      onChange={(event) => onChange?.(event.target.value)}
    />
  );
}

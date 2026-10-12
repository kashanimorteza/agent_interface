import { DatePicker, Input, InputNumber, Switch } from 'antd';
import dayjs from 'dayjs';
import type { InputValue } from '../api/values';
import type { FieldMeta } from '../metadata/types';
import { fieldLabel } from './labels';
import { SensitiveInput } from './SensitiveInput';

export interface FieldInputProps {
  readonly field: FieldMeta;
  readonly value?: InputValue;
  readonly onChange?: (value: InputValue) => void;
  readonly disabled?: boolean;
}

function asNumber(value: InputValue): number | null {
  return typeof value === 'number' ? value : null;
}

function asText(value: InputValue): string | null {
  return typeof value === 'string' ? value : null;
}

/**
 * The input for one Field, chosen from the Field's type and labelled by its description. The
 * value it holds is the value of the Field's type; a date and time is held as a date object.
 */
export function FieldInput({ field, value, onChange, disabled }: FieldInputProps) {
  const label = fieldLabel(field);
  if (field.sensitive) {
    return <SensitiveInput field={field} value={value} onChange={onChange} disabled={disabled} />;
  }
  switch (field.type) {
    case 'integer':
    case 'float':
      return (
        <InputNumber
          aria-label={label}
          style={{ width: '100%' }}
          precision={field.type === 'integer' ? 0 : undefined}
          value={asNumber(value ?? null)}
          disabled={disabled}
          onChange={(next) => onChange?.(next)}
        />
      );
    case 'decimal':
      return (
        <InputNumber<string>
          aria-label={label}
          style={{ width: '100%' }}
          stringMode
          value={asText(value ?? null)}
          disabled={disabled}
          onChange={(next) => onChange?.(next)}
        />
      );
    case 'string':
      return (
        <Input
          aria-label={label}
          maxLength={field.size ?? undefined}
          allowClear={field.nullable}
          value={asText(value ?? null) ?? ''}
          disabled={disabled}
          onChange={(event) => onChange?.(event.target.value)}
        />
      );
    case 'boolean':
      return (
        <Switch
          aria-label={label}
          checked={value === true}
          disabled={disabled}
          onChange={(checked) => onChange?.(checked)}
        />
      );
    case 'datetime': {
      const date = typeof value === 'string' ? dayjs(value) : dayjs.isDayjs(value) ? value : null;
      return (
        <DatePicker
          aria-label={label}
          showTime
          style={{ width: '100%' }}
          allowClear={field.nullable}
          value={date?.isValid() === true ? date : null}
          disabled={disabled}
          onChange={(next) => onChange?.(next)}
        />
      );
    }
  }
}

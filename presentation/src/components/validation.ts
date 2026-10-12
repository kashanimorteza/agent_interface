import dayjs from 'dayjs';
import { z } from 'zod';
import type { InputValue } from '../api/values';
import type { FieldMeta } from '../metadata/types';

export type ValidationKey =
  'required' | 'integer' | 'float' | 'decimal' | 'string' | 'boolean' | 'datetime' | 'maxLength';

export type FormMode = 'add' | 'edit';

const decimal = z.string().regex(/^-?\d+(\.\d+)?([eE][+-]?\d+)?$/);

const dateTime = z.custom<unknown>(
  (value) =>
    (dayjs.isDayjs(value) && value.isValid()) ||
    (typeof value === 'string' && !Number.isNaN(Date.parse(value))),
);

function schemaOf(field: FieldMeta): z.ZodType {
  switch (field.type) {
    case 'integer':
      return z.number().int();
    case 'float':
      return z.number();
    case 'decimal':
      return decimal;
    case 'string':
      return field.size === null ? z.string() : z.string().max(field.size);
    case 'boolean':
      return z.boolean();
    case 'datetime':
      return dateTime;
  }
}

function isAbsent(field: FieldMeta, input: InputValue): boolean {
  return input === undefined || input === null || (input === '' && field.type !== 'string');
}

/**
 * Checks one entered value against its Field Declaration: whether it is required, and whether it
 * is a value of the Field's type. It returns what is wrong, or null when the value is acceptable.
 */
export function validateField(
  field: FieldMeta,
  input: InputValue,
  mode: FormMode,
): ValidationKey | null {
  if (isAbsent(field, input)) {
    const mayBeLeftOut = field.nullable || (mode === 'add' && field.hasDefault);
    return mayBeLeftOut ? null : 'required';
  }
  const result = schemaOf(field).safeParse(input);
  if (result.success) {
    return null;
  }
  const tooLong = result.error.issues.some((issue) => issue.code === 'too_big');
  return field.type === 'string' && tooLong ? 'maxLength' : field.type;
}

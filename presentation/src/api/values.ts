import type { EntityMeta, FieldMeta } from '../metadata/types';

/** A value as API holds it and as pages work with it: decimals and date-times stay exact text. */
export type RowValue = string | number | boolean | null;

export type Row = Readonly<Record<string, RowValue>>;

/** A value as a page's inputs hold it: a date-time input holds an object that can format itself. */
export interface DateLike {
  format: (template: string) => string;
}

export type InputValue = RowValue | DateLike | undefined;

export class RecordShapeError extends Error {}

export class InputValueError extends Error {}

const decimalText = /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/;
const dateTimeTemplate = 'YYYY-MM-DDTHH:mm:ss.SSSZ';

export function fieldOf(entity: EntityMeta, name: string): FieldMeta {
  const field = entity.fields.find((candidate) => candidate.name === name);
  if (field === undefined) {
    throw new InputValueError(`${entity.name} has no Field ${name}.`);
  }
  return field;
}

function isDateLike(value: unknown): value is DateLike {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as { format?: unknown }).format === 'function'
  );
}

function matches(field: FieldMeta, value: unknown): value is RowValue {
  switch (field.type) {
    case 'integer':
      return typeof value === 'number' && Number.isInteger(value);
    case 'float':
      return typeof value === 'number' && Number.isFinite(value);
    case 'decimal':
      return typeof value === 'string' && decimalText.test(value);
    case 'string':
      return typeof value === 'string';
    case 'boolean':
      return typeof value === 'boolean';
    case 'datetime':
      return typeof value === 'string' && !Number.isNaN(Date.parse(value));
  }
}

/** Reads one record as API returns it, keeping every value exact and every absent value null. */
export function readRecord(entity: EntityMeta, json: unknown): Row {
  if (typeof json !== 'object' || json === null || Array.isArray(json)) {
    throw new RecordShapeError(`A ${entity.name} record is not an object.`);
  }
  const source = json as Record<string, unknown>;
  const row: Record<string, RowValue> = {};
  for (const field of entity.fields) {
    const value = source[field.name];
    if (value === null && field.nullable) {
      row[field.name] = null;
    } else if (matches(field, value)) {
      row[field.name] = value;
    } else {
      throw new RecordShapeError(
        `The ${field.name} of a ${entity.name} record has an unexpected form.`,
      );
    }
  }
  return row;
}

/** Reads a list of records as API returns it. */
export function readRecords(entity: EntityMeta, json: unknown): Row[] {
  if (!Array.isArray(json)) {
    throw new RecordShapeError(`A list of ${entity.name} records is not an array.`);
  }
  return json.map((item) => readRecord(entity, item));
}

function refuse(field: FieldMeta): never {
  throw new InputValueError(`The value of ${field.name} is not a ${field.type}.`);
}

/**
 * Translates one value of an input into the form API accepts. An absent value stays absent
 * (null) and is never turned into an empty or zero value; an empty text stays an empty text.
 */
export function toApiValue(field: FieldMeta, input: InputValue): RowValue {
  if (input === undefined || input === null) {
    return null;
  }
  if (input === '' && field.type !== 'string') {
    return field.nullable ? null : refuse(field);
  }
  switch (field.type) {
    case 'integer': {
      const value = typeof input === 'string' && input.trim() !== '' ? Number(input) : input;
      return typeof value === 'number' && Number.isInteger(value) ? value : refuse(field);
    }
    case 'float': {
      const value = typeof input === 'string' && input.trim() !== '' ? Number(input) : input;
      return typeof value === 'number' && Number.isFinite(value) ? value : refuse(field);
    }
    case 'decimal': {
      const value = typeof input === 'number' ? String(input) : input;
      return typeof value === 'string' && decimalText.test(value.trim())
        ? value.trim()
        : refuse(field);
    }
    case 'string':
      return typeof input === 'string' ? input : refuse(field);
    case 'boolean':
      return typeof input === 'boolean' ? input : refuse(field);
    case 'datetime': {
      if (isDateLike(input)) {
        return input.format(dateTimeTemplate);
      }
      return typeof input === 'string' && !Number.isNaN(Date.parse(input)) ? input : refuse(field);
    }
  }
}

/**
 * Translates the values of a form into the record API stores. A generated or immutable Field is
 * never taken from the form: it is carried over from the stored record when editing and left
 * out when adding.
 */
export function writeRecord(
  entity: EntityMeta,
  values: Readonly<Record<string, InputValue>>,
  stored?: Row,
): Record<string, RowValue> {
  const record: Record<string, RowValue> = {};
  for (const field of entity.fields) {
    if (field.generated || field.immutable) {
      const kept = stored?.[field.name];
      if (kept !== undefined) {
        record[field.name] = kept;
      }
      continue;
    }
    const input = values[field.name];
    if (input !== undefined) {
      record[field.name] = toApiValue(field, input);
    }
  }
  return record;
}

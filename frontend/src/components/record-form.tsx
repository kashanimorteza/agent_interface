'use client';

import { useState } from 'react';
import type { FieldSpec, ModelSpec } from '@/lib/models/model-specs';
import { FormField, type FieldValue, type RelatedOption } from '@/components/form-field';

export type RecordValues = Record<string, unknown>;

type Props = {
  spec: ModelSpec;
  initial?: RecordValues;
  related: Record<string, RelatedOption[]>;
  onSubmit: (values: RecordValues) => void | Promise<void>;
  onCancel: () => void;
  busy?: boolean;
};

type FormState = Record<string, FieldValue>;

function initialState(fields: FieldSpec[], initial?: RecordValues): FormState {
  const state: FormState = {};
  for (const field of fields) {
    if (field.credential) {
      state[field.name] = '';
      continue;
    }
    const current = initial?.[field.name];
    if (field.type === 'boolean') {
      state[field.name] = current === undefined ? (field.hasDefault ? field.default === true : false) : current === true;
    } else if (current === undefined || current === null) {
      state[field.name] = field.hasDefault && initial === undefined ? String(field.default) : '';
    } else {
      state[field.name] = String(current);
    }
  }
  return state;
}

/** Converts form strings to the field's logical type; returns an error message when invalid. */
function convert(field: FieldSpec, raw: FieldValue, editing: boolean): { value?: unknown; omit?: boolean; error?: string } {
  if (field.type === 'boolean') return { value: raw === true };
  const text = typeof raw === 'string' ? raw.trim() : '';
  if (text === '') {
    if (field.credential && editing) return { omit: true };
    if (field.nullable) return { value: null };
    if (field.hasDefault && !editing) return { omit: true };
    return { error: 'This field is required.' };
  }
  if (field.relation || field.type === 'integer') {
    const number = Number(text);
    if (!Number.isInteger(number)) return { error: 'Enter a whole number.' };
    return { value: number };
  }
  if (field.type === 'decimal' || field.type === 'float') {
    const number = Number(text);
    if (!Number.isFinite(number)) return { error: 'Enter a number.' };
    return { value: number };
  }
  if (field.type === 'string' && field.size !== undefined && text.length > field.size) {
    return { error: `Use at most ${field.size} characters.` };
  }
  return { value: text };
}

/** Creates or edits one record of one Model: one FormField per writable field. */
export function RecordForm({ spec, initial, related, onSubmit, onCancel, busy }: Props) {
  const editing = initial !== undefined;
  const fields = spec.fields.filter((field) => !field.primaryKey);
  const [state, setState] = useState<FormState>(() => initialState(fields, initial));
  const [errors, setErrors] = useState<Record<string, string>>({});

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const values: RecordValues = {};
    const problems: Record<string, string> = {};
    for (const field of fields) {
      const result = convert(field, state[field.name], editing);
      if (result.error) problems[field.name] = result.error;
      else if (!result.omit) values[field.name] = result.value;
    }
    setErrors(problems);
    if (Object.keys(problems).length) return;
    void onSubmit(values);
  }

  return (
    <form className="surface stack" onSubmit={handleSubmit} noValidate>
      <h2>{editing ? `Edit ${spec.name}` : `New ${spec.name}`}</h2>
      <div className="form-grid">
        {fields.map((field) => (
          <FormField
            key={field.name}
            field={field}
            value={state[field.name]}
            onChange={(value) => setState((previous) => ({ ...previous, [field.name]: value }))}
            error={errors[field.name]}
            related={field.relation ? related[field.relation.target] : undefined}
            editing={editing}
            disabled={busy}
          />
        ))}
      </div>
      <div className="row">
        <button type="submit" className="primary" disabled={busy}>
          {editing ? 'Save' : 'Create'}
        </button>
        <button type="button" onClick={onCancel} disabled={busy}>
          Cancel
        </button>
      </div>
    </form>
  );
}

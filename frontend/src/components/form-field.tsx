'use client';

import type { FieldSpec } from '@/lib/models/model-specs';

export type RelatedOption = { id: number; label: string };
export type FieldValue = string | boolean;

type Props = {
  field: FieldSpec;
  value: FieldValue;
  onChange: (value: FieldValue) => void;
  error?: string;
  related?: RelatedOption[];
  editing: boolean;
  disabled?: boolean;
};

function labelOf(field: FieldSpec): string {
  return field.name.replace(/_id$/, '').replace(/_/g, ' ');
}

/** Renders one Model field for input according to its logical type. */
export function FormField({ field, value, onChange, error, related, editing, disabled }: Props) {
  const id = `field-${field.name}`;
  const required = !field.nullable && !field.hasDefault && !(field.credential && editing);
  const errorId = error ? `${id}-error` : undefined;
  const label = (
    <label htmlFor={id}>
      {labelOf(field)}
      {required ? <span aria-hidden="true"> *</span> : null}
    </label>
  );

  let input: React.ReactNode;
  if (field.credential) {
    input = (
      <input
        id={id}
        type="password"
        autoComplete="new-password"
        value={typeof value === 'string' ? value : ''}
        onChange={(event) => onChange(event.target.value)}
        required={required}
        disabled={disabled}
        aria-describedby={errorId}
        placeholder={editing ? 'Leave blank to keep the stored credential' : undefined}
      />
    );
  } else if (field.relation) {
    input = (
      <select
        id={id}
        value={typeof value === 'string' ? value : ''}
        onChange={(event) => onChange(event.target.value)}
        required={required}
        disabled={disabled}
        aria-describedby={errorId}
      >
        <option value="">{field.nullable ? '— none —' : '— select —'}</option>
        {(related ?? []).map((option) => (
          <option key={option.id} value={String(option.id)}>
            {option.label}
          </option>
        ))}
      </select>
    );
  } else if (field.type === 'boolean') {
    input = (
      <input
        id={id}
        type="checkbox"
        checked={value === true}
        onChange={(event) => onChange(event.target.checked)}
        disabled={disabled}
        aria-describedby={errorId}
      />
    );
  } else {
    const type = field.type === 'datetime' ? 'datetime-local' : field.type === 'string' ? 'text' : 'number';
    const step = field.type === 'integer' ? 1 : field.type === 'decimal' || field.type === 'float' ? 'any' : undefined;
    input = (
      <input
        id={id}
        type={type}
        step={step}
        maxLength={field.type === 'string' ? field.size : undefined}
        value={typeof value === 'string' ? value : ''}
        onChange={(event) => onChange(event.target.value)}
        required={required}
        disabled={disabled}
        aria-describedby={errorId}
      />
    );
  }

  return (
    <div className="field">
      {label}
      {input}
      {field.purpose ? <small className="muted">{field.purpose}</small> : null}
      {error ? (
        <span id={errorId} className="field-error" role="alert">
          {error}
        </span>
      ) : null}
    </div>
  );
}

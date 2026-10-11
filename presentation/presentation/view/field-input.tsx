'use client'

import { useId, useState } from 'react'
import {
  fieldText,
  parseFieldText,
  type FieldDescription,
  type FieldEntry,
} from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { fieldLabel } from './field-label'
import styles from './field-input.module.css'

const FORM: Record<FieldDescription['kind'], string> = {
  string: 'text',
  integer: 'a whole number',
  float: 'a number',
  decimal: 'a decimal number',
  boolean: 'Yes or No',
  datetime: 'a date and time with an offset, such as 2026-01-02T03:04:05+00:00',
  uuid: 'a UUID',
}

const MODE: Partial<Record<FieldDescription['kind'], 'numeric' | 'decimal'>> = {
  integer: 'numeric',
  float: 'decimal',
  decimal: 'decimal',
}

function same(a: FieldEntry, b: FieldEntry): boolean {
  if (a.state !== b.state) return false
  if (a.state === 'value' && b.state === 'value') return a.value === b.value
  if (a.state === 'invalid' && b.state === 'invalid') return a.text === b.text
  return true
}

function textOf(entry: FieldEntry): string {
  if (entry.state === 'value') return fieldText(entry.value)
  if (entry.state === 'invalid') return entry.text
  return ''
}

type Props = {
  field: FieldDescription
  entry: FieldEntry
  onChange: (entry: FieldEntry) => void
  /** Hides the visible label when the surroundings already name the Field. */
  hideLabel?: boolean
  /** Names the input when the Field's own name does not say what it is for. */
  label?: string
  /** Names the choice that leaves an optional value unset. */
  absentLabel?: string
  /** A problem the owner found with the entry, shown beside it. */
  problem?: string
  disabled?: boolean
}

/** Presents and edits one value of the kind its Field has, and reports what was entered in that kind. */
export function FieldInput({
  field,
  entry,
  onChange,
  hideLabel = false,
  label: given,
  absentLabel = 'No value',
  problem,
  disabled = false,
}: Props) {
  const id = useId()
  const hint = `${id}-hint`
  const absent = entry.state === 'absent'
  // What the user typed is kept as typed while it still means the entry the owner holds.
  const [typed, setTyped] = useState<string | null>(null)
  const shown =
    typed !== null && same(parseFieldText(field.kind, typed), entry)
      ? typed
      : textOf(entry)
  const label = given ?? fieldLabel(field.name)
  const message =
    entry.state === 'invalid' ? `Enter ${FORM[field.kind]}.` : problem
  const describedBy = message === undefined ? undefined : hint
  const common = {
    id,
    disabled: disabled || absent,
    'aria-required': field.required,
    'aria-invalid': message !== undefined,
    'aria-describedby': describedBy,
    className: styles.control,
    ...autoDirection,
  }
  return (
    <div className={styles.field}>
      <label
        htmlFor={id}
        className={hideLabel ? styles.visuallyHidden : styles.label}
      >
        {label}
        {field.required && <span className={styles.required}> (required)</span>}
      </label>
      {field.kind === 'boolean' ? (
        <select
          {...common}
          value={entry.state === 'value' ? String(entry.value) : ''}
          onChange={(event) =>
            onChange(parseFieldText('boolean', event.target.value))
          }
        >
          <option value="">Choose</option>
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
      ) : (
        <input
          {...common}
          type="text"
          inputMode={MODE[field.kind]}
          autoComplete="off"
          value={shown}
          placeholder={
            field.default === undefined ? undefined : fieldText(field.default)
          }
          onChange={(event) => {
            setTyped(event.target.value)
            onChange(parseFieldText(field.kind, event.target.value))
          }}
        />
      )}
      {!field.required && (
        <label className={styles.absent}>
          <input
            type="checkbox"
            checked={absent}
            disabled={disabled}
            onChange={(event) =>
              onChange(
                event.target.checked ? { state: 'absent' } : { state: 'empty' },
              )
            }
          />
          <span>{absentLabel}</span>
        </label>
      )}
      {message !== undefined && (
        <p id={hint} className={styles.problem} role="alert">
          {message}
        </p>
      )}
    </div>
  )
}

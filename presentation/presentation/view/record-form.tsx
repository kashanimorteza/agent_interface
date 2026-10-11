'use client'

import { useState, type FormEvent } from 'react'
import type {
  FieldDescription,
  FieldEntry,
  RecordValues,
} from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { Button } from './button'
import { FieldInput } from './field-input'
import styles from './record-form.module.css'

type Entries = Readonly<Record<string, FieldEntry>>

type Props = {
  fields: readonly FieldDescription[]
  /** An existing record to fill the form with for editing; absent when adding. Give a new key to start over with another. */
  record?: RecordValues
  submitLabel: string
  busy?: boolean
  /** Why a Field's entry is not acceptable, by Field name. */
  problems?: Readonly<Record<string, string>>
  /** Reports what was entered, Field by Field. */
  onSubmit: (entries: Entries) => void
}

function initial(
  fields: readonly FieldDescription[],
  record: RecordValues | undefined,
): Entries {
  const entries: Record<string, FieldEntry> = {}
  for (const field of fields) {
    const stored = record?.[field.name]
    if (record !== undefined && stored !== undefined) {
      entries[field.name] =
        stored === null
          ? field.required
            ? { state: 'empty' }
            : { state: 'absent' }
          : { state: 'value', value: stored }
    } else if (record === undefined && field.default !== undefined) {
      entries[field.name] =
        field.default === null
          ? { state: 'absent' }
          : { state: 'value', value: field.default }
    } else {
      entries[field.name] = { state: 'empty' }
    }
  }
  return entries
}

/** Presents a form for one record, with one input for each Field described. */
export function RecordForm({
  fields,
  record,
  submitLabel,
  busy = false,
  problems = {},
  onSubmit,
}: Props) {
  const [entries, setEntries] = useState(() => initial(fields, record))
  const submit = (event: FormEvent) => {
    event.preventDefault()
    onSubmit(entries)
  }
  return (
    <form
      className={styles.form}
      onSubmit={submit}
      noValidate
      {...autoDirection}
    >
      <div className={styles.fields}>
        {fields.map((field) => (
          <FieldInput
            key={field.name}
            field={field}
            entry={entries[field.name] ?? { state: 'empty' }}
            problem={problems[field.name]}
            disabled={busy}
            onChange={(next) =>
              setEntries((current) => ({ ...current, [field.name]: next }))
            }
          />
        ))}
      </div>
      <div className={styles.actions}>
        <Button type="submit" variant="primary" disabled={busy}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}

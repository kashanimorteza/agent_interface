'use client'

import { useState, type FormEvent } from 'react'
import {
  isEnterable,
  type FieldDescription,
  type FieldEntry,
  type RecordValues,
} from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import type { RelatedChoices } from '@/interaction/related'
import { Button } from './button'
import { ErrorNotice, Loading } from './feedback'
import { fieldLabel } from './field-label'
import { FieldInput } from './field-input'
import { RelatedRecordChoice } from './related-record-choice'
import { ShownField } from './shown-field'
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
  /** The records a related Field is chosen from; a related Field is entered as text when absent. */
  related?: RelatedChoices
  /** Reports what was entered, Field by Field; a Field that cannot be entered is not among them. */
  onSubmit: (entries: Entries) => void
}

function initial(
  fields: readonly FieldDescription[],
  record: RecordValues | undefined,
): Entries {
  const entries: Record<string, FieldEntry> = {}
  for (const field of fields.filter(isEnterable)) {
    const stored = record?.[field.name]
    if (record !== undefined && field.sensitive === true) {
      // A stored sensitive value is never put in front of the user.
      entries[field.name] = { state: 'empty' }
    } else if (record !== undefined && stored !== undefined) {
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

/** Presents a form for one record: an input for each Field a user may enter, and the other Fields shown. */
export function RecordForm({
  fields,
  record,
  submitLabel,
  busy = false,
  problems = {},
  related,
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
        {fields.map((field) => {
          const choice =
            field.relation !== undefined && related?.status === 'ready'
              ? related.choices[field.name]
              : undefined
          if (
            isEnterable(field) &&
            field.relation !== undefined &&
            related?.status === 'loading'
          ) {
            return (
              <Loading
                key={field.name}
                label={`Loading ${fieldLabel(field)}`}
              />
            )
          }
          if (choice?.status === 'failed') {
            return <ErrorNotice key={field.name} failure={choice.failure} />
          }
          if (choice?.status === 'ready') {
            return (
              <RelatedRecordChoice
                key={field.name}
                field={field}
                records={choice.records}
                valueField={choice.valueField}
                describe={choice.describe}
                entry={entries[field.name] ?? { state: 'empty' }}
                problem={problems[field.name]}
                disabled={busy}
                onChange={(next) =>
                  setEntries((current) => ({ ...current, [field.name]: next }))
                }
              />
            )
          }
          return isEnterable(field) ? (
            <FieldInput
              key={field.name}
              field={field}
              entry={entries[field.name] ?? { state: 'empty' }}
              problem={problems[field.name]}
              placeholder={
                record !== undefined && field.sensitive === true
                  ? 'Leave empty to keep the current value'
                  : undefined
              }
              disabled={busy}
              onChange={(next) =>
                setEntries((current) => ({ ...current, [field.name]: next }))
              }
            />
          ) : (
            <ShownField
              key={field.name}
              field={field}
              value={record?.[field.name]}
            />
          )
        })}
      </div>
      <div className={styles.actions}>
        <Button type="submit" variant="primary" disabled={busy}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}

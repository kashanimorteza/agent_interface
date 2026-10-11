'use client'

import { useId } from 'react'
import type { RecordValues } from '@/api'
import type { FieldDescription, FieldEntry } from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { fieldLabel } from './field-label'
import styles from './related-record-choice.module.css'

type Props = {
  /** The Field that relates to another Entity. */
  field: FieldDescription
  /** The records of the Entity it relates to, in the order they are offered. */
  records: readonly RecordValues[]
  /** The Field of the related Entity whose value the choice reports. */
  valueField: string
  /** Text by which a record is told apart from the others; the owner decides what a record shows of itself. */
  describe: (record: RecordValues) => string
  entry: FieldEntry
  onChange: (entry: FieldEntry) => void
  /** Hides the visible label when the surroundings already name the Field. */
  hideLabel?: boolean
  /** Names the choice when the Field's own name does not say what it is for. */
  label?: string
  /** Names the choice that leaves an optional value unset. */
  absentLabel?: string
  /** A problem the owner found with the entry, shown beside it. */
  problem?: string
  disabled?: boolean
}

/** Chooses one record of the related Entity and reports the value of its related Field. */
export function RelatedRecordChoice({
  field,
  records,
  valueField,
  describe,
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
  const chosen =
    entry.state === 'value'
      ? records.findIndex((record) => record[valueField] === entry.value)
      : -1
  const label = given ?? fieldLabel(field)
  return (
    <div className={styles.field}>
      <label
        htmlFor={id}
        className={hideLabel ? styles.visuallyHidden : styles.label}
      >
        {label}
        {field.required && <span className={styles.required}> (required)</span>}
      </label>
      <select
        id={id}
        className={styles.control}
        disabled={disabled || absent}
        aria-required={field.required}
        aria-invalid={problem !== undefined}
        aria-describedby={problem === undefined ? undefined : hint}
        value={chosen === -1 ? '' : String(chosen)}
        onChange={(event) => {
          const index = event.target.value
          onChange(
            index === ''
              ? { state: 'empty' }
              : {
                  state: 'value',
                  value: records[Number(index)]![valueField] ?? null,
                },
          )
        }}
        {...autoDirection}
      >
        <option value="">Choose</option>
        {records.map((record, index) => (
          <option key={index} value={String(index)}>
            {describe(record)}
          </option>
        ))}
      </select>
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
      {problem !== undefined && (
        <p id={hint} className={styles.problem} role="alert">
          {problem}
        </p>
      )}
    </div>
  )
}

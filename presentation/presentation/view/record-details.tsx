import type { ReactNode } from 'react'
import type { FieldDescription, RecordValues } from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { Concealed } from './concealed'
import { Empty } from './feedback'
import { fieldLabel } from './field-label'
import { valueText } from './field-value'
import styles from './record-details.module.css'

type Props = {
  fields: readonly FieldDescription[]
  /** The record to present; null when there is none. */
  record: RecordValues | null
  /** Names the details for people who cannot see them. */
  caption: string
  /** Shown instead of the details when there is no record. */
  emptyTitle?: string
  emptyHint?: ReactNode
}

/** Presents one record as its Fields, each named by its description, in the order given. */
export function RecordDetails({
  fields,
  record,
  caption,
  emptyTitle = 'No such record',
  emptyHint,
}: Props) {
  if (record === null) {
    return <Empty title={emptyTitle}>{emptyHint}</Empty>
  }
  return (
    <dl className={styles.details} aria-label={caption} {...autoDirection}>
      {fields.map((field) => {
        const value = record[field.name]
        return (
          <div key={field.name} className={styles.row}>
            <dt className={styles.label}>{fieldLabel(field)}</dt>
            <dd className={styles.value}>
              {field.sensitive === true ? (
                <Concealed />
              ) : value === null || value === undefined ? (
                <span className={styles.absent} aria-label="No value">
                  <span aria-hidden="true">–</span>
                </span>
              ) : value === '' ? (
                <span className={styles.emptyText}>Empty</span>
              ) : (
                valueText(value)
              )}
            </dd>
          </div>
        )
      })}
    </dl>
  )
}

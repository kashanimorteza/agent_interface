import type { ReactNode } from 'react'
import type {
  FieldDescription,
  FieldValue,
  RecordValues,
} from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { Concealed } from './concealed'
import { Empty } from './feedback'
import { fieldLabel } from './field-label'
import { valueText } from './field-value'
import styles from './record-table.module.css'

const NUMERIC: ReadonlySet<FieldDescription['kind']> = new Set([
  'integer',
  'float',
  'decimal',
])

type Props = {
  fields: readonly FieldDescription[]
  /** The records in the order they are shown. */
  records: readonly RecordValues[]
  /** Names the table for people who cannot see it. */
  caption: string
  /** Shown instead of the table when there are no records. */
  emptyTitle?: string
  emptyHint?: ReactNode
  /** What a user can do with one record, shown in the last column. */
  rowActions?: (record: RecordValues) => ReactNode
}

function Cell({
  kind,
  value,
  sensitive,
}: {
  kind: FieldDescription['kind']
  value: FieldValue | undefined
  sensitive: boolean
}) {
  if (sensitive) {
    return (
      <td className={styles.text}>
        <Concealed />
      </td>
    )
  }
  if (value === null || value === undefined) {
    return (
      <td className={styles.absent} aria-label="No value">
        <span aria-hidden="true">–</span>
      </td>
    )
  }
  return (
    <td
      className={NUMERIC.has(kind) ? styles.number : styles.text}
      {...autoDirection}
    >
      {valueText(value)}
    </td>
  )
}

/** Presents records as rows with one column for each Field it is given. */
export function RecordTable({
  fields,
  records,
  caption,
  emptyTitle = 'No records',
  emptyHint,
  rowActions,
}: Props) {
  if (records.length === 0) {
    return <Empty title={emptyTitle}>{emptyHint}</Empty>
  }
  return (
    <div
      className={styles.scroll}
      role="region"
      aria-label={caption}
      tabIndex={0}
    >
      <table className={styles.table}>
        <caption className={styles.caption}>{caption}</caption>
        <thead>
          <tr>
            {fields.map((field) => (
              <th
                key={field.name}
                scope="col"
                className={NUMERIC.has(field.kind) ? styles.number : undefined}
              >
                {fieldLabel(field)}
              </th>
            ))}
            {rowActions !== undefined && (
              <th scope="col">
                <span className={styles.visuallyHidden}>Actions</span>
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {records.map((record, index) => (
            <tr key={index}>
              {fields.map((field) => (
                <Cell
                  key={field.name}
                  kind={field.kind}
                  value={record[field.name]}
                  sensitive={field.sensitive === true}
                />
              ))}
              {rowActions !== undefined && (
                <td>
                  <div className={styles.actions}>{rowActions(record)}</div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

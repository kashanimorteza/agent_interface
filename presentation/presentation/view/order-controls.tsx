'use client'

import type { FieldDescription } from '@/interaction/fields'
import type { OrderAndLimit } from '@/interaction/order'
import { autoDirection } from '@/theme/theme'
import { FieldInput } from './field-input'
import { fieldLabel } from './field-label'
import styles from './order-controls.module.css'

type Props = {
  fields: readonly FieldDescription[]
  /** The directions the contract names. */
  directions: readonly string[]
  value: OrderAndLimit
  /** Reports the choices as they stand. */
  onChange: (value: OrderAndLimit) => void
}

/** Lets a user choose a Field and a direction to order a list by, and how many records it returns. */
export function OrderControls({ fields, directions, value, onChange }: Props) {
  const { order, limit } = value
  return (
    <fieldset className={styles.controls} {...autoDirection}>
      <legend className={styles.legend}>Order and limit</legend>
      <label className={styles.part}>
        <span>Order by</span>
        <select
          className={styles.select}
          value={order?.field ?? ''}
          onChange={(event) => {
            const field = event.target.value
            onChange({
              ...value,
              order:
                field === ''
                  ? null
                  : {
                      field,
                      direction: order?.direction ?? directions[0] ?? '',
                    },
            })
          }}
        >
          <option value="">No order</option>
          {fields.map((f) => (
            <option key={f.name} value={f.name}>
              {fieldLabel(f)}
            </option>
          ))}
        </select>
      </label>
      <label className={styles.part}>
        <span>Direction</span>
        <select
          className={styles.select}
          value={order?.direction ?? ''}
          disabled={order === null}
          onChange={(event) => {
            if (order !== null) {
              onChange({
                ...value,
                order: { ...order, direction: event.target.value },
              })
            }
          }}
        >
          {order === null && <option value="" />}
          {directions.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>
      <div className={styles.limit}>
        <FieldInput
          field={{ name: 'limit', kind: 'integer', required: false }}
          entry={limit}
          label="Limit"
          absentLabel="No limit"
          onChange={(next) => onChange({ ...value, limit: next })}
        />
      </div>
    </fieldset>
  )
}

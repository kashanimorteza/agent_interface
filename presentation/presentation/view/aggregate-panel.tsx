'use client'

import type { FieldValue } from '@/api'
import type {
  FieldDescription,
  OperatorDescription,
} from '@/interaction/fields'
import {
  changeOperation,
  type AggregateOperation,
  type AggregateRequest,
} from '@/interaction/aggregate'
import { autoDirection } from '@/theme/theme'
import { Button } from './button'
import { FilterEditor } from './filter-editor'
import { fieldLabel } from './field-label'
import styles from './aggregate-panel.module.css'

type Props = {
  operations: readonly AggregateOperation[]
  /** The Fields and operators Filters can be built from, and how they combine. */
  filterFields: readonly FieldDescription[]
  filterOperators: readonly OperatorDescription[]
  combinations: readonly string[]
  value: AggregateRequest
  /** Reports the operation and arguments as they stand. */
  onChange: (value: AggregateRequest) => void
  /** Asks for the result of the chosen operation. */
  onRun: (value: AggregateRequest) => void
  /** The single value the last request gave; absent until there is one. */
  result?: FieldValue
  /** One entry per Filter condition: why it is not complete, or null. */
  problems?: readonly (string | null)[]
  busy?: boolean
}

function shown(result: FieldValue): string {
  if (result === null) return 'No value'
  if (typeof result === 'boolean') return result ? 'Yes' : 'No'
  return String(result)
}

/** Lets a user choose a count or aggregate, give it a Field and Filters where it takes them, and read the single value. */
export function AggregatePanel({
  operations,
  filterFields,
  filterOperators,
  combinations,
  value,
  onChange,
  onRun,
  result,
  problems,
  busy = false,
}: Props) {
  const operation = operations.find((o) => o.name === value.operation)
  return (
    <section
      className={styles.panel}
      aria-label="Count and aggregates"
      {...autoDirection}
    >
      <div className={styles.choices}>
        <label className={styles.part}>
          <span>Operation</span>
          <select
            className={styles.select}
            value={value.operation}
            onChange={(event) => {
              const chosen = operations.find(
                (o) => o.name === event.target.value,
              )
              if (chosen !== undefined) onChange(changeOperation(value, chosen))
            }}
          >
            {operations.map((o) => (
              <option key={o.name} value={o.name}>
                {o.name}
              </option>
            ))}
          </select>
        </label>
        {operation?.fields !== undefined && (
          <label className={styles.part}>
            <span>Field</span>
            <select
              className={styles.select}
              value={value.field ?? ''}
              onChange={(event) =>
                onChange({ ...value, field: event.target.value })
              }
            >
              {operation.fields.map((f) => (
                <option key={f.name} value={f.name}>
                  {fieldLabel(f)}
                </option>
              ))}
            </select>
          </label>
        )}
      </div>
      {operation?.takesFilters === true && (
        <FilterEditor
          fields={filterFields}
          operators={filterOperators}
          combinations={combinations}
          draft={value.filters}
          onChange={(filters) => onChange({ ...value, filters })}
          problems={problems}
        />
      )}
      <div className={styles.run}>
        <Button
          variant="primary"
          disabled={busy || operation === undefined}
          onClick={() => onRun(value)}
        >
          Calculate
        </Button>
        {result !== undefined && (
          <output className={styles.result}>
            <span className={styles.resultLabel}>Result</span>{' '}
            <strong>{shown(result)}</strong>
          </output>
        )}
      </div>
    </section>
  )
}

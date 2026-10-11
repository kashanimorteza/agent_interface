'use client'

import {
  type FieldDescription,
  type OperatorDescription,
} from '@/interaction/fields'
import {
  applicableOperators,
  changeField,
  changeOperator,
  newCondition,
  type ConditionDraft,
  type FilterDraft,
} from '@/interaction/filter'
import { autoDirection } from '@/theme/theme'
import { Button } from './button'
import { FieldInput } from './field-input'
import { fieldLabel } from './field-label'
import styles from './filter-editor.module.css'

type Props = {
  fields: readonly FieldDescription[]
  operators: readonly OperatorDescription[]
  /** The ways several conditions can combine, as the contract names them. */
  combinations: readonly string[]
  draft: FilterDraft
  /** Reports the Filter as it stands; the Component applies nothing itself. */
  onChange: (draft: FilterDraft) => void
  /** One entry per condition: why it is incomplete, or null. */
  problems?: readonly (string | null)[]
}

/** Lets a user build Filters on any Field and choose how they combine. */
export function FilterEditor({
  fields,
  operators,
  combinations,
  draft,
  onChange,
  problems = [],
}: Props) {
  const replace = (index: number, next: ConditionDraft) =>
    onChange({
      ...draft,
      conditions: draft.conditions.map((c, i) => (i === index ? next : c)),
    })
  const add = () => {
    const condition = newCondition(fields, operators)
    if (condition === null) return
    const conditions = [...draft.conditions, condition]
    onChange({
      conditions,
      combination:
        conditions.length > 1
          ? (draft.combination ?? combinations[0] ?? null)
          : null,
    })
  }
  const remove = (index: number) => {
    const conditions = draft.conditions.filter((_, i) => i !== index)
    onChange({
      conditions,
      combination: conditions.length > 1 ? draft.combination : null,
    })
  }
  return (
    <fieldset className={styles.editor} {...autoDirection}>
      <legend className={styles.legend}>Filters</legend>
      {draft.conditions.length === 0 && (
        <p className={styles.none}>No filters. Every record matches.</p>
      )}
      <ul className={styles.list}>
        {draft.conditions.map((condition, index) => {
          const field = fields.find((f) => f.name === condition.field)
          const choices =
            field === undefined ? [] : applicableOperators(operators, field)
          const operator = operators.find((o) => o.name === condition.operator)
          const problem = problems[index] ?? null
          return (
            <li key={index} className={styles.condition}>
              <label className={styles.part}>
                <span>Field</span>
                <select
                  className={styles.select}
                  value={condition.field}
                  onChange={(event) => {
                    const chosen = fields.find(
                      (f) => f.name === event.target.value,
                    )
                    if (chosen !== undefined) {
                      replace(index, changeField(condition, chosen, operators))
                    }
                  }}
                >
                  {fields.map((f) => (
                    <option key={f.name} value={f.name}>
                      {fieldLabel(f)}
                    </option>
                  ))}
                </select>
              </label>
              <label className={styles.part}>
                <span>Operator</span>
                <select
                  className={styles.select}
                  value={condition.operator}
                  onChange={(event) => {
                    const chosen = choices.find(
                      (o) => o.name === event.target.value,
                    )
                    if (chosen !== undefined) {
                      replace(
                        index,
                        changeOperator(condition, chosen, operator),
                      )
                    }
                  }}
                >
                  {choices.map((o) => (
                    <option key={o.name} value={o.name}>
                      {o.name}
                    </option>
                  ))}
                </select>
              </label>
              {field !== undefined &&
                operator !== undefined &&
                operator.value !== 'none' && (
                  <div className={styles.values}>
                    {condition.values.map((entry, valueIndex) => (
                      <div key={valueIndex} className={styles.value}>
                        <FieldInput
                          field={{
                            name: 'value',
                            kind: field.kind,
                            required: true,
                            sensitive: field.sensitive === true,
                          }}
                          entry={entry}
                          hideLabel
                          onChange={(next) =>
                            replace(index, {
                              ...condition,
                              values: condition.values.map((v, i) =>
                                i === valueIndex ? next : v,
                              ),
                            })
                          }
                        />
                        {operator.value === 'many' &&
                          condition.values.length > 1 && (
                            <Button
                              onClick={() =>
                                replace(index, {
                                  ...condition,
                                  values: condition.values.filter(
                                    (_, i) => i !== valueIndex,
                                  ),
                                })
                              }
                            >
                              Remove value
                            </Button>
                          )}
                      </div>
                    ))}
                    {operator.value === 'many' && (
                      <Button
                        onClick={() =>
                          replace(index, {
                            ...condition,
                            values: [...condition.values, { state: 'empty' }],
                          })
                        }
                      >
                        Add value
                      </Button>
                    )}
                  </div>
                )}
              <Button onClick={() => remove(index)}>Remove filter</Button>
              {problem !== null && (
                <p className={styles.problem} role="alert">
                  {problem}
                </p>
              )}
            </li>
          )
        })}
      </ul>
      {draft.conditions.length > 1 && (
        <label className={styles.part}>
          <span>Combine filters with</span>
          <select
            className={styles.select}
            value={draft.combination ?? ''}
            onChange={(event) =>
              onChange({ ...draft, combination: event.target.value })
            }
          >
            {combinations.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </label>
      )}
      <div>
        <Button onClick={add} disabled={fields.length === 0}>
          Add filter
        </Button>
      </div>
    </fieldset>
  )
}

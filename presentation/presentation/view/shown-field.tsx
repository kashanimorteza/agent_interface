import { useId } from 'react'
import type { FieldDescription, FieldValue } from '@/interaction/fields'
import { autoDirection } from '@/theme/theme'
import { Concealed } from './concealed'
import { fieldLabel } from './field-label'
import { valueText } from './field-value'
import styles from './shown-field.module.css'

type Props = {
  field: FieldDescription
  /** The value the record holds; absent when there is no record yet. */
  value?: FieldValue
}

/** Shows a Field whose value a user can see but never enter, such as one that is fixed or that Model supplies. */
export function ShownField({ field, value }: Props) {
  const id = useId()
  return (
    <div className={styles.field}>
      <span id={id} className={styles.label}>
        {fieldLabel(field)}
      </span>
      <output aria-labelledby={id} className={styles.value} {...autoDirection}>
        {field.sensitive === true ? (
          <Concealed />
        ) : value === undefined || value === null ? (
          <span className={styles.absent}>No value</span>
        ) : (
          valueText(value)
        )}
      </output>
    </div>
  )
}

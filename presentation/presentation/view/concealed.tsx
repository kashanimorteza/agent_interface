import styles from './concealed.module.css'

/** Stands where a sensitive value would be: the value itself is never rendered. */
export function Concealed() {
  return (
    <span className={styles.concealed}>
      <span aria-hidden="true">••••••</span>
      <span className={styles.visuallyHidden}>Hidden</span>
    </span>
  )
}

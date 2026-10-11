import type { ReactNode } from 'react'
import styles from './stack.module.css'

/** Lays its children out in one column with the Theme's spacing between them. */
export function Stack({ children }: { children: ReactNode }) {
  return <div className={styles.stack}>{children}</div>
}

/** Lays a row of related actions side by side, wrapping when there is no room. */
export function Toolbar({
  label,
  children,
}: {
  /** Names the group of actions for people who cannot see it. */
  label: string
  children: ReactNode
}) {
  return (
    <div className={styles.toolbar} role="group" aria-label={label}>
      {children}
    </div>
  )
}

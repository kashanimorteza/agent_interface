import type { ReactNode } from 'react'
import type { Failure } from '@/interaction/failure'
import { autoDirection } from '@/theme/theme'
import styles from './feedback.module.css'

export function Loading({ label = 'Loading' }: { label?: string }) {
  return (
    <p className={styles.loading} role="status">
      <span className={styles.spinner} aria-hidden="true" />
      <span>{label}</span>
    </p>
  )
}

export function Empty({
  title,
  children,
}: {
  title: string
  children?: ReactNode
}) {
  return (
    <div className={styles.empty} {...autoDirection}>
      <p className={styles.emptyTitle}>{title}</p>
      {children}
    </div>
  )
}

export function Success({ children }: { children: ReactNode }) {
  return (
    <p className={styles.success} role="status" {...autoDirection}>
      {children}
    </p>
  )
}

function bodyText(body: unknown): string {
  return typeof body === 'string' ? body : JSON.stringify(body)
}

/** Presents an error exactly as it was given: nothing is reworded. */
export function ErrorNotice({ failure }: { failure: Failure }) {
  if (failure.kind === 'problem') {
    const { type, status, title, detail } = failure.problem
    return (
      <div className={styles.error} role="alert" {...autoDirection}>
        <dl className={styles.details}>
          <dt>Type</dt>
          <dd>{type}</dd>
          <dt>Status</dt>
          <dd>{status}</dd>
          {title !== null && (
            <>
              <dt>Title</dt>
              <dd>{title}</dd>
            </>
          )}
          {detail !== null && (
            <>
              <dt>Detail</dt>
              <dd>{detail}</dd>
            </>
          )}
        </dl>
      </div>
    )
  }
  if (failure.kind === 'unrecognized') {
    return (
      <div className={styles.error} role="alert" {...autoDirection}>
        <dl className={styles.details}>
          <dt>Status</dt>
          <dd>{failure.status}</dd>
          <dt>Response</dt>
          <dd>{bodyText(failure.body)}</dd>
        </dl>
      </div>
    )
  }
  return (
    <div className={styles.error} role="alert" {...autoDirection}>
      <p className={styles.message}>{failure.message}</p>
    </div>
  )
}

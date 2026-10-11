'use client'

import { useEffect, useId, useRef } from 'react'
import { autoDirection } from '@/theme/theme'
import { Button } from './button'
import styles from './confirmation.module.css'

type Props = {
  open: boolean
  /** Names what will be affected, such as "Delete the User with id 4?". */
  question: string
  confirmLabel: string
  cancelLabel?: string
  busy?: boolean
  onConfirm: () => void
  onCancel: () => void
}

/** Asks a user to confirm an action that cannot be undone; the action is carried out only on confirmation. */
export function Confirmation({
  open,
  question,
  confirmLabel,
  cancelLabel = 'Cancel',
  busy = false,
  onConfirm,
  onCancel,
}: Props) {
  const dialog = useRef<HTMLDialogElement>(null)
  const questionId = useId()
  useEffect(() => {
    const element = dialog.current
    if (element === null) return
    if (open && !element.open) element.showModal()
    if (!open && element.open) element.close()
  }, [open])
  return (
    <dialog
      ref={dialog}
      className={styles.dialog}
      aria-labelledby={questionId}
      onCancel={(event) => {
        event.preventDefault()
        onCancel()
      }}
      onClick={(event) => {
        if (event.target === dialog.current) onCancel()
      }}
      {...autoDirection}
    >
      <div className={styles.content}>
        <p id={questionId} className={styles.question}>
          {question}
        </p>
        <div className={styles.actions}>
          <Button onClick={onCancel} disabled={busy}>
            {cancelLabel}
          </Button>
          <Button variant="danger" onClick={onConfirm} disabled={busy}>
            {confirmLabel}
          </Button>
        </div>
      </div>
    </dialog>
  )
}

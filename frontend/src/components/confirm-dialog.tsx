'use client';

import { useEffect, useRef } from 'react';

type Props = {
  open: boolean;
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
  busy?: boolean;
};

/** Asks the user to confirm a destructive action before it is sent. */
export function ConfirmDialog({ open, title, message, onConfirm, onCancel, busy }: Props) {
  const ref = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog ref={ref} onCancel={(event) => { event.preventDefault(); onCancel(); }} aria-labelledby="confirm-title">
      <div className="stack">
        <h2 id="confirm-title">{title}</h2>
        <p>{message}</p>
        <div className="row">
          <button type="button" className="danger" onClick={onConfirm} disabled={busy}>
            Confirm
          </button>
          <button type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </button>
        </div>
      </div>
    </dialog>
  );
}

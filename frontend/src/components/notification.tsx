'use client';

import { useNotification } from '@/hooks/use-notification';

/** Shows the outcome of the latest operation — success or the error returned by the Backend API. */
export function Notification() {
  const { current, dismiss } = useNotification();
  if (!current) return null;
  const isError = current.kind === 'error';
  return (
    <div className={`notification ${current.kind}`} role={isError ? 'alert' : 'status'}>
      <span>{current.message}</span>
      <button type="button" onClick={dismiss} aria-label="Dismiss notification">
        ×
      </button>
    </div>
  );
}

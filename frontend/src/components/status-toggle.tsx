'use client';

export type StatusRecord = { id: number; status?: unknown };

type Props = {
  record: StatusRecord;
  onToggle: (record: StatusRecord) => void;
  busy?: boolean;
};

/** Enables or disables one record through its status field. */
export function StatusToggle({ record, onToggle, busy }: Props) {
  const checked = record.status === true;
  return (
    <label className="switch">
      <input
        type="checkbox"
        role="switch"
        aria-checked={checked}
        checked={checked}
        onChange={() => onToggle(record)}
        disabled={busy}
      />
      <span>{checked ? 'Active' : 'Inactive'}</span>
    </label>
  );
}

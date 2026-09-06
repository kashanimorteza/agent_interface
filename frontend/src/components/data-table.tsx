'use client';

import type { FieldSpec, ModelSpec } from '@/lib/models/model-specs';
import type { RelatedOption } from '@/components/form-field';
import { StatusToggle, type StatusRecord } from '@/components/status-toggle';

export type TableRecord = { id: number } & Record<string, unknown>;

type Props = {
  spec: ModelSpec;
  records: TableRecord[];
  related: Record<string, RelatedOption[]>;
  busy?: boolean;
  loading?: boolean;
  onEdit: (record: TableRecord) => void;
  onDelete: (record: TableRecord) => void;
  onToggleStatus: (record: StatusRecord) => void;
};

function headerOf(field: FieldSpec): string {
  return field.name.replace(/_id$/, '').replace(/_/g, ' ');
}

function cellText(field: FieldSpec, value: unknown, related: Record<string, RelatedOption[]>): string {
  if (value === null || value === undefined) return '—';
  if (field.relation) {
    const option = (related[field.relation.target] ?? []).find((candidate) => candidate.id === value);
    return option ? option.label : String(value);
  }
  if (field.type === 'boolean') return value === true ? 'Yes' : 'No';
  return String(value);
}

/** Lists the records of one Model with its non-credential fields as columns and row actions. */
export function DataTable({ spec, records, related, busy, loading, onEdit, onDelete, onToggleStatus }: Props) {
  const columns = spec.fields.filter((field) => !field.credential);
  const hasStatus = spec.fields.some((field) => field.name === 'status');
  return (
    <div className="table-wrap surface">
      <table>
        <thead>
          <tr>
            {columns.map((field) => (
              <th key={field.name} scope="col">
                {headerOf(field)}
              </th>
            ))}
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={columns.length + 1} className="muted">
                Loading…
              </td>
            </tr>
          ) : records.length === 0 ? (
            <tr>
              <td colSpan={columns.length + 1} className="muted">
                No {spec.title.toLowerCase()} yet.
              </td>
            </tr>
          ) : (
            records.map((record) => (
              <tr key={record.id}>
                {columns.map((field) => (
                  <td key={field.name}>
                    {hasStatus && field.name === 'status' ? (
                      <StatusToggle record={record} onToggle={onToggleStatus} busy={busy} />
                    ) : (
                      cellText(field, record[field.name], related)
                    )}
                  </td>
                ))}
                <td>
                  <div className="row">
                    <button type="button" onClick={() => onEdit(record)} disabled={busy}>
                      Edit
                    </button>
                    <button type="button" className="danger" onClick={() => onDelete(record)} disabled={busy}>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

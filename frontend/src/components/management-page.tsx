'use client';

import { useState } from 'react';
import { getSpec } from '@/lib/models/model-specs';
import { useModelRecords, type ModelRecord } from '@/hooks/use-model-records';
import { ConfirmDialog } from '@/components/confirm-dialog';
import { DataTable } from '@/components/data-table';
import { RecordForm, type RecordValues } from '@/components/record-form';

type Mode = { kind: 'list' } | { kind: 'create' } | { kind: 'edit'; record: ModelRecord };

/** The management page of one Model: list, create or edit, confirm before delete, toggle status, show outcomes. */
export function ManagementPage({ modelKey }: { modelKey: string }) {
  const spec = getSpec(modelKey);
  const { records, related, loading, busy, error, reload, create, update, remove, toggleStatus } = useModelRecords(spec);
  const [mode, setMode] = useState<Mode>({ kind: 'list' });
  const [pendingDelete, setPendingDelete] = useState<ModelRecord | null>(null);

  async function handleSubmit(values: RecordValues) {
    const ok = mode.kind === 'edit' ? await update(mode.record.id, values) : await create(values);
    if (ok) setMode({ kind: 'list' });
  }

  async function handleConfirmDelete() {
    if (!pendingDelete) return;
    const ok = await remove(pendingDelete.id);
    if (ok) setPendingDelete(null);
  }

  return (
    <div className="stack">
      <header className="row" style={{ justifyContent: 'space-between' }}>
        <div>
          <h1>{spec.title}</h1>
          <p className="muted">{spec.purpose}</p>
        </div>
        <div className="row">
          <button type="button" onClick={() => void reload()} disabled={busy || loading}>
            Refresh
          </button>
          <button type="button" className="primary" onClick={() => setMode({ kind: 'create' })} disabled={busy || mode.kind !== 'list'}>
            New {spec.name}
          </button>
        </div>
      </header>

      {mode.kind !== 'list' ? (
        <RecordForm
          key={mode.kind === 'edit' ? `edit-${mode.record.id}` : 'create'}
          spec={spec}
          initial={mode.kind === 'edit' ? mode.record : undefined}
          related={related}
          onSubmit={handleSubmit}
          onCancel={() => setMode({ kind: 'list' })}
          busy={busy}
        />
      ) : null}

      {error && !loading ? <p className="field-error">{error}</p> : null}

      <DataTable
        spec={spec}
        records={records}
        related={related}
        busy={busy}
        loading={loading}
        onEdit={(record) => setMode({ kind: 'edit', record })}
        onDelete={(record) => setPendingDelete(record)}
        onToggleStatus={(record) => void toggleStatus(record)}
      />

      <ConfirmDialog
        open={pendingDelete !== null}
        title={`Delete ${spec.name}`}
        message={pendingDelete ? `Delete "${String(pendingDelete.name ?? pendingDelete.id)}"? This cannot be undone.` : ''}
        onConfirm={() => void handleConfirmDelete()}
        onCancel={() => setPendingDelete(null)}
        busy={busy}
      />
    </div>
  );
}

'use client';

/**
 * Interaction Logic for one Model's management flow: list, create, update, delete, and toggle status
 * through API Access, with related records for relation fields and notifications of every outcome.
 * This hook is the only place Presentation reaches API Access.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { ModelSpec } from '@/lib/models/model-specs';
import { ApiError } from '@/lib/api/client';
import { createRecord, deleteRecord, listRecords, updateRecord, type RecordData } from '@/lib/api/models';
import { useNotification } from '@/hooks/use-notification';

export type ModelRecord = { id: number } & RecordData;
export type RelatedOption = { id: number; label: string };
export type RelatedRecords = Record<string, RelatedOption[]>;

const RELATED_LIMIT = 500;

function labelOf(row: RecordData): string {
  const candidate = row.name ?? row.code ?? row.symbol;
  return typeof candidate === 'string' && candidate ? candidate : `#${String(row.id)}`;
}

function describe(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return String(error);
}

/** Removes blank credential values so an edit never overwrites a stored credential with nothing. */
function withoutBlankCredentials(spec: ModelSpec, values: RecordData): RecordData {
  const result: RecordData = {};
  for (const [name, value] of Object.entries(values)) {
    const field = spec.fields.find((candidate) => candidate.name === name);
    if (field?.credential && (value === '' || value === null || value === undefined)) continue;
    result[name] = value;
  }
  return result;
}

export function useModelRecords(spec: ModelSpec) {
  const { notify } = useNotification();
  const [records, setRecords] = useState<ModelRecord[]>([]);
  const [related, setRelated] = useState<RelatedRecords>({});
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mounted = useRef(true);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  const relationTargets = useMemo(
    () => Array.from(new Set(spec.fields.flatMap((field) => (field.relation ? [field.relation.target] : [])))),
    [spec],
  );

  const reload = useCallback(async () => {
    setLoading(true);
    try {
      const [rows, ...relatedRows] = await Promise.all([
        listRecords(spec.key, { orderBy: ['id'], limit: RELATED_LIMIT }),
        ...relationTargets.map((target) => listRecords(target, { orderBy: ['id'], limit: RELATED_LIMIT })),
      ]);
      if (!mounted.current) return;
      setRecords(rows as ModelRecord[]);
      setRelated(
        Object.fromEntries(
          relationTargets.map((target, index) => [
            target,
            relatedRows[index].map((row) => ({ id: Number(row.id), label: labelOf(row) })),
          ]),
        ),
      );
      setError(null);
    } catch (failure) {
      if (!mounted.current) return;
      const message = describe(failure);
      setError(message);
      notify('error', message);
    } finally {
      if (mounted.current) setLoading(false);
    }
  }, [spec.key, relationTargets, notify]);

  useEffect(() => {
    void reload();
  }, [reload]);

  const perform = useCallback(
    async (action: () => Promise<void>, success: string): Promise<boolean> => {
      setBusy(true);
      try {
        await action();
        notify('success', success);
        await reload();
        return true;
      } catch (failure) {
        notify('error', describe(failure));
        return false;
      } finally {
        if (mounted.current) setBusy(false);
      }
    },
    [notify, reload],
  );

  const create = useCallback(
    (values: RecordData) =>
      perform(async () => {
        await createRecord(spec.key, withoutBlankCredentials(spec, values));
      }, `${spec.name} created.`),
    [perform, spec],
  );

  const update = useCallback(
    (id: number, values: RecordData) =>
      perform(async () => {
        await updateRecord(spec.key, id, withoutBlankCredentials(spec, values));
      }, `${spec.name} updated.`),
    [perform, spec],
  );

  const remove = useCallback(
    (id: number) =>
      perform(async () => {
        await deleteRecord(spec.key, id);
      }, `${spec.name} deleted.`),
    [perform, spec],
  );

  const toggleStatus = useCallback(
    (record: { id: number; status?: unknown }) =>
      perform(async () => {
        await updateRecord(spec.key, record.id, { status: !(record.status === true) });
      }, `${spec.name} ${record.status === true ? 'disabled' : 'enabled'}.`),
    [perform, spec],
  );

  return { records, related, loading, busy, error, reload, create, update, remove, toggleStatus };
}

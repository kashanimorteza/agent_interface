import { useDelete, useUpdate } from '@refinedev/core';
import { App, Button, Popconfirm, Space } from 'antd';
import { useTranslation } from 'react-i18next';
import { isServed } from '../api/adapter';
import { ApiError } from '../api/errors';
import type { Row } from '../api/values';
import type { EntityMeta } from '../metadata/types';

interface RecordActionsProps {
  readonly entity: EntityMeta;
  readonly row: Row;
  /** Called after an action succeeded. */
  readonly onDone?: () => void;
}

/** Deletes, enables and disables one record, reporting what API answered. */
export function RecordActions({ entity, row, onDone }: RecordActionsProps) {
  const { t } = useTranslation();
  const { notification } = App.useApp();
  const { mutateAsync: remove, mutation: removing } = useDelete();
  const { mutateAsync: change, mutation: changing } = useUpdate();
  const id = row[entity.primaryKey];
  const active = row['is_active'];

  function report(error: unknown) {
    notification.error({
      message: error instanceof ApiError ? (error.kind ?? t('state.error')) : t('state.error'),
      description: error instanceof Error ? error.message : undefined,
    });
  }

  async function run(action: () => Promise<unknown>, done: string) {
    try {
      await action();
      notification.success({ message: done });
      onDone?.();
    } catch (error) {
      report(error);
    }
  }

  if (typeof id !== 'number' && typeof id !== 'string') {
    return null;
  }
  const mayEnable = isServed(entity, 'enable') && active !== true;
  const mayDisable = isServed(entity, 'disable') && active !== false;
  return (
    <Space size="small">
      {isServed(entity, 'delete') && (
        <Popconfirm
          title={t('actions.confirmDelete')}
          okText={t('actions.confirm')}
          cancelText={t('actions.cancel')}
          okButtonProps={{ danger: true }}
          onConfirm={() => {
            void run(
              () => remove({ resource: entity.segment, id, mutationMode: 'pessimistic' }),
              t('actions.deleted'),
            );
          }}
        >
          <Button danger size="small" loading={removing.isPending}>
            {t('actions.delete')}
          </Button>
        </Popconfirm>
      )}
      {mayEnable && (
        <Button
          size="small"
          loading={changing.isPending}
          onClick={() => {
            void run(
              () =>
                change({
                  resource: entity.segment,
                  id,
                  values: {},
                  meta: { operation: 'enable' },
                  mutationMode: 'pessimistic',
                }),
              t('actions.enabled'),
            );
          }}
        >
          {t('actions.enable')}
        </Button>
      )}
      {mayDisable && (
        <Button
          size="small"
          loading={changing.isPending}
          onClick={() => {
            void run(
              () =>
                change({
                  resource: entity.segment,
                  id,
                  values: {},
                  meta: { operation: 'disable' },
                  mutationMode: 'pessimistic',
                }),
              t('actions.disabled'),
            );
          }}
        >
          {t('actions.disable')}
        </Button>
      )}
    </Space>
  );
}

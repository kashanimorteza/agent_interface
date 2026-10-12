import { useForm } from '@refinedev/antd';
import type { BaseKey, HttpError } from '@refinedev/core';
import { Button, Form, Space, Spin } from 'antd';
import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { InputValue, Row } from '../api/values';
import type { EntityMeta } from '../metadata/types';
import { ErrorState } from './ErrorState';
import { FieldItem } from './FieldItem';
import { RelatedFieldItem } from './RelatedFieldItem';
import { StaticFieldItem } from './StaticFieldItem';
import type { FormMode } from './validation';

type Values = Record<string, InputValue>;

interface RecordFormProps {
  readonly entity: EntityMeta;
  readonly mode: FormMode;
  /** The identity of the record being edited. */
  readonly id?: BaseKey;
  readonly onSaved?: (row: Row) => void;
  readonly onCancel?: () => void;
}

/** The Default Values the Declaration states, which a form starts from when adding a record. */
function defaultsOf(entity: EntityMeta): Record<string, string | number | boolean> {
  const values: Record<string, string | number | boolean> = {};
  for (const field of entity.fields) {
    if (field.hasDefault && !field.generated && !field.immutable && field.default !== null) {
      values[field.name] = field.default;
    }
  }
  return values;
}

/**
 * The form for adding a record and for editing one, built from the Entity's Fields: an input for
 * every Field that may be entered, in the Declaration's order, with what API returns on a refusal.
 */
export function RecordForm({ entity, mode, id, onSaved, onCancel }: RecordFormProps) {
  const { t } = useTranslation();
  const [refusal, setRefusal] = useState<unknown>(null);
  const defaults = useMemo(() => defaultsOf(entity), [entity]);
  const { formProps, query, formLoading, mutation } = useForm<Row, HttpError, Values, Row, Row>({
    resource: entity.segment,
    action: mode === 'add' ? 'create' : 'edit',
    id,
    redirect: false,
    successNotification: false,
    errorNotification: false,
    warnWhenUnsavedChanges: false,
    defaultFormValues: mode === 'add' ? () => defaults : undefined,
    onMutationSuccess: (data) => {
      setRefusal(null);
      onSaved?.(data.data);
    },
    onMutationError: (error) => {
      setRefusal(error);
    },
  });
  const stored = query?.data?.data;
  if (mode === 'edit' && query?.isError === true) {
    return <ErrorState error={query.error} />;
  }
  return (
    <Spin spinning={formLoading}>
      <Form {...formProps} layout="vertical" initialValues={mode === 'add' ? defaults : stored}>
        {entity.fields.map((field) => {
          if (field.generated || field.immutable) {
            return (
              <StaticFieldItem
                key={field.name}
                entity={entity}
                field={field}
                mode={mode}
                record={stored}
              />
            );
          }
          const relation = entity.relations.find((candidate) => candidate.field === field.name);
          return relation === undefined ? (
            <FieldItem key={field.name} field={field} mode={mode} />
          ) : (
            <RelatedFieldItem
              key={field.name}
              entity={entity}
              field={field}
              relation={relation}
              mode={mode}
            />
          );
        })}
        {refusal !== null && <ErrorState error={refusal} />}
        <Form.Item style={{ marginTop: 16 }}>
          <Space>
            <Button type="primary" htmlType="submit" loading={mutation.isPending}>
              {t('form.save')}
            </Button>
            <Button onClick={onCancel}>{t('form.cancel')}</Button>
          </Space>
        </Form.Item>
      </Form>
    </Spin>
  );
}

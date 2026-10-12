import { DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import type { CrudFilter } from '@refinedev/core';
import { Alert, Button, Flex, Input, Segmented, Select, Space, Typography } from 'antd';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { pageOperatorOf } from '../api/queries';
import { toApiValue, type InputValue } from '../api/values';
import { filterOperators, type Combination, type FilterOperator } from '../api/vocabulary';
import type { FieldMeta } from '../metadata/types';
import { FieldInput } from './FieldInput';
import { fieldLabel } from './labels';
import type { RecordList } from './useRecordList';

interface Draft {
  readonly key: number;
  readonly field: string | undefined;
  readonly operator: FilterOperator | undefined;
  readonly value: InputValue;
}

const textOperators: readonly FilterOperator[] = ['CONTAINS', 'STARTS_WITH', 'ENDS_WITH'];
const emptyOperators: readonly FilterOperator[] = ['IS_NULL', 'IS_NOT_NULL'];

function operatorsFor(field: FieldMeta | undefined): readonly FilterOperator[] {
  return filterOperators.filter(
    (operator) => field?.type === 'string' || !textOperators.includes(operator),
  );
}

function toFilter(draft: Draft, fields: readonly FieldMeta[]): CrudFilter {
  const field = fields.find((candidate) => candidate.name === draft.field);
  if (field === undefined || draft.operator === undefined) {
    throw new Error('incomplete');
  }
  const operator = pageOperatorOf[draft.operator];
  if (emptyOperators.includes(draft.operator)) {
    return { field: field.name, operator, value: undefined };
  }
  if (draft.operator === 'IN') {
    const parts = (typeof draft.value === 'string' ? draft.value : '')
      .split(',')
      .map((part) => part.trim())
      .filter((part) => part !== '');
    if (parts.length === 0) {
      throw new Error('incomplete');
    }
    return { field: field.name, operator, value: parts.map((part) => toApiValue(field, part)) };
  }
  const value = toApiValue(field, draft.value);
  if (value === null) {
    throw new Error('incomplete');
  }
  return { field: field.name, operator, value };
}

/** Narrows the records of an Entity by filters on any of its Fields, combined as the user chooses. */
export function FilterEditor({ list }: { readonly list: RecordList }) {
  const { t } = useTranslation();
  const { entity } = list;
  const [drafts, setDrafts] = useState<readonly Draft[]>([]);
  const [combination, setCombination] = useState<Combination>(list.combination);
  const [incomplete, setIncomplete] = useState(false);
  const [next, setNext] = useState(1);

  function change(key: number, patch: Partial<Draft>) {
    setDrafts((current) =>
      current.map((draft) => (draft.key === key ? { ...draft, ...patch } : draft)),
    );
  }

  function apply() {
    try {
      const filters = drafts.map((draft) => toFilter(draft, entity.fields));
      setIncomplete(false);
      list.setCombination(combination);
      list.setFilters(filters);
    } catch {
      setIncomplete(true);
    }
  }

  function clear() {
    setDrafts([]);
    setIncomplete(false);
    setCombination('AND');
    list.setCombination('AND');
    list.setFilters([]);
  }

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Typography.Text strong>{t('filter.title')}</Typography.Text>
      {drafts.map((draft) => {
        const field = entity.fields.find((candidate) => candidate.name === draft.field);
        const needsValue = draft.operator !== undefined && !emptyOperators.includes(draft.operator);
        return (
          <Flex key={draft.key} gap={8} wrap align="start">
            <Select
              aria-label={t('filter.field')}
              placeholder={t('filter.field')}
              style={{ minWidth: 200 }}
              value={draft.field}
              options={entity.fields.map((candidate) => ({
                value: candidate.name,
                label: fieldLabel(candidate),
              }))}
              onChange={(name: string) => {
                change(draft.key, { field: name, operator: undefined, value: undefined });
              }}
            />
            <Select
              aria-label={t('filter.operator')}
              placeholder={t('filter.operator')}
              style={{ minWidth: 180 }}
              value={draft.operator}
              disabled={field === undefined}
              options={operatorsFor(field).map((operator) => ({
                value: operator,
                label: t(`filter.operators.${operator}`),
              }))}
              onChange={(operator: FilterOperator) => {
                change(draft.key, { operator, value: undefined });
              }}
            />
            {field !== undefined && needsValue && draft.operator === 'IN' && (
              <Input
                aria-label={t('filter.value')}
                placeholder={t('filter.values')}
                style={{ minWidth: 220 }}
                value={typeof draft.value === 'string' ? draft.value : ''}
                onChange={(event) => {
                  change(draft.key, { value: event.target.value });
                }}
              />
            )}
            {field !== undefined && needsValue && draft.operator !== 'IN' && (
              <div style={{ minWidth: 220 }}>
                <FieldInput
                  field={{ ...field, nullable: true }}
                  value={draft.value}
                  onChange={(value) => {
                    change(draft.key, { value });
                  }}
                />
              </div>
            )}
            <Button
              aria-label={t('filter.remove')}
              icon={<DeleteOutlined />}
              onClick={() => {
                setDrafts((current) => current.filter((candidate) => candidate.key !== draft.key));
              }}
            />
          </Flex>
        );
      })}
      {drafts.length > 1 && (
        <Segmented
          aria-label={t('filter.combination')}
          value={combination}
          options={[
            { value: 'AND', label: t('filter.and') },
            { value: 'OR', label: t('filter.or') },
          ]}
          onChange={setCombination}
        />
      )}
      {incomplete && <Alert type="warning" showIcon message={t('filter.incomplete')} />}
      <Space>
        <Button
          icon={<PlusOutlined />}
          onClick={() => {
            setDrafts((current) => [
              ...current,
              { key: next, field: undefined, operator: undefined, value: undefined },
            ]);
            setNext(next + 1);
          }}
        >
          {t('filter.add')}
        </Button>
        <Button type="primary" onClick={apply}>
          {t('filter.apply')}
        </Button>
        <Button onClick={clear}>{t('filter.clear')}</Button>
      </Space>
    </Space>
  );
}

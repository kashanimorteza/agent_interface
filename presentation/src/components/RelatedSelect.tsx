import { useSelect } from '@refinedev/antd';
import type { CrudFilter } from '@refinedev/core';
import { Form, Select } from 'antd';
import { useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import type { InputValue, Row } from '../api/values';
import { entities } from '../metadata/resources.config';
import type { EntityMeta, FieldMeta, RelationMeta } from '../metadata/types';
import { fieldLabel } from './labels';

interface RelatedSelectProps {
  readonly entity: EntityMeta;
  readonly field: FieldMeta;
  readonly relation: RelationMeta;
  readonly value?: InputValue;
  readonly onChange?: (value: InputValue) => void;
  readonly disabled?: boolean;
}

/**
 * The choice of a related Field: the records of the Entity it relates to, shown by their label.
 * Its choices follow the dependencies of the Field: they are the related records that match the
 * value chosen in the Field it depends on.
 */
export function RelatedSelect({
  entity,
  field,
  relation,
  value,
  onChange,
  disabled,
}: RelatedSelectProps) {
  const { t } = useTranslation();
  const form = Form.useFormInstance();
  const values = Form.useWatch<Record<string, InputValue> | undefined>([], form);
  const target = entities.find((candidate) => candidate.name === relation.entity);
  if (target === undefined) {
    throw new Error(`The Entity ${relation.entity} of the Relation ${relation.field} is unknown.`);
  }
  const filters: CrudFilter[] = entity.dependencies
    .filter((dependency) => dependency.field === field.name)
    .flatMap((dependency) => {
      const chosen = values?.[dependency.on];
      return chosen === undefined || chosen === null
        ? []
        : [{ field: dependency.via, operator: 'eq' as const, value: chosen }];
    });
  const parents = entity.dependencies
    .filter((dependency) => dependency.field === field.name)
    .map((dependency) => values?.[dependency.on]);
  const parentKey = JSON.stringify(parents);
  const previousKey = useRef(parentKey);
  useEffect(() => {
    const before = JSON.parse(previousKey.current) as unknown[];
    previousKey.current = parentKey;
    const changedFromChosen = before.some(
      (earlier, index) => earlier !== null && earlier !== undefined && earlier !== parents[index],
    );
    if (changedFromChosen) {
      onChange?.(undefined);
    }
    // only a change of the chosen value of a Field this one depends on clears this choice
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [parentKey]);
  const { selectProps } = useSelect<Row>({
    resource: target.segment,
    optionLabel: target.labelField,
    optionValue: relation.targetField,
    searchField: target.labelField,
    defaultValue: typeof value === 'number' || typeof value === 'string' ? value : undefined,
    filters,
    pagination: { currentPage: 1, pageSize: 20, mode: 'server' },
    onSearch: (search) =>
      search === '' ? [] : [{ field: target.labelField, operator: 'contains', value: search }],
  });
  const { options, onSearch, loading, filterOption, showSearch } = selectProps;
  return (
    <Select
      options={options}
      onSearch={onSearch}
      loading={loading}
      filterOption={filterOption}
      showSearch={showSearch}
      aria-label={fieldLabel(field)}
      placeholder={t('related.placeholder')}
      allowClear={field.nullable}
      value={value as string | number | null | undefined}
      disabled={disabled}
      onChange={(next: string | number | null | undefined) => onChange?.(next)}
    />
  );
}

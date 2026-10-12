import { Flex, Segmented, Select } from 'antd';
import { useTranslation } from 'react-i18next';
import { fieldLabel } from './labels';
import type { RecordList } from './useRecordList';

/** Orders the records of an Entity by any one of its Fields, in either direction. */
export function OrderControl({ list }: { readonly list: RecordList }) {
  const { t } = useTranslation();
  const current = list.sorters[0];
  return (
    <Flex gap={8} wrap align="center">
      <Select
        aria-label={t('order.by')}
        virtual={false}
        placeholder={t('order.by')}
        style={{ minWidth: 200 }}
        allowClear
        value={current?.field}
        options={list.entity.fields.map((field) => ({
          value: field.name,
          label: fieldLabel(field),
        }))}
        onChange={(field: string | undefined) => {
          list.setSorters(field === undefined ? [] : [{ field, order: current?.order ?? 'asc' }]);
        }}
      />
      <Segmented
        aria-label={t('order.direction')}
        disabled={current === undefined}
        value={current?.order ?? 'asc'}
        options={[
          { value: 'asc', label: t('order.ascending') },
          { value: 'desc', label: t('order.descending') },
        ]}
        onChange={(order) => {
          if (current !== undefined) {
            list.setSorters([{ field: current.field, order: order === 'desc' ? 'desc' : 'asc' }]);
          }
        }}
      />
    </Flex>
  );
}

import { ConfigProvider, Table, type TableColumnsType } from 'antd';
import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import type { Row } from '../api/values';
import { compactThemeOf } from '../theme/modes';
import { useDisplayMode } from '../theme/DisplayMode';
import { EmptyState } from './EmptyState';
import { ErrorState } from './ErrorState';
import { fieldLabel } from './labels';
import { FieldValue } from './FieldValue';
import { LoadingState } from './LoadingState';
import type { RecordList } from './useRecordList';

interface RecordTableProps {
  readonly list: RecordList;
  /** The actions offered for one record, shown in the last column. */
  readonly actions?: (row: Row) => ReactNode;
}

/** Lists the records of an Entity: one column for each Field, in the Declaration's order. */
export function RecordTable({ list, actions }: RecordTableProps) {
  const { t } = useTranslation();
  const { mode } = useDisplayMode();
  const { entity } = list;
  if (list.error !== null && list.error !== undefined) {
    return <ErrorState error={list.error} />;
  }
  if (list.isLoading) {
    return <LoadingState />;
  }
  const columns: TableColumnsType<Row> = entity.fields.map((field) => ({
    key: field.name,
    title: fieldLabel(field),
    dataIndex: field.name,
    render: (value: Row[string]) => <FieldValue entity={entity} field={field} value={value} />,
  }));
  if (actions !== undefined) {
    columns.push({
      key: '__actions',
      title: t('table.actions'),
      fixed: 'right',
      render: (_value: unknown, row: Row) => actions(row),
    });
  }
  return (
    <ConfigProvider theme={compactThemeOf(mode)}>
      <Table<Row>
        {...list.tableProps}
        rowKey={entity.primaryKey}
        columns={columns}
        scroll={{ x: 'max-content' }}
        locale={{ emptyText: <EmptyState /> }}
      />
    </ConfigProvider>
  );
}

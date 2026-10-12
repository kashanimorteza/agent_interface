import { useTable } from '@refinedev/antd';
import type { CrudFilters, CrudSorting } from '@refinedev/core';
import type { TableProps } from 'antd';
import { useState } from 'react';
import type { Combination } from '../api/vocabulary';
import type { Row } from '../api/values';
import type { EntityMeta } from '../metadata/types';

export interface RecordList {
  readonly entity: EntityMeta;
  readonly tableProps: TableProps<Row>;
  readonly isLoading: boolean;
  readonly error: unknown;
  readonly filters: CrudFilters;
  readonly setFilters: (filters: CrudFilters) => void;
  readonly sorters: CrudSorting;
  readonly setSorters: (sorters: CrudSorting) => void;
  readonly combination: Combination;
  readonly setCombination: (combination: Combination) => void;
}

/**
 * The state of the list of one Entity's records: its page, its filters with their combination
 * and its order. The table, the filter editor and the order control all work on this state.
 */
export function useRecordList(entity: EntityMeta): RecordList {
  const [combination, setCombination] = useState<Combination>('AND');
  const table = useTable<Row>({
    resource: entity.segment,
    syncWithLocation: false,
    pagination: { pageSize: 10 },
    meta: { combination },
  });
  return {
    entity,
    tableProps: table.tableProps,
    isLoading: table.tableQuery.isLoading,
    error: table.tableQuery.error,
    filters: table.filters,
    setFilters: (filters) => {
      table.setFilters(filters, 'replace');
    },
    sorters: table.sorters,
    setSorters: table.setSorters,
    combination,
    setCombination,
  };
}

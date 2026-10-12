import type { CrudFilter, CrudFilters, CrudOperators, CrudSorting } from '@refinedev/core';
import type { components } from './contract';
import { combinations, type Combination, type FilterOperator } from './vocabulary';

export type FilterBody = components['schemas']['FilterBody'];
export type OrderBody = components['schemas']['OrderBody'];

export class UnsupportedQueryError extends Error {}

/**
 * The page operator that expresses each operator API publishes. It is keyed by the published
 * vocabulary, so a vocabulary change fails the type check until it is reconciled here.
 */
export const pageOperatorOf = {
  EQUALS: 'eq',
  NOT_EQUALS: 'ne',
  GREATER_THAN: 'gt',
  GREATER_OR_EQUAL: 'gte',
  LESS_THAN: 'lt',
  LESS_OR_EQUAL: 'lte',
  IN: 'in',
  CONTAINS: 'contains',
  STARTS_WITH: 'startswith',
  ENDS_WITH: 'endswith',
  IS_NULL: 'null',
  IS_NOT_NULL: 'nnull',
} as const satisfies Record<FilterOperator, CrudOperators>;

export type PageOperator = (typeof pageOperatorOf)[FilterOperator];

const apiOperatorOf = new Map<string, FilterOperator>(
  (Object.entries(pageOperatorOf) as Array<[FilterOperator, PageOperator]>).map(([api, page]) => [
    page,
    api,
  ]),
);

export interface ListQuery {
  readonly filters?: CrudFilters;
  readonly sorters?: CrudSorting;
  readonly combination?: Combination;
  readonly limit?: number;
}

export interface ListBody {
  filters?: FilterBody[];
  combination?: Combination;
  orders?: OrderBody[];
  limit?: number;
}

export interface CountBody {
  filters?: FilterBody[];
  combination?: Combination;
}

function isLogical(filter: CrudFilter): filter is Extract<CrudFilter, { field: string }> {
  return 'field' in filter;
}

function toFilterBody(filter: Extract<CrudFilter, { field: string }>): FilterBody {
  const operator = apiOperatorOf.get(filter.operator);
  if (operator === undefined) {
    throw new UnsupportedQueryError(`The operator ${filter.operator} is not published by API.`);
  }
  if (operator === 'IS_NULL' || operator === 'IS_NOT_NULL') {
    return { field: filter.field, operator };
  }
  if (operator === 'IN' && !Array.isArray(filter.value)) {
    throw new UnsupportedQueryError('The operator IN needs a list of values.');
  }
  return { field: filter.field, operator, value: filter.value };
}

/**
 * Translates the filters of a page into the forms API accepts. API takes one combination for
 * all filters, so a page filter set is either a flat list or one AND/OR group.
 */
export function toFilterBodies(filters: CrudFilters = []): {
  filters: FilterBody[];
  combination: Combination | null;
} {
  const [first] = filters;
  if (filters.length === 1 && first !== undefined && !isLogical(first)) {
    const combination: Combination = first.operator === 'or' ? 'OR' : 'AND';
    const inner = first.value.map((item) => {
      if (!isLogical(item)) {
        throw new UnsupportedQueryError('API accepts one combination of filters, not nested ones.');
      }
      return toFilterBody(item);
    });
    return { filters: inner, combination };
  }
  return {
    filters: filters.map((filter) => {
      if (!isLogical(filter)) {
        throw new UnsupportedQueryError('API accepts one combination of filters, not nested ones.');
      }
      return toFilterBody(filter);
    }),
    combination: null,
  };
}

export function toOrderBodies(sorters: CrudSorting = []): OrderBody[] {
  return sorters.map((sorter) => ({
    field: sorter.field,
    direction: sorter.order === 'desc' ? 'DESCENDING' : 'ASCENDING',
  }));
}

function filterPart(query: ListQuery): CountBody {
  const { filters, combination } = toFilterBodies(query.filters);
  if (filters.length === 0) {
    return {};
  }
  return { filters, combination: query.combination ?? combination ?? 'AND' };
}

export function toCountBody(query: ListQuery): CountBody {
  return filterPart(query);
}

export function toListBody(query: ListQuery): ListBody {
  const body: ListBody = { ...filterPart(query) };
  const orders = toOrderBodies(query.sorters);
  if (orders.length > 0) {
    body.orders = orders;
  }
  if (query.limit !== undefined) {
    body.limit = query.limit;
  }
  return body;
}

export function isCombination(value: unknown): value is Combination {
  return combinations.some((candidate) => candidate === value);
}

export const filterOperators = [
  'EQUALS',
  'NOT_EQUALS',
  'GREATER_THAN',
  'GREATER_OR_EQUAL',
  'LESS_THAN',
  'LESS_OR_EQUAL',
  'IN',
  'CONTAINS',
  'STARTS_WITH',
  'ENDS_WITH',
  'IS_NULL',
  'IS_NOT_NULL',
] as const;

export type FilterOperator = (typeof filterOperators)[number];

export const orderDirections = ['ASCENDING', 'DESCENDING'] as const;

export type OrderDirection = (typeof orderDirections)[number];

export const combinations = ['AND', 'OR'] as const;

export type Combination = (typeof combinations)[number];

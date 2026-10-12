import { useOne } from '@refinedev/core';
import { Descriptions } from 'antd';
import type { BaseKey } from '@refinedev/core';
import type { Row } from '../api/values';
import type { EntityMeta } from '../metadata/types';
import { ErrorState } from './ErrorState';
import { FieldValue } from './FieldValue';
import { fieldLabel } from './labels';
import { LoadingState } from './LoadingState';

interface RecordDetailsProps {
  readonly entity: EntityMeta;
  readonly id: BaseKey;
}

/** Shows one record in full: every Field, in the Declaration's order, headed by its description. */
export function RecordDetails({ entity, id }: RecordDetailsProps) {
  const { query, result } = useOne<Row>({ resource: entity.segment, id });
  if (query.isError) {
    return <ErrorState error={query.error} />;
  }
  if (query.isLoading || result === undefined) {
    return <LoadingState />;
  }
  return (
    <Descriptions
      bordered
      column={1}
      items={entity.fields.map((field) => ({
        key: field.name,
        label: fieldLabel(field),
        children: <FieldValue entity={entity} field={field} value={result[field.name]} />,
      }))}
    />
  );
}

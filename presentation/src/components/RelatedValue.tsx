import { useMany } from '@refinedev/core';
import { Typography } from 'antd';
import type { Row, RowValue } from '../api/values';
import { entities } from '../metadata/resources.config';
import type { RelationMeta } from '../metadata/types';

/** A related Field's value shown as the related record, falling back to the bare value. */
export function RelatedValue({
  relation,
  value,
}: {
  readonly relation: RelationMeta;
  readonly value: Exclude<RowValue, null>;
}) {
  const target = entities.find((entity) => entity.name === relation.entity);
  const byIdentity = target !== undefined && relation.targetField === target.primaryKey;
  const { result } = useMany<Row>({
    resource: target?.segment ?? relation.entity,
    ids: [typeof value === 'boolean' ? String(value) : value],
    queryOptions: { enabled: byIdentity },
  });
  const record = result.data[0];
  const label = byIdentity && record !== undefined ? record[target.labelField] : undefined;
  return <Typography.Text>{typeof label === 'string' ? label : String(value)}</Typography.Text>;
}

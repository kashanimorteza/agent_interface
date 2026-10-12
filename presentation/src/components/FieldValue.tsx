import { Tag, Typography } from 'antd';
import { useTranslation } from 'react-i18next';
import type { RowValue } from '../api/values';
import type { EntityMeta, FieldMeta } from '../metadata/types';
import { formatDateTime } from './format';
import { RelatedValue } from './RelatedValue';

interface FieldValueProps {
  readonly entity: EntityMeta;
  readonly field: FieldMeta;
  readonly value: RowValue | undefined;
}

/** One Field's value as a user reads it: a related record by name, a sensitive value never. */
export function FieldValue({ entity, field, value }: FieldValueProps) {
  const { t, i18n } = useTranslation();
  if (field.sensitive) {
    return <Typography.Text type="secondary">{t('value.hidden')}</Typography.Text>;
  }
  if (value === null || value === undefined) {
    return <Typography.Text type="secondary">{t('value.none')}</Typography.Text>;
  }
  const relation = entity.relations.find((candidate) => candidate.field === field.name);
  if (relation !== undefined) {
    return <RelatedValue relation={relation} value={value} />;
  }
  switch (field.type) {
    case 'boolean':
      return (
        <Tag color={value === true ? 'success' : 'default'}>
          {t(value === true ? 'value.yes' : 'value.no')}
        </Tag>
      );
    case 'datetime':
      return <Typography.Text>{formatDateTime(String(value), i18n.language)}</Typography.Text>;
    default:
      return <Typography.Text>{String(value)}</Typography.Text>;
  }
}

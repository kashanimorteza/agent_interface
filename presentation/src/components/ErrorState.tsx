import { Alert, Typography } from 'antd';
import { useTranslation } from 'react-i18next';
import { ApiError, ApiUnreachableError } from '../api/errors';
import { RecordMissingError } from '../api/read';

/** Shows an error as it was returned: for an error of API, its kind and detail, unchanged. */
export function ErrorState({ error }: { readonly error: unknown }) {
  const { t } = useTranslation();
  if (error instanceof ApiError) {
    return (
      <Alert
        type="error"
        showIcon
        message={error.kind ?? t('state.error')}
        description={
          <>
            <div>{error.detail}</div>
            <Typography.Text type="secondary">
              {t('state.status', { status: error.statusCode })}
            </Typography.Text>
          </>
        }
      />
    );
  }
  if (error instanceof ApiUnreachableError) {
    return (
      <Alert type="error" showIcon message={t('state.unreachable')} description={error.message} />
    );
  }
  if (error instanceof RecordMissingError) {
    return <Alert type="warning" showIcon message={t('state.missing')} />;
  }
  return (
    <Alert
      type="error"
      showIcon
      message={t('state.error')}
      description={error instanceof Error ? error.message : undefined}
    />
  );
}

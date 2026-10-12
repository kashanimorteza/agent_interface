import { Flex, Spin, Typography } from 'antd';
import { useTranslation } from 'react-i18next';

export function LoadingState() {
  const { t } = useTranslation();
  return (
    <Flex align="center" justify="center" gap={8} role="status" style={{ padding: 24 }}>
      <Spin />
      <Typography.Text type="secondary">{t('state.loading')}</Typography.Text>
    </Flex>
  );
}

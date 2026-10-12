import { Layout, Typography } from 'antd';
import { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { NavigationSlot } from './NavigationSlot';

/** The Navigation area of the page frame. */
export function FrameSider() {
  const { t } = useTranslation();
  const navigation = useContext(NavigationSlot);
  return (
    <Layout.Sider breakpoint="lg" collapsedWidth={0} width={248} theme="light">
      <Typography.Title level={4} style={{ margin: 0, padding: 16 }}>
        {t('app.title')}
      </Typography.Title>
      {navigation}
    </Layout.Sider>
  );
}

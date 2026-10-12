import { useMenu } from '@refinedev/core';
import { Menu } from 'antd';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router';

/** The menu of Presentation: one entry for every Entity, leading to its page. */
export function Navigation() {
  const { t } = useTranslation();
  const { menuItems, selectedKey } = useMenu();
  return (
    <Menu
      mode="inline"
      aria-label={t('navigation.menu')}
      selectedKeys={[selectedKey]}
      items={menuItems.map((item) => ({
        key: item.key,
        label: item.route === undefined ? item.label : <Link to={item.route}>{item.label}</Link>,
      }))}
    />
  );
}

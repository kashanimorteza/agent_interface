import { MoonOutlined, SunOutlined } from '@ant-design/icons';
import { Segmented } from 'antd';
import { useTranslation } from 'react-i18next';
import { useDisplayMode } from './DisplayMode';
import { displayModes } from './modes';

export function ModeSwitch() {
  const { t } = useTranslation();
  const { mode, setMode } = useDisplayMode();
  return (
    <Segmented
      aria-label={t('mode.label')}
      value={mode}
      options={displayModes.map((value) => ({
        value,
        label: t(`mode.${value}`),
        icon: value === 'dark' ? <MoonOutlined /> : <SunOutlined />,
      }))}
      onChange={setMode}
    />
  );
}

import { ThemedLayout } from '@refinedev/antd';
import { App, ConfigProvider } from 'antd';
import type { ReactNode } from 'react';
import { antdLocales } from '../i18n/antdLocale';
import { useDirection } from '../i18n/direction';
import { useLanguage } from '../i18n/useLanguage';
import { FrameHeader } from './FrameHeader';
import { FrameSider } from './FrameSider';
import { NavigationSlot } from './NavigationSlot';

interface PageFrameProps {
  /** What fills the Navigation area. */
  readonly navigation: ReactNode;
  /** The page shown in the content area. */
  readonly children: ReactNode;
}

/**
 * The frame every page appears in: a header with the language and display mode controls, an
 * area for Navigation and an area for the page content. It names no Entity.
 */
export function PageFrame({ navigation, children }: PageFrameProps) {
  const direction = useDirection();
  const { language } = useLanguage();
  return (
    <ConfigProvider direction={direction} locale={antdLocales[language]}>
      <App>
        <NavigationSlot.Provider value={navigation}>
          <ThemedLayout Sider={FrameSider} Header={FrameHeader}>
            {children}
          </ThemedLayout>
        </NavigationSlot.Provider>
      </App>
    </ConfigProvider>
  );
}

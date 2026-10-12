import { Flex, Layout, theme } from 'antd';
import { LanguageSwitch } from '../i18n/LanguageSwitch';
import { ModeSwitch } from '../theme/ModeSwitch';

/** The header of the page frame: the language and display mode controls. */
export function FrameHeader() {
  const { token } = theme.useToken();
  return (
    <Layout.Header
      style={{
        background: token.colorBgContainer,
        paddingInline: token.padding,
        borderBottom: `${token.lineWidth}px ${token.lineType} ${token.colorBorderSecondary}`,
      }}
    >
      <Flex align="center" justify="flex-end" gap={token.marginSM} style={{ height: '100%' }}>
        <ModeSwitch />
        <LanguageSwitch />
      </Flex>
    </Layout.Header>
  );
}

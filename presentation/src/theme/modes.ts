import { theme, type ThemeConfig } from 'antd';
import { tokens } from './tokens';

export const displayModes = ['light', 'dark'] as const;

export type DisplayMode = (typeof displayModes)[number];

/** What a mode changes about the seed tokens; the light mode is the seed tokens as they are. */
const modeTokens: Readonly<Record<DisplayMode, NonNullable<ThemeConfig['token']>>> = {
  light: {},
  dark: {
    colorPrimary: '#3fc1be',
    colorInfo: '#3fc1be',
    colorSuccess: '#5fc27a',
    colorWarning: '#e0a43a',
    colorError: '#ff7b72',
    colorTextLightSolid: '#04201f',
  },
};

const baseAlgorithm = {
  light: theme.defaultAlgorithm,
  dark: theme.darkAlgorithm,
} as const;

export function themeOf(mode: DisplayMode): ThemeConfig {
  return {
    algorithm: baseAlgorithm[mode],
    token: { ...tokens, ...modeTokens[mode] },
  };
}

/** The same mode with the denser sizing used for tables that hold many rows. */
export function compactThemeOf(mode: DisplayMode): ThemeConfig {
  return {
    algorithm: [baseAlgorithm[mode], theme.compactAlgorithm],
    token: { ...tokens, ...modeTokens[mode] },
  };
}

import type { ThemeConfig } from 'antd';

export const fontFamily =
  "'Vazirmatn', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif";

/**
 * The seed tokens every part of the application takes its look from. The color, shape and
 * type of each part, and of each display mode, derive from these.
 */
export const tokens: NonNullable<ThemeConfig['token']> = {
  colorPrimary: '#0e7c7b',
  colorInfo: '#0e7c7b',
  colorSuccess: '#237a35',
  colorWarning: '#8a5a00',
  colorError: '#c92a2a',
  borderRadius: 6,
  fontFamily,
  fontSize: 14,
  wireframe: false,
};

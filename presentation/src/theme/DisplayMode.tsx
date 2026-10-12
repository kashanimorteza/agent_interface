import { ConfigProvider } from 'antd';
import { createContext, useContext, useMemo, useState, type ReactNode } from 'react';
import { themeOf, type DisplayMode } from './modes';

interface DisplayModeValue {
  readonly mode: DisplayMode;
  readonly setMode: (mode: DisplayMode) => void;
}

const DisplayModeContext = createContext<DisplayModeValue | null>(null);

function preferredMode(): DisplayMode {
  const query =
    typeof window.matchMedia === 'function'
      ? window.matchMedia('(prefers-color-scheme: dark)')
      : null;
  return query?.matches === true ? 'dark' : 'light';
}

/** Holds the chosen display mode and gives every part below it the look of that mode. */
export function DisplayModeProvider({ children }: { readonly children: ReactNode }) {
  const [mode, setMode] = useState<DisplayMode>(preferredMode);
  const value = useMemo(() => ({ mode, setMode }), [mode]);
  return (
    <DisplayModeContext.Provider value={value}>
      <ConfigProvider theme={themeOf(mode)}>{children}</ConfigProvider>
    </DisplayModeContext.Provider>
  );
}

export function useDisplayMode(): DisplayModeValue {
  const value = useContext(DisplayModeContext);
  if (value === null) {
    throw new Error('useDisplayMode needs a DisplayModeProvider above it.');
  }
  return value;
}

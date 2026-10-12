import { useEffect } from 'react';
import type { Language } from './languages';
import { useLanguage } from './useLanguage';

export type Direction = 'rtl' | 'ltr';

/** The reading direction of each selected language. */
export const directionOf: Readonly<Record<Language, Direction>> = {
  fa: 'rtl',
  en: 'ltr',
};

/** Gives the reading direction of the selected language and applies it to the whole document. */
export function useDirection(): Direction {
  const { language } = useLanguage();
  const direction = directionOf[language];
  useEffect(() => {
    document.documentElement.dir = direction;
    document.documentElement.lang = language;
  }, [direction, language]);
  return direction;
}

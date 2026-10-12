import type { Locale } from 'antd/es/locale';
import enUS from 'antd/locale/en_US';
import faIR from 'antd/locale/fa_IR';
import type { Language } from './languages';

/** The texts of the component library, in each selected language. */
export const antdLocales: Readonly<Record<Language, Locale>> = {
  fa: faIR,
  en: enUS,
};

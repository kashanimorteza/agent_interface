import { useTranslation } from 'react-i18next';
import { defaultLanguage, isLanguage, languages, type Language } from './languages';

export interface LanguageChoice {
  readonly language: Language;
  readonly languages: readonly Language[];
  readonly setLanguage: (language: Language) => void;
}

export function useLanguage(): LanguageChoice {
  const { i18n } = useTranslation();
  const current = i18n.resolvedLanguage;
  return {
    language: isLanguage(current) ? current : defaultLanguage,
    languages,
    setLanguage: (language) => {
      void i18n.changeLanguage(language);
    },
  };
}

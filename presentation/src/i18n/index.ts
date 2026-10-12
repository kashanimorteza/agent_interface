import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { en } from './en';
import { fa } from './fa';
import { defaultLanguage } from './languages';

void i18n.use(initReactI18next).init({
  resources: { fa: { translation: fa }, en: { translation: en } },
  lng: defaultLanguage,
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;

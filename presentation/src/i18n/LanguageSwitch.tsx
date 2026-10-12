import { Segmented } from 'antd';
import { useTranslation } from 'react-i18next';
import { useLanguage } from './useLanguage';

export function LanguageSwitch() {
  const { t } = useTranslation();
  const { language, languages, setLanguage } = useLanguage();
  return (
    <Segmented
      aria-label={t('language.label')}
      value={language}
      options={languages.map((code) => ({ value: code, label: t(`language.${code}`) }))}
      onChange={setLanguage}
    />
  );
}

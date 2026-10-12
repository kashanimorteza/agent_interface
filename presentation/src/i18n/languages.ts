export const languages = ['fa', 'en'] as const;

export type Language = (typeof languages)[number];

/** The first selected language is the one the application starts in. */
export const defaultLanguage: Language = languages[0];

export function isLanguage(value: string | undefined): value is Language {
  return languages.some((language) => language === value);
}

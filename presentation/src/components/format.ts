/** A date and time as text in the language, always in the Gregorian calendar the Declarations use. */
export function formatDateTime(value: string, language: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat(language, {
    calendar: 'gregory',
    dateStyle: 'medium',
    timeStyle: 'medium',
  }).format(date);
}

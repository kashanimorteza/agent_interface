/**
 * The one place the address of API is read. It holds the Base URL API's runtime
 * Configuration states, and no address is written anywhere in source.
 */
export function apiAddress(): string {
  const setting = import.meta.env.VITE_API_URL;
  if (setting === undefined || setting.trim() === '') {
    throw new Error('The API address setting VITE_API_URL is not set.');
  }
  return setting.trim().replace(/\/+$/, '');
}

export const API_ADDRESS_VARIABLE = 'PRESENTATION_API_URL'

export class ApiAddressError extends Error {
  override name = 'ApiAddressError'
}

export type ApiAddress = {
  /** The complete Base URL of the running API, including its URL Key, without a trailing slash. */
  readonly baseUrl: string
}

/**
 * Reads the one runtime API address setting. An unset or malformed value is
 * reported with an `ApiAddressError` and never replaced by another address.
 * The value is never echoed: it may carry the URL Key.
 */
export function readApiAddress(
  environment: Readonly<Record<string, string | undefined>>,
): ApiAddress {
  const raw = environment[API_ADDRESS_VARIABLE]
  if (raw === undefined || raw.trim() === '') {
    throw new ApiAddressError(
      `The API address is not set. Set ${API_ADDRESS_VARIABLE} to the complete Base URL of the running API, including its URL Key.`,
    )
  }
  let url: URL
  try {
    url = new URL(raw.trim())
  } catch {
    throw new ApiAddressError(
      `The API address in ${API_ADDRESS_VARIABLE} is not a valid URL. Set it to the complete Base URL of the running API, such as http://host:port/key.`,
    )
  }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    throw new ApiAddressError(
      `The API address in ${API_ADDRESS_VARIABLE} must use http or https.`,
    )
  }
  if (
    url.search !== '' ||
    url.hash !== '' ||
    url.username !== '' ||
    url.password !== ''
  ) {
    throw new ApiAddressError(
      `The API address in ${API_ADDRESS_VARIABLE} must be a plain Base URL without credentials, query or fragment.`,
    )
  }
  return { baseUrl: url.origin + url.pathname.replace(/\/+$/, '') }
}

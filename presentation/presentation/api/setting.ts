import { ApiAddressError, readApiAddress, type ApiAddress } from './address.ts'

export type ApiSetting =
  { readonly address: ApiAddress } | { readonly problem: string }

/** Reads the runtime API address setting on the server; a bad setting is reported, never replaced. */
export function loadApiSetting(): ApiSetting {
  try {
    return { address: readApiAddress(process.env) }
  } catch (error) {
    if (error instanceof ApiAddressError) return { problem: error.message }
    throw error
  }
}

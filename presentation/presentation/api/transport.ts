import type { ApiAddress } from './address.ts'

export type Placement = 'path' | 'query' | 'body'

export type ParameterDescriptor = {
  readonly name: string
  readonly in: Placement
  readonly required: boolean
}

export type EndpointDescriptor = {
  readonly method: string
  readonly path: string
  readonly parameters: readonly ParameterDescriptor[]
}

export type TransportResponse = {
  readonly status: number
  readonly ok: boolean
  readonly contentType: string | null
  /** The body as the API sent it: parsed JSON when it is JSON, the text otherwise, null when empty. */
  readonly body: unknown
}

/** The API could not be reached at all, as opposed to answering with an error. */
export class TransportFailure extends Error {
  override name = 'TransportFailure'
}

function present(value: unknown): boolean {
  return value !== undefined
}

function pathOf(
  endpoint: EndpointDescriptor,
  args: Readonly<Record<string, unknown>>,
): string {
  return endpoint.path.replace(/\{([^}]+)\}/g, (_, name: string) => {
    const value = args[name]
    if (!present(value) || value === null) {
      throw new TypeError(`The path parameter ${name} is required.`)
    }
    return encodeURIComponent(String(value))
  })
}

function queryOf(
  endpoint: EndpointDescriptor,
  args: Readonly<Record<string, unknown>>,
): string {
  const query = new URLSearchParams()
  for (const parameter of endpoint.parameters) {
    const value = args[parameter.name]
    if (parameter.in === 'query' && present(value) && value !== null) {
      query.append(parameter.name, String(value))
    }
  }
  const text = query.toString()
  return text === '' ? '' : `?${text}`
}

function bodyOf(
  endpoint: EndpointDescriptor,
  args: Readonly<Record<string, unknown>>,
): string | undefined {
  const members = endpoint.parameters.filter(
    (parameter) => parameter.in === 'body',
  )
  if (members.length === 0) return undefined
  const body: Record<string, unknown> = {}
  for (const parameter of members) {
    if (present(args[parameter.name]))
      body[parameter.name] = args[parameter.name]
  }
  return JSON.stringify(body)
}

async function parse(response: Response): Promise<unknown> {
  const text = await response.text()
  if (text === '') return null
  try {
    return JSON.parse(text) as unknown
  } catch {
    return text
  }
}

/**
 * Sends the call of one Endpoint to the API: each Parameter travels where the
 * endpoint description places it, and the response is handed back unchanged.
 */
export async function send(
  address: ApiAddress,
  endpoint: EndpointDescriptor,
  args: Readonly<Record<string, unknown>>,
): Promise<TransportResponse> {
  const url = `${address.baseUrl}${pathOf(endpoint, args)}${queryOf(endpoint, args)}`
  const body = bodyOf(endpoint, args)
  let response: Response
  try {
    response = await fetch(url, {
      method: endpoint.method.toUpperCase(),
      headers:
        body === undefined ? undefined : { 'Content-Type': 'application/json' },
      body,
    })
  } catch {
    throw new TransportFailure('The API could not be reached.')
  }
  return {
    status: response.status,
    ok: response.ok,
    contentType: response.headers.get('content-type'),
    body: await parse(response),
  }
}

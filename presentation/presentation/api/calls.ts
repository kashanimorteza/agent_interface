import type { ApiAddress } from './address.ts'
import { outcome, type ApiResult } from './errors.ts'
import { endpoints, type Endpoints } from './generated/endpoints.ts'
import type { paths } from './generated/schema.ts'
import { argumentsToWire, type ParameterForms } from './translation.ts'
import { send, type EndpointDescriptor } from './transport.ts'

type Flatten<T> = { [K in keyof T]: T[K] }
type Present<T> = [NonNullable<T>] extends [never] ? unknown : NonNullable<T>

type Operation<E> = E extends { path: infer P; method: infer M }
  ? P extends keyof paths
    ? M extends keyof paths[P]
      ? paths[P][M]
      : never
    : never
  : never

type PathPart<Op> = Op extends { parameters: { path: infer P } } ? P : unknown
type QueryPart<Op> = Op extends { parameters: { query?: infer Q } }
  ? Present<Q>
  : unknown
type BodyPart<Op> = Op extends { requestBody?: infer R }
  ? Present<R> extends { content: { 'application/json': infer B } }
    ? B
    : unknown
  : unknown

/** The Parameters of one Endpoint as the published description defines them. */
type PublishedArguments<Op> = Flatten<
  PathPart<Op> & QueryPart<Op> & BodyPart<Op>
>

/** The same Parameters with the values they take as interface data. */
type CallArguments<W> = {
  [K in keyof W]: K extends keyof ParameterForms
    ? ParameterForms[K] | (null extends W[K] ? null : never)
    : W[K]
}

type Call<E> =
  CallArguments<PublishedArguments<Operation<E>>> extends infer A
    ? (
        ...args: Record<PropertyKey, never> extends A ? [args?: A] : [args: A]
      ) => Promise<ApiResult<unknown>>
    : never

/** One call for every Endpoint the API serves: Group, then Adapter, then Endpoint name. */
export type ApiClient = {
  [G in keyof Endpoints]: {
    [A in keyof Endpoints[G]]: {
      [O in keyof Endpoints[G][A]]: Call<Endpoints[G][A][O]>
    }
  }
}

type EndpointTable = Readonly<
  Record<
    string,
    Readonly<Record<string, Readonly<Record<string, EndpointDescriptor>>>>
  >
>

/**
 * Builds the calls from the endpoint table, so an Endpoint added to or removed
 * from the description adds or removes its call when the table is regenerated.
 */
export function createApiClient(address: ApiAddress): ApiClient {
  const table: EndpointTable = endpoints
  const client: Record<string, Record<string, Record<string, unknown>>> = {}
  for (const [group, adapters] of Object.entries(table)) {
    const byAdapter: Record<string, Record<string, unknown>> = {}
    client[group] = byAdapter
    for (const [adapter, operations] of Object.entries(adapters)) {
      const byName: Record<string, unknown> = {}
      byAdapter[adapter] = byName
      for (const [name, endpoint] of Object.entries(operations)) {
        byName[name] = (args: Record<string, unknown> = {}) =>
          outcome(() => send(address, endpoint, argumentsToWire(args)))
      }
    }
  }
  return client as unknown as ApiClient
}

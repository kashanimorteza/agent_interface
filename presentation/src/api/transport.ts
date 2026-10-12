import { apiAddress } from './address';
import type { paths } from './contract';

export type ApiPath = keyof paths;

export type Method = 'get' | 'post' | 'put' | 'patch' | 'delete';

export type MethodOf<P extends ApiPath> = {
  [M in Method]: NonNullable<paths[P][M]> extends never ? never : M;
}[Method];

type JsonBody<O> = O extends { requestBody?: infer R }
  ? NonNullable<R> extends { content: { 'application/json': infer B } }
    ? B
    : never
  : never;

type ParametersOf<O> = O extends { parameters: infer Q } ? Q : never;

type QueryOf<O> = ParametersOf<O> extends { query?: infer Q } ? NonNullable<Q> : never;

export interface SendRequest<P extends ApiPath, M extends MethodOf<P>> {
  readonly path?: Readonly<Record<string, string | number>>;
  readonly query?: Readonly<Partial<Record<keyof QueryOf<NonNullable<paths[P][M]>>, string>>>;
  readonly body?: JsonBody<NonNullable<paths[P][M]>>;
}

export interface Sent {
  readonly status: number;
  readonly ok: boolean;
  readonly mediaType: string;
  readonly body: unknown;
}

function fill(path: string, values: Readonly<Record<string, string | number>> = {}): string {
  return path.replace(/\{(\w+)\}/g, (_match, name: string) => {
    const value = values[name];
    if (value === undefined) {
      throw new Error(`The path parameter ${name} is missing.`);
    }
    return encodeURIComponent(String(value));
  });
}

function queryString(query: Readonly<Record<string, string | undefined>> = {}): string {
  const search = new URLSearchParams();
  for (const [name, value] of Object.entries(query)) {
    if (value !== undefined) {
      search.append(name, value);
    }
  }
  const text = search.toString();
  return text === '' ? '' : `?${text}`;
}

async function readBody(response: Response): Promise<unknown> {
  const text = await response.text();
  if (text === '') {
    return null;
  }
  const mediaType = response.headers.get('content-type') ?? '';
  return mediaType.includes('json') ? (JSON.parse(text) as unknown) : text;
}

/**
 * The only function of Presentation that sends a request to API. It addresses the Endpoint
 * from the address setting and returns the response as API sent it.
 */
export async function send<P extends ApiPath, M extends MethodOf<P>>(
  method: M,
  path: P,
  request: SendRequest<P, M> = {},
): Promise<Sent> {
  const url = `${apiAddress()}${fill(path, request.path)}${queryString(request.query)}`;
  const hasBody = request.body !== undefined;
  const response = await fetch(url, {
    method: method.toUpperCase(),
    headers: {
      accept: 'application/json, application/problem+json',
      ...(hasBody ? { 'content-type': 'application/json' } : {}),
    },
    body: hasBody ? JSON.stringify(request.body) : undefined,
  });
  return {
    status: response.status,
    ok: response.ok,
    mediaType: response.headers.get('content-type') ?? '',
    body: await readBody(response),
  };
}

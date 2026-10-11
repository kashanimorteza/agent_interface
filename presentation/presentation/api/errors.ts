import { TransportFailure, type TransportResponse } from './transport.ts'
import { TranslationError } from './values.ts'

/** An error the API returned as Problem Details, exactly as it was sent. */
export type ApiProblem = {
  readonly type: string
  readonly status: number
  readonly title: string | null
  readonly detail: string | null
}

export type ApiFailure =
  | { readonly kind: 'problem'; readonly problem: ApiProblem }
  /** The API could not be reached; it returned nothing. */
  | { readonly kind: 'unreachable'; readonly message: string }
  /** The API answered with an error that is not Problem Details; nothing is invented for it. */
  | {
      readonly kind: 'unrecognized'
      readonly status: number
      readonly body: unknown
    }
  /** A value could not be put into the form the API publishes, so nothing was sent. */
  | { readonly kind: 'untranslatable'; readonly message: string }

export type ApiResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly failure: ApiFailure }

function text(value: unknown): string | null {
  return typeof value === 'string' ? value : null
}

function problemOf(response: TransportResponse): ApiProblem | null {
  const { body, contentType } = response
  if (contentType === null || !contentType.includes('application/problem+json'))
    return null
  if (body === null || typeof body !== 'object') return null
  const members = body as Record<string, unknown>
  if (typeof members.type !== 'string') return null
  return {
    type: members.type,
    status:
      typeof members.status === 'number' ? members.status : response.status,
    title: text(members.title),
    detail: text(members.detail),
  }
}

/** Hands a response on: a result as the API gave it, or its error without retry, recovery or rewording. */
export function interpret(response: TransportResponse): ApiResult<unknown> {
  if (response.ok) return { ok: true, value: response.body }
  const problem = problemOf(response)
  if (problem !== null)
    return { ok: false, failure: { kind: 'problem', problem } }
  return {
    ok: false,
    failure: {
      kind: 'unrecognized',
      status: response.status,
      body: response.body,
    },
  }
}

/** Runs one request and reports a failure to reach the API distinctly from an error the API returned. */
export async function outcome(
  request: () => Promise<TransportResponse>,
): Promise<ApiResult<unknown>> {
  try {
    return interpret(await request())
  } catch (error) {
    if (error instanceof TransportFailure) {
      return {
        ok: false,
        failure: { kind: 'unreachable', message: error.message },
      }
    }
    if (error instanceof TranslationError) {
      return {
        ok: false,
        failure: { kind: 'untranslatable', message: error.message },
      }
    }
    throw error
  }
}

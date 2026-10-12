import type { HttpError } from '@refinedev/core';
import type { Sent } from './transport';

/** An error API returned, delivered as it was returned: its kind, status and detail. */
export class ApiError extends Error implements HttpError {
  readonly statusCode: number;
  readonly kind: string | null;
  readonly title: string | null;
  readonly detail: string;

  constructor(status: number, kind: string | null, title: string | null, detail: string) {
    super(detail);
    this.name = 'ApiError';
    this.statusCode = status;
    this.kind = kind;
    this.title = title;
    this.detail = detail;
  }
}

/** The failure to reach API at all, as opposed to an error API returned. */
export class ApiUnreachableError extends Error implements HttpError {
  readonly statusCode = 0;

  constructor(cause: unknown) {
    super(cause instanceof Error ? cause.message : String(cause), { cause });
    this.name = 'ApiUnreachableError';
  }
}

function text(value: unknown): string | null {
  return typeof value === 'string' ? value : null;
}

function problemOf(sent: Sent): ApiError {
  const body = sent.body;
  if (typeof body === 'object' && body !== null && !Array.isArray(body)) {
    const problem = body as Record<string, unknown>;
    const detail = problem['detail'];
    return new ApiError(
      sent.status,
      text(problem['type']),
      text(problem['title']),
      typeof detail === 'string' ? detail : detail === undefined ? '' : JSON.stringify(detail),
    );
  }
  return new ApiError(sent.status, null, null, typeof body === 'string' ? body : '');
}

/**
 * Delivers the outcome of one call: the decoded body when API answered successfully, API's own
 * error when it refused, and an unreachable failure when no answer came.
 */
export async function call(attempt: Promise<Sent>): Promise<unknown> {
  let sent: Sent;
  try {
    sent = await attempt;
  } catch (cause) {
    throw new ApiUnreachableError(cause);
  }
  if (sent.ok) {
    return sent.body;
  }
  throw problemOf(sent);
}

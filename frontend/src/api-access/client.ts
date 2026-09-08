// The one place this layer talks to the application.
//
// Everything above asks for an operation and gets back either a result or a
// refusal carrying the reason the application gave. Nothing above performs a
// request of its own, and nothing about the transport travels upward.
//
// Where the application is comes from the binding the composition declares,
// delivered at start-up. It is never written down here.

export const APPLICATION_ADDRESS = process.env.APPLICATION_ADDRESS ?? "";

/** A refusal the application answered with, in the words it used. */
export class Refused extends Error {
  readonly status: number;
  readonly kind: string;

  constructor(status: number, kind: string, reason: string) {
    super(reason);
    this.name = "Refused";
    this.status = status;
    this.kind = kind;
  }
}

/** The application could not be reached at all. */
export class Unreachable extends Error {
  constructor(address: string, cause: unknown) {
    super(`the application at ${address || "an address nobody has declared"} could not be reached`);
    this.name = "Unreachable";
    this.cause = cause;
  }
}

export interface Request {
  readonly path: string;
  readonly method?: "GET" | "POST" | "PATCH" | "DELETE";
  readonly body?: unknown;
  readonly query?: Readonly<Record<string, string | number | undefined>>;
}

function addressFor(path: string, query: Request["query"]): string {
  const parameters = new URLSearchParams();
  for (const [name, value] of Object.entries(query ?? {})) {
    if (value !== undefined) parameters.set(name, String(value));
  }
  const asked = parameters.toString();
  return `${APPLICATION_ADDRESS}${path}${asked ? `?${asked}` : ""}`;
}

async function refusalFrom(response: Response): Promise<Refused> {
  let kind = "Refused";
  let reason = response.statusText || "the application refused the request";
  try {
    const answered = await response.json();
    if (answered && typeof answered === "object") {
      // The application says what it refused and why; both are carried as they
      // came, never reworded into something it did not say.
      if (typeof answered.reason === "string") reason = answered.reason;
      if (typeof answered.refused === "string") kind = answered.refused;
      if (Array.isArray(answered.detail)) {
        reason = answered.detail
          .map((one: { loc?: unknown[]; msg?: string }) =>
            `${(one.loc ?? []).slice(1).join(".") || "the request"}: ${one.msg ?? ""}`.trim(),
          )
          .join("; ");
        kind = "Invalid";
      }
    }
  } catch {
    // A refusal that carries no readable body still carries its status.
  }
  return new Refused(response.status, kind, reason);
}

/** Ask the application for something, through the only door there is. */
export async function ask<T>(request: Request): Promise<T> {
  const { path, method = "GET", body, query } = request;

  let response: Response;
  try {
    response = await fetch(addressFor(path, query), {
      method,
      headers: body === undefined ? {} : { "content-type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
      cache: "no-store",
    });
  } catch (cause) {
    throw new Unreachable(APPLICATION_ADDRESS, cause);
  }

  if (!response.ok) throw await refusalFrom(response);
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

// Saying exactly what changed, and nothing else.
//
// A field nobody touched is left out, so it keeps whatever value it already
// has. A field deliberately emptied is sent as empty, because that is a change.
// And a value the application supplies for itself is never invented here to
// make a request look complete.

import type { FieldDescription } from "./contract/catalogue";

export type Value = string | number | boolean | null;

/** What a person has entered, and which of those fields they actually touched. */
export interface Entered {
  readonly values: Readonly<Record<string, Value>>;
  readonly touched: ReadonlySet<string>;
}

/**
 * The body of a change: only the touched fields.
 *
 * Leaving a field alone and clearing it are different things, and this is where
 * that difference becomes two different requests.
 */
export function changeBody(
  entered: Entered,
  fields: readonly FieldDescription[],
): Record<string, Value> {
  const changeable = new Map(fields.map((field) => [field.name, field]));
  const body: Record<string, Value> = {};

  for (const name of entered.touched) {
    const field = changeable.get(name);
    if (!field || !field.changeable) continue;
    body[name] = entered.values[name] ?? null;
  }
  return body;
}

/**
 * The body of a creation: what was actually supplied.
 *
 * A field left blank that the application can supply for itself — because it
 * has a default, or generates it — is left out rather than filled in with
 * something the person never chose.
 */
export function creationBody(
  entered: Entered,
  fields: readonly FieldDescription[],
): Record<string, Value> {
  const body: Record<string, Value> = {};

  for (const field of fields) {
    const supplied = entered.values[field.name];
    const blank = supplied === undefined || supplied === "";

    if (blank && !field.required) continue;
    if (blank && field.nullable) {
      body[field.name] = null;
      continue;
    }
    if (blank) continue;
    body[field.name] = supplied as Value;
  }
  return body;
}

/** Whether an entered value differs from the one a record already carries. */
export function differs(entered: Value | undefined, held: unknown): boolean {
  if (entered === undefined) return false;
  if (held === null || held === undefined) return entered !== null && entered !== "";
  return String(entered) !== String(held);
}

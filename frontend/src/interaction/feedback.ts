// What the interface is doing, as something it can say out loud.
//
// Waiting, emptiness and refusal are three different things, and an interface
// that shows the same blank space for all three leaves a person guessing. Each
// gets its own name here so what is rendered can tell them apart.

import { Refused, Unreachable } from "@/api-access";

export type Progress = "idle" | "working" | "settled" | "refused";

export interface Refusal {
  /** What the application called it, or how it could not be reached. */
  readonly kind: string;
  /** The reason, in the words the application used. */
  readonly reason: string;
  readonly status: number | null;
}

/** A refusal as it came, never reworded into something it did not say. */
export function refusalFrom(error: unknown): Refusal {
  if (error instanceof Refused) {
    return { kind: error.kind, reason: error.message, status: error.status };
  }
  if (error instanceof Unreachable) {
    return { kind: "Unreachable", reason: error.message, status: null };
  }
  return {
    kind: "Unexpected",
    reason: error instanceof Error ? error.message : String(error),
    status: null,
  };
}

export interface Standing<T> {
  readonly progress: Progress;
  readonly value: T | null;
  readonly refusal: Refusal | null;
}

export function idle<T>(): Standing<T> {
  return { progress: "idle", value: null, refusal: null };
}

export function working<T>(previous: Standing<T>): Standing<T> {
  return { progress: "working", value: previous.value, refusal: null };
}

export function settled<T>(value: T): Standing<T> {
  return { progress: "settled", value, refusal: null };
}

export function refused<T>(previous: Standing<T>, error: unknown): Standing<T> {
  return { progress: "refused", value: previous.value, refusal: refusalFrom(error) };
}

/** Whether a settled result has nothing in it — empty, which is not an error. */
export function isEmpty<T>(standing: Standing<readonly T[]>): boolean {
  return standing.progress === "settled" && (standing.value?.length ?? 0) === 0;
}

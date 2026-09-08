"use client";

// Holding what a person types until they mean it.
//
// What has been typed is not yet what someone means, and the difference between
// a field they left alone and one they deliberately cleared is the difference
// between two different requests. This keeps both.
//
// Whatever can be seen to be wrong from here is caught here — a required field
// left blank, a value too long for what the contract accepts, a number that is
// not one. Anything the application decides is still asked of the application.

import { useCallback, useMemo, useState } from "react";

import { differs, type Entered, type FieldDescription, type Record_, type Value } from "@/api-access";

export interface Entry {
  readonly values: Readonly<Record<string, Value>>;
  readonly touched: ReadonlySet<string>;
  readonly complaints: Readonly<Record<string, string>>;
  readonly hasComplaints: boolean;
  readonly hasChanges: boolean;
  set(name: string, value: Value): void;
  clear(name: string): void;
  reset(): void;
  entered(): Entered;
}

function startingValues(fields: readonly FieldDescription[], from: Record_ | null): Record<string, Value> {
  const values: Record<string, Value> = {};
  for (const field of fields) {
    // A write-only field is never returned, so there is nothing to start it
    // from — it begins blank whether the record exists or not.
    const held = from && !field.writeOnly ? from[field.name] : undefined;
    values[field.name] = held === undefined || held === null ? "" : (held as Value);
  }
  return values;
}

function complaintAbout(field: FieldDescription, value: Value, forCreation: boolean): string | null {
  const blank = value === "" || value === null || value === undefined;

  if (blank) {
    // A field the application fills in for itself is not missing when it is
    // blank; only one the contract insists on is.
    if (forCreation && field.required && !field.nullable) return "this is needed";
    return null;
  }
  if (field.maxLength !== null && String(value).length > field.maxLength) {
    return `at most ${field.maxLength} characters`;
  }
  if ((field.type === "integer" || field.type === "number") && Number.isNaN(Number(value))) {
    return "this has to be a number";
  }
  if (field.type === "integer" && !Number.isInteger(Number(value))) {
    return "this has to be a whole number";
  }
  return null;
}

/** What a person is entering, for one kind of data. */
export function useEntry(
  fields: readonly FieldDescription[],
  options: { readonly from?: Record_ | null; readonly forCreation?: boolean } = {},
): Entry {
  const { from = null, forCreation = false } = options;
  const [values, setValues] = useState<Record<string, Value>>(() => startingValues(fields, from));
  const [touched, setTouched] = useState<ReadonlySet<string>>(() => new Set<string>());

  const set = useCallback((name: string, value: Value) => {
    setValues((held) => ({ ...held, [name]: value }));
    setTouched((held) => new Set(held).add(name));
  }, []);

  const clear = useCallback((name: string) => {
    // Clearing is a change, and stays one: the field is touched and empty.
    setValues((held) => ({ ...held, [name]: "" }));
    setTouched((held) => new Set(held).add(name));
  }, []);

  const reset = useCallback(() => {
    setValues(startingValues(fields, from));
    setTouched(new Set<string>());
  }, [fields, from]);

  const complaints = useMemo(() => {
    const found: Record<string, string> = {};
    for (const field of fields) {
      if (!forCreation && !touched.has(field.name)) continue;
      const complaint = complaintAbout(field, values[field.name], forCreation);
      if (complaint) found[field.name] = complaint;
    }
    return found;
  }, [fields, values, touched, forCreation]);

  const hasChanges = useMemo(() => {
    if (forCreation) return Object.values(values).some((value) => value !== "" && value !== null);
    return [...touched].some((name) => differs(values[name], from?.[name] ?? null));
  }, [touched, values, from, forCreation]);

  return {
    values,
    touched,
    complaints,
    hasComplaints: Object.keys(complaints).length > 0,
    hasChanges,
    set,
    clear,
    reset,
    entered: () => ({ values, touched }),
  };
}

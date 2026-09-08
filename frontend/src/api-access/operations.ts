// What can be asked of the application, for any kind of data.
//
// One set of operations serves all of them, because the contract offers the same
// ones for each; which paths they sit at comes from the contract's description
// rather than from anything written here.

import { ask } from "./client";
import { changeBody, creationBody, type Entered, type Value } from "./changes";
import type { ResourceDescription } from "./contract/catalogue";

export type Record_ = Readonly<Record<string, unknown>>;

export interface Page {
  readonly records: readonly Record_[];
  readonly offset: number;
  readonly asked: number;
}

export async function listRecords(
  resource: ResourceDescription,
  { limit, offset = 0 }: { limit: number; offset?: number },
): Promise<Page> {
  const records = await ask<Record_[]>({
    path: `${resource.path}/`,
    query: { limit, offset },
  });
  return { records, offset, asked: limit };
}

export async function readRecord(
  resource: ResourceDescription,
  identifier: Value,
): Promise<Record_> {
  return ask<Record_>({ path: `${resource.path}/${identifier}` });
}

export async function createRecord(
  resource: ResourceDescription,
  entered: Entered,
): Promise<Record_> {
  return ask<Record_>({
    path: `${resource.path}/`,
    method: "POST",
    body: creationBody(entered, resource.fields),
  });
}

export async function changeRecord(
  resource: ResourceDescription,
  identifier: Value,
  entered: Entered,
): Promise<Record_> {
  return ask<Record_>({
    path: `${resource.path}/${identifier}`,
    method: "PATCH",
    body: changeBody(entered, resource.fields),
  });
}

export async function removeRecord(
  resource: ResourceDescription,
  identifier: Value,
): Promise<void> {
  await ask<void>({ path: `${resource.path}/${identifier}`, method: "DELETE" });
}

export async function setRecordStatus(
  resource: ResourceDescription,
  identifier: Value,
  enabled: boolean,
): Promise<Record_> {
  return ask<Record_>({
    path: `${resource.path}/${identifier}/status`,
    method: "POST",
    body: { action: enabled ? "enable" : "disable" },
  });
}

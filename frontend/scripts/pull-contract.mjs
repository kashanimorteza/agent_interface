// Take the client's shapes from the contract's own description.
//
// Nothing about the application's data is written out by hand here. This fetches
// the description the contract publishes, keeps a snapshot of it, generates the
// types from that snapshot, and derives the catalogue of what can be worked with
// and which fields each kind of data carries.
//
//   node scripts/pull-contract.mjs           pull, generate and derive
//   node scripts/pull-contract.mjs --check   compare the snapshot with the live
//                                            contract and report any difference
//
// A field that can be sent but never comes back is write-only — that is how a
// credential is recognised, from the contract rather than from its name.

import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import openapiTS, { astToString } from "openapi-typescript";

import { loadConfiguration } from "../configuration.mjs";

const LAYER_ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const CONTRACT_DIRECTORY = join(LAYER_ROOT, "src", "api-access", "contract");
const SNAPSHOT = join(CONTRACT_DIRECTORY, "description.json");
const TYPES = join(CONTRACT_DIRECTORY, "schema.d.ts");
const CATALOGUE = join(CONTRACT_DIRECTORY, "catalogue.ts");

const checking = process.argv.includes("--check");

function describedAddress() {
  const configuration = loadConfiguration();
  if (!configuration.bindings.application) {
    throw new Error(
      "the composition does not say where the application is; add the address to " +
        "the frontend binding in the project's public configuration",
    );
  }
  return configuration.bindings.application;
}

async function fetchDescription(address) {
  const response = await fetch(`${address}/openapi.json`);
  if (!response.ok) {
    throw new Error(`the contract at ${address} did not describe itself: ${response.status}`);
  }
  return response.json();
}

// <!-------------------------------------------- deriving the catalogue -->

function schemaName(reference) {
  return reference?.$ref?.split("/").pop() ?? null;
}

function fieldsOf(schema, description) {
  const properties = schema?.properties ?? {};
  const required = new Set(schema?.required ?? []);
  return Object.entries(properties).map(([name, property]) => ({
    name,
    required: required.has(name),
    ...describeType(property, description),
  }));
}

function describeType(property, description) {
  const resolved = property.$ref
    ? description.components.schemas[schemaName(property)] ?? {}
    : property;
  const alternatives = resolved.anyOf ?? resolved.oneOf ?? null;

  if (alternatives) {
    const nullable = alternatives.some((one) => one.type === "null");
    const real = alternatives.find((one) => one.type !== "null") ?? {};
    return { type: kindOf(real), nullable, maxLength: real.maxLength ?? null };
  }
  return {
    type: kindOf(resolved),
    nullable: resolved.type === "null",
    maxLength: resolved.maxLength ?? null,
  };
}

function kindOf(schema) {
  if (schema.type === "integer") return "integer";
  if (schema.type === "number") return "number";
  if (schema.type === "boolean") return "boolean";
  if (schema.format === "date-time") return "datetime";
  if (schema.anyOf || schema.oneOf) return "text";
  return schema.type === "string" ? "text" : "text";
}

function operationsOf(paths, base) {
  const collection = paths[`${base}/`] ?? {};
  const single = paths[`${base}/{identifier}`] ?? {};
  const status = paths[`${base}/{identifier}/status`] ?? {};
  return {
    list: Boolean(collection.get),
    create: Boolean(collection.post),
    read: Boolean(single.get),
    change: Boolean(single.patch),
    remove: Boolean(single.delete),
    status: Boolean(status.post),
  };
}

function deriveCatalogue(description) {
  const schemas = description.components?.schemas ?? {};
  const bases = new Set();
  for (const path of Object.keys(description.paths)) {
    const match = path.match(/^(\/[a-z0-9-]+)\/$/);
    if (match) bases.add(match[1]);
  }

  const resources = [];
  for (const base of [...bases].sort()) {
    const collection = description.paths[`${base}/`];
    const listed = collection?.get?.responses?.["200"]?.content?.["application/json"]?.schema;
    const outputName = schemaName(listed?.items ?? {});
    if (!outputName) continue;

    const inputName = `${outputName}Input`;
    const changeName = `${outputName}Change`;
    const output = schemas[outputName];
    const input = schemas[inputName];
    const change = schemas[changeName];
    if (!output || !input) continue;

    const outgoing = fieldsOf(output, description);
    const incoming = fieldsOf(input, description);
    const outgoingNames = new Set(outgoing.map((field) => field.name));

    resources.push({
      name: outputName,
      path: base,
      title: outputName.replace(/(?<=[a-z0-9])(?=[A-Z])/g, " "),
      operations: operationsOf(description.paths, base),
      // A field the contract accepts but never returns is write-only. That is
      // what a credential looks like from out here.
      fields: incoming.map((field) => ({
        ...field,
        writeOnly: !outgoingNames.has(field.name),
        changeable: Boolean(change?.properties?.[field.name]),
      })),
      returned: outgoing,
      identifier:
        outgoing.find((field) => field.name === "id")?.name ?? outgoing[0]?.name ?? "id",
    });
  }
  return resources;
}

function catalogueSource(resources, description) {
  return `// Derived from the contract's own description — do not edit by hand.
//
// Regenerate with \`npm run contract:pull\`; \`npm run contract:check\` says
// whether the contract has moved on since this was taken.
//
// Contract: ${description.info?.title ?? "unknown"} ${description.info?.version ?? ""}

export interface FieldDescription {
  readonly name: string;
  readonly required: boolean;
  readonly type: "text" | "integer" | "number" | "boolean" | "datetime";
  readonly nullable: boolean;
  readonly maxLength: number | null;
  readonly writeOnly: boolean;
  readonly changeable: boolean;
}

export interface ReturnedField {
  readonly name: string;
  readonly required: boolean;
  readonly type: "text" | "integer" | "number" | "boolean" | "datetime";
  readonly nullable: boolean;
  readonly maxLength: number | null;
}

export interface ResourceDescription {
  readonly name: string;
  readonly path: string;
  readonly title: string;
  readonly identifier: string;
  readonly operations: {
    readonly list: boolean;
    readonly create: boolean;
    readonly read: boolean;
    readonly change: boolean;
    readonly remove: boolean;
    readonly status: boolean;
  };
  readonly fields: readonly FieldDescription[];
  readonly returned: readonly ReturnedField[];
}

export const RESOURCES: readonly ResourceDescription[] = ${JSON.stringify(resources, null, 2)} as const;

export function resourceAt(path: string): ResourceDescription | undefined {
  return RESOURCES.find((resource) => resource.path === \`/\${path}\`);
}
`;
}

// <!-------------------------------------------- running -->

const address = describedAddress();
const live = await fetchDescription(address);

if (checking) {
  if (!existsSync(SNAPSHOT)) {
    console.error("no snapshot of the contract has been taken yet");
    process.exit(1);
  }
  const held = JSON.parse(readFileSync(SNAPSHOT, "utf8"));
  const same = JSON.stringify(held) === JSON.stringify(live);
  if (same) {
    console.log(`the contract at ${address} matches the shapes derived from it`);
    process.exit(0);
  }
  const heldPaths = new Set(Object.keys(held.paths ?? {}));
  const livePaths = new Set(Object.keys(live.paths ?? {}));
  console.error(`the contract at ${address} has moved on since the shapes were derived`);
  for (const path of livePaths) if (!heldPaths.has(path)) console.error(`  added:   ${path}`);
  for (const path of heldPaths) if (!livePaths.has(path)) console.error(`  removed: ${path}`);
  process.exit(1);
}

mkdirSync(CONTRACT_DIRECTORY, { recursive: true });
writeFileSync(SNAPSHOT, `${JSON.stringify(live, null, 2)}\n`);

const ast = await openapiTS(live);
writeFileSync(
  TYPES,
  `// Generated from the contract's own description — do not edit by hand.\n${astToString(ast)}`,
);

const resources = deriveCatalogue(live);
writeFileSync(CATALOGUE, catalogueSource(resources, live));

console.log(`took the contract from ${address}`);
console.log(`  ${Object.keys(live.paths).length} paths described`);
console.log(`  ${resources.length} kinds of data derived`);
console.log(
  `  ${resources.reduce((count, r) => count + r.fields.filter((f) => f.writeOnly).length, 0)} write-only fields recognised`,
);

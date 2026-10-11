import { execFile } from 'node:child_process'
import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { promisify } from 'node:util'
import { format, resolveConfig } from 'prettier'
import { endpoints } from '../presentation/api/generated/endpoints.ts'

const run = promisify(execFile)

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const MODEL = join(ROOT, '..', 'model')
const OUTPUT = join(ROOT, 'presentation', 'interaction', 'generated')

/**
 * Reads every Entity through Model's published Interface and prints what is
 * needed as JSON. Model is installed from its directory into a throw-away
 * environment, so nothing is written into Model or kept after the run.
 */
const READ_MODEL = `
import json
from decimal import Decimal
from model.interface import entities


def stated_default(field):
    if repr(field.default) == "NO_DEFAULT":
        return {"stated": False}
    value = field.default
    return {"stated": True, "value": str(value) if isinstance(value, Decimal) else value}


print(
    json.dumps(
        [
            {
                "name": entity.declaration.name,
                "description": entity.declaration.description,
                "fields": [
                    {
                        "name": field.name,
                        "description": field.description,
                        "type": field.type.value,
                        "nullable": field.nullable,
                        "default": stated_default(field),
                        "sensitivity": field.sensitivity.value if field.sensitivity else None,
                        "immutable": field.immutable,
                        "value_generation": field.value_generation.value if field.value_generation else None,
                    }
                    for field in entity.declaration.fields
                ],
                "relations": [
                    {
                        "local_field": relation.local_field,
                        "target_entity": relation.target_entity,
                        "target_field": relation.target_field,
                    }
                    for relation in entity.declaration.relations
                ],
            }
            for entity in entities
        ]
    )
)
`

type Json = null | boolean | number | string | Json[] | { [key: string]: Json }
type JsonObject = { [key: string]: Json }

function fail(message: string): never {
  throw new Error(message)
}

function object(value: Json | undefined, what: string): JsonObject {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    fail(`Model's Interface gave no ${what}.`)
  }
  return value
}

function text(value: Json | undefined, what: string): string {
  if (typeof value !== 'string') fail(`Model's Interface gave no ${what}.`)
  return value
}

async function readModel(): Promise<JsonObject[]> {
  let output: string
  try {
    ;({ stdout: output } = await run(
      'uv',
      [
        'run',
        '--no-project',
        '--with',
        MODEL,
        'python',
        '-I',
        '-c',
        READ_MODEL,
      ],
      { maxBuffer: 16 * 1024 * 1024 },
    ))
  } catch (error) {
    const detail =
      error instanceof Error && 'stderr' in error
        ? String(error.stderr).trim().split('\n').slice(-1)[0]
        : ''
    return fail(
      `Model could not be read through its Interface${detail ? `: ${detail}` : '.'}`,
    )
  }
  const list = JSON.parse(output) as Json
  if (!Array.isArray(list)) fail(`Model's Interface gave no Entity Collection.`)
  return list.map((entity) => object(entity, 'Entity'))
}

/** The Adapter of the API's Entity Group that serves an Entity: its name in lower case, words joined by underscores. */
function adapterOf(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, '_')
}

const ADAPTERS: ReadonlySet<string> = new Set(Object.keys(endpoints.entity))

type Entity = { adapter: string; name: string; description: string }

function entitiesOf(model: readonly JsonObject[]): Entity[] {
  const problems: string[] = []
  const result: Entity[] = model.map((entity) => {
    const name = text(entity.name, 'Entity name')
    const adapter = adapterOf(name)
    if (!ADAPTERS.has(adapter)) {
      problems.push(
        `The Entity ${name} has no Adapter in the API's Entity Group.`,
      )
    }
    return {
      adapter,
      name,
      description: text(entity.description, `description of ${name}`),
    }
  })
  if (new Set(result.map((entity) => entity.adapter)).size !== result.length) {
    problems.push(`Model's Entity Collection names an Entity twice.`)
  }
  if (problems.length > 0) fail(problems.join('\n'))
  return result
}

function entitiesSource(entities: readonly Entity[]): string {
  return [
    `// Generated from Model's Interface. Regenerate; do not edit.`,
    '',
    `export const entities = ${JSON.stringify(entities)} as const`,
    '',
    `export type EntityKey = (typeof entities)[number]['adapter']`,
    '',
  ].join('\n')
}

/** The value kinds Presentation holds a form of; a Type outside them stops the generation. */
const KINDS: ReadonlySet<string> = new Set([
  'string',
  'integer',
  'float',
  'decimal',
  'boolean',
  'datetime',
  'uuid',
])

type Field = {
  name: string
  description?: string
  kind: string
  required: boolean
  default?: Json
  sensitive: boolean
  immutable: boolean
  generated: boolean
  relation?: { entity: string; field: string }
}

function flag(value: Json | undefined, what: string): boolean {
  if (typeof value !== 'boolean') fail(`Model's Interface gave no ${what}.`)
  return value
}

/** Describes the Fields of every Entity exactly as its Declaration states them, in Declaration order. */
function fieldsOf(
  model: readonly JsonObject[],
  entities: readonly Entity[],
): Record<string, Field[]> {
  const problems: string[] = []
  const names = new Map<string, Set<string>>()
  model.forEach((entity, index) => {
    const fields = entity.fields
    if (!Array.isArray(fields)) fail(`Model's Interface gave no Fields.`)
    names.set(
      entities[index]!.adapter,
      new Set(fields.map((f) => text(object(f, 'Field').name, 'Field name'))),
    )
  })
  const result: Record<string, Field[]> = {}
  model.forEach((entity, index) => {
    const owner = entities[index]!
    const relations = new Map<string, { entity: string; field: string }>()
    const declared = entity.relations
    if (!Array.isArray(declared)) fail(`Model's Interface gave no Relations.`)
    for (const entry of declared) {
      const relation = object(entry, 'Relation')
      const target = adapterOf(text(relation.target_entity, 'Relation target'))
      const field = text(relation.target_field, 'Relation target Field')
      if (names.get(target)?.has(field) !== true) {
        problems.push(
          `The Relation of ${owner.name} on ${text(relation.local_field, 'Relation Field')} names ${target}.${field}, which Model does not declare.`,
        )
      }
      relations.set(text(relation.local_field, 'Relation Field'), {
        entity: target,
        field,
      })
    }
    result[owner.adapter] = (entity.fields as Json[]).map((entry) => {
      const declaration = object(entry, 'Field')
      const name = text(declaration.name, 'Field name')
      const kind = text(declaration.type, `Type of ${name}`)
      if (!KINDS.has(kind)) {
        problems.push(
          `The Field ${name} of ${owner.name} has the Type ${kind}, which Presentation holds no form of.`,
        )
      }
      const generated = declaration.value_generation !== null
      const stated = object(declaration.default, `default of ${name}`)
      const field: Field = {
        name,
        kind,
        required: !flag(declaration.nullable, `nullability of ${name}`),
        sensitive: declaration.sensitivity !== null,
        immutable: flag(declaration.immutable, `immutability of ${name}`),
        generated,
      }
      if (typeof declaration.description === 'string') {
        field.description = declaration.description
      }
      if (stated.stated === true && stated.value !== undefined) {
        field.default = stated.value
      }
      const relation = relations.get(name)
      if (relation !== undefined) field.relation = relation
      return field
    })
  })
  if (problems.length > 0) fail(problems.join('\n'))
  return result
}

function declarationsSource(fields: Record<string, Field[]>): string {
  return [
    `// Generated from Model's Interface. Regenerate; do not edit.`,
    '',
    `import type { FieldDescription } from '../fields'`,
    `import type { EntityKey } from './entities'`,
    '',
    `export const declarations = ${JSON.stringify(fields)} as const satisfies Record<EntityKey, readonly FieldDescription[]>`,
    '',
  ].join('\n')
}

async function pretty(source: string, file: string): Promise<string> {
  const options = (await resolveConfig(file)) ?? {}
  return format(source, { ...options, filepath: file })
}

async function main(): Promise<void> {
  const model = await readModel()
  const entities = entitiesOf(model)
  const files: [string, string][] = [
    ['entities.ts', entitiesSource(entities)],
    ['declarations.ts', declarationsSource(fieldsOf(model, entities))],
  ]
  const formatted: [string, string][] = []
  for (const [name, source] of files) {
    formatted.push([name, await pretty(source, join(OUTPUT, name))])
  }
  await mkdir(OUTPUT, { recursive: true })
  for (const [name, source] of formatted) {
    await writeFile(join(OUTPUT, name), source)
  }
}

main().catch((error: unknown) => {
  const message =
    error instanceof Error ? error.message : 'The generation failed.'
  console.error(`Generation failed: ${message}`)
  process.exitCode = 1
})

import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import openapiTS, { astToString, type OpenAPI3 } from 'openapi-typescript'
import { format, resolveConfig } from 'prettier'
import { ApiAddressError, readApiAddress } from '../presentation/api/address.ts'

type Json = null | boolean | number | string | Json[] | { [key: string]: Json }
type JsonObject = { [key: string]: Json }
type Placement = 'path' | 'query' | 'body'
type Parameter = { name: string; in: Placement; required: boolean }

const OUTPUT = join(
  dirname(fileURLToPath(import.meta.url)),
  '..',
  'presentation',
  'api',
  'generated',
)
const METHODS = ['get', 'put', 'post', 'delete', 'patch'] as const

function fail(message: string): never {
  throw new Error(message)
}

function object(value: Json | undefined, what: string): JsonObject {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    fail(`The API description has no ${what}.`)
  }
  return value
}

/** The description names its operations and schemas after the URL Key; the key never reaches the source. */
function withoutKey(description: JsonObject, prefix: string): JsonObject {
  const token = prefix.replace(/^\//, '')
  if (token === '') return description
  const sanitized = token.replace(/[^A-Za-z0-9]/g, '_')
  const paths = object(description.paths, 'paths')
  const renamed: JsonObject = {}
  for (const [path, item] of Object.entries(paths)) {
    if (!path.startsWith(`${prefix}/`)) {
      fail('The API description holds a path outside the configured Base URL.')
    }
    renamed[path.slice(prefix.length)] = item
  }
  const text = JSON.stringify({ ...description, paths: renamed })
    .split(`${sanitized}_`)
    .join('')
  if (text.includes(token) || text.includes(sanitized)) {
    fail('The API description still carries the URL Key after normalizing it.')
  }
  return JSON.parse(text) as JsonObject
}

function resolve(description: JsonObject, node: Json | undefined): JsonObject {
  const value = object(node, 'schema')
  const reference = value.$ref
  if (typeof reference !== 'string') return value
  const name = reference.replace('#/components/schemas/', '')
  const schemas = object(
    object(description.components, 'components').schemas,
    'schemas',
  )
  return object(schemas[name], `schema ${name}`)
}

function parametersOf(
  description: JsonObject,
  operation: JsonObject,
): Parameter[] {
  const result: Parameter[] = []
  const declared = operation.parameters
  if (Array.isArray(declared)) {
    for (const entry of declared) {
      const parameter = object(entry, 'parameter')
      const place = parameter.in
      if (place !== 'path' && place !== 'query') {
        fail(
          `The API description places a parameter in ${String(place)}, which is not served.`,
        )
      }
      result.push({
        name: String(parameter.name),
        in: place,
        required: parameter.required === true,
      })
    }
  }
  if (operation.requestBody !== undefined) {
    const body = object(operation.requestBody, 'request body')
    const content = object(
      object(body.content, 'request content')['application/json'],
      'JSON body',
    )
    const schema = resolve(description, content.schema)
    const properties = object(schema.properties, 'body properties')
    const required = Array.isArray(schema.required) ? schema.required : []
    for (const name of Object.keys(properties)) {
      result.push({ name, in: 'body', required: required.includes(name) })
    }
  }
  return result
}

type Entry = { method: string; path: string; parameters: Parameter[] }

function literal(entry: Entry): string {
  const parameters = entry.parameters
    .map((p) => `{ name: '${p.name}', in: '${p.in}', required: ${p.required} }`)
    .join(', ')
  return `{ method: '${entry.method}', path: '${entry.path}', parameters: [${parameters}] }`
}

function endpointTable(description: JsonObject): string {
  const table: Record<string, Record<string, Record<string, Entry>>> = {}
  const paths = object(description.paths, 'paths')
  for (const [path, item] of Object.entries(paths)) {
    const segments = path.split('/').filter((segment) => segment !== '')
    const [group, adapter, operationName] = segments
    if (
      group === undefined ||
      adapter === undefined ||
      operationName === undefined ||
      segments.length > 4
    ) {
      fail(
        `The API description holds a path (${path}) that is not Group, Adapter and Endpoint.`,
      )
    }
    const methods = METHODS.filter(
      (method) => object(item, 'path item')[method] !== undefined,
    )
    if (methods.length !== 1) {
      fail(`The path ${path} does not hold exactly one Method.`)
    }
    const method = methods[0] as (typeof METHODS)[number]
    const operation = object(object(item, 'path item')[method], 'operation')
    ;((table[group] ??= {})[adapter] ??= {})[operationName] = {
      method,
      path,
      parameters: parametersOf(description, operation),
    }
  }
  const body = Object.entries(table)
    .map(([group, adapters]) => {
      const inner = Object.entries(adapters)
        .map(([adapter, operations]) => {
          const entries = Object.entries(operations)
            .map(([name, entry]) => `${name}: ${literal(entry)},`)
            .join('\n')
          return `${adapter}: {\n${entries}\n},`
        })
        .join('\n')
      return `${group}: {\n${inner}\n},`
    })
    .join('\n')
  return [
    '// Generated from the API description. Regenerate; do not edit.',
    '',
    `export const endpoints = {\n${body}\n} as const`,
    '',
    'export type Endpoints = typeof endpoints',
    '',
  ].join('\n')
}

async function pretty(source: string, file: string): Promise<string> {
  const options = (await resolveConfig(file)) ?? {}
  return format(source, { ...options, filepath: file })
}

async function main(): Promise<void> {
  const address = readApiAddress(process.env)
  const response = await fetch(`${address.baseUrl}/openapi.json`).catch(() =>
    fail(
      'The API did not answer: start it, or correct the API address, and generate again.',
    ),
  )
  if (!response.ok) {
    fail(`The API description could not be read (status ${response.status}).`)
  }
  const prefix = new URL(address.baseUrl).pathname.replace(/\/+$/, '')
  const description = withoutKey((await response.json()) as JsonObject, prefix)

  const schema = astToString(
    await openapiTS(description as unknown as OpenAPI3),
  )
  const files: [string, string][] = [
    [
      'schema.ts',
      `// Generated from the API description. Regenerate; do not edit.\n${schema}`,
    ],
    ['endpoints.ts', endpointTable(description)],
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
  console.error(
    error instanceof ApiAddressError
      ? message
      : `Generation failed: ${message}`,
  )
  process.exitCode = 1
})

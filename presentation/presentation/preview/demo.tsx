'use client'

// TEMPORARY preview page, requested by the user to see the Theme and the built Components.
// It is not part of the Plan: delete this directory and restore app/page.tsx to remove it.
import { useState } from 'react'
import { useApiAccess, type FieldValue } from '@/api'
import { useLoaded } from '@/interaction/async'
import type {
  FieldDescription,
  FieldEntry,
  RecordValues,
} from '@/interaction/fields'
import { noFilters, type FilterDraft } from '@/interaction/filter'
import { unordered, type OrderAndLimit } from '@/interaction/order'
import { firstRequest, type AggregateOperation } from '@/interaction/aggregate'
import { AggregatePanel } from '@/view/aggregate-panel'
import { Button } from '@/view/button'
import { Confirmation } from '@/view/confirmation'
import { Empty, ErrorNotice, Loading, Success } from '@/view/feedback'
import { FieldInput } from '@/view/field-input'
import { FilterEditor } from '@/view/filter-editor'
import { OrderControls } from '@/view/order-controls'
import { PageFrame } from '@/view/page-frame'
import { RecordForm } from '@/view/record-form'
import { RecordTable } from '@/view/record-table'
import styles from './demo.module.css'

// The preview lists these by hand; the real Sections take them from the API contract.
const OPERATORS = [
  { name: 'EQUALS', value: 'one' as const },
  { name: 'NOT_EQUALS', value: 'one' as const },
  {
    name: 'GREATER_THAN',
    value: 'one' as const,
    kinds: ['integer', 'float', 'decimal', 'datetime'] as const,
  },
  { name: 'IN', value: 'many' as const },
  { name: 'CONTAINS', value: 'one' as const, kinds: ['string'] as const },
  { name: 'IS_NULL', value: 'none' as const },
]
const SAMPLE_FIELDS: FieldDescription[] = [
  { name: 'code', kind: 'string', required: true },
  { name: 'decimal_digits', kind: 'integer', required: true, default: 2 },
  { name: 'balance', kind: 'decimal', required: true },
  { name: 'opened_at', kind: 'datetime', required: false },
  { name: 'is_active', kind: 'boolean', required: true, default: true },
  { name: 'description', kind: 'string', required: false },
]
const AGGREGATES: AggregateOperation[] = [
  { name: 'count', takesFilters: true },
  {
    name: 'sum',
    fields: SAMPLE_FIELDS.filter(
      (f) => f.kind === 'decimal' || f.kind === 'integer',
    ),
    takesFilters: true,
  },
]
const SWATCHES = [
  'surface',
  'surface-raised',
  'surface-sunken',
  'border',
  'accent',
  'accent-subtle',
  'danger',
  'success',
  'warning',
  'text',
  'text-muted',
]

function kindOf(value: unknown): FieldDescription['kind'] {
  if (typeof value === 'boolean') return 'boolean'
  if (typeof value === 'number')
    return Number.isInteger(value) ? 'integer' : 'float'
  return 'string'
}

function Block({
  id,
  title,
  children,
}: {
  id: string
  title: string
  children: React.ReactNode
}) {
  return (
    <section id={id} className={styles.block}>
      <h2 className={styles.title}>{title}</h2>
      {children}
    </section>
  )
}

function Connection() {
  const access = useApiAccess()
  const client = access.status === 'ready' ? access.client : null
  const counts = useLoaded(client === null ? null : 'counts', async () => {
    const entries = Object.entries(client!.entity) as [
      string,
      {
        count: () => Promise<{ ok: boolean; value?: unknown; failure?: never }>
      },
    ][]
    return Promise.all(
      entries.map(
        async ([adapter, calls]) => [adapter, await calls.count()] as const,
      ),
    )
  })
  if (access.status === 'misconfigured') {
    return (
      <ErrorNotice
        failure={{ kind: 'untranslatable', message: access.problem }}
      />
    )
  }
  if (counts.status !== 'ready')
    return <Loading label="Asking the API how many records each Entity has" />
  const rows: RecordValues[] = counts.value.map(([adapter, result]) => ({
    entity: adapter,
    records: result.ok ? (result.value as number) : null,
  }))
  const failed = counts.value.find(([, r]) => !r.ok)
  return (
    <div className={styles.stack}>
      {failed === undefined ? (
        <Success>The API answered for all {rows.length} Entities.</Success>
      ) : (
        <ErrorNotice
          failure={{
            kind: 'unreachable',
            message:
              'The API did not answer for every Entity. Check the API address setting and that the API is running.',
          }}
        />
      )}
      <RecordTable
        caption="Records per Entity"
        fields={[
          { name: 'entity', kind: 'string', required: true },
          { name: 'records', kind: 'integer', required: true },
        ]}
        records={rows}
      />
    </div>
  )
}

function Currencies() {
  const access = useApiAccess()
  const list = useLoaded(access.status === 'ready' ? 'currency' : null, () =>
    access.status === 'ready'
      ? access.client.entity.currency.list({ limit: 10 })
      : Promise.reject(),
  )
  if (list.status !== 'ready') return <Loading />
  if (!list.value.ok) return <ErrorNotice failure={list.value.failure} />
  const records = list.value.value as RecordValues[]
  const sample = records[0] ?? {}
  const fields: FieldDescription[] = Object.entries(sample).map(
    ([name, value]) => ({
      name,
      kind: kindOf(value),
      required: false,
    }),
  )
  return (
    <RecordTable
      caption="Currencies"
      fields={fields}
      records={records}
      emptyTitle="No currencies"
      rowActions={(record) => <Button>Open {String(record.code)}</Button>}
    />
  )
}

function Gallery() {
  const [filters, setFilters] = useState<FilterDraft>(noFilters)
  const [order, setOrder] = useState<OrderAndLimit>(unordered)
  const [entry, setEntry] = useState<FieldEntry>({ state: 'empty' })
  const [asking, setAsking] = useState(false)
  const [request, setRequest] = useState(firstRequest(AGGREGATES)!)
  const [submitted, setSubmitted] = useState<string>('')
  const [result, setResult] = useState<FieldValue | undefined>(undefined)
  return (
    <div className={styles.stack}>
      <h3>Feedback</h3>
      <div className={styles.row}>
        <Loading />
        <Success>Saved.</Success>
        <Empty title="No records yet">
          Add the first record to get started.
        </Empty>
        <ErrorNotice
          failure={{
            kind: 'problem',
            problem: {
              type: 'InvalidInputError',
              status: 422,
              title: 'Unprocessable Content',
              detail: "'nope' is not a Field of Account",
            },
          }}
        />
      </div>
      <h3>Inputs</h3>
      <div className={styles.row}>
        <FieldInput
          field={{ name: 'unit_price', kind: 'decimal', required: true }}
          entry={entry}
          onChange={setEntry}
        />
        <FieldInput
          field={{ name: 'note', kind: 'string', required: false }}
          entry={{ state: 'empty' }}
          onChange={() => {}}
        />
      </div>
      <h3>Filters, order and limit</h3>
      <FilterEditor
        fields={SAMPLE_FIELDS}
        operators={OPERATORS}
        combinations={['AND', 'OR']}
        draft={filters}
        onChange={setFilters}
      />
      <OrderControls
        fields={SAMPLE_FIELDS}
        directions={['ASCENDING', 'DESCENDING']}
        value={order}
        onChange={setOrder}
      />
      <h3>Aggregates</h3>
      <AggregatePanel
        operations={AGGREGATES}
        filterFields={SAMPLE_FIELDS}
        filterOperators={OPERATORS}
        combinations={['AND', 'OR']}
        value={request}
        onChange={setRequest}
        onRun={(r) => setResult(r.operation === 'count' ? 42 : '1234.50')}
        result={result}
      />
      <h3>Form</h3>
      <RecordForm
        fields={SAMPLE_FIELDS}
        submitLabel="Add record"
        onSubmit={(entries) =>
          setSubmitted(
            Object.entries(entries)
              .map(([k, v]) => `${k}: ${v.state}`)
              .join(', '),
          )
        }
      />
      {submitted !== '' && <Success>{submitted}</Success>}
      <h3>Confirmation</h3>
      <div>
        <Button variant="danger" onClick={() => setAsking(true)}>
          Delete something
        </Button>
        <Confirmation
          open={asking}
          question="Delete the User with id 4?"
          confirmLabel="Delete user"
          onConfirm={() => setAsking(false)}
          onCancel={() => setAsking(false)}
        />
      </div>
    </div>
  )
}

export function Demo() {
  return (
    <PageFrame
      applicationTitle="Trading Assistant"
      heading="Preview"
      navigation={
        <ul className={styles.nav}>
          <li>
            <a href="#connection">API connection</a>
          </li>
          <li>
            <a href="#data">Live data</a>
          </li>
          <li>
            <a href="#theme">Theme</a>
          </li>
          <li>
            <a href="#components">Components</a>
          </li>
        </ul>
      }
    >
      <p className={styles.note}>
        A temporary preview of the Theme and the built Components. The real
        pages (one Section per Entity) are not built yet.
      </p>
      <Block id="connection" title="API connection">
        <Connection />
      </Block>
      <Block id="data" title="Live data">
        <Currencies />
      </Block>
      <Block id="theme" title="Theme">
        <div className={styles.swatches}>
          {SWATCHES.map((name) => (
            <div key={name} className={styles.swatch}>
              <span
                className={styles.chip}
                style={{ background: `var(--color-${name})` }}
              />
              <code>{name}</code>
            </div>
          ))}
        </div>
        <p dir="auto">
          نمونهٔ متن راست‌به‌چپ: جهت متن به‌صورت خودکار از محتوا تشخیص داده
          می‌شود.
        </p>
      </Block>
      <Block id="components" title="Components">
        <Gallery />
      </Block>
    </PageFrame>
  )
}

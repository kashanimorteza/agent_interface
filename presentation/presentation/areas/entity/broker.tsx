'use client'

import { useState } from 'react'
import { useAggregate } from '@/interaction/aggregate'
import {
  entityOf,
  useEntityAccess,
  type EntityAccess,
} from '@/interaction/entity'
import type { RecordValues } from '@/interaction/fields'
import { useRecordForm, type FormMode } from '@/interaction/form'
import { useListing } from '@/interaction/listing'
import { useRecord } from '@/interaction/record'
import { useRecordActions } from '@/interaction/record-actions'
import { useRelatedChoices } from '@/interaction/related'
import { useRemoveAll } from '@/interaction/remove-all'
import { AggregatePanel } from '@/view/aggregate-panel'
import { applicationTitle } from '@/view/application'
import { Button } from '@/view/button'
import { Confirmation } from '@/view/confirmation'
import { Empty, ErrorNotice, Loading, Success } from '@/view/feedback'
import { FilterEditor } from '@/view/filter-editor'
import { OrderControls } from '@/view/order-controls'
import { PageFrame } from '@/view/page-frame'
import { RecordDetails } from '@/view/record-details'
import { RecordForm } from '@/view/record-form'
import { RecordTable } from '@/view/record-table'
import { Stack, Toolbar } from '@/view/stack'

// The Broker Section: how a user works with Broker records. It is written out in full
// and shares no page with another Section; it composes only shared Components and the Theme.
const entity = entityOf('broker')

type Access = Extract<EntityAccess<'broker'>, { status: 'ready' }>

/** What the Section shows: the records, one record, the form to add one, or the form to edit one. */
type View =
  | { readonly kind: 'list' }
  | { readonly kind: 'details'; readonly id: number }
  | { readonly kind: 'add' }
  | { readonly kind: 'edit'; readonly id: number }

export function BrokerSection() {
  const access = useEntityAccess('broker')
  return (
    <PageFrame applicationTitle={applicationTitle} heading={entity.name}>
      {access.status === 'ready' ? (
        <BrokerRecords access={access} />
      ) : (
        <ErrorNotice failure={access.failure} />
      )}
    </PageFrame>
  )
}

function BrokerRecords({ access }: { access: Access }) {
  const { calls } = access
  const [view, setView] = useState<View>({ kind: 'list' })
  const [notice, setNotice] = useState<string | null>(null)
  const listing = useListing(calls.list, entity.fields)
  const actions = useRecordActions(calls, entity.fields, listing.refresh)
  const removeAll = useRemoveAll(entity.name, calls.truncate, listing.refresh)
  const aggregate = useAggregate(calls, entity.fields)

  /** Clears what the last action reported, so only the latest outcome is shown. */
  const quiet = () => {
    setNotice(null)
    actions.dismiss()
    removeAll.dismiss()
  }
  const toList = () => setView({ kind: 'list' })
  const saved = () => {
    setNotice(`The ${entity.name} was saved.`)
    listing.refresh()
    toList()
  }

  if (view.kind === 'details') {
    return (
      <Stack>
        <Toolbar label="Actions">
          <Button onClick={toList}>Back to the {entity.name} records</Button>
          <Button onClick={() => setView({ kind: 'edit', id: view.id })}>
            Edit
          </Button>
        </Toolbar>
        <BrokerDetails access={access} id={view.id} />
      </Stack>
    )
  }
  if (view.kind === 'add') {
    return (
      <Stack>
        <Toolbar label="Actions">
          <Button onClick={toList}>Back to the {entity.name} records</Button>
        </Toolbar>
        <BrokerForm access={access} mode={{ kind: 'add' }} onSaved={saved} />
      </Stack>
    )
  }
  if (view.kind === 'edit') {
    return (
      <Stack>
        <Toolbar label="Actions">
          <Button onClick={toList}>Back to the {entity.name} records</Button>
        </Toolbar>
        <BrokerEdit access={access} id={view.id} onSaved={saved} />
      </Stack>
    )
  }

  const idOf = (record: RecordValues) => Number(record.id)
  return (
    <Stack>
      <p>{entity.description}</p>
      <Toolbar label="Actions">
        <Button
          variant="primary"
          onClick={() => {
            quiet()
            setView({ kind: 'add' })
          }}
        >
          Add a {entity.name}
        </Button>
        <Button
          variant="danger"
          onClick={() => {
            quiet()
            removeAll.request()
          }}
        >
          Remove every {entity.name} record
        </Button>
      </Toolbar>
      {notice !== null && <Success>{notice}</Success>}
      {actions.state.status === 'done' && (
        <Success>
          The {entity.name} with id {actions.state.id} was{' '}
          {actions.state.action === 'delete'
            ? 'deleted'
            : `${actions.state.action}d`}
          .
        </Success>
      )}
      {actions.state.status === 'failed' && (
        <ErrorNotice failure={actions.state.failure} />
      )}
      {removeAll.state.status === 'done' && (
        <Success>Every {entity.name} record was removed.</Success>
      )}
      {removeAll.state.status === 'failed' && (
        <ErrorNotice failure={removeAll.state.failure} />
      )}
      <FilterEditor
        fields={entity.fields}
        operators={listing.vocabulary.operators}
        combinations={listing.vocabulary.combinations}
        draft={listing.filter}
        onChange={listing.setFilter}
        problems={listing.problems.filters}
      />
      <OrderControls
        fields={entity.fields}
        directions={listing.vocabulary.directions}
        value={listing.orderAndLimit}
        onChange={listing.setOrderAndLimit}
      />
      {listing.problems.limit !== null && (
        <p role="alert">{listing.problems.limit}</p>
      )}
      <Toolbar label="List">
        <Button
          variant="primary"
          onClick={() => {
            quiet()
            listing.apply()
          }}
        >
          List the {entity.name} records
        </Button>
      </Toolbar>
      {listing.state.status === 'loading' && <Loading />}
      {listing.state.status === 'failed' && (
        <ErrorNotice failure={listing.state.failure} />
      )}
      {listing.state.status === 'loaded' && (
        <RecordTable
          caption={`${entity.name} records`}
          fields={entity.fields}
          records={listing.state.records}
          emptyTitle={`No ${entity.name} records`}
          rowActions={(record) => (
            <>
              <Button
                onClick={() => setView({ kind: 'details', id: idOf(record) })}
              >
                Open
              </Button>
              <Button
                onClick={() => {
                  quiet()
                  setView({ kind: 'edit', id: idOf(record) })
                }}
              >
                Edit
              </Button>
              <Button
                disabled={record.is_active === true}
                onClick={() => {
                  quiet()
                  actions.enable(idOf(record))
                }}
              >
                Enable
              </Button>
              <Button
                disabled={record.is_active === false}
                onClick={() => {
                  quiet()
                  actions.disable(idOf(record))
                }}
              >
                Disable
              </Button>
              <Button
                variant="danger"
                onClick={() => {
                  quiet()
                  actions.requestDelete(idOf(record))
                }}
              >
                Delete
              </Button>
            </>
          )}
        />
      )}
      {aggregate.request !== null && (
        <AggregatePanel
          operations={aggregate.operations}
          filterFields={entity.fields}
          filterOperators={listing.vocabulary.operators}
          combinations={listing.vocabulary.combinations}
          value={aggregate.request}
          onChange={aggregate.setRequest}
          onRun={() => aggregate.run()}
          problems={aggregate.problems}
          busy={aggregate.state.status === 'loading'}
          {...(aggregate.state.status === 'ready' && {
            result: aggregate.state.value,
          })}
        />
      )}
      {aggregate.state.status === 'failed' && (
        <ErrorNotice failure={aggregate.state.failure} />
      )}
      <Confirmation
        open={actions.state.status === 'confirming'}
        question={`Delete the ${entity.name} with id ${'id' in actions.state ? actions.state.id : ''}?`}
        confirmLabel="Delete"
        onConfirm={actions.confirm}
        onCancel={actions.cancel}
      />
      <Confirmation
        open={removeAll.state.status === 'confirming'}
        question={
          removeAll.state.status === 'confirming'
            ? removeAll.state.question
            : ''
        }
        confirmLabel="Remove every record"
        onConfirm={removeAll.confirm}
        onCancel={removeAll.cancel}
      />
    </Stack>
  )
}

function BrokerDetails({ access, id }: { access: Access; id: number }) {
  const record = useRecord(access.calls.get_by_id, entity.fields, id)
  if (record.status === 'idle' || record.status === 'loading')
    return <Loading />
  if (record.status === 'failed')
    return <ErrorNotice failure={record.failure} />
  return (
    <RecordDetails
      fields={entity.fields}
      record={record.status === 'loaded' ? record.record : null}
      caption={`${entity.name} ${id}`}
    />
  )
}

function BrokerEdit({
  access,
  id,
  onSaved,
}: {
  access: Access
  id: number
  onSaved: () => void
}) {
  const record = useRecord(access.calls.get_by_id, entity.fields, id)
  if (record.status === 'idle' || record.status === 'loading')
    return <Loading />
  if (record.status === 'failed')
    return <ErrorNotice failure={record.failure} />
  if (record.status === 'absent') return <Empty title="No such record" />
  return (
    <BrokerForm
      access={access}
      mode={{ kind: 'edit', record: record.record }}
      onSaved={onSaved}
    />
  )
}

function BrokerForm({
  access,
  mode,
  onSaved,
}: {
  access: Access
  mode: FormMode
  onSaved: () => void
}) {
  const related = useRelatedChoices(access.lists, entity.fields)
  const flow = useRecordForm(
    entity.fields,
    mode,
    { add: access.calls.add, update: access.calls.update },
    onSaved,
  )
  return (
    <Stack>
      <RecordForm
        fields={entity.fields}
        record={mode.kind === 'edit' ? mode.record : undefined}
        related={related}
        submitLabel={
          mode.kind === 'edit' ? 'Save the changes' : 'Add the record'
        }
        busy={flow.state.status === 'saving'}
        problems={flow.problems}
        onSubmit={flow.submit}
      />
      {flow.state.status === 'failed' && (
        <ErrorNotice failure={flow.state.failure} />
      )}
      {flow.state.status === 'absent' && <Empty title="No such record" />}
    </Stack>
  )
}

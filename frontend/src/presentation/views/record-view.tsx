"use client";

// One record: what it holds, changing it, turning it on or off, removing it.
//
// A change sends the fields that were actually altered. What comes back from
// the application is what is shown afterwards — including a refusal, in its own
// words.

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import type { ResourceDescription, Value } from "@/interaction";
import { useEntry, useRecord } from "@/interaction";
import {
  Action,
  Asking,
  Field,
  Fields,
  Mark,
  Panel,
  Row,
  Spread,
  Stack,
  Standing_,
  shown,
} from "@/presentation/components";

import styles from "./views.module.css";

export function RecordView({
  resource,
  identifier,
}: {
  resource: ResourceDescription;
  identifier: Value;
}) {
  const record = useRecord(resource, identifier);
  const router = useRouter();
  const [editing, setEditing] = useState(false);
  const [askingToRemove, setAskingToRemove] = useState(false);

  const held = record.standing.value;
  const enabled = held?.status === true;

  return (
    <Stack>
      <Spread>
        <div>
          <h1 className={styles.title}>
            {String(held?.name ?? held?.[resource.identifier] ?? identifier)}
          </h1>
          <p className={styles.quiet}>
            {resource.title} · {resource.identifier} {String(identifier)}
            {resource.operations.status && held ? (
              <>
                {" · "}
                <Mark on={enabled}>{enabled ? "enabled" : "disabled"}</Mark>
              </>
            ) : null}
          </p>
        </div>
        <Row>
          {resource.operations.change ? (
            <Action onClick={() => setEditing((open) => !open)}>
              {editing ? "stop editing" : "edit"}
            </Action>
          ) : null}
          {resource.operations.status && held ? (
            <Action onClick={() => void record.setEnabled(!enabled)}>
              {enabled ? "disable" : "enable"}
            </Action>
          ) : null}
          {resource.operations.remove ? (
            <Action manner="refusing" onClick={() => setAskingToRemove(true)}>
              remove
            </Action>
          ) : null}
        </Row>
      </Spread>

      <Standing_ standing={record.standing} waitingFor="fetching it" />

      {held && !editing ? (
        <Panel className={styles.form}>
          <dl className={styles.details}>
            {resource.returned.map((field) => (
              <div key={field.name} className={styles.detail}>
                <dt className={styles.quiet}>{field.name.replace(/_/g, " ")}</dt>
                <dd className={styles.value}>{shown(held[field.name])}</dd>
              </div>
            ))}
          </dl>
        </Panel>
      ) : null}

      {held && editing ? (
        <EditRecord
          resource={resource}
          held={held}
          onDone={() => setEditing(false)}
          onSubmit={record.change}
        />
      ) : null}

      <Row>
        <Link className={styles.quiet} href={`/data/${resource.path.slice(1)}`}>
          back to {resource.title.toLowerCase()}
        </Link>
      </Row>

      {askingToRemove ? (
        <Asking
          question={`Remove this ${resource.title.toLowerCase()}?`}
          detail="It will be gone from the application."
          confirm="remove it"
          onCancel={() => setAskingToRemove(false)}
          onConfirm={() => {
            void record.remove().then((gone) => {
              setAskingToRemove(false);
              if (gone) router.push(`/data/${resource.path.slice(1)}`);
            });
          }}
        />
      ) : null}
    </Stack>
  );
}

function EditRecord({
  resource,
  held,
  onDone,
  onSubmit,
}: {
  resource: ResourceDescription;
  held: Readonly<Record<string, unknown>>;
  onDone(): void;
  onSubmit(entered: ReturnType<ReturnType<typeof useEntry>["entered"]>): Promise<boolean>;
}) {
  const entry = useEntry(resource.fields, { from: held });

  async function submit() {
    if (await onSubmit(entry.entered())) onDone();
  }

  return (
    <Panel className={styles.form}>
      <Stack>
        <h2 className={styles.heading}>Change what is stored</h2>
        <p className={styles.quiet}>
          Only the fields you alter are sent. Anything you leave alone stays as it is.
        </p>
        <Fields>
          {resource.fields
            .filter((field) => field.changeable && field.name !== resource.identifier)
            .map((field) => (
              <Field
                key={field.name}
                field={field}
                value={entry.values[field.name]}
                complaint={entry.complaints[field.name]}
                onChange={(value) => entry.set(field.name, value)}
              />
            ))}
        </Fields>
        <Row>
          <Action
            manner="primary"
            disabled={!entry.hasChanges || entry.hasComplaints}
            onClick={() => void submit()}
          >
            save {entry.touched.size > 0 ? `${entry.touched.size} change(s)` : "changes"}
          </Action>
          <Action manner="quiet" onClick={entry.reset}>
            undo edits
          </Action>
        </Row>
      </Stack>
    </Panel>
  );
}

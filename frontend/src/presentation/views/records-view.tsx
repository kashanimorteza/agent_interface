"use client";

// Working with one kind of data: what is there, and adding to it.
//
// This coordinates pieces. It holds no application rule of its own: everything
// it shows came back from the application, and everything it asks for goes
// through the behaviour beneath it.

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import type { Record_, ResourceDescription } from "@/interaction";
import { useCreation, useEntry, useRecords } from "@/interaction";
import {
  Action,
  Field,
  Fields,
  Panel,
  Records,
  Row,
  Spread,
  Stack,
  Standing_,
} from "@/presentation/components";
import { PAGE_SIZE } from "@/presentation/theme/appearance";

import styles from "./views.module.css";

export function RecordsView({ resource }: { resource: ResourceDescription }) {
  const listing = useRecords(resource, PAGE_SIZE);
  const [adding, setAdding] = useState(false);
  const router = useRouter();

  const records = listing.standing.value ?? [];
  const columns = resource.returned.slice(0, 7);

  return (
    <Stack>
      <Spread>
        <div>
          <h1 className={styles.title}>{resource.title}</h1>
          <p className={styles.quiet}>
            {resource.fields.length} fields · showing {records.length} from{" "}
            {listing.offset + 1}
          </p>
        </div>
        <Row>
          <Action onClick={() => void listing.refresh()}>refresh</Action>
          {resource.operations.create ? (
            <Action manner="primary" onClick={() => setAdding((open) => !open)}>
              {adding ? "cancel" : `add ${resource.title.toLowerCase()}`}
            </Action>
          ) : null}
        </Row>
      </Spread>

      {adding ? (
        <AddRecord
          resource={resource}
          onAdded={(made) => {
            setAdding(false);
            void listing.refresh();
            router.push(`/data/${resource.path.slice(1)}/${made[resource.identifier]}`);
          }}
        />
      ) : null}

      <Panel>
        <Standing_
          standing={listing.standing}
          waitingFor={`fetching ${resource.title.toLowerCase()}`}
          emptyMeans={`Nothing here yet. ${
            resource.operations.create ? "Add the first one." : ""
          }`}
        >
          {records.length > 0 ? (
            <Records
              columns={columns}
              records={records}
              identifier={resource.identifier}
              onOpen={(record) =>
                router.push(`/data/${resource.path.slice(1)}/${record[resource.identifier]}`)
              }
            />
          ) : null}
        </Standing_>
      </Panel>

      <Row>
        <Action disabled={listing.offset === 0} onClick={listing.previous}>
          previous
        </Action>
        <Action disabled={!listing.hasMore} onClick={listing.next}>
          next
        </Action>
        <Link className={styles.quiet} href="/">
          all kinds of data
        </Link>
      </Row>
    </Stack>
  );
}

function AddRecord({
  resource,
  onAdded,
}: {
  resource: ResourceDescription;
  onAdded(made: Record_): void;
}) {
  const creation = useCreation(resource);
  const entry = useEntry(resource.fields, { forCreation: true });

  async function submit() {
    const made = await creation.create(entry.entered());
    if (made) {
      entry.reset();
      onAdded(made);
    }
  }

  return (
    <Panel className={styles.form}>
      <Stack>
        <h2 className={styles.heading}>New {resource.title.toLowerCase()}</h2>
        <Standing_ standing={creation.standing} waitingFor="adding it" />
        <Fields>
          {resource.fields
            .filter((field) => field.name !== resource.identifier)
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
            disabled={entry.hasComplaints || creation.standing.progress === "working"}
            onClick={() => void submit()}
          >
            add it
          </Action>
          <Action manner="quiet" onClick={entry.reset}>
            clear
          </Action>
        </Row>
      </Stack>
    </Panel>
  );
}

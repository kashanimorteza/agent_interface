"use client";

// The pieces the interface is made of.
//
// One definition per idea: a set of records, a value being entered, an action,
// something being asked before it happens, a word about what is going on. Each
// is used wherever that idea appears, and none of them talks to the application.

import type { ReactNode } from "react";

import type { FieldDescription, Record_, ReturnedField, Value } from "@/interaction";
import type { Refusal, Standing } from "@/interaction";

import styles from "./components.module.css";

// <!-------------------------------------------- laying things out -->

export function Panel({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={`${styles.panel} ${className ?? ""}`}>{children}</div>;
}

export function Stack({ children }: { children: ReactNode }) {
  return <div className={styles.stack}>{children}</div>;
}

export function Row({ children }: { children: ReactNode }) {
  return <div className={styles.row}>{children}</div>;
}

export function Spread({ children }: { children: ReactNode }) {
  return <div className={styles.spread}>{children}</div>;
}

// <!-------------------------------------------- doing something -->

export type Manner = "plain" | "primary" | "quiet" | "refusing";

const MANNERS: Record<Manner, string> = {
  plain: "",
  primary: styles.actionPrimary,
  quiet: styles.actionQuiet,
  refusing: styles.actionRefusing,
};

export function Action({
  children,
  onClick,
  manner = "plain",
  disabled = false,
  type = "button",
}: {
  children: ReactNode;
  onClick?: () => void;
  manner?: Manner;
  disabled?: boolean;
  type?: "button" | "submit";
}) {
  return (
    <button
      type={type}
      className={`${styles.action} ${MANNERS[manner]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}

// <!-------------------------------------------- saying what is happening -->

export function Waiting({ what }: { what: string }) {
  return <p className={`${styles.note} ${styles.noteWaiting}`}>{what}…</p>;
}

export function Nothing({ what }: { what: string }) {
  return <p className={`${styles.note} ${styles.noteEmpty}`}>{what}</p>;
}

export function Refusal_({ refusal }: { refusal: Refusal }) {
  return (
    <p className={`${styles.note} ${styles.noteRefused}`} role="alert">
      <strong>{refusal.kind}</strong>
      {refusal.status ? ` (${refusal.status})` : ""}: {refusal.reason}
    </p>
  );
}

/**
 * Whatever the standing of something is, said out loud.
 *
 * Waiting, emptiness and refusal look different because they are different, and
 * a refusal carries the words the application used.
 */
export function Standing_({
  standing,
  waitingFor,
  emptyMeans,
  children,
}: {
  standing: Standing<unknown>;
  waitingFor: string;
  emptyMeans?: string;
  children?: ReactNode;
}) {
  const empty =
    standing.progress === "settled" &&
    Array.isArray(standing.value) &&
    standing.value.length === 0;

  return (
    <>
      {standing.progress === "working" ? <Waiting what={waitingFor} /> : null}
      {standing.refusal ? <Refusal_ refusal={standing.refusal} /> : null}
      {empty && emptyMeans ? <Nothing what={emptyMeans} /> : null}
      {children}
    </>
  );
}

export function Mark({ on, children }: { on: boolean; children: ReactNode }) {
  return (
    <span className={`${styles.mark} ${on ? styles.markOn : styles.markOff}`}>{children}</span>
  );
}

// <!-------------------------------------------- showing records -->

export function shown(value: unknown): ReactNode {
  if (value === null || value === undefined || value === "") {
    return <span className={styles.blank}>—</span>;
  }
  if (typeof value === "boolean") return <Mark on={value}>{value ? "on" : "off"}</Mark>;
  return String(value);
}

export function Records({
  columns,
  records,
  identifier,
  onOpen,
}: {
  columns: readonly ReturnedField[];
  records: readonly Record_[];
  identifier: string;
  onOpen?(record: Record_): void;
}) {
  return (
    <div className={styles.tableWrap}>
      <table className={styles.table}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.name}>{column.name.replace(/_/g, " ")}</th>
            ))}
            {onOpen ? <th /> : null}
          </tr>
        </thead>
        <tbody>
          {records.map((record) => (
            <tr key={String(record[identifier])}>
              {columns.map((column) => (
                <td key={column.name}>{shown(record[column.name])}</td>
              ))}
              {onOpen ? (
                <td>
                  <Action manner="quiet" onClick={() => onOpen(record)}>
                    open
                  </Action>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// <!-------------------------------------------- entering values -->

function controlKind(field: FieldDescription): string {
  if (field.type === "integer" || field.type === "number") return "number";
  if (field.type === "datetime") return "datetime-local";
  return "text";
}

export function Field({
  field,
  value,
  complaint,
  onChange,
}: {
  field: FieldDescription;
  value: Value;
  complaint?: string;
  onChange(value: Value): void;
}) {
  const shownValue = value === null || value === undefined ? "" : String(value);

  return (
    <label className={styles.field}>
      <span className={styles.fieldLabel}>
        {field.name.replace(/_/g, " ")}
        {field.required && !field.nullable ? " *" : ""}
      </span>

      {field.type === "boolean" ? (
        <input
          type="checkbox"
          checked={value === true || value === "true"}
          onChange={(event) => onChange(event.target.checked)}
        />
      ) : (
        <input
          className={`${styles.control} ${complaint ? styles.controlWrong : ""}`}
          type={controlKind(field)}
          value={shownValue}
          maxLength={field.maxLength ?? undefined}
          step={field.type === "number" ? "any" : undefined}
          onChange={(event) => onChange(event.target.value)}
        />
      )}

      {field.writeOnly ? (
        <span className={styles.fieldNote}>set here; never shown back</span>
      ) : null}
      {complaint ? <span className={styles.fieldComplaint}>{complaint}</span> : null}
    </label>
  );
}

export function Fields({ children }: { children: ReactNode }) {
  return <div className={styles.fields}>{children}</div>;
}

// <!-------------------------------------------- asking first -->

export function Asking({
  question,
  detail,
  confirm,
  onConfirm,
  onCancel,
}: {
  question: string;
  detail?: string;
  confirm: string;
  onConfirm(): void;
  onCancel(): void;
}) {
  return (
    <div className={styles.veil} role="dialog" aria-modal="true">
      <Panel className={styles.asking}>
        <Stack>
          <h2>{question}</h2>
          {detail ? <p>{detail}</p> : null}
          <Row>
            <Action manner="refusing" onClick={onConfirm}>
              {confirm}
            </Action>
            <Action manner="quiet" onClick={onCancel}>
              keep it
            </Action>
          </Row>
        </Stack>
      </Panel>
    </div>
  );
}

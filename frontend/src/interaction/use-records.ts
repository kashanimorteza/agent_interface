"use client";

// Working with one kind of data: what is listed, what is open, what just
// changed.
//
// The steps are the same whichever kind of data it is, so they live here once.
// None of them decides anything the application decides: an outcome that depends
// on an application rule is asked for and shown as it came back.

import { useCallback, useEffect, useState } from "react";

import {
  changeRecord,
  createRecord,
  listRecords,
  readRecord,
  removeRecord,
  setRecordStatus,
  type Entered,
  type Record_,
  type ResourceDescription,
  type Value,
} from "@/api-access";

import { idle, refused, settled, working, type Standing } from "./feedback";

export interface Listing {
  readonly standing: Standing<readonly Record_[]>;
  readonly offset: number;
  readonly pageSize: number;
  readonly hasMore: boolean;
  refresh(): Promise<void>;
  next(): void;
  previous(): void;
}

/** The records of one kind, a page at a time. */
export function useRecords(resource: ResourceDescription, pageSize: number): Listing {
  const [standing, setStanding] = useState<Standing<readonly Record_[]>>(idle);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);

  const refresh = useCallback(async () => {
    setStanding((previous) => working(previous));
    try {
      // One more than the page, to know whether there is another page without
      // asking the application to count everything.
      const page = await listRecords(resource, { limit: pageSize + 1, offset });
      setHasMore(page.records.length > pageSize);
      setStanding(settled(page.records.slice(0, pageSize)));
    } catch (error) {
      setStanding((previous) => refused(previous, error));
    }
  }, [resource, pageSize, offset]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return {
    standing,
    offset,
    pageSize,
    hasMore,
    refresh,
    next: () => setOffset((at) => at + pageSize),
    previous: () => setOffset((at) => Math.max(0, at - pageSize)),
  };
}

export interface OneRecord {
  readonly standing: Standing<Record_>;
  refresh(): Promise<void>;
  change(entered: Entered): Promise<boolean>;
  remove(): Promise<boolean>;
  setEnabled(enabled: boolean): Promise<boolean>;
}

/** One record of one kind, and the things that can be done to it. */
export function useRecord(
  resource: ResourceDescription,
  identifier: Value,
): OneRecord {
  const [standing, setStanding] = useState<Standing<Record_>>(idle);

  const refresh = useCallback(async () => {
    setStanding((previous) => working(previous));
    try {
      setStanding(settled(await readRecord(resource, identifier)));
    } catch (error) {
      setStanding((previous) => refused(previous, error));
    }
  }, [resource, identifier]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const attempt = useCallback(
    async (what: () => Promise<Record_ | void>): Promise<boolean> => {
      setStanding((previous) => working(previous));
      try {
        const answered = await what();
        // What the application returned is what is shown, not what was sent.
        if (answered) setStanding(settled(answered));
        return true;
      } catch (error) {
        setStanding((previous) => refused(previous, error));
        return false;
      }
    },
    [],
  );

  return {
    standing,
    refresh,
    change: (entered) => attempt(() => changeRecord(resource, identifier, entered)),
    remove: () => attempt(() => removeRecord(resource, identifier)),
    setEnabled: (enabled) => attempt(() => setRecordStatus(resource, identifier, enabled)),
  };
}

export interface Creation {
  readonly standing: Standing<Record_>;
  create(entered: Entered): Promise<Record_ | null>;
}

/** Adding one record of one kind. */
export function useCreation(resource: ResourceDescription): Creation {
  const [standing, setStanding] = useState<Standing<Record_>>(idle);

  const create = useCallback(
    async (entered: Entered): Promise<Record_ | null> => {
      setStanding((previous) => working(previous));
      try {
        const made = await createRecord(resource, entered);
        setStanding(settled(made));
        return made;
      } catch (error) {
        setStanding((previous) => refused(previous, error));
        return null;
      }
    },
    [resource],
  );

  return { standing, create };
}

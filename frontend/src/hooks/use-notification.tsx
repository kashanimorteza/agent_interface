'use client';

/** Notification state — the outcome of the latest operation, owned by Interaction Logic. */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

export type NotificationKind = "success" | "error";
export type Notification = { kind: NotificationKind; message: string };

type NotificationContextValue = {
  current: Notification | null;
  notify: (kind: NotificationKind, message: string) => void;
  dismiss: () => void;
};

const NotificationContext = createContext<NotificationContextValue | null>(null);
const SUCCESS_TIMEOUT_MS = 4000;

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const [current, setCurrent] = useState<Notification | null>(null);
  const notify = useCallback((kind: NotificationKind, message: string) => setCurrent({ kind, message }), []);
  const dismiss = useCallback(() => setCurrent(null), []);

  useEffect(() => {
    if (current?.kind !== "success") return;
    const timer = setTimeout(() => setCurrent(null), SUCCESS_TIMEOUT_MS);
    return () => clearTimeout(timer);
  }, [current]);

  const value = useMemo(() => ({ current, notify, dismiss }), [current, notify, dismiss]);
  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>;
}

export function useNotification(): NotificationContextValue {
  const value = useContext(NotificationContext);
  if (!value) throw new Error("useNotification must be used inside NotificationProvider");
  return value;
}

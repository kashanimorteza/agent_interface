import { useEffect, useRef, useState } from 'react'

export type Loaded<T> =
  | { readonly status: 'idle' }
  | { readonly status: 'loading' }
  | { readonly status: 'ready'; readonly value: T }

/**
 * Loads a value whenever the key changes and reports waiting, the value, or
 * nothing to do (a null key). An answer that arrives for an earlier key is
 * dropped, so what is shown always belongs to the current key.
 */
export function useLoaded<T>(
  key: string | null,
  load: () => Promise<T>,
): Loaded<T> {
  const latest = useRef(load)
  useEffect(() => {
    latest.current = load
  })
  const [settled, setSettled] = useState<{ key: string; value: T } | null>(null)
  useEffect(() => {
    if (key === null) return
    let current = true
    void latest.current().then((value) => {
      if (current) setSettled({ key, value })
    })
    return () => {
      current = false
    }
  }, [key])
  if (key === null) return { status: 'idle' }
  if (settled !== null && settled.key === key) {
    return { status: 'ready', value: settled.value }
  }
  return { status: 'loading' }
}

import { createContext, type ReactNode } from 'react';

/** What fills the Navigation area of the page frame. */
export const NavigationSlot = createContext<ReactNode>(null);

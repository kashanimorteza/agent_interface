'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { MODEL_KEYS, MODEL_SPECS } from '@/lib/models/model-specs';

const HOME = { route: '/', title: 'Home' };

/** Links to the home page and to every Model's management page. */
export function Navigation() {
  const pathname = usePathname();
  const entries = [HOME, ...MODEL_KEYS.map((key) => ({ route: MODEL_SPECS[key].route, title: MODEL_SPECS[key].title }))];
  return (
    <nav className="app-nav" aria-label="Main">
      <ul>
        {entries.map((entry) => (
          <li key={entry.route}>
            <Link href={entry.route} aria-current={pathname === entry.route ? 'page' : undefined}>
              {entry.title}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}

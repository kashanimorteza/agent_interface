import Link from 'next/link';
import { Navigation } from '@/components/navigation';
import { Notification } from '@/components/notification';

/** The persistent application frame: header with the application name, navigation, notification, and content. */
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link href="/" className="app-title">
          Trading Assistant
        </Link>
        <Navigation />
      </header>
      <main className="app-main stack">
        <Notification />
        {children}
      </main>
    </div>
  );
}

// The frame every page is shown inside.
//
// The appearance decided once is applied here, at the top, so everything below
// inherits it rather than choosing again. So is the way the interface reads.

import type { Metadata } from "next";
import Link from "next/link";

import { RESOURCES } from "@/interaction";
import { appearanceAttribute, directionAttribute } from "@/presentation/theme/appearance";
import "@/presentation/theme/theme.css";

import styles from "./layout.module.css";

export const metadata: Metadata = {
  title: "Trading Assistant",
  description: "Enter and manage the data the platform is built from.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" dir={directionAttribute()} data-appearance={appearanceAttribute()}>
      <body>
        <div className={styles.frame} data-frame="frame">
          <aside className={styles.aside} data-frame="aside">
            <Link href="/" className={styles.brand}>
              Trading Assistant
            </Link>
            <nav className={styles.nav} data-frame="nav">
              {RESOURCES.map((resource) => (
                <Link
                  key={resource.name}
                  href={`/data/${resource.path.slice(1)}`}
                  className={styles.navLink}
                >
                  {resource.title}
                </Link>
              ))}
            </nav>
          </aside>
          <main className={styles.main} data-frame="main">{children}</main>
        </div>
      </body>
    </html>
  );
}

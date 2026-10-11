import type { ReactNode } from 'react'
import { autoDirection } from '@/theme/theme'
import styles from './page-frame.module.css'

type Props = {
  applicationTitle: string
  /** The navigation place; absent when a page has none. */
  navigation?: ReactNode
  /** The page's own heading. */
  heading: string
  children: ReactNode
}

/** The consistent outer structure every page sits in. */
export function PageFrame({
  applicationTitle,
  navigation,
  heading,
  children,
}: Props) {
  return (
    <div className={styles.frame}>
      <a href="#content" className={styles.skip}>
        Skip to content
      </a>
      <header className={styles.header} {...autoDirection}>
        <span className={styles.title}>{applicationTitle}</span>
      </header>
      <div className={styles.body}>
        {navigation !== undefined && (
          <nav aria-label="Main" className={styles.navigation}>
            {navigation}
          </nav>
        )}
        <main id="content" className={styles.main}>
          <h1 className={styles.heading} {...autoDirection}>
            {heading}
          </h1>
          {children}
        </main>
      </div>
    </div>
  )
}

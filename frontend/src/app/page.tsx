// Where a person arrives: everything the platform is made of, in one place.

import Link from "next/link";

import { RESOURCES } from "@/interaction";
import styles from "@/presentation/views/views.module.css";

export default function Home() {
  return (
    <div>
      <h1 className={styles.title}>Trading Assistant</h1>
      <p className={styles.quiet}>
        Everything the platform is built from. Pick one to see what is there and to add,
        change or remove records.
      </p>

      <div className={styles.index} style={{ marginTop: "var(--space-5)" }}>
        {RESOURCES.map((resource) => (
          <Link
            key={resource.name}
            href={`/data/${resource.path.slice(1)}`}
            className={styles.card}
          >
            <div className={styles.cardName}>{resource.title}</div>
            <div className={styles.cardNote}>
              {resource.fields.length} fields
              {resource.operations.status ? " · can be enabled or disabled" : ""}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

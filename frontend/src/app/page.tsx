import Link from 'next/link';
import { MODEL_KEYS, MODEL_SPECS } from '@/lib/models/model-specs';

/** The home page: the entry into data management with a link to every Model's management page. */
export default function HomePage() {
  return (
    <div className="stack">
      <div>
        <h1>Trading Assistant</h1>
        <p className="muted">Enter and manage the platform&apos;s trading information, strategies, actions, and related data.</p>
      </div>
      <ul className="form-grid" style={{ listStyle: 'none', margin: 0, padding: 0 }}>
        {MODEL_KEYS.map((key) => {
          const spec = MODEL_SPECS[key];
          return (
            <li key={key} className="surface stack">
              <Link href={spec.route}>
                <strong>{spec.title}</strong>
              </Link>
              <span className="muted">{spec.purpose}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

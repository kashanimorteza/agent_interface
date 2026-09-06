import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { ManagementPage } from '@/components/management-page';
import { MODEL_KEYS, MODEL_SPECS, modelForRoute } from '@/lib/models/model-specs';

type Params = Promise<{ model: string }>;

export const dynamicParams = false;

export function generateStaticParams(): { model: string }[] {
  return MODEL_KEYS.map((key) => ({ model: MODEL_SPECS[key].route.slice(1) }));
}

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const key = modelForRoute((await params).model);
  return { title: key ? `${MODEL_SPECS[key].title} — Trading Assistant` : 'Trading Assistant' };
}

/** One management page per Model, resolved from the route segment. */
export default async function ModelPage({ params }: { params: Params }) {
  const key = modelForRoute((await params).model);
  if (!key) notFound();
  return <ManagementPage modelKey={key} />;
}

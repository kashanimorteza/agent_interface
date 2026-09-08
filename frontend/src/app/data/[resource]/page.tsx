// Everything of one kind of data.

import { notFound } from "next/navigation";

import { RESOURCES, resourceAt } from "@/interaction";
import { RecordsView } from "@/presentation/views/records-view";

export function generateStaticParams() {
  return RESOURCES.map((resource) => ({ resource: resource.path.slice(1) }));
}

export default async function ResourcePage({
  params,
}: {
  params: Promise<{ resource: string }>;
}) {
  const { resource: asked } = await params;
  const resource = resourceAt(asked);
  if (!resource) notFound();

  return <RecordsView resource={resource} />;
}

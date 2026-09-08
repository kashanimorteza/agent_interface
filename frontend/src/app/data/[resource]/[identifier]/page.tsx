// One record of one kind of data.

import { notFound } from "next/navigation";

import { resourceAt } from "@/interaction";
import { RecordView } from "@/presentation/views/record-view";

export default async function RecordPage({
  params,
}: {
  params: Promise<{ resource: string; identifier: string }>;
}) {
  const { resource: asked, identifier } = await params;
  const resource = resourceAt(asked);
  if (!resource) notFound();

  return <RecordView resource={resource} identifier={identifier} />;
}

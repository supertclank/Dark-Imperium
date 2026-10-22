import { notFound } from "next/navigation";
import { CompendiumList } from "@/components/CompendiumList";
export default async function Entries({
  params,
}: {
  params: Promise<{ kind: string }>;
}) {
  const { kind } = await params;
  const titles: Record<string, string> = {
    species: "Species",
    classes: "Classes",
    weapons: "Weapons",
  };
  if (!titles[kind]) notFound();
  return <CompendiumList kind={kind} title={titles[kind]} />;
}

import { CharacterSheet } from "@/components/CharacterSheet";
export default async function Sheet({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CharacterSheet id={id} />;
}

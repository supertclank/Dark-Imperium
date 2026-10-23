"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { SavedCharacter } from "@/lib/builder";
import { useResource, ResourceState } from "./Resource";
import { AdvancementPanel } from "./AdvancementPanel";
import { RollPanel } from "./RollPanel";
import { CalculatedSummary } from "./CalculatedSummary";
export function CharacterSheet({ id }: { id: string }) {
  const {
    data: loaded,
    error,
    retry,
  } = useResource<SavedCharacter>(`/characters/${id}`);
  const [confirm, setConfirm] = useState(false),
    [busy, setBusy] = useState(false),
    [failure, setFailure] = useState("");
  const [updated, setUpdated] = useState<SavedCharacter | null>(null);
  const character = updated?.id === id ? updated : loaded;
  const router = useRouter();
  async function refresh() {
    setUpdated(await api<SavedCharacter>(`/characters/${id}`));
  }
  async function remove() {
    setBusy(true);
    try {
      await api(`/characters/${id}`, { method: "DELETE" });
      router.push("/characters");
    } catch (e) {
      setFailure((e as Error).message);
      setBusy(false);
    }
  }
  if (!character) return <ResourceState error={error} retry={retry} />;
  return (
    <>
      <Link href="/characters" className="back-link">
        ← Your characters
      </Link>
      <RollPanel
        playLayout
        key={`rolls:${character.id}:${character.level}`}
        character={character}
        onRefresh={refresh}
      />
      <details className="sheet-management">
        <summary>Character advancement</summary>
        <AdvancementPanel
          key={`advancement:${character.id}:${character.runtime.stateVersion}`}
          character={character}
          onChanged={setUpdated}
        />
      </details>
      <div className="danger-zone">
        {failure && <p role="alert">{failure}</p>}
        {confirm ? (
          <>
            <p>
              Permanently delete <strong>{character.name}</strong> and its
              inventory?
            </p>
            <button className="danger" disabled={busy} onClick={remove}>
              Delete permanently
            </button>
            <button
              className="secondary"
              disabled={busy}
              onClick={() => setConfirm(false)}
            >
              Keep character
            </button>
          </>
        ) : (
          <button className="text-button" onClick={() => setConfirm(true)}>
            Delete character
          </button>
        )}
      </div>
    </>
  );
}

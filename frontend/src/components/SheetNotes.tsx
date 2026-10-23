"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
type Notes = { text: string; version: number };
export function SheetNotes({
  characterId,
  active,
}: {
  characterId: string;
  active: boolean;
}) {
  const [saved, setSaved] = useState<Notes | null>(null),
    [text, setText] = useState(""),
    [busy, setBusy] = useState(false),
    [message, setMessage] = useState(""),
    [error, setError] = useState("");
  useEffect(() => {
    if (!active || saved) return;
    let live = true;
    api<Notes>(`/characters/${characterId}/notes`)
      .then((v) => {
        if (live) {
          setSaved(v);
          setText(v.text);
        }
      })
      .catch((e) => {
        if (live) setError(e.message);
      });
    return () => {
      live = false;
    };
  }, [active, characterId, saved]);
  async function save() {
    if (!saved) return;
    setBusy(true);
    setError("");
    try {
      const value = await api<Notes>(`/characters/${characterId}/notes`, {
        method: "PUT",
        body: JSON.stringify({ text, expectedVersion: saved.version }),
      });
      setSaved(value);
      setMessage("Notes saved.");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div hidden={!active}>
      <h2>Private character notes</h2>
      <p className="small">
        Saved with this character. Notes do not change rules or roll
        calculations.
      </p>
      <label htmlFor={`notes-${characterId}`}>Session notes</label>
      <textarea
        id={`notes-${characterId}`}
        rows={12}
        maxLength={20000}
        value={text}
        disabled={!saved || busy}
        onChange={(e) => {
          setText(e.target.value);
          setMessage("");
        }}
      />
      <div className="notes-controls">
        <small>{text.length.toLocaleString()} / 20,000</small>
        <button
          disabled={!saved || busy || text === saved.text}
          onClick={() => void save()}
        >
          {busy ? "Saving…" : "Save notes"}
        </button>
      </div>
      {message && <p role="status">{message}</p>}
      {error && <p role="alert">{error}</p>}
    </div>
  );
}

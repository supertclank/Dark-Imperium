"use client";
import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import type { RollOption } from "@/lib/rolls";
import { RollActionButton } from "./RollActionButton";
export type Inspection = {
  id: string;
  name: string;
  kind: string;
  description: string;
  fields: { label: string; value: string }[];
  sources?: { locator: { heading?: string; pdfPage?: number } }[];
  rules?: string[];
  status: string;
  note?: string;
  actionItemId?: string;
  profileId?: string;
};
export function SheetInspector({
  characterId,
  target,
  options,
  disabled,
  onRoll,
  onClose,
}: {
  characterId: string;
  target: { id: string; name: string; local?: Inspection };
  options: RollOption[];
  disabled: boolean;
  onRoll: (o: RollOption) => void;
  onClose: () => void;
}) {
  const [data, setData] = useState<Inspection | null>(target.local ?? null),
    [error, setError] = useState("");
  const panel = useRef<HTMLElement>(null),
    close = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    let active = true;
    setData(target.local ?? null);
    setError("");
    if (!target.local)
      api<Inspection>(
        `/characters/${characterId}/details/${encodeURIComponent(target.id)}`,
      )
        .then((v) => {
          if (active) setData(v);
        })
        .catch((e) => {
          if (active) setError(e.message);
        });
    return () => {
      active = false;
    };
  }, [characterId, target]);
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    close.current?.focus();
    return () => {
      if (previous?.isConnected) previous.focus();
    };
  }, []);
  return (
    <aside
      className="sheet-inspector"
      role="dialog"
      aria-label={`${target.name} details`}
      ref={panel}
      onKeyDown={(e) => {
        if (e.key === "Escape") {
          e.stopPropagation();
          onClose();
        }
        if (e.key === "Tab" && window.matchMedia("(max-width:700px)").matches) {
          const all = Array.from(
            panel.current?.querySelectorAll<HTMLElement>(
              'button:not(:disabled),a[href],[tabindex="0"]',
            ) ?? [],
          );
          const first = all[0],
            last = all[all.length - 1];
          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last?.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first?.focus();
          }
        }
      }}
    >
      <div className="inspector-heading">
        <div>
          <p className="eyebrow">{data?.kind ?? "Rules reference"}</p>
          <h2>{data?.name ?? target.name}</h2>
        </div>
        <button ref={close} onClick={onClose} aria-label="Close details">
          ×
        </button>
      </div>
      {error ? (
        <p role="alert">{error}</p>
      ) : !data ? (
        <p role="status">Loading pinned rules…</p>
      ) : (
        <>
          <p className="inspector-status">{data.status}</p>
          <dl className="inspector-fields">
            {data.fields.map((f, i) => (
              <div key={i}>
                <dt>{f.label}</dt>
                <dd>{f.value}</dd>
              </div>
            ))}
          </dl>
          {data.actionItemId && (
            <div className="inspector-rolls">
              {options
                .filter((o) => o.itemId === data.actionItemId)
                .map((o) => (
                  <RollActionButton
                    key={o.id}
                    option={o}
                    disabled={disabled}
                    onRoll={() => onRoll(o)}
                  />
                ))}
            </div>
          )}
          {data.note && <p>{data.note}</p>}
          <h3>Rules & details</h3>
          <div className="canonical-description">{data.description}</div>
          {data.rules?.map((text, i) => (
            <p className="canonical-description" key={i}>
              {text}
            </p>
          ))}
          {data.sources?.length ? (
            <footer>
              <h3>Source</h3>
              {data.sources.map((s, i) => (
                <p key={i}>
                  {s.locator.heading}
                  {s.locator.pdfPage ? ` · PDF ${s.locator.pdfPage}` : ""}
                </p>
              ))}
              {data.profileId && (
                <small>Pinned profile: {data.profileId}</small>
              )}
            </footer>
          ) : null}
        </>
      )}
    </aside>
  );
}

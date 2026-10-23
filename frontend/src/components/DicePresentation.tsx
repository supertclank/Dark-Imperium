"use client";

import { useEffect, useRef, useState } from "react";

import { api } from "@/lib/api";

import type { RollResult, RollSession } from "@/lib/rolls";

import {
  defaultPreferences,
  effectiveMode,
  preferenceKey,
  readPreferences,
  type DicePreferences,
} from "@/lib/dice-presentation";

import type { PhysicalRenderer } from "@/lib/dice-renderer";

import { DiceResult } from "./DiceResult";

export type PresentationEvent = { serial: number; replay: boolean } & (
  | { result: RollResult; session?: never }
  | { session: RollSession; result?: never }
);

export type PresentationState =
  | "IDLE"
  | "AUTHORISING"
  | "ROLLING"
  | "COCKED_REROLL"
  | "READING_PHYSICAL_RESULT"
  | "SUBMITTING_RESULT"
  | "REVEALED"
  | "DISMISSED"
  | "ERROR";

export function DicePresentation({
  event,
  onReveal,
  onCancel,
  requesting = false,
}: {
  event: PresentationEvent | null;
  onReveal?: (result: RollResult) => void;
  onCancel?: () => void;
  requesting?: boolean;
}) {
  const [preferences, setPreferences] =
      useState<DicePreferences>(defaultPreferences),
    [ready, setReady] = useState(false),
    [reduce, setReduce] = useState(false),
    [state, setState] = useState<PresentationState>("IDLE"),
    [shown, setShown] = useState<{
      event: PresentationEvent;
      result: RollResult;
    } | null>(null),
    [error, setError] = useState(""),
    [notice, setNotice] = useState("");

  const host = useRef<HTMLDivElement>(null),
    renderer = useRef<PhysicalRenderer | null>(null),
    callbacks = useRef({ onReveal, onCancel }),
    retry = useRef<null | (() => void)>(null),
    completedEvent = useRef<PresentationEvent | null>(null),
    skip = useRef(false),
    stop = useRef(() => {});
  callbacks.current = { onReveal, onCancel };

  const mode = effectiveMode(preferences.mode, reduce);

  function change(next: DicePreferences) {
    setPreferences(next);
    try {
      localStorage.setItem(preferenceKey, JSON.stringify(next));
    } catch {}
    window.dispatchEvent(new CustomEvent("dice-preferences", { detail: next }));
  }

  useEffect(() => {
    try {
      setPreferences(readPreferences(localStorage.getItem(preferenceKey)));
    } catch {}
    setReady(true);
    const m = window.matchMedia?.("(prefers-reduced-motion: reduce)");
    if (m) setReduce(m.matches);
    const motion = () => setReduce(m?.matches ?? false),
      sync = (e: Event) =>
        setPreferences((e as CustomEvent<DicePreferences>).detail),
      hide = () => setState("DISMISSED");
    m?.addEventListener("change", motion);
    window.addEventListener("dice-preferences", sync);
    window.addEventListener("dice-presentation-start", hide);
    return () => {
      m?.removeEventListener("change", motion);
      window.removeEventListener("dice-preferences", sync);
      window.removeEventListener("dice-presentation-start", hide);
    };
  }, []);

  useEffect(() => {
    if (requesting) setState("AUTHORISING");
  }, [requesting]);

  useEffect(() => {
    if (!ready || !event || requesting) return;
    if (completedEvent.current === event) {
      setState("DISMISSED");
      return;
    }
    let active = true,
      submitting = false;
    stop.current = () => {
      active = false;
    };
    let timer: ReturnType<typeof setTimeout> | undefined;
    skip.current = false;
    setError("");
    setNotice("");
    setShown(null);
    setState("ROLLING");

    const reveal = (result: RollResult) => {
      if (!active) return;
      completedEvent.current = event;
      setNotice((n) =>
        n === "Cocked die – rerolling" ? "Cocked die rerolled" : n,
      );
      setShown({ event, result });
      setState("REVEALED");
      callbacks.current.onReveal?.(result);
      timer = setTimeout(() => {
        if (active) {
          setState("DISMISSED");
          renderer.current?.dispose();
          renderer.current = null;
        }
      }, 5000);
    };

    const submit = (values: number[][] | null, fallback = false) => {
      if (!active || submitting || completedEvent.current === event) return;
      submitting = true;
      setState("SUBMITTING_RESULT");
      setError("");
      const input = {
        values,
        fallback,
        physicsVersion: event.session!.physicsVersion,
        geometryVersion: event.session!.geometryVersion,
      };
      retry.current = () => submit(values, fallback);

      api<RollResult>(
        `/roll-sessions/${event.session!.rollSessionId}/finalize`,
        { method: "POST", body: JSON.stringify(input) },
      )
        .then(reveal)
        .catch((e) => {
          if (active) {
            setError((e as Error).message);
            setState("ERROR");
          }
        })
        .finally(() => {
          submitting = false;
        });
    };

    const failed = () => {
      if (!active || completedEvent.current === event) return;
      renderer.current?.dispose();
      renderer.current = null;
      if (event.result) {
        setNotice("Stored result replay · physical trajectory unavailable");
        reveal(event.result);
      } else {
        setNotice(
          "Physical simulation unavailable · using one server fallback",
        );
        submit(null, true);
      }
    };

    let session = event.session;

    if (event.result) {
      const physical = event.result.physical;
      if (
        physical?.source === "PHYSICS" &&
        physical.physicsVersion === "rapier-0.21.0-di-1" &&
        physical.geometryVersion === "di-physical-2"
      )
        session = {
          rollSessionId: "replay",
          label: event.result.label,
          groups: event.result.dice.groups.map((g) => ({
            count: g.dice.length,
            sides: g.sides,
            keep: g.keep,
            keepCount: g.kept.length,
          })),
          modifier: event.result.dice.modifier,
          presentationSeed: physical.presentationSeed,
          expiresAt: "",
          status: "COMPLETED",
          physicsVersion: physical.physicsVersion,
          geometryVersion: physical.geometryVersion,
          maxRerolls: 3,
        };
      else {
        setNotice("Stored result replay · no new roll");
        reveal(event.result);
      }
    }

    if (session) {
      const original = session;
      import("@/lib/dice-renderer")
        .then(async ({ startPhysicalRoll }) => {
          if (!active) return;
          const visual = mode === "TEXT_ONLY" ? null : host.current;
          const handle = await startPhysicalRoll(
            original,
            visual,
            mode === "3D",
            (values) => {
              if (!active) return;
              setState("READING_PHYSICAL_RESULT");
              if (event.result) {
                if (
                  JSON.stringify(values) !==
                  JSON.stringify(event.result.dice.groups.map((g) => g.dice))
                ) {
                  renderer.current?.dispose();
                  renderer.current = null;
                  setNotice("Replay trajectory differs · canonical stored result unchanged");
                }
                reveal(event.result);
              } else submit(values);
            },
            failed,
            () => {
              if (active) {
                setState("COCKED_REROLL");
                setNotice("Cocked die – rerolling");
              }
            },
          );
          if (!active) {
            handle.dispose();
            return;
          }
          renderer.current = handle;
          if (skip.current) handle.skip();
        })
        .catch(failed);
    }

    return () => {
      active = false;
      clearTimeout(timer);
      retry.current = null;
      renderer.current?.dispose();
      renderer.current = null;
    };

    // Mode is sampled at launch: changing preferences never restarts a live physical throw.
  }, [event, ready, requesting]);

  async function cancel() {
    if (!event?.session) return;
    try {
      await api(`/roll-sessions/${event.session.rollSessionId}/cancel`, {
        method: "POST",
      });
      stop.current();
      renderer.current?.dispose();
      renderer.current = null;
      setState("DISMISSED");
      callbacks.current.onCancel?.();
    } catch (e) {
      setError((e as Error).message);
    }
  }

  const visible =
    !!event && !["IDLE", "AUTHORISING", "DISMISSED"].includes(state);

  return (
    <div className="dice-presentation">
      <details className="dice-preferences">
        <summary>Dice presentation settings</summary>
        <label>
          Dice presentation
          <select
            aria-label="Dice presentation"
            value={preferences.mode}
            onChange={(e) =>
              change({
                ...preferences,
                mode: e.target.value as DicePreferences["mode"],
              })
            }
          >
            <option value="3D">3D</option>
            <option value="REDUCED_MOTION">Reduced Motion</option>
            <option value="TEXT_ONLY">Text Only</option>
          </select>
        </label>
        <p className="small">
          All modes use the same physical simulation. Preferences apply to the
          next roll.
        </p>
      </details>

      {requesting && <p role="status">Authorising roll…</p>}
      <section
        className="dice-overlay"
        data-state={state}
        aria-label="Dice presentation"
        hidden={!visible}
      >
        <div className="dice-canvas" ref={host} />
        {visible && (
          <div className="dice-overlay-controls">
            {state === "REVEALED" ? (
              <button
                onClick={() => {
                  setState("DISMISSED");
                  renderer.current?.dispose();
                  renderer.current = null;
                }}
              >
                Dismiss
              </button>
            ) : (
              <>
                <span role="status">
                  {state === "SUBMITTING_RESULT"
                    ? "Saving physical result…"
                    : state === "COCKED_REROLL"
                      ? "Cocked die – rerolling"
                      : state === "ERROR"
                        ? "Roll needs attention"
                        : "Rolling…"}
                </span>
                {["ROLLING", "COCKED_REROLL"].includes(state) && (
                  <button
                    onClick={() => {
                      skip.current = true;
                      renderer.current?.skip();
                    }}
                  >
                    Skip animation
                  </button>
                )}
                {state === "ERROR" && retry.current && (
                  <button onClick={() => retry.current?.()}>
                    Retry submission
                  </button>
                )}
                {event.session && (
                  <button
                    onClick={() => void cancel()}
                    disabled={state === "SUBMITTING_RESULT"}
                  >
                    Cancel roll
                  </button>
                )}
              </>
            )}
          </div>
        )}
        {error && visible && (
          <p className="dice-floating-result" role="alert">
            {error}
          </p>
        )}
        {visible && state === "REVEALED" && shown?.event === event && (
          <div className="dice-floating-result" role="status">
            {notice && <p>{notice}</p>}
            <DiceResult result={shown.result} />
          </div>
        )}
      </section>
    </div>
  );
}

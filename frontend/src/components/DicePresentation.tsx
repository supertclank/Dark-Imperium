"use client";
import { useEffect, useRef, useState } from "react";
import type { RollResult } from "@/lib/rolls";
import {
  defaultPreferences,
  effectiveMode,
  presentRoll,
  physicalDice,
  preferenceKey,
  readPreferences,
  type DicePreferences,
} from "@/lib/dice-presentation";
import type { DiceTrayRenderer } from "@/lib/dice-renderer";
import { DiceResult } from "./DiceResult";
export type PresentationEvent = {
  result: RollResult;
  serial: number;
  replay: boolean;
};
export type PresentationState =
  | "IDLE"
  | "REQUESTING"
  | "ROLLING"
  | "SETTLING"
  | "REVEALED"
  | "DISMISSED";
export function DicePresentation({
  event,
  onReveal,
  requesting = false,
}: {
  event: PresentationEvent | null;
  onReveal?: (result: RollResult) => void;
  requesting?: boolean;
}) {
  const [preferences, setPreferences] =
      useState<DicePreferences>(defaultPreferences),
    [ready, setReady] = useState(false),
    [reduce, setReduce] = useState(false);
  const [revealedEvent, setRevealedEvent] = useState<PresentationEvent | null>(
    null,
  );
  const [state, setState] = useState<PresentationState>("IDLE"),
    [failure, setFailure] = useState("");
  const host = useRef<HTMLDivElement>(null),
    renderer = useRef<DiceTrayRenderer | null>(null),
    reveal = useRef(onReveal),
    skip = useRef(false);
  const audio = useRef<AudioContext | null>(null),
    sound = useRef(false);
  sound.current = preferences.sound;
  reveal.current = onReveal;
  useEffect(
    () => () => {
      void audio.current?.close();
    },
    [],
  );
  function updatePreferences(next: DicePreferences) {
    setPreferences(next);
    try {
      localStorage.setItem(preferenceKey, JSON.stringify(next));
    } catch {}
    window.dispatchEvent(new CustomEvent("dice-preferences", { detail: next }));
  }
  function enableSound(enabled: boolean) {
    updatePreferences({ ...preferences, sound: enabled });
    if (enabled)
      try {
        audio.current ??= new AudioContext();
        void audio.current.resume().catch(() => {});
      } catch {}
  }
  function clickSound() {
    if (!sound.current || !audio.current || audio.current.state !== "running")
      return;
    try {
      const ctx = audio.current,
        osc = ctx.createOscillator(),
        gain = ctx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(145, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(55, ctx.currentTime + 0.09);
      gain.gain.setValueAtTime(0.035, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
      osc.connect(gain).connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.13);
    } catch {}
  }

  const mode = effectiveMode(preferences.mode, reduce);
  useEffect(() => {
    try {
      setPreferences(readPreferences(localStorage.getItem(preferenceKey)));
    } catch {}
    setReady(true);
    const media = window.matchMedia?.("(prefers-reduced-motion: reduce)");
    if (!media) return;
    setReduce(media.matches);
    const update = () => setReduce(media.matches);
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    if (ready)
      try {
        localStorage.setItem(preferenceKey, JSON.stringify(preferences));
      } catch {}
  }, [preferences, ready]);
  useEffect(() => {
    const sync = (e: Event) =>
      setPreferences((e as CustomEvent<DicePreferences>).detail);
    window.addEventListener("dice-preferences", sync);
    return () => window.removeEventListener("dice-preferences", sync);
  }, []);
  useEffect(() => {
    const hide = () => {
      setState("DISMISSED");
      renderer.current?.dispose();
      renderer.current = null;
    };
    window.addEventListener("dice-presentation-start", hide);
    return () => window.removeEventListener("dice-presentation-start", hide);
  }, []);
  useEffect(() => {
    if (requesting) setState("REQUESTING");
  }, [requesting]);
  useEffect(() => {
    if (!ready || !event || requesting) return;
    if (revealedEvent === event) {
      setState("DISMISSED");
      return;
    }
    let active = true,
      completed = false,
      timer: ReturnType<typeof setTimeout> | undefined;
    skip.current = false;
    setFailure("");
    setState("ROLLING");
    const done = () => {
      if (!active || completed) return;
      completed = true;
      clickSound();
      setRevealedEvent(event);
      setState("REVEALED");
      reveal.current?.(event.result);
      timer = setTimeout(() => {
        if (active) {
          setState("DISMISSED");
          renderer.current?.dispose();
          renderer.current = null;
        }
      }, 4500);
    };
    const fallback = () => {
      if (!active) return;
      setFailure("3D unavailable · stored result");
      renderer.current?.dispose();
      renderer.current = null;
      timer = setTimeout(done, 0);
    };
    if (mode === "TEXT_ONLY") done();
    else if (physicalDice(presentRoll(event.result)).length > 20) {
      setFailure(
        "Large pool · complete text result (20 physical dice maximum)",
      );
      done();
    } else
      import("@/lib/dice-renderer")
        .then(async ({ createDiceRenderer }) => {
          if (!active || !host.current) return;
          const created = await createDiceRenderer(
            host.current,
            fallback,
            () => {
              if (mode === "REDUCED_MOTION") timer = setTimeout(done, 150);
              else done();
            },
            () => {
              if (active) setState("SETTLING");
            },
          );
          if (!active) {
            created.dispose();
            return;
          }
          renderer.current = created;
          created.show(
            presentRoll(event.result),
            mode === "REDUCED_MOTION" || skip.current,
          );
        })
        .catch(fallback);
    return () => {
      active = false;
      clearTimeout(timer);
      renderer.current?.dispose();
      renderer.current = null;
    };
  }, [event, ready, mode, requesting]);
  const visible =
    event &&
    state !== "IDLE" &&
    state !== "DISMISSED" &&
    state !== "REQUESTING";
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
              updatePreferences({
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
        <label>
          Dice sound
          <select
            aria-label="Dice sound"
            value={preferences.sound ? "on" : "off"}
            onChange={(e) => enableSound(e.target.value === "on")}
          >
            <option value="off">Off</option>
            <option value="on">On</option>
          </select>
        </label>
      </details>
      {requesting && <p role="status">Requesting authoritative roll…</p>}
      <section
        className="dice-overlay"
        data-state={state}
        aria-label="Dice presentation"
        hidden={!visible}
      >
        <div className="dice-canvas" ref={host} />
        {visible && (
          <div className="dice-overlay-controls">
            {state === "ROLLING" || state === "SETTLING" ? (
              <>
                <span role="status">
                  {state === "SETTLING" ? "Settling…" : "Rolling…"}
                </span>
                <button
                  type="button"
                  onClick={() => {
                    skip.current = true;
                    renderer.current?.skip();
                  }}
                >
                  Skip animation
                </button>
              </>
            ) : (
              <button
                type="button"
                onClick={() => {
                  setState("DISMISSED");
                  renderer.current?.dispose();
                  renderer.current = null;
                }}
              >
                Dismiss
              </button>
            )}
          </div>
        )}
        {visible && state === "REVEALED" && revealedEvent === event && (
          <div className="dice-floating-result" role="status">
            {failure && <p>{failure}</p>}
            <DiceResult result={event.result} mode="TEXT_ONLY" />
          </div>
        )}
      </section>
    </div>
  );
}

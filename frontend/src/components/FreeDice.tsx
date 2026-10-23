"use client";
import { useEffect, useRef, useState } from "react";
import { useDiceCoordinator } from "@/lib/dice-coordinator";
import { api, ApiError } from "@/lib/api";
import type { RollHistory, RollResult } from "@/lib/rolls";
import { useSession } from "./Session";
import { DicePresentation, type PresentationEvent } from "./DicePresentation";
import { DiceResult } from "./DiceResult";
const sides = [20, 12, 10, 8, 6, 4, 100];
type Request = { requestId: string; pool: { count: number; sides: number }[] };
export function FreeDice() {
  const coordinator = useDiceCoordinator();
  const { user } = useSession();
  const [open, setOpen] = useState(false),
    [pool, setPool] = useState<Record<number, number>>({}),
    [history, setHistory] = useState<RollResult[]>([]),
    [latest, setLatest] = useState<RollResult | null>(null),
    [event, setEvent] = useState<PresentationEvent | null>(null),
    [phase, setPhase] = useState<"IDLE" | "REQUESTING" | "PRESENTING">("IDLE"),
    [error, setError] = useState(""),
    [retry, setRetry] = useState<Request | null>(null);
  const flight = useRef(false);
  useEffect(() => {
    setHistory([]);
    setLatest(null);
    setEvent(null);
    if (user)
      api<RollHistory>("/rolls/free")
        .then((h) => setHistory(h.items))
        .catch(() => {});
  }, [user?.id]);
  const count = Object.values(pool).reduce((a, b) => a + b, 0),
    groups = sides
      .filter((s) => pool[s] > 0)
      .map((s) => ({ sides: s, count: pool[s] })),
    summary = groups.map((g) => `${g.count}d${g.sides}`).join(" + ");
  function change(s: number, delta: number) {
    setPool((p) => ({
      ...p,
      [s]: Math.max(0, Math.min(100, p[s] || 0) + delta),
    }));
  }
  function present(result: RollResult, replay: boolean) {
    if (replay && !coordinator.acquire()) return;
    setLatest(null);
    setPhase("PRESENTING");
    setEvent((e) => ({ result, replay, serial: (e?.serial ?? 0) + 1 }));
  }
  async function roll(request: Request) {
    if (flight.current || !coordinator.acquire()) return;
    flight.current = true;
    setEvent(null);
    setPhase("REQUESTING");
    setLatest(null);
    setError("");
    setRetry(request);
    try {
      const result = await api<RollResult>("/rolls/free", {
        method: "POST",
        body: JSON.stringify(request),
      });
      setRetry(null);
      present(result, false);
    } catch (e) {
      setError((e as Error).message);
      if (e instanceof ApiError && e.status > 0 && e.status < 500)
        setRetry(null);
      setPhase("IDLE");
      coordinator.release();
    } finally {
      flight.current = false;
    }
  }
  if (!user) return null;
  return (
    <>
      <button
        type="button"
        className="free-dice-launcher"
        aria-expanded={open}
        onClick={() => setOpen(!open)}
      >
        Dice
      </button>
      <div className="free-dice-settings">
        <DicePresentation
          event={event}
          requesting={phase === "REQUESTING"}
          onReveal={(r) => {
            setLatest(r);
            setPhase("IDLE");
            coordinator.release();
            setHistory((h) =>
              h.some((x) => x.id === r.id) ? h : [r, ...h].slice(0, 25),
            );
          }}
        />
      </div>
      {open && (
        <aside className="free-dice-panel" aria-label="Free dice roller">
          <h2>Free dice</h2>
          <p>Raw dice · no modifiers · private server rolls</p>
          <div className="free-dice-pool">
            {sides.map((s) => (
              <div key={s}>
                <button
                  disabled={
                    coordinator.otherBusy || phase !== "IDLE" || count >= 100
                  }
                  onClick={() => change(s, 1)}
                >
                  d{s}
                </button>
                <button
                  aria-label={`Remove d${s}`}
                  disabled={
                    coordinator.otherBusy || phase !== "IDLE" || !pool[s]
                  }
                  onClick={() => change(s, -1)}
                >
                  −
                </button>
                <output aria-label={`d${s} quantity`}>{pool[s] || 0}</output>
                <button
                  aria-label={`Add d${s}`}
                  disabled={
                    coordinator.otherBusy || phase !== "IDLE" || count >= 100
                  }
                  onClick={() => change(s, 1)}
                >
                  +
                </button>
              </div>
            ))}
          </div>
          <p aria-label="Dice pool">{summary || "Choose dice"}</p>
          <p className="small">
            Up to 100 dice. Pools above 20 physical dice use the complete text
            result.
          </p>
          <button
            disabled={coordinator.otherBusy || phase !== "IDLE"}
            onClick={() => setPool({})}
          >
            Clear Dice
          </button>
          <button
            disabled={
              coordinator.otherBusy ||
              phase !== "IDLE" ||
              count === 0 ||
              retry !== null
            }
            onClick={() =>
              void roll({ requestId: crypto.randomUUID(), pool: groups })
            }
          >
            Roll pool
          </button>
          {error && <p role="alert">{error}</p>}
          {retry && phase === "IDLE" && (
            <button onClick={() => void roll(retry)}>
              Retry same free roll
            </button>
          )}
          {phase !== "IDLE" ? (
            <p role="status">
              Rolling… results and history appear after settling.
            </p>
          ) : (
            <>
              {latest && (
                <>
                  <DiceResult result={latest} />
                  <button onClick={() => present(latest, true)}>
                    Replay Dice
                  </button>
                  <button
                    onClick={() =>
                      void roll({
                        requestId: crypto.randomUUID(),
                        pool: latest.dice.groups.map((g) => ({
                          sides: g.sides,
                          count: g.dice.length,
                        })),
                      })
                    }
                  >
                    Roll Again
                  </button>
                </>
              )}
              <h3>Free roll history</h3>
              <ol>
                {history.map((r) => (
                  <li key={r.id}>
                    <span>
                      {r.label} · {r.total}
                    </span>{" "}
                    <button onClick={() => present(r, true)}>
                      Replay {r.label}
                    </button>
                  </li>
                ))}
              </ol>
            </>
          )}
        </aside>
      )}
    </>
  );
}

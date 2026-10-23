"use client";
import { useEffect, useRef, useState } from "react";
import { useDiceCoordinator } from "@/lib/dice-coordinator";
import { api, ApiError } from "@/lib/api";
import { SavedCharacter, signed } from "@/lib/builder";
import {
  RollHistory,
  RollOption,
  RollOptions,
  RollRequest,
  RollResult,
  RollSession,
} from "@/lib/rolls";
import { DicePresentation, type PresentationEvent } from "./DicePresentation";
import { RollActionButton } from "./RollActionButton";
import { PlaySheet } from "./PlaySheet";
import { DiceResult } from "./DiceResult";

type Props = {
  character: SavedCharacter;
  onRefresh: () => Promise<void>;
  playLayout?: boolean;
};
export function RollPanel({ character, onRefresh, playLayout = false }: Props) {
  const coordinator = useDiceCoordinator();
  const [options, setOptions] = useState<RollOptions | null>(null);
  const [history, setHistory] = useState<RollHistory>({
    items: [],
    limit: 25,
    hasMore: false,
  });
  const [latest, setLatest] = useState<RollResult | null>(null);
  const [confirmation, setConfirmation] = useState<RollOption | null>(null);
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const [lastRequest, setLastRequest] = useState<RollRequest | null>(null),
    [uncertain, setUncertain] = useState(false);
  const [presentation, setPresentation] = useState<PresentationEvent | null>(
    null,
  );
  const seenResults = useRef(new Set<string>());
  function present(result: RollResult, replay = false) {
    if (replay && !coordinator.acquire()) return;
    setPresenting(true);
    setLatest(null);
    setPresentation((p) => ({ result, serial: (p?.serial ?? 0) + 1, replay }));
  }
  const inFlight = useRef(false);
  const [presenting, setPresenting] = useState(false);
  const base = `/characters/${character.id}/rolls`;
  useEffect(() => {
    let active = true;
    Promise.all([api<RollOptions>(`${base}/options`), api<RollHistory>(base)])
      .then(([o, h]) => {
        if (active) {
          setOptions(o);
          setHistory(h);
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      });
    return () => {
      active = false;
    };
  }, [base, character.runtime.stateVersion]);
  async function refresh() {
    await onRefresh();
    const [o, h] = await Promise.all([
      api<RollOptions>(`${base}/options`),
      api<RollHistory>(base),
    ]);
    setOptions(o);
    setHistory(h);
  }
  async function submit(request: RollRequest) {
    if (inFlight.current || !coordinator.acquire()) return;
    inFlight.current = true;
    setPresentation(null);
    setBusy(true);
    setPresenting(true);
    setLatest(null);
    setError("");
    setLastRequest(request);
    setConfirmation(null);
    try {
      const session = await api<RollSession>(
        `/characters/${character.id}/roll-sessions`,
        {
          method: "POST",
          body: JSON.stringify(request),
        },
      );
      setUncertain(false);
      if (session.result) present(session.result, true);
      else if (session.status === "CREATED")
        setPresentation((p) => ({
          session,
          serial: (p?.serial ?? 0) + 1,
          replay: false,
        }));
      else
        throw new ApiError(
          409,
          "Roll session expired or was cancelled. Start a new roll.",
        );
    } catch (e) {
      const failure = e as ApiError;
      coordinator.release();
      setPresenting(false);
      setError(failure.message);
      const ambiguous =
        !(e instanceof ApiError) ||
        failure.status === 0 ||
        failure.status >= 500;
      setUncertain(ambiguous);
      if (!ambiguous) {
        setLastRequest(null);
        try {
          await refresh();
        } catch {
          setOptions(null);
        }
      }
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }
  function requestRoll(
    option: RollOption,
    parent?: RollResult,
    confirmed = false,
  ) {
    if (
      !options ||
      !option.available ||
      coordinator.otherBusy ||
      busy ||
      presenting ||
      uncertain
    )
      return;
    if (option.consumes && !confirmed) {
      setConfirmation(option);
      return;
    }
    const ability = option.abilities.length
      ? parent?.context.ability
      : undefined;
    void submit({
      requestId: crypto.randomUUID(),
      rollId: option.id,
      profileId: options.profileId,
      profileDigest: options.profileDigest,
      expectedStateVersion: options.stateVersion,
      visibility: "PRIVATE",
      confirmConsumption: option.consumes,
      ...(ability ? { ability } : {}),
      ...(parent ? { parentResultId: parent.id } : {}),
    });
  }
  const grouped =
    options?.options.reduce<Record<string, RollOption[]>>((groups, o) => {
      const key = o.itemId || o.category;
      (groups[key] ??= []).push(o);
      return groups;
    }, {}) || {};
  const again = latest
    ? options?.options.find(
        (o) => o.id === latest.requestedRollId && !o.consumes,
      )
    : undefined;
  const linkedDamage =
    latest?.rollType === "attack"
      ? options?.options.find(
          (o) => o.actionId === latest.actionId && o.category === "damage",
        )
      : undefined;
  return (
    <section
      className={playLayout ? "play-roll-panel" : "panel roll-panel"}
      aria-label="Character rolls"
    >
      {!playLayout && (
        <>
          <h2 id="rolling-heading">Roll dice</h2>
          <p>
            Server-authorised physical rolls. Confirmed consumables are reserved
            until the result is saved.
          </p>
        </>
      )}
      {!options && !error && <p role="status">Loading supported rolls…</p>}
      <DicePresentation
        event={presentation}
        requesting={busy}
        onReveal={(result) => {
          setLatest(result);
          setPresenting(false);
          coordinator.release();
          void refresh().catch(() =>
            setError("Result saved. Refresh the sheet to load current state."),
          );
        }}
        onCancel={() => {
          setPresenting(false);
          setPresentation(null);
          coordinator.release();
        }}
      />
      {playLayout ? (
        <PlaySheet
          character={character}
          options={options?.options ?? []}
          disabled={coordinator.otherBusy || busy || presenting || uncertain}
          onRoll={requestRoll}
        />
      ) : (
        <div className="roll-controls">
          {Object.entries(grouped).map(([key, items]) => {
            const weapon = !!items[0].itemId;
            const label = weapon
              ? character.calculated.actions.find((a) => a.itemId === key)
                  ?.name || items[0].label
              : {
                  attribute: "Ability checks",
                  skill: "Skill checks",
                  save: "Saving throws",
                  ability: "Initiative",
                  damage: "Innate damage",
                }[key] || key;
            const choices = items[0].abilities;
            return (
              <details key={key} open={weapon || key === "ability"}>
                <summary>{label}</summary>
                <div className="roll-button-grid">
                  {items.map((option) => (
                    <div key={option.id}>
                      <RollActionButton
                        option={option}
                        disabled={
                          coordinator.otherBusy ||
                          busy ||
                          presenting ||
                          uncertain
                        }
                        onRoll={() => requestRoll(option)}
                      />
                      <p className="small muted">
                        Baseline:{" "}
                        {option.groups
                          .map((g) => `${g.count}d${g.sides}`)
                          .join(" + ")}{" "}
                        {signed(option.modifier)}
                        {option.consumes
                          ? ` · Quantity: ${option.quantity}`
                          : ""}
                        {choices.length
                          ? " · Uses this historical profile’s default ability"
                          : ""}
                      </p>
                      {!option.available && <p>{option.reason}</p>}
                    </div>
                  ))}
                </div>
              </details>
            );
          })}
        </div>
      )}
      {confirmation && (
        <div
          className="consumption-confirm"
          role="group"
          aria-label="Confirm grenade use"
        >
          <p>
            Use {confirmation.label.replace(/ damage$/, "")}? This will consume
            1 of {confirmation.quantity}.
          </p>
          <button
            type="button"
            disabled={busy}
            onClick={() => requestRoll(confirmation, undefined, true)}
          >
            Confirm use of one {confirmation.label.replace(/ damage$/, "")}
          </button>
          <button
            type="button"
            disabled={busy}
            onClick={() => setConfirmation(null)}
          >
            Cancel grenade use
          </button>
        </div>
      )}
      {busy && <p role="status">Resolving roll on the server…</p>}
      {error && <p role="alert">{error}</p>}
      {uncertain && (
        <p>
          The outcome is uncertain. Retry this same request to recover the
          original result without duplicate consumption.
        </p>
      )}
      {lastRequest && uncertain && (
        <button
          type="button"
          className="secondary"
          disabled={busy}
          onClick={() => void submit(lastRequest)}
        >
          Retry same request
        </button>
      )}
      <button
        type="button"
        className="secondary"
        disabled={coordinator.otherBusy || busy || presenting}
        onClick={() => {
          setError("");
          void refresh().catch((e) => setError(e.message));
        }}
      >
        Refresh rolls and character
      </button>
      <div aria-live="polite" aria-atomic="true">
        {latest && (
          <>
            <h3>Latest result</h3>
            <DiceResult result={latest} mode="TEXT_ONLY" />
            <div className="roll-result-actions">
              <button
                type="button"
                className="secondary"
                onClick={() => present(latest, true)}
              >
                Replay animation
              </button>
              {again && (
                <button
                  type="button"
                  disabled={
                    coordinator.otherBusy ||
                    busy ||
                    presenting ||
                    uncertain ||
                    !again.available
                  }
                  onClick={() => {
                    if (!options) return;
                    const request: RollRequest = {
                      requestId: crypto.randomUUID(),
                      rollId: again.id,
                      profileId: options.profileId,
                      profileDigest: options.profileDigest,
                      expectedStateVersion: options.stateVersion,
                      visibility: "PRIVATE",
                      confirmConsumption: false,
                      ...(latest.context.ability && again.abilities.length
                        ? { ability: latest.context.ability }
                        : {}),
                    };
                    void submit(request);
                  }}
                >
                  Roll Again
                </button>
              )}
            </div>
            {linkedDamage && (
              <button
                type="button"
                disabled={
                  coordinator.otherBusy ||
                  busy ||
                  presenting ||
                  uncertain ||
                  !linkedDamage.available
                }
                onClick={() => requestRoll(linkedDamage, latest)}
              >
                Roll linked damage after manually confirming hit
              </button>
            )}
          </>
        )}
      </div>
      <details className="play-history" open={!playLayout}>
        <summary>Recent rolls</summary>
        {presenting ? (
          <p>History hidden until dice settle.</p>
        ) : !history.items.length ? (
          <p>No rolls recorded yet.</p>
        ) : (
          <ol className="roll-history">
            {history.items.map((result) => (
              <li key={result.id}>
                <details>
                  <summary>
                    <time dateTime={result.timestamp}>
                      {new Date(result.timestamp).toLocaleTimeString()}
                    </time>{" "}
                    · {result.label} · {result.total}
                    {result.damageType ? ` ${result.damageType.name}` : ""}
                  </summary>
                  <DiceResult result={result} mode="TEXT_ONLY" />
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => present(result, true)}
                  >
                    Replay Dice
                  </button>
                </details>
              </li>
            ))}
          </ol>
        )}
        {history.hasMore && (
          <p>
            Showing the latest {history.limit} rolls. Older results remain
            stored.
          </p>
        )}
      </details>
    </section>
  );
}

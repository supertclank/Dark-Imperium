"use client";
import { useEffect, useId, useSyncExternalStore } from "react";
let owner: string | null = null;
const listeners = new Set<() => void>();
const notify = () => listeners.forEach((fn) => fn());
export function useDiceCoordinator() {
  const id = useId();
  const current = useSyncExternalStore(
    (fn) => {
      listeners.add(fn);
      return () => {
        listeners.delete(fn);
      };
    },
    () => owner,
    () => null,
  );
  const release = () => {
    if (owner === id) {
      owner = null;
      notify();
    }
  };
  useEffect(() => release, []);
  return {
    otherBusy: current !== null && current !== id,
    acquire: () => {
      if (owner !== null && owner !== id) return false;
      owner = id;
      notify();
      window.dispatchEvent(new Event("dice-presentation-start"));
      return true;
    },
    release,
  };
}

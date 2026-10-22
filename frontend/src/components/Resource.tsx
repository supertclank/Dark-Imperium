"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";
export function useResource<T>(path: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const router = useRouter();
  useEffect(() => {
    let active = true;
    setError("");
    setData(null);
    api<T>(path)
      .then((value) => {
        if (active) setData(value);
      })
      .catch((e: Error) => {
        if (!active) return;
        if (e instanceof ApiError && e.status === 401) router.replace("/login");
        else setError(e.message);
      });
    return () => {
      active = false;
    };
  }, [path, attempt, router]);
  return { data, error, retry: () => setAttempt((v) => v + 1) };
}
export function ResourceState({
  error,
  retry,
}: {
  error: string;
  retry: () => void;
}) {
  return error ? (
    <div className="panel">
      <p role="alert" className="error">
        {error}
      </p>
      <button onClick={retry}>Try again</button>
    </div>
  ) : (
    <p role="status" className="loading">
      Retrieving records…
    </p>
  );
}

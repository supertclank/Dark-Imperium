"use client";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { usePathname, useRouter } from "next/navigation";
import { api, ApiError, User } from "@/lib/api";

const Context = createContext<{
  user: User | null;
  loading: boolean;
  error: string;
  refresh: () => Promise<void>;
}>({ user: null, loading: true, error: "", refresh: async () => {} });
export function SessionProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  async function refresh() {
    setError("");
    try {
      setUser(await api<User>("/auth/me"));
    } catch (e) {
      setUser(null);
      if (!(e instanceof ApiError && e.status === 401))
        setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    void refresh();
  }, []);
  return (
    <Context.Provider value={{ user, loading, error, refresh }}>
      {children}
    </Context.Provider>
  );
}
export const useSession = () => useContext(Context);
export function AuthGate({ children }: { children: ReactNode }) {
  const { user, loading, error, refresh } = useSession();
  const router = useRouter();
  const path = usePathname();
  useEffect(() => {
    if (!loading && !user && !error)
      router.replace(`/login?next=${encodeURIComponent(path)}`);
  }, [loading, user, error, router, path]);
  if (error)
    return (
      <div className="panel">
        <p role="alert">{error}</p>
        <button onClick={() => void refresh()}>Retry connection</button>
      </div>
    );
  if (loading || !user)
    return (
      <p role="status" className="loading">
        Accessing the archive…
      </p>
    );
  return <>{children}</>;
}

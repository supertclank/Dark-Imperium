"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { useSession } from "./Session";
export function Header() {
  const { user, refresh } = useSession();
  const path = usePathname();
  const router = useRouter();
  const [error, setError] = useState("");
  async function logout() {
    try {
      await api("/auth/logout", { method: "POST" });
      await refresh();
      router.push("/");
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <>
      <header className="header">
        <Link href="/" className="brand">
          <span className="brand-mark" aria-hidden="true">
            ✦
          </span>
          <span>
            DARK IMPERIUM<small>PERSONNEL ARCHIVE</small>
          </span>
        </Link>
        <nav aria-label="Main navigation">
          <Link
            href="/characters"
            aria-current={path.startsWith("/characters") ? "page" : undefined}
          >
            Characters
          </Link>
          <Link
            href="/compendium"
            aria-current={path.startsWith("/compendium") ? "page" : undefined}
          >
            Compendium
          </Link>
        </nav>
        <div className="account">
          {user ? (
            <button className="text-button" onClick={logout}>
              Log out
            </button>
          ) : (
            <Link href="/login">
              Log in <span aria-hidden="true">↗</span>
            </Link>
          )}
        </div>
      </header>
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
    </>
  );
}

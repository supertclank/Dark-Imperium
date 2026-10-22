"use client";
import { useState, type FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useSession } from "./Session";
export function AuthForm({ register = false }: { register?: boolean }) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const router = useRouter();
  const { refresh } = useSession();
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setBusy(true);
    const data = new FormData(e.currentTarget);
    try {
      await api(`/auth/${register ? "register" : "login"}`, {
        method: "POST",
        body: JSON.stringify({
          email: data.get("email"),
          password: data.get("password"),
        }),
      });
      if (register) {
        router.push("/login?registered=1");
        return;
      }
      await refresh();
      const target = new URLSearchParams(window.location.search).get("next");
      router.push(
        target && /^\/(characters|compendium)(\/[^?]*)?$/.test(target)
          ? target
          : "/characters",
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="auth-layout">
      <div className="auth-intro">
        <p className="eyebrow">PERSONNEL ACCESS</p>
        <h1>{register ? "Join the archive." : "Welcome back."}</h1>
        <p className="lead">
          Your characters. Your campaign. Your corner of the Imperium.
        </p>
        <div className="quote">
          “A name is the first thing
          <br />
          worth remembering.”<span>PERSONNEL DIVISION / FIELD NOTES</span>
        </div>
      </div>
      <form className="panel auth-form" onSubmit={submit}>
        <p className="eyebrow">
          {register ? "NEW ACCOUNT" : "IDENTITY VERIFICATION"}
        </p>
        <h2>{register ? "Create your account" : "Log in to continue"}</h2>
        {!register && (
          <p className="muted small">
            Newly registered? Use your email and password below.
          </p>
        )}
        <label htmlFor="email">Email address</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          maxLength={254}
          autoComplete="email"
          placeholder="you@example.com"
        />
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          required
          minLength={12}
          maxLength={128}
          autoComplete={register ? "new-password" : "current-password"}
          aria-describedby="password-help"
        />
        <p id="password-help" className="small muted">
          12–128 characters. Spaces and passphrases welcome.
        </p>
        {error && (
          <p role="alert" className="error">
            {error}
          </p>
        )}
        <button className="primary" disabled={busy}>
          {busy ? "Please wait…" : register ? "Create account" : "Log in"}{" "}
          <span aria-hidden="true">→</span>
        </button>
        <p className="small">
          {register ? "Already have an account?" : "New to the archive?"}{" "}
          <Link href={register ? "/login" : "/register"}>
            {register ? "Log in" : "Register"}
          </Link>
        </p>
      </form>
    </div>
  );
}

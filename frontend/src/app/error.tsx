"use client";
export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <div className="panel">
      <h1>The archive could not be loaded.</h1>
      <p>Please try again.</p>
      <button onClick={reset}>Retry</button>
    </div>
  );
}

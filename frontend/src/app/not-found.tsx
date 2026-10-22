import Link from "next/link";
export default function NotFound() {
  return (
    <div className="empty panel">
      <p className="eyebrow">RECORD NOT FOUND / 404</p>
      <h1>This archive is empty.</h1>
      <Link className="button primary" href="/characters">
        Return to your characters
      </Link>
    </div>
  );
}

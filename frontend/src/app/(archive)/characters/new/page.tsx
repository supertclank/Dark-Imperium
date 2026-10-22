import Link from "next/link";
import { CharacterForm } from "@/components/CharacterForm";
export default function NewCharacter() {
  return (
    <>
      <Link className="back-link" href="/characters">
        ← Your characters
      </Link>
      <div className="page-heading">
        <div>
          <p className="eyebrow">NEW PERSONNEL RECORD</p>
          <h1>Create a character</h1>
          <p className="muted">
            Choose an origin. Take up arms. Begin your story.
          </p>
        </div>
        <span className="edition-tag">LEVEL 01</span>
      </div>
      <CharacterForm />
    </>
  );
}

import Link from "next/link";
export default function Home() {
  return (
    <>
      <div className="eyebrow home-label">
        <span className="status-dot" /> PERSONNEL DIVISION / ARCHIVE 001
      </div>
      <section className="hero">
        <div>
          <p className="eyebrow">IN THE SHADOW OF THE IMPERIUM</p>
          <h1>
            Every soldier
            <br />
            has a <em>story.</em>
          </h1>
          <p className="lead">
            Give yours a name. Build a character, prepare your equipment, and
            keep your place in the campaign.
          </p>
          <div className="actions">
            <Link className="button primary" href="/characters/new">
              Create a character <span aria-hidden="true">↗</span>
            </Link>
            <Link className="button secondary" href="/characters">
              Open your archive
            </Link>
          </div>
          <p className="small muted">
            A private companion for your Dark Imperium tabletop game.
          </p>
        </div>
        <div className="seal-panel" aria-hidden="true">
          <div className="seal-orbit orbit-one" />
          <div className="seal-orbit orbit-two" />
          <div className="seal-core">✦</div>
          <span className="seal-top">IMPERIAL PERSONNEL RECORD</span>
          <span className="seal-bottom">HOLD THE LINE.</span>
          <span className="seal-code">DI / 001 — M41</span>
        </div>
      </section>
      <section className="home-grid" aria-label="Archive features">
        <Link href="/characters" className="feature">
          <span className="eyebrow">01 / PERSONNEL</span>
          <h2>
            Your characters <span>↗</span>
          </h2>
          <p>
            One place for your soldiers, their attributes, and their equipment.
          </p>
        </Link>
        <Link href="/compendium" className="feature">
          <span className="eyebrow">02 / REFERENCE</span>
          <h2>
            The compendium <span>↗</span>
          </h2>
          <p>
            Explore the species, classes, and weapons available to your group.
          </p>
        </Link>
        <div className="feature note">
          <span className="eyebrow">FIELD NOTE</span>
          <h2>A foundation for play</h2>
          <p>
            Rules and statistics in this edition are development placeholders.
            Your group’s rulebook remains the authority.
          </p>
        </div>
      </section>
    </>
  );
}

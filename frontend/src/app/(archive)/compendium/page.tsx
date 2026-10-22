import Link from "next/link";
export default function Compendium() {
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">02 / REFERENCE</p>
          <h1>The compendium</h1>
          <p className="muted">
            Knowledge for the journey ahead. Browse the current development
            content.
          </p>
        </div>
      </div>
      <div className="card-grid">
        {[
          {
            slug: "species",
            name: "Species",
            description: "The origins that shape your character.",
          },
          {
            slug: "classes",
            name: "Classes",
            description: "Training, purpose, and a place in the ranks.",
          },
          {
            slug: "weapons",
            name: "Weapons",
            description: "The tools you carry into the darkness.",
          },
        ].map((item, i) => (
          <Link
            className="feature compendium-card"
            key={item.slug}
            href={`/compendium/${item.slug}`}
          >
            <span className="eyebrow">VOLUME 0{i + 1}</span>
            <div className="volume-mark" aria-hidden="true">
              {["Ⅰ", "Ⅱ", "Ⅲ"][i]}
            </div>
            <h2>{item.name} ↗</h2>
            <p>{item.description}</p>
          </Link>
        ))}
      </div>
      <p className="field-note">
        This compendium contains representative development data. Additional
        content and progression will follow in future releases.
      </p>
    </>
  );
}

"use client";
import Link from "next/link";
import { useState } from "react";
import { Content, Weapon } from "@/lib/api";
import { useResource, ResourceState } from "./Resource";
export function CompendiumList({
  kind,
  title,
}: {
  kind: string;
  title: string;
}) {
  const { data, error, retry } = useResource<(Content | Weapon)[]>(`/${kind}`);
  const [search, setSearch] = useState("");
  const items = data?.filter((item) =>
    `${item.name} ${item.description}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );
  return (
    <>
      <Link className="back-link" href="/compendium">
        ← Compendium
      </Link>
      <div className="page-heading">
        <div>
          <p className="eyebrow">REFERENCE / DEVELOPMENT CONTENT</p>
          <h1>{title}</h1>
        </div>
        <div className="search">
          <label htmlFor="search">Search {title.toLowerCase()}</label>
          <input
            id="search"
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search the archive…"
          />
        </div>
      </div>
      {!data ? (
        <ResourceState error={error} retry={retry} />
      ) : (
        <div className="reference-list">
          {items?.length === 0 ? (
            <p className="panel">No records match your search.</p>
          ) : (
            items?.map((item) => (
              <article className="panel reference-entry" key={item.id}>
                <span className="eyebrow">{title} / FIELD REFERENCE</span>
                <h2>{item.name}</h2>
                <p className="muted">{item.description}</p>
                {"damageDice" in item && (
                  <>
                    <dl className="reference-stats">
                      <div>
                        <dt>Category</dt>
                        <dd>{item.category}</dd>
                      </div>
                      <div>
                        <dt>Damage</dt>
                        <dd>
                          {item.damageDice} {item.damageType}
                        </dd>
                      </div>
                      <div>
                        <dt>Normal range</dt>
                        <dd>{item.normalRange} m</dd>
                      </div>
                      <div>
                        <dt>Long range</dt>
                        <dd>{item.longRange} m</dd>
                      </div>
                    </dl>
                    <div className="tags">
                      {item.properties.map((p) => (
                        <span key={p.key}>{p.label}</span>
                      ))}
                    </div>
                  </>
                )}
              </article>
            ))
          )}
        </div>
      )}
    </>
  );
}

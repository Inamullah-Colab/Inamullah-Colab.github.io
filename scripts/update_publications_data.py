#!/usr/bin/env python3
"""Build _data/publications.yml from markdown_generator/publications.tsv."""

from __future__ import annotations

import csv
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "markdown_generator" / "publications.tsv"
OUTPUT_FILE = ROOT / "_data" / "publications.yml"


def clean(value: str | None) -> str:
    return (value or "").strip()


def main() -> int:
    if not SOURCE_FILE.exists():
        raise SystemExit(f"Missing source file: {SOURCE_FILE}")

    publications: list[dict] = []
    with SOURCE_FILE.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            date = clean(row.get("pub_date"))
            if not date:
                continue

            publication = {
                "title": clean(row.get("title")),
                "slug": clean(row.get("url_slug")),
                "date": date,
                "year": int(date[:4]),
                "type": clean(row.get("type")) or "manuscripts",
                "venue": clean(row.get("venue")),
                "status": clean(row.get("status")),
                "image": clean(row.get("image")),
                "summary": clean(row.get("excerpt")),
                "citation_key": clean(row.get("citation_key")),
                "links": [],
            }

            label = clean(row.get("link_label"))
            url = clean(row.get("link_url")) or clean(row.get("paper_url"))
            if label and url:
                publication["links"].append({"label": label, "url": url})

            press_label = clean(row.get("press_label"))
            press_url = clean(row.get("press_url"))
            if press_label and press_url:
                publication["links"].append({"label": press_label, "url": press_url})

            publications.append(publication)

    publications.sort(key=lambda item: item["date"], reverse=True)

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(publications, handle, sort_keys=False, allow_unicode=False)

    print(f"Wrote {len(publications)} publications to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

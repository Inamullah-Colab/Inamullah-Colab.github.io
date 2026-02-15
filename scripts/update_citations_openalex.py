#!/usr/bin/env python3
"""Update publication citation counts from OpenAlex into _data/citations.yml."""

from __future__ import annotations

import datetime as dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "_data" / "citations.yml"


def fetch_json(url: str) -> dict | None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "inamullah-colab-citation-updater/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def get_count_from_doi(doi: str) -> int | None:
    doi_url = "https://doi.org/" + doi
    url = "https://api.openalex.org/works/" + urllib.parse.quote(doi_url, safe="")
    data = fetch_json(url)
    if not data:
        return None
    count = data.get("cited_by_count")
    return int(count) if isinstance(count, int) else None


def get_count_from_arxiv(arxiv_id: str) -> int | None:
    filt = f"locations.landing_page_url:https://arxiv.org/abs/{arxiv_id}"
    query = urllib.parse.urlencode({"filter": filt, "per-page": 1})
    url = f"https://api.openalex.org/works?{query}"
    data = fetch_json(url)
    if not data:
        return None
    results = data.get("results") or []
    if not results:
        return None
    count = results[0].get("cited_by_count")
    return int(count) if isinstance(count, int) else None


def main() -> int:
    if not DATA_FILE.exists():
        print(f"Missing file: {DATA_FILE}")
        return 1

    with DATA_FILE.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    papers = cfg.get("papers") or {}
    if not isinstance(papers, dict):
        print("Invalid citations.yml: 'papers' must be a map")
        return 1

    total = 0
    for _, item in papers.items():
        if not isinstance(item, dict):
            continue
        source = str(item.get("source", "")).strip().lower()
        pid = str(item.get("id", "")).strip()
        include = bool(item.get("include_in_total", True))
        count = None

        if source == "doi" and pid:
            count = get_count_from_doi(pid)
        elif source == "arxiv" and pid:
            count = get_count_from_arxiv(pid)

        if count is not None:
            item["count"] = int(count)

        current = int(item.get("count", 0) or 0)
        if include:
            total += current

    cfg["total"] = int(total)
    cfg["last_updated_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    with DATA_FILE.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=False)

    print(f"Updated total citations: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

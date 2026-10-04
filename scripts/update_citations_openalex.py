#!/usr/bin/env python3
"""Update publication citation counts from OpenAlex into _data/citations.yml."""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "_data" / "citations.yml"


def fetch_json(url: str) -> dict | None:
    params = {"select": "id,cited_by_count"}
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "inamullah-colab-citation-updater/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        # Do not log the request URL, which may contain an API key.
        print(f"OpenAlex request failed ({type(exc).__name__})", file=sys.stderr)
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
    count = get_count_from_doi(f"10.48550/arXiv.{arxiv_id}")
    if count is not None:
        return count
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
    refreshed = 0
    failed = []
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    for key, item in papers.items():
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
            item["last_updated_utc"] = now
            refreshed += 1
            print(f"{key}: {count}")
        else:
            failed.append(key)
            print(f"Could not refresh {key}; keeping the previous count", file=sys.stderr)

        current = int(item.get("count", 0) or 0)
        if include:
            total += current

    if not refreshed:
        print("No citation counts were refreshed; leaving data unchanged", file=sys.stderr)
        return 1
    cfg["total"] = int(total)
    if not failed:
        cfg["last_updated_utc"] = now

    with DATA_FILE.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=False)

    print(f"Updated total citations: {total}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

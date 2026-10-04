#!/usr/bin/env python3
"""Mirror citation counts from the owner's public Google Scholar profile."""

import argparse
import datetime as dt
import html
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

DATA_FILE = Path(__file__).resolve().parents[1] / "_data" / "citations.yml"


def plain_text(markup):
    return html.unescape(re.sub(r"<[^>]*>", "", markup)).strip()


def parse_profile(markup, profile_id):
    rows = re.findall(r'<tr\b[^>]*class="gsc_a_tr"[^>]*>(.*?)</tr>', markup, re.S)
    counts = {}
    for row in rows:
        link = re.search(r'citation_for_view=([^"&]+)', row)
        count_cell = re.search(r'<a\b[^>]*class="gsc_a_ac(?:\s[^\"]*)?"[^>]*>(.*?)</a>', row, re.S)
        if not link or not count_cell:
            raise ValueError("Unrecognised Google Scholar publication row")
        article_id = urllib.parse.unquote(html.unescape(link.group(1)))
        if not article_id.startswith(profile_id + ":"):
            raise ValueError("Profile ID does not match the publication row")
        value = plain_text(count_cell.group(1)).replace(",", "")
        if value and not value.isdigit():
            raise ValueError("Invalid citation count")
        counts[article_id.split(":", 1)[1]] = int(value or 0)

    summary = re.search(r'<table\b[^>]*id="gsc_rsb_st"[^>]*>(.*?)</table>', markup, re.S)
    total_cell = re.search(r'<td\b[^>]*class="gsc_rsb_std"[^>]*>(.*?)</td>', summary.group(1), re.S) if summary else None
    if not counts or not total_cell:
        raise ValueError("Google Scholar profile unavailable or blocked; keeping existing counts")
    total = plain_text(total_cell.group(1)).replace(",", "")
    if not total.isdigit():
        raise ValueError("Invalid profile citation total")
    # A truncated profile must not silently reset totals or missing papers.
    if sum(counts.values()) != int(total):
        raise ValueError("Publication counts do not match the profile total")
    return counts, int(total)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-file", type=Path, help="Previously fetched public profile HTML")
    args = parser.parse_args(argv)
    try:
        cfg = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
        profile_id = cfg["scholar_profile_id"]
        if args.html_file:
            markup = args.html_file.read_text(encoding="utf-8")
        else:
            query = urllib.parse.urlencode({"user": profile_id, "hl": "en", "pagesize": 100})
            request = urllib.request.Request("https://scholar.google.com/citations?" + query,
                                            headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                markup = response.read().decode("utf-8")
        counts, total = parse_profile(markup, profile_id)
        for key, paper in cfg["papers"].items():
            if paper["scholar_id"] not in counts:
                raise ValueError(f"Missing Google Scholar publication: {key}")
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
        for key, paper in cfg["papers"].items():
            paper["count"] = counts[paper["scholar_id"]]
            paper["last_updated_utc"] = now
            print(f"{key}: {paper['count']}")
        cfg["total"] = total
        cfg["last_updated_utc"] = now
        DATA_FILE.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
        print(f"Google Scholar total: {total}")
        return 0
    except Exception as exc:
        print(f"Citation refresh failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

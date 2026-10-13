#!/usr/bin/env python3
"""List the acts for a playlist window, in show order.

Usage:
  python3 lineup.py                      # citywide: headliners, today -> +13 days
  python3 lineup.py --area Frelard       # Frelard: headliners AND openers
  python3 lineup.py --area Frelard --start 2026-10-18 --json

Reads data/seattle.json (run build_site.py first). Skips cancelled/postponed shows.
For an area, openers are included because small rooms are where the discovery is:
headliners get 3 songs, openers 2 (see PLAYLIST.md).
"""
import argparse
import datetime as dt
import json
import re
from zoneinfo import ZoneInfo

SKIP = ("tribute", "open mic", "showcase", " jam", "dance party", "dj night", "karaoke", "drag ")


def clean(name):
    """Artist name to search Spotify for: drop tour/album suffixes and early/late show tags."""
    n = re.sub(r"\s*\((early|late) show\)", "", name, flags=re.I)
    n = re.sub(r"\s+[-–]\s+.*(release|tour|anniversary|night \d).*$", "", n, flags=re.I)
    n = n.split(": ")[0]
    n = re.sub(r"\s+(ft\.|feat\.|featuring)\s.*$", "", n, flags=re.I)
    return n.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", help='e.g. "Frelard"; omit for citywide')
    ap.add_argument("--start", help="YYYY-MM-DD (default: today, Pacific)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--data", default="data/seattle.json")
    a = ap.parse_args()

    d = json.load(open(a.data))
    start = dt.date.fromisoformat(a.start) if a.start else dt.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    end = start + dt.timedelta(days=13)
    venues = d["venues"]
    acts, seen = [], set()
    for e in d["events"]:
        if not (start.isoformat() <= e["date"] <= end.isoformat()):
            continue
        if e.get("status") in ("cancelled", "postponed"):
            continue
        v = venues.get(e["venue"], {})
        if a.area and v.get("area") != a.area:
            continue
        if any(w in (" " + e["title"].lower()) for w in SKIP):
            continue
        bill = [(e["title"], "headliner")] + ([(s, "opener") for s in e["support"]] if a.area else [])
        for name, role in bill:
            name = clean(name)
            if role == "opener" and re.match(r"(dj|mc)\s", name, re.I):
                continue
            k = name.lower()
            if k in seen:
                continue
            seen.add(k)
            acts.append({"name": name, "role": role, "songs": 3 if role == "headliner" else 2,
                         "date": e["date"], "venue": v.get("short", e["venue"])})

    if a.json:
        print(json.dumps({"area": a.area, "start": start.isoformat(), "end": end.isoformat(), "acts": acts}, ensure_ascii=False, indent=1))
        return
    label = a.area or d.get("edition", "Seattle")
    heads = sum(x["role"] == "headliner" for x in acts)
    print(f"{label} {start:%b %-d}–{end:%b %-d}: {len(acts)} acts ({heads} headliners, {len(acts) - heads} openers), "
          f"{sum(x['songs'] for x in acts)} songs max")
    for x in acts:
        print(f"  {x['date']}  {x['venue']:<16} {'' if x['role'] == 'headliner' else '  + '}{x['name']}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass

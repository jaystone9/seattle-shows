#!/usr/bin/env python3
"""List the acts for a playlist window, in show order.

Usage:
  python3 lineup.py                      # citywide: headliners, today -> +13 days
  python3 lineup.py --area Frelard       # Frelard: headliners AND openers
  python3 lineup.py --area Frelard --start 2026-10-18 --json
  python3 lineup.py --city chicago       # another edition (cities.py): reads chicago/shows/

Reads shows/*.json. Skips cancelled/postponed shows.
For an area, openers are included because small rooms are where the discovery is:
every act gets its top 3 songs (see PLAYLIST.md).
"""
import argparse
import datetime as dt
import json
import re
from zoneinfo import ZoneInfo

SKIP = ("tribute", "open mic", "showcase", " jam", "dance party", "dj night", "karaoke", "drag ")


def clean(name):
    """Artist name to search Spotify for: drop tour/album suffixes and early/late show tags."""
    m = re.match(r"^.*\b(?:early|late) show with (.+)$", name, flags=re.I)  # "Honky Tonk Early Show with X"
    if m:
        name = m.group(1)
    n = re.sub(r"\s*\(((early|late) show|album release|record release|matinee)\)", "", name, flags=re.I)
    n = re.sub(r"\s+[-–]\s+(early show|late show|matinee)$", "", n, flags=re.I)
    n = re.sub(r"\s+on tour$", "", n, flags=re.I)
    n = re.sub(r"\s+[-–]\s+.*(release|tour|anniversary|night \d).*$", "", n, flags=re.I)
    # "Tractor Presents: X", "STG Presents: An Evening with X" → X; otherwise text before ":" is the act
    m = re.match(r"^.*\bpresents?:\s*(?:an evening with\s+)?(.+)$", n, flags=re.I)
    n = m.group(1) if m else n.split(": ")[0]
    n = re.sub(r"\s*\((argentina|mexico|uk|japan|brazil|chile|colombia|france|germany)\)$", "", n, flags=re.I)
    n = re.sub(r"\s+(ft\.|feat\.|featuring)\s.*$", "", n, flags=re.I)
    return n.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", help='e.g. "Frelard"; omit for citywide')
    ap.add_argument("--start", help="YYYY-MM-DD (default: today, Pacific)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--city", help="another edition from cities.py, e.g. chicago")
    a = ap.parse_args()

    # Read the venue files directly (not data/seattle.json) so a window that started
    # before today, e.g. Sunday's playlist on a Tuesday, still includes its first days.
    import glob
    import build_site
    tz, shows_dir, edition = "America/Los_Angeles", "shows", "Seattle"
    if a.city:
        build_site.use_city(a.city)
        tz, shows_dir, edition = build_site.CITY["tz"], build_site.path("shows"), build_site.CITY["name"]
    venue_key, split_title = build_site.venue_key, build_site.split_title
    start = dt.date.fromisoformat(a.start) if a.start else dt.datetime.now(ZoneInfo(tz)).date()
    end = start + dt.timedelta(days=13)
    venues = build_site.VENUES
    events = []
    for f in sorted(glob.glob(f"{shows_dir}/*.json")):
        for ev in json.load(open(f)):
            title, support = split_title(ev["title"])
            events.append({"date": ev.get("date", ""), "time": ev.get("start") or ev.get("doors") or "",
                           "venue": venue_key(ev), "title": title, "support": support,
                           "status": (ev.get("status") or "").lower()})
    events.sort(key=lambda e: (e["date"], e["time"]))
    d = {"events": events, "edition": edition}
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
            acts.append({"name": name, "role": role, "songs": 3,
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

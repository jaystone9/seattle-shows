#!/usr/bin/env python3
"""Draft this week's 2 Week Soundcheck newsletter issue from data/seattle.json.

Usage: python3 build_issue.py [data/seattle.json] [issues/]
Writes issues/<start>.html (paste into the beehiiv editor) and issues/<start>.txt.
Covers the playlist window; headliner + venue + ticket link per show.
"""
import datetime as dt
import html
import json
import os
import sys

SITE = "https://jaystone9.github.io/seattle-shows/"


def main(src="data/seattle.json", outdir="issues"):
    d = json.load(open(src))
    pl = d.get("playlist") or {}
    start = pl.get("start") or dt.date.today().isoformat()
    end = pl.get("end") or (dt.date.fromisoformat(start) + dt.timedelta(days=13)).isoformat()
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    rng = f"{s:%b} {s.day}–{e.day}" if s.month == e.month else f"{s:%b} {s.day}–{e:%b} {e.day}"
    shows = [x for x in d["events"] if start <= x["date"] <= end and x.get("status") != "cancelled"]
    venues = d["venues"]

    h, t = [], []
    h.append(f"<p>Here's what's playing in {d['edition']} {rng}: {len(shows)} shows across "
             f"{len({x['venue'] for x in shows})} venues. Start with the playlist, then grab tickets for whatever sticks.</p>")
    if pl.get("url"):
        h.append(f'<p><a href="{pl["url"]}"><strong>Listen: {pl.get("songs")} songs from {pl.get("artists")} headliners</strong></a></p>')
        t.append(f"Listen: {pl['url']}\n")
    h.append(f'<p>Full lineup, search and calendar: <a href="{SITE}">{SITE}</a></p>')
    cur = None
    for x in shows:
        if x["date"] != cur:
            cur = x["date"]
            day = dt.date.fromisoformat(cur)
            h.append(f"<h3>{day:%A, %B} {day.day}</h3>")
            t.append(f"\n{day:%A, %B} {day.day}")
        v = venues.get(x["venue"], {}).get("short", x["venue"])
        sup = f" with {', '.join(x['support'])}" if x["support"] else ""
        tm = ""
        if x.get("time"):
            hh, mm = map(int, x["time"].split(":"))
            tm = f"{hh % 12 or 12}{':%02d' % mm if mm else ''}{'pm' if hh >= 12 else 'am'}, "
        link = f' · <a href="{html.escape(x["url"])}">{"Tickets" if x["link"] == "tickets" else "Details"}</a>' if x.get("url") else ""
        h.append(f"<p><strong>{html.escape(x['title'])}</strong>{html.escape(sup)}<br>{tm}{html.escape(v)}{link}</p>")
        t.append(f"  {x['title']}{sup} — {tm}{v}  {x.get('url') or ''}")
    os.makedirs(outdir, exist_ok=True)
    open(f"{outdir}/{start}.html", "w").write("\n".join(h))
    open(f"{outdir}/{start}.txt", "w").write(f"2 Week Soundcheck · {d['edition']} · {rng}\n\n" + "\n".join(t) + "\n")
    print(f"Subject: {d['edition']}, {rng}: {len(shows)} shows and the playlist")
    print(f"wrote {outdir}/{start}.html and .txt")


if __name__ == "__main__":
    main(*sys.argv[1:])

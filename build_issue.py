#!/usr/bin/env python3
"""Draft this week's 2 Week Soundcheck newsletter issue from data/seattle.json.

Usage: python3 build_issue.py [data/seattle.json] [issues/]
Writes issues/<start>.html (paste into the beehiiv editor) and issues/<start>.txt,
and prints the subject and preview text.

The issue is deliberately short (Jay, Oct 12, 2026: "I don't want it to be messy"):
  1. Subject: "<dates>: Seattle 2 Week Playlist"
  2. One line on what this is
  3. The playlist (a linked card; in beehiiv, paste the Spotify link on its own line
     to get Spotify's preview card instead)
  4. Closing link: all N shows are on the site, searchable by venue and artist.
"""
import datetime as dt
import html
import json
import os
import sys

SITE = "https://2weeksoundcheck.com/"
PINK = "#D6336C"
INK = "#1C2433"


def rng(s, e):
    return f"{s:%b} {s.day}–{e.day}" if s.month == e.month else f"{s:%b} {s.day}–{e:%b} {e.day}"


def main(src="data/seattle.json", outdir="issues"):
    d = json.load(open(src))
    pl = d.get("playlist") or {}
    per = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(pl.get("per_artist") or 3, str(pl.get("per_artist") or 3))
    start = pl.get("start") or dt.date.today().isoformat()
    end = pl.get("end") or (dt.date.fromisoformat(start) + dt.timedelta(days=13)).isoformat()
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    dates = rng(s, e)
    shows = [x for x in d["events"] if start <= x["date"] <= end and x.get("status") != "cancelled"]
    n = len(shows)
    venues = d["venues"]
    edition = d.get("edition", "Seattle")

    subject = f"{dates}: {edition} 2 Week Playlist"
    preview_text = f"{pl.get('songs', '')} songs from the {pl.get('artists', n)} headliners playing {edition} over the next two weeks."

    h, t = [], []
    h.append(f"<p>Every headliner playing {edition} {dates}, {per} songs each, in show order. "
             f"Hit shuffle, and when something grabs you, go see it.</p>")
    t.append(f"Every headliner playing {edition} {dates}, {per} songs each, in show order.\n")

    if pl.get("url"):
        url = html.escape(pl["url"])
        h.append(f"<p><!-- In beehiiv, you can replace this card by pasting the link on its own line: {url} --></p>")
        h.append(
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;margin:8px 0 20px">'
            f'<tr><td style="background:{INK};border-radius:14px;padding:22px 24px">'
            f'<a href="{url}" style="text-decoration:none;color:#ffffff;display:block">'
            f'<span style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:{PINK};font-weight:700">This week\'s playlist</span><br>'
            f'<span style="font-size:24px;font-weight:800;line-height:1.2">{html.escape(pl.get("name", "The playlist"))}</span><br>'
            f'<span style="font-size:15px;color:#C9CFDB">{pl.get("songs")} songs · {pl.get("artists")} artists</span><br><br>'
            f'<span style="display:inline-block;background:{PINK};color:#ffffff;font-weight:700;padding:10px 18px;border-radius:999px">▶ Listen on Spotify</span>'
            f'</a></td></tr></table>')
        t.append(f"▶ Listen: {pl['url']}\n")

    h.append(f'<p style="margin-top:28px"><a href="{SITE}"><strong>All {n} shows are on the site →</strong></a><br>'
             f'<span style="color:#5A6476">Searchable by venue and artist, with tickets and a preview for every headliner.</span></p>')
    t.append(f"All {n} shows are on the site, searchable by venue and artist: {SITE}")

    os.makedirs(outdir, exist_ok=True)
    open(f"{outdir}/{start}.html", "w").write("\n".join(h) + "\n")
    open(f"{outdir}/{start}.txt", "w").write(f"Subject: {subject}\nPreview: {preview_text}\n\n" + "\n".join(t) + "\n")
    print(f"Subject: {subject}")
    print(f"Preview text: {preview_text}")
    print(f"wrote {outdir}/{start}.html and .txt")


if __name__ == "__main__":
    main(*sys.argv[1:])

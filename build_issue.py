#!/usr/bin/env python3
"""Draft this week's 2 Week Soundcheck newsletter issue from data/seattle.json.

Usage: python3 build_issue.py [data/seattle.json] [issues/]
Writes issues/<start>.html (paste into the beehiiv editor) and issues/<start>.txt,
and prints the subject and preview text.

The issue is deliberately short (Jay, Oct 12, 2026: "I don't want it to be messy"):
  1. Subject: "<dates>: Seattle 2 Week Playlist"
  2. One line on what this is (top 3 songs per artist)
  3. Both playlists, each with a line and a pink button: Seattle (headliners),
     then Frelard (Ballard + Fremont small rooms, openers included)
  4. Closing link: all N shows are on the site.
"""
import datetime as dt
import html
import json
import os
import sys

SITE = "https://2weeksoundcheck.com/"
PINK = "#D6336C"
INK = "#1C2433"
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def rng(s, e):
    return f"{s:%b} {s.day}–{e.day}" if s.month == e.month else f"{s:%b} {s.day}–{e:%b} {e.day}"


def button(url, label):
    return (f'<p><a href="{html.escape(url)}" style="display:inline-block;background:{PINK};color:#ffffff;font-weight:700;'
            f'padding:10px 18px;border-radius:999px;text-decoration:none">{label}</a></p>')


def main(src="data/seattle.json", outdir="issues"):
    d = json.load(open(src))
    pl = d.get("playlist") or {}
    start = pl.get("start") or dt.date.today().isoformat()
    end = pl.get("end") or (dt.date.fromisoformat(start) + dt.timedelta(days=13)).isoformat()
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    dates = rng(s, e)
    shows = [x for x in d["events"] if start <= x["date"] <= end and x.get("status") != "cancelled"]
    n = len(shows)
    edition = d.get("edition", "Seattle")
    # Area playlists (Frelard) for the same two weeks. Every issue carries both playlists.
    areas = {a: p for a, p in (d.get("area_playlists") or {}).items() if p.get("start") == start and p.get("url")}
    fr = areas.get("Frelard")
    if not fr:
        print("WARNING: no Frelard playlist for this window in playlists.json; build it (PLAYLIST.md 4b) and rerun.")
    pers = {(p.get("per_artist") or 3) for p in [pl] + ([fr] if fr else [])}
    per = WORDS.get(pers.pop(), "") if len(pers) == 1 else ""  # only state a count when both playlists agree

    subject = f"{dates}: {edition} 2 Week Playlist"
    preview_text = f"{pl.get('songs', '')} songs from the {pl.get('artists', n)} headliners playing {edition} over the next two weeks"
    preview_text += f", plus a Frelard playlist for Ballard and Fremont." if fr else "."

    h, t = [], []
    intro = (f"Two playlists for {dates}, the top {per + ' ' if per else ''}songs from each artist, in show order. "
             if fr else f"Every headliner playing {edition} {dates}, the top {per + ' ' if per else ''}songs each, in show order. ")
    h.append(f"<p>{intro}Hit shuffle, and when something grabs you, go see it.</p>")
    t.append(intro.strip() + "\n")

    if pl.get("url"):
        h.append(f"<p><strong>All of {edition}:</strong> {pl.get('songs')} songs from {pl.get('artists')} headliners across the city.</p>")
        h.append(button(pl["url"], "▶ Listen to the Seattle playlist on Spotify"))
        t.append(f"All of {edition} ({pl.get('songs')} songs, {pl.get('artists')} headliners): {pl['url']}\n")
    if fr:
        h.append(f"<p><strong>Frelard:</strong> {fr.get('songs')} songs from {fr.get('artists')} artists at the small rooms in Ballard and Fremont, openers included.</p>")
        h.append(button(fr["url"], "▶ Listen to the Frelard playlist on Spotify"))
        t.append(f"Frelard ({fr.get('songs')} songs, {fr.get('artists')} artists, openers included): {fr['url']}\n")

    h.append(f'<p style="margin-top:28px"><a href="{SITE}"><strong>All {n} shows are on the site →</strong></a><br>'
             f'<span style="color:#5A6476">Searchable by neighborhood, venue and artist, with tickets and a preview for every headliner.</span></p>')
    t.append(f"All {n} shows are on the site, searchable by neighborhood, venue and artist: {SITE}")
    if fr:
        t.append(f"Just Frelard: {SITE}?area=frelard")

    os.makedirs(outdir, exist_ok=True)
    open(f"{outdir}/{start}.html", "w").write("\n".join(h) + "\n")
    open(f"{outdir}/{start}.txt", "w").write(f"Subject: {subject}\nPreview: {preview_text}\n\n" + "\n".join(t) + "\n")
    print(f"Subject: {subject}")
    print(f"Preview text: {preview_text}")
    print(f"wrote {outdir}/{start}.html and .txt")


if __name__ == "__main__":
    main(*sys.argv[1:])

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
  4. "Start with this one": one song by one headliner, with when/where to see them.
     The Sunday run can add an original one-line note in issues/<start>-spotlight.json:
       {"artist": "Edgehill", "note": "..."}
     Never quote song lyrics here; they're copyrighted.
  5. Closing link: all N shows are on the site, searchable by venue and artist.
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


def spotlight_pick(shows, previews, outdir, start):
    """The show to feature: from the spotlight file if present, else the first
    show in the first week whose headliner has a preview song."""
    path = f"{outdir}/{start}-spotlight.json"
    want = json.load(open(path)) if os.path.exists(path) else {}
    with_pv = [x for x in shows if previews.get(x["title"])]
    if want.get("artist"):
        hit = [x for x in with_pv if x["title"].lower() == want["artist"].lower()]
        if hit:
            return hit[0], want.get("note", "")
    week1_end = (dt.date.fromisoformat(start) + dt.timedelta(days=6)).isoformat()
    first = [x for x in with_pv if x["date"] <= week1_end] or with_pv
    return (first[0], "") if first else (None, "")


def main(src="data/seattle.json", outdir="issues"):
    d = json.load(open(src))
    pl = d.get("playlist") or {}
    start = pl.get("start") or dt.date.today().isoformat()
    end = pl.get("end") or (dt.date.fromisoformat(start) + dt.timedelta(days=13)).isoformat()
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    dates = rng(s, e)
    shows = [x for x in d["events"] if start <= x["date"] <= end and x.get("status") != "cancelled"]
    n = len(shows)
    venues = d["venues"]
    previews = json.load(open("previews.json")) if os.path.exists("previews.json") else {}
    edition = d.get("edition", "Seattle")

    subject = f"{dates}: {edition} 2 Week Playlist"
    preview_text = f"{pl.get('songs', '')} songs from the {pl.get('artists', n)} headliners playing {edition} over the next two weeks."

    h, t = [], []
    h.append(f"<p>Every headliner playing {edition} {dates}, five songs each, in show order. "
             f"Hit shuffle, and when something grabs you, go see it.</p>")
    t.append(f"Every headliner playing {edition} {dates}, five songs each, in show order.\n")

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

    show, note = spotlight_pick(shows, previews, outdir, start)
    if show:
        pv = previews[show["title"]]
        day = dt.date.fromisoformat(show["date"])
        v = venues.get(show["venue"], {}).get("short", show["venue"])
        when = f"{day:%A}, {day:%b} {day.day} at {v}"
        song_url = f"https://open.spotify.com/track/{pv['track']}"
        tix = f' · <a href="{html.escape(show["url"])}">Tickets</a>' if show.get("url") and show.get("link") == "tickets" else ""
        h.append(f"<h3>Start with this one</h3>")
        h.append(f'<p><a href="{song_url}"><strong>“{html.escape(pv.get("song", "Top song"))}”</strong></a> by <strong>{html.escape(show["title"])}</strong>'
                 + (f". {html.escape(note)}" if note else "") + f"</p>")
        h.append(f"<p>See them {when}{tix}</p>")
        t.append(f"Start with this one: \"{pv.get('song')}\" by {show['title']} {song_url}" + (f"\n{note}" if note else ""))
        t.append(f"See them {when}  {show.get('url') or ''}\n")

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

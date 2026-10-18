#!/usr/bin/env python3
"""Draft this week's 2 Week Soundcheck newsletter issue and its pre-send check email.

Usage: python3 build_issue.py [data/seattle.json] [issues/] [--check-links]

Writes:
  issues/<start>.html        the subscriber issue (paste into the beehiiv editor)
  issues/<start>.txt         the same issue as plain text, with subject and preview
  issues/<start>-check.txt   the "ready to send?" check email that goes to Jay only

Two newsletters each Sunday (Jay, Oct 14, 2026):
  1. CHECK (Jay only): the beehiiv test of the real issue, plus the check email from this
     script: link results, numbers and flags. Nothing goes to subscribers without Jay's OK.
  2. ISSUE (all subscribers), deliberately short:
     - Subject "<dates>: Seattle 2 Week Playlist"
     - One intro line (top 3 songs per artist, in show order)
     - "All of Seattle" line + pink button
     - "Frelard" line (why it exists, in Jay's voice, no name) + pink button
     - One line linking a free tool to copy the playlists to other apps
     - Closing: all N shows on the site, the neighborhood ask, forward ask, sponsor line

--check-links tries each link over HTTP and records the result in the check email. The
Claude workspace usually can't reach these sites from the shell, so during the Sunday run
Claude opens each link in the browser instead and marks the results in the check email.
"""
import datetime as dt
import html
import json
import os
import sys
import urllib.request

SITE = "https://2weeksoundcheck.com/"
PINK = "#D6336C"
MUTED = "#5A6476"
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
DEFAULT_TRANSFER = "https://www.tunemymusic.com/transfer"


def rng(s, e):
    return f"{s:%b} {s.day}–{e.day}" if s.month == e.month else f"{s:%b} {s.day}–{e:%b} {e.day}"


def button(url, label):
    return (f'<p><a href="{html.escape(url)}" style="display:inline-block;background:{PINK};color:#ffffff;font-weight:700;'
            f'padding:10px 18px;border-radius:999px;text-decoration:none">{label}</a></p>')


def link(url, text, bold=False):
    t = f"<strong>{text}</strong>" if bold else text
    return f'<a href="{html.escape(url)}" style="color:{PINK}">{t}</a>'


def check(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (2 Week Soundcheck link check)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return "OK" if r.status < 400 else f"FAIL ({r.status})"
    except Exception as ex:  # network blocked or a real failure; Claude checks in the browser
        return f"not checked here ({type(ex).__name__}); open it in the browser"


def main(*args):
    flags = {a for a in args if a.startswith("--")}
    pos = [a for a in args if not a.startswith("--")]
    src = pos[0] if pos else "data/seattle.json"
    outdir = pos[1] if len(pos) > 1 else "issues"

    d = json.load(open(src))
    cfg = json.load(open("newsletter.json")) if os.path.exists("newsletter.json") else {}
    transfer = cfg.get("transfer_url") or DEFAULT_TRANSFER

    pl = d.get("playlist") or {}
    start = pl.get("start") or dt.date.today().isoformat()
    end = pl.get("end") or (dt.date.fromisoformat(start) + dt.timedelta(days=13)).isoformat()
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    dates = rng(s, e)
    shows = [x for x in d["events"] if start <= x["date"] <= end and x.get("status") != "cancelled"]
    n = len(shows)
    edition = d.get("edition", "Seattle")
    areas = {a: p for a, p in (d.get("area_playlists") or {}).items() if p.get("start") == start and p.get("url")}
    fr = areas.get("Frelard")
    warnings = []
    if not pl.get("url"):
        warnings.append("The Seattle playlist has no link for this window.")
    if not fr:
        warnings.append("No Frelard playlist for this window in playlists.json. Build it (PLAYLIST.md 4b) and rerun.")
    pers = {(p.get("per_artist") or 3) for p in [pl] + ([fr] if fr else [])}
    per = WORDS.get(pers.pop(), "") if len(pers) == 1 else ""  # only state a count when both playlists agree
    if not per:
        warnings.append("The two playlists use different songs-per-artist counts, so the intro leaves the count out.")

    subject = f"{dates}: {edition} 2 Week Playlist"
    preview_text = (f"Two new playlists for the next two weeks: all of {edition}, plus Frelard." if fr
                    else f"Songs from every headliner playing {edition} over the next two weeks.")

    # ---------- the subscriber issue ----------
    h, t = [], []
    count = f"top {per} " if per else "top "
    intro = (f"Two playlists for {dates}: the {count}songs from each artist, in show order."
             if fr else f"Every headliner playing {edition} {dates}: the {count}songs from each, in show order.")
    h.append(f"<p>{intro} Hit shuffle, and when something grabs you, go see it.</p>")
    t.append(intro + " Hit shuffle, and when something grabs you, go see it.\n")

    if pl.get("url"):
        h.append(f"<h3>All of {edition}</h3>")
        h.append(f"<p>{pl.get('songs')} songs from {pl.get('artists')} headliners across the city.</p>")
        h.append(button(pl["url"], f"▶ Listen to the {edition} playlist on Spotify"))
        t.append(f"ALL OF {edition.upper()}: {pl.get('songs')} songs from {pl.get('artists')} headliners across the city.\n{pl['url']}\n")
    if fr:
        why = ("I live in Ballard and want to go to more shows close to home, so this one covers "
               "the small rooms in Fremont and Ballard, openers included.")
        h.append("<h3>Frelard</h3>")
        h.append(f"<p>{why} {fr.get('songs')} songs from {fr.get('artists')} artists.</p>")
        h.append(button(fr["url"], "▶ Listen to the Frelard playlist on Spotify"))
        t.append(f"FRELARD: {why} {fr.get('songs')} songs from {fr.get('artists')} artists.\n{fr['url']}\n")

    # Genre playlists: each genre name links straight to its standing Spotify playlist (Jay, Oct 18, 2026),
    # so readers open Spotify without visiting the site. Text links in one line, not buttons.
    gps = d.get("genre_playlists") or []
    if gps:
        word = {7: "Seven"}.get(len(gps), str(len(gps)))
        h.append("<h3>Just want one genre?</h3>")
        h.append(f"<p>{word} genre playlists from the same shows, refreshed every Sunday. "
                 "Follow one on Spotify and it updates itself:</p>")
        h.append("<p>" + " &nbsp;·&nbsp; ".join(link(g["url"], g["genre"], bold=True) for g in gps) + "</p>")
        t.append(f"JUST WANT ONE GENRE? {word} genre playlists from the same shows, refreshed every Sunday. "
                 "Follow one on Spotify and it updates itself:\n"
                 + "\n".join(f"  {g['genre']}: {g['url']}" for g in gps) + "\n")
    h.append(f"<p>Not on Spotify? {link(transfer, 'Copy either playlist to Apple Music, YouTube Music and more, free →')}</p>")
    t.append(f"Not on Spotify? Copy either playlist to Apple Music, YouTube Music and more, free: {transfer}\n")

    h.append("<hr>")
    h.append(f'<p>{link(SITE, f"All {n} shows are on the site →", bold=True)}<br>'
             f'<span style="color:{MUTED}">Filter by date, neighborhood, venue or artist.</span></p>')
    h.append("<p>Want a playlist for your neighborhood next? Reply and tell us where.</p>")
    h.append(f"<p>Know someone who'd like this? Forward it to them. They can sign up at {link(SITE, '2weeksoundcheck.com')}.</p>")
    h.append(f'<p style="color:{MUTED}">Run a venue or local business? Sponsor an issue. Just reply to this email.</p>')
    t.append(f"All {n} shows are on the site. Filter by date, neighborhood, venue or artist: {SITE}\n")
    t.append("Want a playlist for your neighborhood next? Reply and tell us where.\n")
    t.append(f"Know someone who'd like this? Forward it to them. They can sign up at {SITE}\n")
    t.append("Run a venue or local business? Sponsor an issue. Just reply to this email.")

    os.makedirs(outdir, exist_ok=True)
    open(f"{outdir}/{start}.html", "w").write("\n".join(h) + "\n")
    open(f"{outdir}/{start}.txt", "w").write(f"Subject: {subject}\nPreview: {preview_text}\n\n" + "\n".join(t) + "\n")

    # ---------- the check email (Jay only) ----------
    links = [(f"{edition} playlist", pl.get("url")), ("Frelard playlist", fr and fr.get("url")),
             ("Copy-to-other-apps tool", transfer), ("Site", SITE)]
    links[2:2] = [(f"{g['genre']} playlist", g.get("url")) for g in gps]
    do_http = "--check-links" in flags
    c = [f"Subject: CHECK before sending: {subject}", "",
         "This is the pre-send check. The beehiiv test of the real issue arrives separately.",
         "Nothing goes to subscribers until you say OK.", "",
         "LINKS"]
    for label, url in links:
        if not url:
            c.append(f"  [MISSING] {label}")
        else:
            c.append(f"  [{check(url) if do_http else '  '}] {label}: {url}")
    c += ["", "NUMBERS",
          f"  Dates: {dates}",
          f"  Shows on the site in this window: {n}",
          f"  {edition}: {pl.get('songs', '?')} songs, {pl.get('artists', '?')} headliners, {pl.get('per_artist', '?')} per artist"]
    if fr:
        c.append(f"  Frelard: {fr.get('songs', '?')} songs, {fr.get('artists', '?')} artists, {fr.get('per_artist', '?')} per artist")
    for g in gps:
        stale = "" if g.get("start") == start else f"  [NOT REFRESHED: still {g.get('start')}]"
        c.append(f"  {g['genre']}: {g.get('songs', '?')} songs, {g.get('artists', '?')} artists{stale}")
    for name, p in (("Seattle", pl), ("Frelard", fr or {})):
        if p.get("skipped"):
            c.append(f"  {name} skipped (not on Spotify or ambiguous): {', '.join(p['skipped'])}")
    c += ["", "FLAGS"] + ([f"  - {w}" for w in warnings] or ["  None from the build. Add anything found in the run (failed venues, reports)."])
    c += ["", "SUBJECT AND PREVIEW", f"  {subject}", f"  {preview_text}", "",
          "Reply OK (or tell Claude in the chat) and it goes to subscribers."]
    open(f"{outdir}/{start}-check.txt", "w").write("\n".join(c) + "\n")

    print(f"Subject: {subject}")
    print(f"Preview text: {preview_text}")
    for w in warnings:
        print("WARNING:", w)
    print(f"wrote {outdir}/{start}.html, .txt and -check.txt")


if __name__ == "__main__":
    main(*sys.argv[1:])

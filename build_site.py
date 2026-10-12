#!/usr/bin/env python3
"""Build the 2 Week Soundcheck site data for one city edition.

Usage: python3 build_site.py [shows_dir] [playlist.json] [out.json]
Defaults: shows/  playlist.json  data/seattle.json

Reads the same shows/*.json the calendar feed uses, keeps today onward
(Pacific), splits headliner from support, labels each link as a ticket page
or an info page, and adds the current playlist + newsletter settings.
"""
import datetime as dt
import glob
import json
import re
import sys
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Los_Angeles")

VENUES = {
    "The Sunset Tavern": {"short": "Sunset Tavern", "hood": "Ballard", "site": "https://sunsettavern.com/"},
    "Tractor Tavern": {"short": "Tractor Tavern", "hood": "Ballard", "site": "https://tractortavern.com/"},
    "Conor Byrne Pub": {"short": "Conor Byrne", "hood": "Ballard", "site": "https://www.conorbyrnepub.com/"},
    "Hidden Hall": {"short": "Hidden Hall", "hood": "Fremont", "site": "https://www.hiddenhall.com/"},
    "Nectar Lounge": {"short": "Nectar Lounge", "hood": "Fremont", "site": "https://www.nectarlounge.com/"},
    "The Crocodile": {"short": "The Crocodile", "hood": "Belltown", "site": "https://www.thecrocodile.com/"},
    "Showbox at the Market": {"short": "Showbox", "hood": "Pike Place", "site": "https://www.showboxpresents.com/"},
    "Showbox SoDo": {"short": "Showbox SoDo", "hood": "SoDo", "site": "https://www.showboxpresents.com/"},
    "Benaroya Hall": {"short": "Benaroya Hall", "hood": "Downtown", "site": "https://www.benaroyahall.org/"},
    "WaMu Theater": {"short": "WaMu Theater", "hood": "SoDo", "site": "https://www.wamutheater.com/"},
    "Chateau Ste. Michelle": {"short": "Ste. Michelle", "hood": "Woodinville", "site": "https://www.ste-michelle.com/visit-us/summer-concerts"},
    "Dune Peninsula": {"short": "Dune Peninsula", "hood": "Tacoma", "site": "https://www.metroparkstacoma.org/"},
    "Climate Pledge Arena": {"short": "Climate Pledge Arena", "hood": "Seattle Center", "site": "https://climatepledgearena.com/events/"},
    "T-Mobile Park": {"short": "T-Mobile Park", "hood": "SoDo", "site": "https://www.mlb.com/mariners/tickets/concerts"},
}

TICKET_HOSTS = ("tixr.com", "ticketweb.com", "showboxpresents.com", "thecrocodile.com",
                "wamutheater.com", "tickpick.com", "gametime.co", "dice.fm", "axs.com",
                "ticketmaster.com", "etix.com", "seetickets", "venuepilot", "eventbrite",
                "seattlechambermusic.org", "seattlesymphony.org", "opendate", "climatepledgearena.com")

PRESENTER = re.compile(r"^(Showbox Presents|Hotel Crocodile Presents|Tractor Presents|KEXP Presents|KBCS Presents|Seattle Symphony)\s*:\s*", re.I)


def venue_key(ev):
    v, room = ev.get("venue", ""), ev.get("room") or ""
    if v == "The Showbox":
        return room if room in VENUES else "Showbox at the Market"
    for k in VENUES:
        if k.lower() in v.lower() or v.lower().startswith(k.lower().split(" at ")[0].lower()):
            return k
    return v


def split_title(title):
    t = title.strip()
    support = []
    m = re.search(r"\s*\(with ([^)]*)\)", t)
    if m:
        support = [s.strip() for s in re.split(r",\s*|\s+&\s+more$", m.group(1)) if s.strip() and s.strip() not in ("& more", "Special Guests")]
        t = (t[:m.start()] + t[m.end():]).strip()
    t = PRESENTER.sub("", t)
    return t, support


def main(src="shows", pl="playlist.json", out="data/seattle.json"):
    today = dt.datetime.now(TZ).date()
    events, seen = [], set()
    for f in sorted(glob.glob(f"{src}/*.json")):
        for ev in json.load(open(f)):
            try:
                d = dt.date.fromisoformat(ev["date"])
            except Exception:
                continue
            if d < today:
                continue
            key = venue_key(ev)
            title, support = split_title(ev["title"])
            k = (ev["date"], key, title.lower(), ev.get("start") or ev.get("doors") or "")
            if k in seen:
                continue
            seen.add(k)
            url = ev.get("url") or ""
            host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
            events.append({
                "date": ev["date"],
                "time": ev.get("start") or ev.get("doors"),
                "doors": ev.get("doors"),
                "title": title,
                "support": support,
                "venue": key,
                "status": (ev.get("status") or "").lower() or None,
                "url": url or VENUES.get(key, {}).get("site"),
                "link": "tickets" if any(h in host for h in TICKET_HOSTS) else "details",
            })
    events.sort(key=lambda e: (e["date"], e["time"] or "99", e["title"].lower()))
    try:
        playlist = json.load(open(pl))
    except FileNotFoundError:
        playlist = None
    data = {
        "brand": "2 Week Soundcheck",
        "edition": "Seattle",
        "generated": dt.datetime.now(TZ).isoformat(timespec="minutes"),
        "calendar": "webcal://jaystone9.github.io/seattle-shows/seattle-shows.ics",
        "newsletter": json.load(open("newsletter.json")) if glob.glob("newsletter.json") else {},
        "playlist": playlist,
        "venues": VENUES,
        "events": events,
    }
    import os
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(events)} upcoming events -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])

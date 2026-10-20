#!/usr/bin/env python3
"""Build the 2 Week Soundcheck site data for one city edition.

Usage: python3 build_site.py [shows_dir] [playlists.json] [out.json]
       python3 build_site.py --city chicago     (another edition; see cities.py)
Defaults: shows/  playlists.json  data/seattle.json
playlists.json is a list, newest first; the first entry is "this week's".

Reads the same shows/*.json the calendar feed uses, keeps today onward
(Pacific), splits headliner from support, labels each link as a ticket page
or an info page, and adds the current playlist + newsletter settings.
"""
import datetime as dt
import glob
import json
import os
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
    "Neumos": {"short": "Neumos", "hood": "Capitol Hill", "site": "https://www.neumos.com/"},
    "Barboza": {"short": "Barboza", "hood": "Capitol Hill", "site": "https://www.thebarboza.com/"},
    "Climate Pledge Arena": {"short": "Climate Pledge Arena", "hood": "Seattle Center", "site": "https://climatepledgearena.com/events/"},
    "T-Mobile Park": {"short": "T-Mobile Park", "hood": "SoDo", "site": "https://www.mlb.com/mariners/tickets/concerts"},
    "The Paramount Theatre": {"short": "Paramount", "hood": "Downtown", "site": "https://www.stgpresents.org/venues/paramount-theatre/"},
    "The Moore Theatre": {"short": "The Moore", "hood": "Belltown", "site": "https://www.stgpresents.org/venues/moore-theatre/"},
    "The Neptune Theatre": {"short": "The Neptune", "hood": "U District", "site": "https://www.stgpresents.org/venues/neptune-theatre/"},
    "The Vera Project": {"short": "Vera Project", "hood": "Seattle Center", "site": "https://theveraproject.org/"},
    "Black Lodge": {"short": "Black Lodge", "hood": "Eastlake", "site": "https://dice.fm/venue/the-black-lodge-qppa"},
    "Belltown Yacht Club": {"short": "Belltown Yacht Club", "hood": "Belltown", "site": "http://bycseattle.com/"},
    "Add-a-Ball": {"short": "Add-a-Ball", "hood": "Fremont", "site": "http://add-a-ball.com/"},
    "Substation": {"short": "Substation", "hood": "Fremont", "site": "https://substationseattle.com/"},
}

# Neighborhood -> area, for the area filter and area playlists. Frelard is the
# small-room heart of the project (Ballard + Fremont).
AREAS = {
    "Frelard": ["Ballard", "Fremont"],
    "Capitol Hill & Belltown": ["Capitol Hill", "Belltown", "Eastlake"],
    "Downtown & Seattle Center": ["Downtown", "Pike Place", "Seattle Center"],
    "U District": ["U District"],
    "SoDo": ["SoDo"],
    "Out of town": ["Woodinville", "Tacoma"],
}
# Genre playlists, in the order the chips appear. Slugs make shareable links: ?playlist=folk
GENRES = ["Pop", "Indie & Rock", "Folk & Country", "Electronic", "Hip-hop & R&B",
          "Punk & Metal", "Jazz, World & Classical"]
GENRE_SLUGS = {"Pop": "pop", "Indie & Rock": "indie", "Folk & Country": "folk", "Electronic": "electronic",
               "Hip-hop & R&B": "hip-hop", "Punk & Metal": "punk", "Jazz, World & Classical": "jazz"}

OTHER_GENRE = "Other / Local"  # in the genre window but no confirmed genre (yet)


def genre_names(title):
    """Names to look up in genres.json for a show title: the title, lineup.py's cleaned
    name, then each act of a co-bill ("A & B", "A x B", "A with B", "Fest: Headliner")."""
    from lineup import clean
    base = [title, clean(title)]
    if ": " in title:
        base.append(title.split(": ", 1)[1])
    out = []
    for n in base:
        out.append(n)
        for part in re.split(r"\s+(?:x|\+|with)\s+", n, flags=re.I):
            out.append(part)
            out += re.split(r"\s+&\s+", part)
    return [n.strip() for n in dict.fromkeys(out) if n.strip()]


def show_genres(title, confirmed):
    """Confirmed genres for a show; [] = Other / Local. The full name wins over its parts."""
    from lineup import clean
    for n in (title, clean(title)):
        if n.lower() in confirmed:
            return confirmed[n.lower()]
    found = []
    for n in genre_names(title):
        for g in confirmed.get(n.lower(), []):
            if g not in found:
                found.append(g)
    return [g for g in GENRES if g in found]


for _v in VENUES.values():
    _v["area"] = next((a for a, hoods in AREAS.items() if _v["hood"] in hoods), "Seattle")

TICKET_HOSTS = ("tixr.com", "ticketweb.com", "showboxpresents.com", "thecrocodile.com",
                "wamutheater.com", "tickpick.com", "gametime.co", "dice.fm", "axs.com",
                "ticketmaster.com", "etix.com", "seetickets", "venuepilot", "eventbrite",
                "seattlechambermusic.org", "seattlesymphony.org", "opendate", "climatepledgearena.com", "neumos.com", "thebarboza.com")

PRESENTER = re.compile(r"^(Showbox Presents|Hotel Crocodile Presents|Tractor Presents|KEXP Presents|KBCS Presents|Seattle Symphony)\s*:\s*", re.I)


def venue_key(ev):
    v, room = ev.get("venue", ""), ev.get("room") or ""
    if v == "The Showbox":
        return room if room in VENUES else "Showbox at the Market"
    if room == "Barboza":
        return "Barboza"
    for k in VENUES:
        if k.lower() in v.lower() or v.lower().startswith(k.lower().split(" at ")[0].lower()):
            return k
    return v


def split_title(title):
    t = title.strip()
    support = []
    m = re.search(r"\s*\(with ((?:[^()]|\([^()]*\))*)\)", t)  # allows one nested "(trio)"
    if m:
        support = [s.strip() for s in re.split(r",\s*|\s+&\s+more$", m.group(1)) if s.strip() and s.strip() not in ("& more", "Special Guests")]
        t = (t[:m.start()] + t[m.end():]).strip()
    t = PRESENTER.sub("", t)
    return t, support


CITY = None   # None = Seattle (root files); else a cities.CITIES entry


def path(name):
    """A per-city file (playlists.json, previews.json, ...): at the repo root for Seattle,
    in the city's folder otherwise. genres.json and contact.json are shared."""
    return f"{CITY['dir']}/{name}" if CITY else name


def use_city(slug):
    global CITY, VENUES, AREAS, TZ
    from cities import CITIES
    CITY = CITIES[slug]
    VENUES = {k: dict(v) for k, v in CITY["venues"].items()}
    AREAS = CITY["areas"]
    TZ = ZoneInfo(CITY["tz"])
    for v in VENUES.values():
        v["area"] = next((a for a, hoods in AREAS.items() if v["hood"] in hoods), CITY["name"])


def main(src="shows", pl="playlists.json", out="data/seattle.json"):
    if CITY:
        src, pl, out = path("shows"), path("playlists.json"), CITY["data"]
    today = dt.datetime.now(TZ).date()
    # Keep shows from the start of the current playlist window (e.g. last Sunday), so the
    # home page chart can still show the days that have already passed, muted.
    keep_from = today
    try:
        cur = next((p for p in json.load(open(pl)) if not p.get("area")), None)
        if cur and cur["start"] <= today.isoformat() <= cur["end"]:
            keep_from = dt.date.fromisoformat(cur["start"])
    except Exception:
        pass
    events, seen = [], set()
    for f in sorted(glob.glob(f"{src}/*.json")):
        for ev in json.load(open(f)):
            try:
                d = dt.date.fromisoformat(ev["date"])
            except Exception:
                continue
            if d < keep_from:
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
    # previews.json: {show title: {"artist": id, "track": id, "song": name}} for the next two weeks
    try:
        pv = json.load(open(path("previews.json")))
    except FileNotFoundError:
        pv = {}
    for e in events:
        p = pv.get(e["title"])
        if p and p.get("track"):
            e["preview"] = {"track": p["track"], "song": p.get("song")}
    # Genres (genres.json, confirmed each Sunday) for shows in the current playlist window only;
    # shows further out aren't reviewed yet, so they carry no "genres" key.
    try:
        confirmed = {k.lower(): v.get("genres") or [] for k, v in json.load(open("genres.json")).items()}
    except FileNotFoundError:
        confirmed = {}
    # A new edition gets genres only once its own genre playlists exist (i.e. its artists have
    # been through the Sunday genre review); before that most shows would wrongly read "Other / Local".
    try:
        if CITY and not json.load(open(path("genre_playlists.json"))):
            confirmed = {}
    except FileNotFoundError:
        confirmed = {}
    try:
        cur = next((p for p in json.load(open(pl)) if not p.get("area")), None)
        g_from, g_to = cur["start"], cur["end"]
        if g_to < today.isoformat():
            raise ValueError
    except Exception:
        g_from, g_to = today.isoformat(), (today + dt.timedelta(days=13)).isoformat()
    if confirmed:
        for e in events:
            if g_from <= e["date"] <= g_to:
                e["genres"] = show_genres(e["title"], confirmed)
    try:
        playlists = json.load(open(pl))
    except FileNotFoundError:
        playlists = []
    # Entries with an "area" (e.g. "Frelard") are area playlists; the rest are the citywide one.
    playlist = next((p for p in playlists if not p.get("area")), None)
    area_playlists = {}
    for p in playlists:
        if p.get("area") and p["area"] not in area_playlists:
            area_playlists[p["area"]] = p
    # Standing genre playlists (one per genre, same Spotify playlist refreshed each Sunday).
    # They live in their own file so they never become "this week's" playlist or enter the archive.
    try:
        gp = {p["genre"]: p for p in json.load(open(path("genre_playlists.json"))) if p.get("id")}
    except FileNotFoundError:
        gp = {}
    genre_playlists = [dict(gp[g], slug=GENRE_SLUGS[g]) for g in GENRES if g in gp]
    # Dated snapshot of each genre playlist per window (Jay, Oct 18, 2026), for the Playlists archive.
    # Kept apart from playlists.json so they never count as the citywide or an area playlist.
    try:
        genre_archive = json.load(open(path("genre_archive.json")))
    except FileNotFoundError:
        genre_archive = []
    order = {g: i for i, g in enumerate(GENRES)}
    genre_archive.sort(key=lambda p: (p["start"], -order.get(p["genre"], 99)), reverse=True)
    data = {
        "brand": "2 Week Soundcheck",
        "edition": CITY["name"] if CITY else "Seattle",
        "generated": dt.datetime.now(TZ).isoformat(timespec="minutes"),
        "calendar": f"webcal://2weeksoundcheck.com/{CITY['calendar_file'] if CITY else 'seattle-shows.ics'}",
        "newsletter": json.load(open(path("newsletter.json"))) if glob.glob(path("newsletter.json")) else {},
        "playlist": playlist,
        "playlists": playlists,
        "area_playlists": area_playlists,
        "genre_playlists": genre_playlists,
        "genre_archive": genre_archive,
        "areas": list(AREAS),
        "genres": [{"genre": g, "slug": GENRE_SLUGS[g]} for g in GENRES] + [{"genre": OTHER_GENRE, "slug": "other"}],
        "genre_window": [g_from, g_to],
        "contact": json.load(open("contact.json")) if glob.glob("contact.json") else {},
        "venues": VENUES,
        "events": events,
    }
    import os
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as fh:
        json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(events)} upcoming events -> {out}")
    city_pages()
    stamp_assets()


def city_picker():
    """The <select id="city"> options for every page: Seattle, then each other edition,
    linked once it's live and "coming soon" (disabled) until then."""
    from cities import CITIES
    opts = [("seattle", "Seattle", False)] + [(k, c["name"] if c["live"] else f"{c['name']} (coming soon)", not c["live"]) for k, c in CITIES.items()]
    return opts


def city_pages():
    """Write /<city>/index.html and /<city>/playlists.html from the Seattle pages, and keep the
    city picker on every page in sync with cities.py. Seattle's pages stay the templates, so a
    design change there reaches every edition on the next build."""
    from cities import CITIES
    opts = city_picker()

    def picker(html, current):
        body = "".join(f'\n        <option value="{k}"{" selected" if k == current else ""}{" disabled" if off else ""}>{label}</option>'
                       for k, label, off in opts)
        return re.sub(r'(<select id="city" aria-label="City">).*?(\s*</select>)', lambda m: m.group(1) + body + m.group(2), html, flags=re.S)

    for page in ("index.html", "playlists.html", "contact.html"):
        if glob.glob(page):
            html = open(page).read()
            new = picker(html, "seattle")
            if new != html:
                open(page, "w").write(new)

    for slug, c in CITIES.items():
        name = c["name"]
        for page in ("index.html", "playlists.html"):
            html = open(page).read()
            subs = [
                ("<body>", f'<body data-city="{slug}" data-tz="{c["tz"]}" data-data="../{c["data"]}">'),
                ('href="site.css', 'href="../site.css'),
                ('src="common.js', 'src="../common.js'),
                ('href="contact.html', 'href="../contact.html'),
                ('content="https://2weeksoundcheck.com/"', f'content="https://2weeksoundcheck.com/{slug}/"'),
                ('content="https://2weeksoundcheck.com/playlists.html"', f'content="https://2weeksoundcheck.com/{slug}/playlists.html"'),
                ("og-image.jpg", f"og-image-{slug}.jpg"),
                ("Seattle", name),
                ('const PL_AREAS = ["Frelard"];', f"const PL_AREAS = {json.dumps(c['area_playlists'])};"),
            ]
            for a, b in subs:
                html = html.replace(a, b)
            html = picker(html, slug)   # after the name swap, so the Seattle option keeps its label
            os.makedirs(slug, exist_ok=True)
            out = f"{slug}/{page}"
            if not glob.glob(out) or open(out).read() != html:
                open(out, "w").write(html)


def stamp_assets(pages=("index.html", "playlists.html", "contact.html"), assets=("site.css", "common.js")):
    """Add ?v=<content hash> to the shared CSS/JS links so browsers fetch new copies after each change."""
    import hashlib
    import re
    from cities import CITIES
    pages = list(pages) + [f"{k}/{p}" for k in CITIES for p in ("index.html", "playlists.html")]
    for page in pages:
        if not glob.glob(page):
            continue
        html = open(page).read()
        new = html
        for asset in assets:
            if not glob.glob(asset):
                continue
            v = hashlib.md5(open(asset, "rb").read()).hexdigest()[:8]
            new = re.sub(r'(["\'])((?:\.\./)?)' + re.escape(asset) + r'(\?v=[0-9a-f]+)?(["\'])', r"\g<1>\g<2>" + asset + "?v=" + v + r"\g<4>", new)
        if new != html:
            open(page, "w").write(new)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--city" in args:
        i = args.index("--city")
        use_city(args[i + 1])
        del args[i:i + 2]
    main(*args)

#!/usr/bin/env python3
"""Build seattle-shows.ics from shows/*.json.

Usage: python3 build_ics.py <shows_dir> <out.ics>
Each JSON file: array of {venue, room, title, date YYYY-MM-DD, doors HH:MM|null,
start HH:MM|null, url, status}. Times are America/Los_Angeles local.
UIDs are stable (venue+date+title) so weekly rebuilds update in place.
"""
import json, sys, glob, hashlib, datetime as dt

ADDR = {
    "The Sunset Tavern": "The Sunset Tavern, 5433 Ballard Ave NW, Seattle, WA 98107",
    "Tractor Tavern": "Tractor Tavern, 5213 Ballard Ave NW, Seattle, WA 98107",
    "Hidden Hall": "Hidden Hall, 400 N 35th St, Seattle, WA 98103",
    "Conor Byrne Pub": "Conor Byrne Pub, 5140 Ballard Ave NW, Seattle, WA 98107",
    "Nectar Lounge": "Nectar Lounge, 412 N 36th St, Seattle, WA 98103",
    "The Crocodile": "The Crocodile, 2505 1st Ave, Seattle, WA 98121",
    "Showbox at the Market": "The Showbox, 1426 1st Ave, Seattle, WA 98101",
    "Showbox SoDo": "Showbox SoDo, 1700 1st Ave S, Seattle, WA 98134",
    "Benaroya Hall": "Benaroya Hall, 200 University St, Seattle, WA 98101",
    "WaMu Theater": "WaMu Theater, 800 Occidental Ave S, Seattle, WA 98134",
    "Chateau Ste. Michelle": "Chateau Ste. Michelle, 14111 NE 145th St, Woodinville, WA 98072",
    "Dune Peninsula": "Dune Peninsula at Point Defiance Park, 5400 N Pearl St, Tacoma, WA 98407",
    "Neumos": "Neumos, 925 E Pike St, Seattle, WA 98122",
    "Barboza": "Barboza (downstairs at Neumos), 925 E Pike St, Seattle, WA 98122",
    "Climate Pledge Arena": "Climate Pledge Arena, 334 1st Ave N, Seattle, WA 98109",
    "T-Mobile Park": "T-Mobile Park, 1250 1st Ave S, Seattle, WA 98134",
}

VTZ = """BEGIN:VTIMEZONE
TZID:America/Los_Angeles
BEGIN:DAYLIGHT
TZOFFSETFROM:-0800
TZOFFSETTO:-0700
TZNAME:PDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0700
TZOFFSETTO:-0800
TZNAME:PST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE"""


def esc(s):
    return (str(s).replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    b = line.encode("utf-8")
    if len(b) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        c = ch.encode("utf-8")
        if len(cur) + len(c) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += c
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def address(ev):
    v, room = ev["venue"], ev.get("room")
    if v == "The Showbox" and room in ADDR:
        return ADDR[room]
    if room == "Barboza":
        return ADDR["Barboza"]
    for k, a in ADDR.items():
        if k.lower() in v.lower() or v.lower() in k.lower():
            return a
    return v


def main(src, out):
    events, seen = [], set()
    for f in sorted(glob.glob(f"{src}/*.json")):
        for ev in json.load(open(f)):
            try:
                d = dt.date.fromisoformat(ev["date"])
            except Exception:
                continue
            key = (ev["venue"].lower(), ev["date"], ev["title"].strip().lower(),
                   ev.get("start") or ev.get("doors") or "")
            if key in seen:
                continue
            seen.add(key)
            events.append((d, ev))
    events.sort(key=lambda x: (x[0], x[1].get("start") or x[1].get("doors") or ""))

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//Seattle Shows//EN",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:2 Week Soundcheck · Seattle",
         "X-WR-TIMEZONE:America/Los_Angeles",
         "X-WR-CALDESC:Concerts at Jay's favorite Seattle venues - refreshed weekly",
         "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:P1D", VTZ]
    for d, ev in events:
        uid = hashlib.sha1(f"{ev['venue']}|{ev['date']}|{ev['title']}|{ev.get('start') or ev.get('doors') or ''}"
                           .lower().encode()).hexdigest()[:20] + "@seattle-shows"
        venue = ev["venue"] + (f" – {ev['room']}" if ev.get("room") else "")
        status = (ev.get("status") or "").strip()
        summary = ev["title"].strip()
        if status:
            summary = f"[{status.upper()}] {summary}"
        summary += f" @ {(ev.get('room') or 'The Showbox') if ev['venue'] == 'The Showbox' else ('Barboza' if ev.get('room') == 'Barboza' else ev['venue'])}"
        desc = [f"Venue: {venue}"]
        if ev.get("doors"):
            desc.append(f"Doors: {ev['doors']}")
        if ev.get("start"):
            desc.append(f"Show: {ev['start']}")
        if not ev.get("doors") and not ev.get("start"):
            desc.append("Time not listed - check the venue")
        if ev.get("url"):
            desc.append(f"Tickets/info: {ev['url']}")
        L += ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{now}"]
        t = ev.get("start") or ev.get("doors")
        if t:
            hh, mm = (int(x) for x in t.split(":")[:2])
            s = dt.datetime(d.year, d.month, d.day, hh, mm)
            e = s + dt.timedelta(hours=3)
            L += [f"DTSTART;TZID=America/Los_Angeles:{s:%Y%m%dT%H%M%S}",
                  f"DTEND;TZID=America/Los_Angeles:{e:%Y%m%dT%H%M%S}"]
        else:
            L += [f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
                  f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}"]
        L += [f"SUMMARY:{esc(summary)}", f"LOCATION:{esc(address(ev))}",
              f"DESCRIPTION:{esc(chr(10).join(desc))}", "TRANSP:TRANSPARENT"]
        if ev.get("url"):
            L.append(f"URL:{ev['url']}")
        if status.lower() == "cancelled":
            L.append("STATUS:CANCELLED")
        L.append("END:VEVENT")
    L.append("END:VCALENDAR")
    with open(out, "w", newline="") as fh:
        fh.write("\r\n".join(fold(x) if "\n" not in x else "\r\n".join(fold(y) for y in x.split("\n")) for x in L) + "\r\n")
    print(f"{len(events)} events -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

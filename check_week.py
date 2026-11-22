#!/usr/bin/env python3
"""Weekly close-out check for 2 Week Soundcheck.

Answers one question: is this week actually finished for every city?
  python3 check_week.py                 check the week that started last Sunday (Pacific time)
  python3 check_week.py --week 2026-11-15
  python3 check_week.py --mark genres   record that the standing genre playlists were refreshed
  python3 check_week.py --mark sent:seattle      record a newsletter send (seattle, chicago, salt-lake)
  python3 check_week.py --mark skipped:seattle "reason"   record that Jay chose not to send

Exit code 0 = everything done, 1 = something is missing (each gap is printed on its own line).
Why this exists: on Nov 15, 2026 the Sunday steps were never run. The site kept the
Nov 8-21 playlists until Nov 17, the standing genre playlists kept last week's songs and
neither beehiiv issue was sent. Nothing flagged it. Run this at the end of every Sunday.
"""
import datetime, json, os, sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
CITIES = [("seattle", ""), ("chicago", "chicago"), ("salt-lake", "salt-lake")]
STATUS = os.path.join(ROOT, "weekly_status.json")


def last_sunday():
    today = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    return today - datetime.timedelta(days=(today.weekday() + 1) % 7)


def load(path, default=None):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def status():
    return load("weekly_status.json", {"weeks": {}})


def mark(week, what, note):
    s = status()
    w = s["weeks"].setdefault(week, {})
    today = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    if what == "genres":
        w["genres_refreshed"] = today
    elif what.startswith("sent:"):
        w.setdefault("sent", {})[what.split(":", 1)[1]] = today
    elif what.startswith("skipped:"):
        w.setdefault("sent", {})[what.split(":", 1)[1]] = "skipped " + today + (": " + note if note else "")
    else:
        sys.exit("unknown --mark value: " + what)
    with open(STATUS, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("recorded", what, "for week", week)


def venue_area_gaps():
    """Flag any venue whose hood isn't covered by any neighborhood group in AREAS, so a
    newly added venue doesn't silently fall back to the city-wide feed with no neighborhood
    playlist of its own (this is how Pioneer Square/Georgetown/Columbia City/Roosevelt were
    found ungrouped on Nov 22, 2026 -- fixed then, but nothing would have caught the next one)."""
    gaps = []
    import build_site as bs  # freshly imported: CITY is None, VENUES/AREAS are Seattle's own
    all_hoods = {h for hoods in bs.AREAS.values() for h in hoods}
    for name, v in bs.VENUES.items():
        if v["hood"] not in all_hoods:
            gaps.append(f"seattle: {name} (hood \"{v['hood']}\") isn't in any AREAS group in "
                        f"build_site.py -- add its hood to a group or create a new one")
    from cities import CITIES as CITY_DATA
    for slug, c in CITY_DATA.items():
        all_hoods = {h for hoods in c["areas"].values() for h in hoods}
        for name, v in c["venues"].items():
            if v["hood"] not in all_hoods:
                gaps.append(f"{slug}: {name} (hood \"{v['hood']}\") isn't in any AREAS group "
                            f"in cities.py -- add its hood to a group or create a new one")
    return gaps


def check(week):
    gaps = venue_area_gaps()
    for city, folder in CITIES:
        pl = load(os.path.join(folder, "playlists.json"), [])
        areas = {p.get("area") for p in pl}
        for area in sorted(areas, key=lambda a: a or ""):
            newest = next((p for p in pl if p.get("area") == area), None)
            if not newest or newest.get("start") != week:
                gaps.append(f"{city}: the {area or 'citywide'} playlist on file starts "
                            f"{newest.get('start') if newest else 'never'}, not {week} (prep branch not merged?)")
        for g in load(os.path.join(folder, "genre_playlists.json"), []):
            if g.get("start") != week:
                gaps.append(f"{city}: genre playlist {g.get('genre')} is dated {g.get('start')}, not {week}")
                break
        built = (load(f"data/{city}.json", {}).get("playlists") or [{}])[0].get("start")
        if built != week:
            gaps.append(f"{city}: the built site data shows a playlist starting {built}, not {week} "
                        f"(run build_site.py for this city and push)")
    w = status()["weeks"].get(week, {})
    if not w.get("genres_refreshed"):
        gaps.append("standing genre playlists on Spotify: no record of this week's refresh "
                    "(PLAYLIST.md step 4c, then: python3 check_week.py --mark genres)")
    for city, _ in CITIES:
        if not (w.get("sent") or {}).get(city):
            gaps.append(f"{city}: no record that this week's newsletter was sent "
                        f"(after sending: python3 check_week.py --mark sent:{city})")
    return gaps


def main():
    args = sys.argv[1:]
    week = last_sunday().isoformat()
    if "--week" in args:
        i = args.index("--week"); week = args[i + 1]; del args[i:i + 2]
    if "--mark" in args:
        i = args.index("--mark")
        mark(week, args[i + 1], " ".join(args[i + 2:]))
        return
    gaps = check(week)
    if gaps:
        print(f"NOT DONE for the week of {week}:")
        for g in gaps:
            print(" -", g)
        sys.exit(1)
    print(f"All done for the week of {week}: playlists, genre playlists, site and all three sends.")


if __name__ == "__main__":
    main()

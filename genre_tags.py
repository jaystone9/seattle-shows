#!/usr/bin/env python3
"""Turn Last.fm artist tags into 2 Week Soundcheck genres.

Input: a text file of Last.fm lookups, one line per artist:
    show name|looked-up name|Last.fm name|listeners|tag:count,tag:count,...
(made in the browser, since the workspace can't reach Last.fm; see GENRES.md).

Output: a proposal per artist, sorted into
    ok     clear tags and a big enough following that the match is safe
    check  clear tags, but a small following, so confirm it's the right artist
    flag   no tags, too few listeners, weak or mixed tags: Jay decides
Confirmed decisions live in genres.json; artists already there are skipped.

Usage: python3 genre_tags.py lookups.txt [--json]
"""
import json
import re
import sys

GENRES = ["Pop", "Indie & Rock", "Folk & Country", "Electronic", "Hip-hop & R&B",
          "Punk & Metal", "Funk & Blues", "Jazz, World & Classical"]

# A second genre is only allowed when it sits next to the first, so a folk
# listener never gets a hip-hop or electronic track from a crossover act.
NEIGHBORS = {
    "Pop": {"Indie & Rock", "Electronic", "Hip-hop & R&B"},
    "Indie & Rock": {"Pop", "Folk & Country", "Punk & Metal", "Electronic", "Funk & Blues"},
    "Folk & Country": {"Indie & Rock", "Jazz, World & Classical", "Funk & Blues"},
    "Electronic": {"Pop", "Indie & Rock", "Hip-hop & R&B"},
    "Hip-hop & R&B": {"Pop", "Electronic", "Jazz, World & Classical", "Funk & Blues"},
    "Punk & Metal": {"Indie & Rock"},
    "Funk & Blues": {"Indie & Rock", "Folk & Country", "Hip-hop & R&B", "Jazz, World & Classical"},
    "Jazz, World & Classical": {"Folk & Country", "Hip-hop & R&B", "Funk & Blues"},
}

EXACT = {
    "Pop": "pop synthpop synth-pop dance-pop electropop k-pop kpop pop rock teen pop power pop hyperpop art pop "
           "bedroom pop alternative pop country pop eurovision",
    "Indie & Rock": "indie indie rock indie pop rock alternative alternative rock shoegaze dream pop psychedelic "
                    "psychedelic rock garage rock classic rock hard rock lo-fi post-rock grunge britpop art rock math rock "
                    "noise rock surf rock surf slowcore jangle pop krautrock progressive rock blues rock southern rock "
                    "rock and roll rockabilly soft rock new wave post-punk twee noise pop chamber pop baroque pop "
                    "neo-psychedelia space rock heavy psych stoner rock melodic rock aor latin rock modern indie pop "
                    "roots rock art punk crank wave coldwave",
    "Folk & Country": "folk indie folk country americana alt-country alternative country singer-songwriter bluegrass "
                      "folk rock acoustic outlaw country country rock roots folk pop freak folk red dirt honky tonk "
                      "old-time anti-folk psychedelic folk experimental folk alt folk country soul",
    "Electronic": "electronic house techno dubstep edm drum and bass dnb bass trance electronica ambient idm deep house "
                  "tech house dance electro downtempo synthwave future bass riddim breakbeat uk garage trip-hop trip hop "
                  "progressive house melodic techno electro house big room hardstyle glitch hop chillwave "
                  "experimental electronic darkwave dark wave ebm dark techno vaporwave hypnagogic pop turntablism coldwave",
    "Hip-hop & R&B": "hip-hop hip hop rap rnb r&b soul neo-soul neo soul trap underground hip-hop underground rap "
                     "gangsta rap conscious hip hop alternative rnb contemporary r&b pop rap jazz rap detroit rap",
    "Punk & Metal": "punk punk rock hardcore hardcore punk metal heavy metal death metal black metal metalcore "
                    "post-hardcore emo pop punk thrash metal doom metal sludge sludge metal stoner metal grindcore ska "
                    "ska punk crust deathcore progressive metal progressive metalcore nu metal screamo melodic hardcore "
                    "metallic hardcore hair metal riot grrrl powerviolence",
    "Funk & Blues": "blues chicago blues electric blues delta blues soul blues modern blues classic blues "
                    "texas blues blues guitar harmonica blues funk p-funk funk rock jazz funk funk soul "
                    "new orleans funk boogaloo",
    "Jazz, World & Classical": "jazz classical world latin reggae afrobeat afrobeats bossa nova soundtrack orchestral "
                               "cumbia flamenco celtic opera contemporary classical fusion jazz fusion reggaeton salsa dub "
                               "bebop smooth jazz big band swing gospel choral baroque chamber music latin jazz mpb "
                               "mariachi dancehall new roots jazz hop saxophone",
}
TAG2G = {}


def _phrases(s):
    """Greedy split of a space-separated list into known tag phrases (longest first)."""
    words, out, i = s.split(), [], 0
    while i < len(words):
        for n in (4, 3, 2, 1):
            p = " ".join(words[i:i + n])
            if p in KNOWN or n == 1:
                out.append(p)
                i += n
                break
    return out


KNOWN = {
    "chicago blues", "electric blues", "delta blues", "soul blues", "modern blues", "classic blues", "texas blues",
    "blues guitar", "harmonica blues", "funk rock", "jazz funk", "funk soul", "new orleans funk",
    "dance-pop", "pop rock", "teen pop", "power pop", "art pop", "bedroom pop", "alternative pop", "country pop",
    "indie rock", "indie pop", "alternative rock", "dream pop", "psychedelic rock", "garage rock", "classic rock",
    "hard rock", "post-rock", "art rock", "math rock", "noise rock", "surf rock", "jangle pop", "progressive rock",
    "blues rock", "southern rock", "rock and roll", "soft rock", "new wave", "noise pop", "chamber pop", "baroque pop",
    "space rock", "heavy psych", "stoner rock", "melodic rock", "latin rock", "modern indie pop", "roots rock",
    "art punk", "crank wave", "indie folk", "alt-country", "alternative country", "folk rock", "outlaw country",
    "country rock", "folk pop", "freak folk", "red dirt", "honky tonk", "psychedelic folk", "experimental folk",
    "alt folk", "country soul", "drum and bass", "deep house", "tech house", "future bass", "uk garage", "trip hop",
    "progressive house", "melodic techno", "electro house", "big room", "glitch hop", "experimental electronic",
    "dark wave", "dark techno", "hypnagogic pop", "hip hop", "neo soul", "underground hip-hop", "underground rap",
    "gangsta rap", "conscious hip hop", "alternative rnb", "contemporary r&b", "pop rap", "jazz rap", "detroit rap",
    "punk rock", "hardcore punk", "heavy metal", "death metal", "black metal", "pop punk", "thrash metal",
    "doom metal", "sludge metal", "stoner metal", "ska punk", "progressive metal", "progressive metalcore", "nu metal",
    "melodic hardcore", "metallic hardcore", "hair metal", "riot grrrl", "bossa nova", "contemporary classical",
    "jazz fusion", "smooth jazz", "big band", "chamber music", "latin jazz", "new roots", "jazz hop",
}
for g, s in EXACT.items():
    for p in _phrases(s):
        TAG2G[p] = g

# Anything not listed exactly falls back to these word patterns.
PATTERNS = [
    (r"metal|hardcore|grind|punk", "Punk & Metal"),
    (r"folk|country|bluegrass|americana", "Folk & Country"),
    (r"house|techno|dubstep|trance|drum.?n.?bass|edm|electro", "Electronic"),
    (r"hip.?hop|\brap\b|r&b|rnb", "Hip-hop & R&B"),
    (r"blues|funk", "Funk & Blues"),
    (r"jazz|classical|reggae|latin|afro|orchestr", "Jazz, World & Classical"),
    (r"indie|rock|shoegaze|psych|grunge", "Indie & Rock"),
]
# Tags that aren't about the music (places, eras, "female vocalists"...) are ignored.


def genre_of(tag):
    if tag in TAG2G:
        return TAG2G[tag]
    for pat, g in PATTERNS:
        if re.search(pat, tag):
            return g
    return None


MIN_LISTENERS = 1000     # below this, Last.fm tags are too thin to trust
SAFE_LISTENERS = 25000   # below this, same-name mix-ups are common: confirm the match
MIN_SCORE = 60           # the top genre's tag weight must reach this
SECOND = 0.5             # a second genre needs half the top genre's weight


def propose(listeners, tags):
    """tags: [(name, count)]. Returns (status, genres, reason)."""
    if listeners < MIN_LISTENERS:
        return "flag", [], "few Last.fm listeners" if listeners else "not on Last.fm"
    score = {}
    for name, count in tags:
        if count < 10:
            continue
        g = genre_of(name)
        if g:
            score[g] = score.get(g, 0) + count
    if not score:
        return "flag", [], "no genre tags"
    ranked = sorted(score.items(), key=lambda x: -x[1])
    top_g, top = ranked[0]
    if top < MIN_SCORE:
        return "flag", [], "weak tags"
    close = [g for g, s in ranked[1:] if s >= top * SECOND]
    far = [g for g in close if g not in NEIGHBORS[top_g]]
    near = [g for g in close if g in NEIGHBORS[top_g]]
    genres = [top_g] + near[:1]
    if far and score[far[0]] >= top * 0.8:
        return "flag", [], "mixed: " + " / ".join([top_g] + far)
    status = "ok" if listeners >= SAFE_LISTENERS else "check"
    note = ("drops " + far[0]) if far else ""
    return status, genres, note


def main(path, as_json=False):
    try:
        known = json.load(open("genres.json"))
    except FileNotFoundError:
        known = {}
    rows = {}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        show, q, matched, listeners, tagstr = (line.split("|") + [""] * 5)[:5]
        tags = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in tagstr.split(",") if ":" in t]
        status, genres, reason = propose(int(listeners or 0), tags)
        rows.setdefault(show, []).append({"name": q, "lastfm": matched or None, "listeners": int(listeners or 0),
                                          "tags": [t for t, _ in tags[:4]], "status": status,
                                          "genres": genres, "reason": reason, "confirmed": q in known})
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    for st in ("ok", "check", "flag"):
        items = [(s, r) for s, rs in rows.items() for r in rs if r["status"] == st and not r["confirmed"]]
        print(f"\n== {st} ({len(items)})")
        for s, r in items:
            print(f"{r['name']:<34} {', '.join(r['genres']) or '-':<34} {r['listeners']:>9,}  {r['reason']}  [{', '.join(r['tags'])}]")


if __name__ == "__main__":
    main(sys.argv[1], "--json" in sys.argv)

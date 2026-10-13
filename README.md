# Seattle Shows

A calendar feed of concerts at Jay's favorite Seattle-area venues, six months out, refreshed weekly by a Claude scheduled task.

**Subscribe (iPhone):** webcal://2weeksoundcheck.com/seattle-shows.ics

Venues: The Sunset Tavern, Tractor Tavern, Hidden Hall, Conor Byrne Pub, Nectar Lounge, The Crocodile, The Showbox (Market + SoDo), Benaroya Hall, WaMu Theater, Chateau Ste. Michelle, Dune Peninsula at Point Defiance, Neumos + Barboza, Climate Pledge Arena, T-Mobile Park.

See `REFRESH.md` for how the weekly update works.

## 2 Week Soundcheck site
The public site (index.html + data/seattle.json) is the Seattle edition of 2 Week Soundcheck (target domain 2weeksoundcheck.com). Pages: index.html (shows, filters, previews), playlists.html (archive), contact.html (report a problem + contact; set `contact.json` form_endpoint or addresses to turn the forms on). `build_site.py` rebuilds the data from shows/, playlists.json and previews.json; `build_issue.py` drafts the weekly newsletter. Newsletter provider: beehiiv (set `newsletter.json` embed_url once the account exists).

**Neighborhoods:** `build_site.py` groups venues into areas (`AREAS`); the Shows page filters by area (`?area=frelard`). Frelard (Ballard + Fremont) also gets its own weekly playlist with openers included: `lineup.py --area Frelard` lists the acts, and playlists.json entries with `"area": "Frelard"` feed the site and newsletter.

# Seattle Shows

A calendar feed of concerts at Jay's favorite Seattle-area venues, six months out, refreshed weekly by a Claude scheduled task.

**Subscribe (iPhone):** webcal://2weeksoundcheck.com/seattle-shows.ics

Venues: The Sunset Tavern, Tractor Tavern, Hidden Hall, Conor Byrne Pub, Nectar Lounge, The Crocodile, The Showbox (Market + SoDo), Benaroya Hall, WaMu Theater, Chateau Ste. Michelle, Dune Peninsula at Point Defiance, Neumos + Barboza, Climate Pledge Arena, T-Mobile Park.

See `REFRESH.md` for how the weekly update works.

## 2 Week Soundcheck site
The public site is 2 Week Soundcheck (2weeksoundcheck.com). The homepage (index.html) is a city chooser, built from `templates/home.html` with each city's current playlist dates and its Sunday signup (a city switch that loads that city's beehiiv form, so signups land in the right segment). Each city has its own pages at /seattle/ and /chicago/ (index.html: shows, filters, previews; playlists.html: archive), all generated from `templates/shows.html` and `templates/playlists.html`: edit the templates, never the generated pages. contact.html (report a problem + contact) is shared. The root playlists.html and old filter links (?area=frelard etc.) forward to /seattle/. `build_site.py` rebuilds the data from shows/, playlists.json and previews.json and regenerates every page; `build_issue.py` drafts the weekly newsletter.

**Neighborhoods:** `build_site.py` groups venues into areas (`AREAS`); the Shows page filters by area (`?area=frelard`). Frelard (Ballard + Fremont) also gets its own weekly playlist with openers included: `lineup.py --area Frelard` lists the acts, and playlists.json entries with `"area": "Frelard"` feed the site and newsletter.

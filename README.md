# Seattle Shows

A calendar feed of concerts at Jay's favorite Seattle-area venues, six months out, refreshed weekly by a Claude scheduled task.

**Subscribe (iPhone):** webcal://jaystone9.github.io/seattle-shows/seattle-shows.ics

Venues: The Sunset Tavern, Tractor Tavern, Hidden Hall, Conor Byrne Pub, Nectar Lounge, The Crocodile, The Showbox (Market + SoDo), Benaroya Hall, WaMu Theater, Chateau Ste. Michelle, Dune Peninsula at Point Defiance, Climate Pledge Arena, T-Mobile Park.

See `REFRESH.md` for how the weekly update works.

## 2 Week Soundcheck site
The public site (index.html + data/seattle.json) is the Seattle edition of 2 Week Soundcheck (target domain 2weeksoundcheck.com). `build_site.py` rebuilds the data; `build_issue.py` drafts the weekly newsletter. Newsletter provider: beehiiv (set `newsletter.json` embed_url once the account exists).

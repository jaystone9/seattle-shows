# Weekly refresh procedure

Goal: keep `seattle-shows.ics` (subscribed on Jay's iPhone via
webcal://2weeksoundcheck.com/seattle-shows.ics) covering every
music event at the venues below from TODAY through TODAY + 6 months.

## Venues (one JSON file each in `shows/`)
| File | Venue | Where to look |
|---|---|---|
| sunset-tavern.json | The Sunset Tavern, Ballard | sunsettavern.com (DICE widget is unfetchable — use do206.com venue pages, Songkick, Tractor's TicketWeb for Tractor-presented shows) |
| tractor-tavern.json | Tractor Tavern, Ballard | tractortavern.com/calendar (single page, TicketWeb links) |
| hidden-hall.json | Hidden Hall, Fremont | hiddenhall.com calendar + "Just Announced" + Tixr event pages (main calendar page truncates ~Feb) |
| conor-byrne.json | Conor Byrne Pub, Ballard | site blocks fetches — use do206.com venue/day pages, Songkick, JamBase |
| nectar-lounge.json | Nectar Lounge, Fremont | nectarlounge.com calendar + Tixr (same system as Hidden Hall) |
| crocodile.json | The Crocodile (all rooms) | calendar.thecrocodile.com (one page; ignore its "Sold out" images — they're on every event) |
| showbox.json | Showbox at the Market + Showbox SoDo (room field) | showboxpresents.com calendar (load-more pages of 20) |
| benaroya-hall.json | Benaroya Hall (Taper Auditorium / Nordstrom Recital Hall) | official sites block fetches — use Bachtrack, ConcertFix, Songkick, seattlechambermusic.org; one entry per performance date |
| wamu-theater.json | WaMu Theater | wamutheater.com event calendar (ignore generic "This event Ended" banner) |
| chateau-ste-michelle.json | Chateau Ste. Michelle, Woodinville | ste-michelle.com summer concerts (lineup usually announced ~March) |
| neumos.json | Neumos (room null) + Barboza (room "Barboza"), Capitol Hill | neumos.com / thebarboza.com won't fetch; AXS venue pages (only first ~20 events show), Songkick ("Neumos", "Barboza", "Barboza at Neumos"), Do206, JamBase, ConcertFix |
| climate-pledge-arena.json | Climate Pledge Arena, Seattle Center | climatepledgearena.com/events (calendar only shows ~2 weeks and its next-page links won't fetch; use Songkick venue calendar + ConcertFix, AXS for ticket links). Skip Kraken/Torrent/Storm games, Dancing with the Stars, family shows |
| t-mobile-park.json | T-Mobile Park, SoDo | mlb.com/mariners/tickets/concerts + ballpark events calendar; stadium shows are usually announced in winter for the summer |
| dune-peninsula.json | Dune Peninsula, Point Defiance, Tacoma | Metro Parks Tacoma + Showbox Outdoor Concerts (summer series) |
| paramount-theatre.json | The Paramount Theatre, Downtown (STG) | STG's WordPress events feed filtered by venue (calendar pages show one month and won't page; stgpresents.org is blocked from the shell), then each STG event page for times/support/status. Drop the many non-concerts: Broadway, ballet/dance, comedy, podcasts, talks, film-with-orchestra nights, drag, holiday and tribute shows |
| moore-theatre.json | The Moore Theatre, Belltown (STG) | Same as Paramount |
| neptune-theatre.json | The Neptune Theatre, U District (STG) | Same as Paramount |
| vera-project.json | The Vera Project, Seattle Center (all ages) | PRIMARY SOURCE (Jay, Oct 15, 2026): theveraproject.org/events in the browser pane (the workspace sees a blank page; it's a DICE widget). Click LOAD MORE until it's gone; each card shows the venue (The Vera Project or The Black Lodge), date, time and a link.dice.fm link. Open each concert's DICE page and read its ld+json (description = full lineup, doorTime, eventStatus). Use the dice.fm/event/... URL. Do206 (do206.com/venues/the-vera-project) and Songkick venue 403 only fill gaps; they miss local bills (e.g. Sleevies, Oct 23, 2026 was only on DICE). Skip classes (LS/SP/CL/RS/DJ 101 etc.), screen-printing sessions, showcases, cover nights and benefits. Do206 lists Black Lodge shows under Vera: file "Black Lodge Presents" pages under Black Lodge |
| black-lodge.json | Black Lodge, 429 Eastlake Ave E (run by Vera; DIY, all ages) | PRIMARY SOURCE: the same theveraproject.org/events DICE list (cards marked The Black Lodge); open each DICE page for lineup/doors. Then Discotech (app.discotech.me/seattle/the-black-lodge), Songkick venue 883311, Bandsintown (headliners only; its 7pm times are unreliable, use null) to fill gaps. Not JamBase (wrong Black Lodge). Posts only a few weeks ahead. Skip comedy (e.g. Late Night w/ Chris Gethard) |
| belltown-yacht-club.json | Belltown Yacht Club, 2320 1st Ave (under Screwdriver) | Own site won't render; Do206 venue page + event pages, Songkick, JamBase, Bandsintown; tickets on DICE. Skip dance/DJ, trivia, film, market and theme nights |
| add-a-ball.json | Add-a-Ball, Fremont (pinball bar; shows Fri/Sat) | JamBase venue page + VenuePilot ticket pages (doors/start/lineups), Songkick. Skip pinball tournaments |
| substation.json | Substation, 645 NW 45th St (Fremont/Ballard line) | substationseattle.com homepage lists every upcoming event, each linked to Eventbrite; open each Eventbrite page for support, "Doors @ / Music @" times and status. Mostly electronic DJs/producers on tour plus indie/punk/metal bands. Skip dance battles, promoter takeovers and showcases with no named lineup, and podcast/comedy acts |

## Record format
`{"venue", "room" (or null), "title" ("Headliner (with Support, Support)"), "date" YYYY-MM-DD,
"doors" HH:MM|null, "start" HH:MM|null (24h Pacific), "url", "status" null|"sold out"|"cancelled"|"postponed"}`

GOAL (Jay, Oct 12): help people discover new music and go see real bands/artists. Keep: concerts by named artists, including named DJs/producers on their own tour, and classical concerts.
DROP themed/kitschy nights: tribute and cover acts ("X Tribute", "Music of X", "Celebrating X", "plays [album/cartoon]", Thankful Dead, Grateful Shred, Super Diamond...), theme/dance parties (Gimme Gimme Disco, Emo Nite, 90s/2000s nights, "X Night", Halloween/holiday parties), recurring jams/open mics/song shares/country & swing dance nights/square dances, showcases and benefits, holiday pops and family shows, movie nights.
CONCERTS ONLY (Jay, Oct 12): skip sports of any kind (Kraken, Storm, Torrent, Seahawks, Sounders, Mariners games, WWE/UFC, monster trucks), comedy, film screenings, podcasts, talks, trivia, drag and cabaret/reality-TV shows (e.g. Countess Luann), Dancing with the Stars, family/ice shows, conventions, events held at OTHER venues. No movie nights: skip film-with-live-orchestra screenings ("Elf in Concert", "Hook in Concert", Chaplin, etc.).
Never invent events — only what a listing shows. Drop events dated before today.
Keep titles/venue names identical week to week where the listing is unchanged (UIDs are derived from venue|date|title|time, so stable text = in-place updates on the phone, not duplicates).

## Steps
1. Re-collect each venue (parallel subagents are fine), overwrite `shows/<file>.json`.
2. `python3 build_ics.py shows seattle-shows.ics` and `python3 build_site.py` (rebuilds data/seattle.json for the 2 Week Soundcheck site)
3. Sanity check: event count within reason of last week (see `log.md`), file parses.
4. Append a line to `log.md`: date, total events, per-venue counts, notable gaps.
5. Commit and push to `main`. GitHub Pages republishes automatically.

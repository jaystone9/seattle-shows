# Weekly refresh: Chicago edition

Same rules as the Seattle `REFRESH.md` (record format, what to keep and drop, never invent
events, stable titles week to week). Times are 24h **Central** (America/Chicago).
Window: TODAY through TODAY + 6 months. One JSON file per venue in `chicago/shows/`.

## Venues
| File | Venue (exact `venue` value) | Where to look |
|---|---|---|
| empty-bottle.json | Empty Bottle, Ukrainian Village | emptybottle.com/shows loads by script; use the browser, Songkick, Do312. Its off-site series (e.g. Plantasia, Beyond the Gate) are real concerts but list them only if held at the Empty Bottle itself |
| subterranean.json | Subterranean, Wicker Park | subt.net (See Tickets). Many DJ/anime/themed raves, Broadway Rave, brunches: drop |
| sleeping-village.json | Sleeping Village, Avondale | site blocks fetches; browser, Songkick, Do312. Drop DJ nights |
| avondale-music-hall.json | Avondale Music Hall, Avondale | avondalemusichall.com (Eventim). Drop theme nights |
| color-club.json | Color Club, Avondale | lh-st.com listings / DICE venue page. Drop dance parties |
| concord-music-hall.json | Concord Music Hall, Logan Square | concordmusichall.com/calendar. EDM-heavy: keep named touring artists only, drop wrestling and festival days |
| outset.json | Outset, Bucktown | site blocks fetches; browser, Songkick. Mostly DJs: keep named touring artists only |
| metro.json | Metro, Wrigleyville | metrochicago.com (Etix). Drop Smart Bar club nights and author talks |
| schubas.json | Schubas, Lakeview | lh-st.com (shared with Lincoln Hall; filter by venue). Drop open mics, CHIRP listening bar, student showcases |
| lincoln-hall.json | Lincoln Hall, Lincoln Park | lh-st.com. Drop comedy, wrestling, DJ/baby-rave parties, book launches |
| the-vic.json | The Vic, Lakeview | victheatre.com blocks fetches; JAM/AXS, Songkick. Drop comedy and Brew & View movie nights |
| park-west.json | Park West, Lincoln Park | parkwestchicago.com / jamusa.com (AXS). Drop comedy, podcasts, karaoke |
| beat-kitchen.json | Beat Kitchen, Roscoe Village | beatkitchen.com (See Tickets). MANY tribute acts, comedy, brunch, podcasts, 80s/indie dance nights: drop all |
| martyrs.json | Martyrs', North Center | martyrslive.com calendar is often stale; use Songkick, Do312. Drop tribute bills |
| constellation.json | Constellation, Roscoe Village | constellation-chicago.com (See Tickets). Drop film nights |
| old-town-school.json | Old Town School of Folk Music, Lincoln Square | oldtownschool.org/concerts. Drop kids' concerts, sing-alongs, teen open mics, dance parties |
| kingston-mines.json | Kingston Mines, Lincoln Park | kingstonmines.com home page has a month-by-month Google Calendar widget (use the browser and click through the months; WebFetch fails). One entry per night: Main Stage act as headliner `(with <North Stage act>)`; skip acoustic pre-sets, "Band TBA" slots and closed nights. Drop Sunday nights (Mike Wheeler's weekly Sunday residency). Thu doors 18:00/start 19:30, Fri-Sat 19:00/21:00. Link the TicketWeb venue page. Added Oct 20, 2026 (tip from Jay's friend in Chicago) |
| bookclub.json | Bookclub, Lakeview | bookclubchi.com/events (browser); each event page lists the lineup and show time. Drop open mics, the "Headliners" comedy series, film festivals, DJ/costume/juke parties and fundraisers; keep artist showcases under the first-billed act. Added Oct 20, 2026 |
| wrigley-field.json | Wrigley Field, Wrigleyville | mlb.com/cubs/tickets/concerts. Summer only; usually announced in winter |
| green-mill.json | Green Mill, Uptown | greenmilljazz.com/calendar (cover at the door, link the calendar). FEATURED BOOKINGS ONLY (Jay, Oct 19, 2026): drop the weekly residency bands (Chicago Cellar Boys, Soul Message, Righteous Rooster Organ Trio, Joel Paterson & Friends, Chris Foreman, Alfonso Ponticelli, Alan Gresik's Swing Orchestra, Andy Brown's weekly set), the Sunday poetry slam and benefits |
| riviera.json | Riviera Theatre, Uptown | jamusa.com/riviera-theatre (AXS). Drop comedy and drag |
| aragon.json | Aragon Ballroom, Uptown | aragon.com / livenation.com. EDM-heavy: keep named touring artists |
| thalia-hall.json | Thalia Hall, Pilsen | thaliahallchicago.com/shows loads by script; browser, Songkick. Drop comedy, movie nights, DJ parties |
| radius.json | Radius, Pilsen | radius-chicago.com/events/all (WebFetch works; AXS ticket links; lists doors only, runs ~5 months out). Mostly electronic. Keep named DJs/producers; drop branded parties (Boots Halloween, Elrow, Boiler Room, F*CK FANTASM, M.E.A.T./Market Days). Added Oct 21, 2026 (Jay) |
| bottom-lounge.json | Bottom Lounge, West Loop | bottomlounge.com (Ticketweb) |
| cobra-lounge.json | Cobra Lounge, Near West Side | cobralounge.com/events often empty; Songkick, Do312, Bandsintown |
| hideout.json | Hideout, Goose Island | hideoutchicago.com (Opendate). Drop talks, political/community events, comedy |
| salt-shed.json | The Salt Shed, Goose Island | saltshedchicago.com loads by script; browser, Songkick, Live Nation |
| united-center.json | United Center, Near West Side | unitedcenter.com/events. Drop Bulls/Blackhawks, Disney on Ice, comedy, Wild 'N Out |
| chicago-theatre.json | The Chicago Theatre, The Loop | msg.com/the-chicago-theatre. Drop comedy, podcasts, speakers |
| auditorium-theatre.json | Auditorium Theatre, The Loop | auditoriumtheatre.org. Drop dance, speakers, film-with-orchestra |
| symphony-center.json | Symphony Center, The Loop | cso.org. Keep CSO/visiting concerts; drop film-with-orchestra and holiday family shows. One entry per performance date |
| house-of-blues.json | House of Blues Chicago, River North | houseofblues.com/chicago (Ticketmaster). Drop Gospel Brunch and cartoon-theme concerts |
| reggies.json | Reggies, South Loop | reggieslive.com (Ticketweb). MANY tributes, "classic albums" nights, comedy, bingo, karaoke, tailgates: drop all |
| buddy-guys-legends.json | Buddy Guy's Legends, South Loop | buddyguy.com/events (browser; Etix links, about 5 weeks out). Drop the weekly Wednesday "Host the Jam" nights. Buddy Guy's own January residency is announced in December on buddyguy.com/january-info (check the weekdays match the coming January; the page can show last year's dates). Added Oct 20, 2026 |
| jazz-showcase.json | Jazz Showcase, South Loop | jazzshowcase.com/calendar |
| soldier-field.json | Soldier Field, South Loop | soldierfield.com/events. Drop Bears/Fire games. Summer stadium shows only |
| huntington-bank-pavilion.json | Huntington Bank Pavilion, Northerly Island | huntingtonbankpavilion.com. Seasonal (about May to September) |
| pritzker-pavilion.json | Jay Pritzker Pavilion, The Loop | Millennium Park / Grant Park Music Festival. Summer only; drop film nights |
| space.json | SPACE, Evanston (North Suburbs) | evanstonspace.com loads by script; browser, Songkick. Out of Space / Cahn Auditorium shows only if held at SPACE itself |
| studio5.json | Studio5, Evanston | studio5.dance calendar is script-only; the real listing is the Ticket Tailor org page tickettailor.com/events/studio5performingartscenter. "Live at Studio5!" Friday jazz/world series, doors 30 min before; the season is posted a couple of months ahead. Drop Practical Theatre Company runs, readings and online streams. Added Oct 20, 2026 |
| north-shore-center.json | North Shore Center for the Performing Arts, Skokie | northshorecenter.org calendar is script-only (event pages /events/<year>/<slug> fetch fine); use the Do312 venue page (3 pages) and JamBase/Songkick. Rooms: George Van Dusen Theatre, North Theatre (room field when stated). Keep Music of the Baroque and named touring acts; drop musicals, kids' theatre runs, comedy, talks, dance, circus, holiday spectaculars and the NiteLite Presents tribute series. Added Oct 20, 2026 |
| skokie-theatre.json | Skokie Theatre, Skokie | now branded "The Skokie" (theskokie.com); listing on Ticket Tailor tickettailor.com/events/theskokie1. Almost all comedy, storytelling, classes, tributes and immersive theatre; about one real concert a season (annual Skokie Blues Revue in October). Added Oct 20, 2026; low yield |
| gorton-center.json | Gorton Center, Lake Forest | gortoncenter.org events list fetches (event pages can 429). "Rendezvous Arts" monthly Friday concert series is where the music is; tickets on CueBox. Drop sing-alongs, storytelling, comedy, dance, film, holiday shows, classes, drives. Added Oct 20, 2026 |
| genesee-theatre.json | Genesee Theatre, Waukegan | geneseetheatre.com/events/all (the plain /events page shows only 12); detail pages give doors. Ticketmaster. Drop comedy, mediums, tributes, Nutcracker, kids' shows, Ghost Wauk tours. Added Oct 20, 2026 |
| hey-nonny.json | Hey Nonny, Arlington Heights | heynonny.com/shows (paged ?516ba680_page=N; curl is blocked, WebFetch works). Opendate tickets; link the heynonny.com show page. Every card shows a "Sold out" badge image regardless, so ignore it. DROP the lounge residencies by title: "Social Sessions in the Lounge", "HeyDay Happy Hour", "Friday/Saturday in the Lounge with ..."; also Hey Comedy, First Person Live!, bingo and school fundraisers, Chris White Trio Charlie Brown programs, tributes. Added Oct 20, 2026 |
| metropolis.json | Metropolis Performing Arts Centre, Arlington Heights | metropolisarts.com/event/ (calendar is script-only; /event/page/N/ fetch). OvationTix. A community theatre: drop the Main Stage season, Family Series, school shows, Second City revues and the Artists Lounge Live tribute series; about one real concert a year (Creole Stomp). Added Oct 20, 2026; low yield |
| des-plaines-theatre.json | Des Plaines Theatre, Des Plaines | desplainestheatre.com WordPress feed wp-json/tribe/events/v1/events (paginates). Etix. Onesti-run and tribute-heavy: drop every "Bourbon 'N Brass" bar residency night (half the feed), "$1 Film Series", "VIP Upgrade" pseudo-events, films, film-with-orchestra, Wheel of Fortune Live, comedy, ventriloquists and all tribute acts. Added Oct 20, 2026 |
| rosemont-theatre.json | Rosemont Theatre, Rosemont | rosemont.com/theatre/event-calendar (single page). Ticketmaster; no doors published. Mostly Latin touring acts. Drop ballet, Riverdance, comedy and talk shows. Added Oct 20, 2026 |
| prairie-center.json | Prairie Center for the Arts, Schaumburg | prairiecenter.org blocks fetches; use the Do312 venue page, cross-check Songkick. OvationTix. Drop Nutcracker, holiday concerts, Thursday Night Laughs, youth orchestra recitals, magic, acrobats, tributes; 2-4 real concerts a year. Added Oct 20, 2026; low yield |
| fitzgeralds.json | FitzGerald's, Berwyn | fitzgeraldsnightclub.com (Ticketweb). Drop Moth StorySLAM and songwriter circles |
| ravinia.json | Ravinia, Highland Park (North Suburbs) | ravinia.org. Summer season plus occasional winter dates. Drop film-with-orchestra |
| allstate-arena.json | Allstate Arena, Rosemont (North Suburbs) | rosemont.com/allstate. Drop hockey, circus, family/Disney shows |
| credit-union-1-amphitheatre.json | Credit Union 1 Amphitheatre, Tinley Park | livenation.com venue page. Summer only |

**North Suburbs** (Jay, Oct 20, 2026, on a tip from his dad): the North Shore and northwest suburbs are their own neighborhood with an area playlist (headliners + openers), for readers in Deerfield, Highland Park, Northbrook, Arlington Heights etc. Durty Nellie's (Palatine) closed for good Oct 4, 2026 and was dropped.

**Weekly residencies** (the same act every week, e.g. Green Mill's house bands, Martyrs' Sunday Hoyle Brothers sets, Beat Kitchen's Monday Extraordinary Popular Delusions) are dropped everywhere (Jay, Oct 19, 2026). Multi-night runs by a featured artist (Jazz Showcase stands, CSO programs) and monthly series stay.

Do312 (do312.com) and Songkick venue pages are the best fallbacks when a venue site
won't load in the workspace. Use the venue's own ticket link as `url` whenever it exists.

## Steps
1. Re-collect each venue (parallel subagents are fine), overwrite `chicago/shows/<file>.json`.
2. `python3 build_ics.py chicago/shows chicago-shows.ics --city chicago` and
   `python3 build_site.py --city chicago`.
3. Sanity check counts against last week (`chicago/log.md`).
4. Append a line to `chicago/log.md`: date, total events, per-venue counts, notable gaps.
5. Commit and push to `main`.

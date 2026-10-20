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
| space.json | SPACE, Evanston | evanstonspace.com loads by script; browser, Songkick. Out of Space / Cahn Auditorium shows only if held at SPACE itself |
| fitzgeralds.json | FitzGerald's, Berwyn | fitzgeraldsnightclub.com (Ticketweb). Drop Moth StorySLAM and songwriter circles |
| ravinia.json | Ravinia, Highland Park | ravinia.org. Summer season plus occasional winter dates. Drop film-with-orchestra |
| allstate-arena.json | Allstate Arena, Rosemont | rosemont.com/allstate. Drop hockey, circus, family/Disney shows |
| credit-union-1-amphitheatre.json | Credit Union 1 Amphitheatre, Tinley Park | livenation.com venue page. Summer only |

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

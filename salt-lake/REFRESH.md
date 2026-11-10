# Salt Lake City venue refresh

Added Nov 10, 2026. 11 venues, one file each in `salt-lake/shows/`. Same content rules as the other cities
(concerts by real artists only; no comedy, tribute acts, theme or dance parties, film-with-orchestra nights,
showcases or benefits).

## Sources (all read in the browser; the workspace can't fetch them)
- **snspresents.com** (S&S Presents homepage): one long list covering Kilby Court, The Urban Lounge, Metro Music Hall
  (All Ages and 21+ rooms are one venue here), plus S&S shows at The Complex, The Depot, Soundwell and The Union.
  No door or show times on this page. Sold-out shows have no ticket link. Skip Ogden Amphitheater, Utah State
  Fairpark (Kilby Block Party), "Various Locations" (Golden Ticket).
- **thestateroompresents.com** iCal feeds: `/index.php?option=com_dpcalendar&task=ical.download&id=N` with
  15 = The State Room, 16 = The Commonwealth Room, 17 = Eccles Theater (Live at the Eccles: mostly comedy and
  film nights, drop those), 19 = Deer Valley (summer), 20 = Other Rooms (skip).
- **depotslc.com/shows**: JSON-LD events with start times and Ticketmaster links.
- **thecomplexslc.com/shows** (not /events, which returns 403): The Grand, Rockwell and The Lot are rooms of
  The Complex. Click "load more" until it's gone.
- **soundwellslc.com**: "Upcoming events" list with doors times.
- **deltacenter.com**: `/wp-json/wp/v2/mec-events?mec_category=28&per_page=100` lists concerts; each event page
  carries the date as JSON-LD `startDate`.

## Not yet covered
Seasonal rooms (Red Butte Garden, Utah First Credit Union Amphitheatre, Granary Live, Sandy Amphitheater, Deer
Valley), Maverik Center, Abravanel Hall, and smaller rooms (The DLC at Quarters, Aces High Saloon, The Beehive).

## Dropped on the first pass (Nov 10, 2026)
Depot: On Cinema, Gimme Gimme Disco, Rock Fight, Punchis Banda Rave, NYE Masquerade, Laura Clery, Watch What
Crappens, Red NOT Chili Peppers, Jordan Jensen, Fly Fishing Film Tour, Peter Antoniou. Eccles: every comedy,
"in Concert" film night, Cirque, Derek Hough, Price is Right, Roger Waters Presents Legacy (a Pink Floyd show).
State Room / Commonwealth: Petty Theft, Steely Dead, Wild Rumours, Jammy Buffet, The Songs of R.E.M., A Funky
Bluesy Christmas, KRCL's Anniversary Bash, RadioWest 25th, Bob Marley Birthday Bash. Complex: Legends, Jimmy
Failla, Desi Banks, Emo Night Karaoke, Dark Star Orchestra. Metro: Viva La Diva, Sappho's New Year's Ball, Blade
Rave, Broadway Rave, Alaska Thunderf*ck, Quake. Urban Lounge / Kilby: SLC Celebration of Electronic Music,
12 Bands of Christmas, Not Friendmas Eve, Gloss Haus, Localized. Delta Center: New Year's Eve Festival.

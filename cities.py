"""City editions other than Seattle.

Seattle keeps its data at the repo root (shows/, playlists.json, data/seattle.json); its
pages are generated at /seattle/ like every other city's, and the homepage lists every live city. Every other city lives in its own folder
(<slug>/shows/*.json, <slug>/playlists.json, ...) and is built with --city <slug>:

    python3 build_ics.py chicago/shows chicago-shows.ics --city chicago
    python3 build_site.py --city chicago

`live` controls the city picker: False shows "Chicago (coming soon)" and keeps the
/chicago/ pages out of the menu and off the homepage; True links them from every page.
"""

CHICAGO_VENUES = {
    # Wicker Park, Logan Square & Avondale
    "Empty Bottle": {"short": "Empty Bottle", "hood": "Ukrainian Village", "site": "https://www.emptybottle.com/"},
    "Subterranean": {"short": "Subterranean", "hood": "Wicker Park", "site": "https://subt.net/"},
    "Sleeping Village": {"short": "Sleeping Village", "hood": "Avondale", "site": "https://www.sleeping-village.com/"},
    "Avondale Music Hall": {"short": "Avondale Music Hall", "hood": "Avondale", "site": "https://avondalemusichall.com/"},
    "Color Club": {"short": "Color Club", "hood": "Avondale", "site": "https://dice.fm/venue/color-club-chicago"},
    "Concord Music Hall": {"short": "Concord Music Hall", "hood": "Logan Square", "site": "https://concordmusichall.com/"},
    "Outset": {"short": "Outset", "hood": "Bucktown", "site": "https://www.outsetchicago.com/"},
    # Lakeview, Lincoln Park & North Side
    "Metro": {"short": "Metro", "hood": "Wrigleyville", "site": "https://metrochicago.com/"},
    "Schubas": {"short": "Schubas", "hood": "Lakeview", "site": "https://lh-st.com/"},
    "Lincoln Hall": {"short": "Lincoln Hall", "hood": "Lincoln Park", "site": "https://lh-st.com/"},
    "The Vic": {"short": "The Vic", "hood": "Lakeview", "site": "https://www.victheatre.com/"},
    "Park West": {"short": "Park West", "hood": "Lincoln Park", "site": "https://www.parkwestchicago.com/"},
    "Beat Kitchen": {"short": "Beat Kitchen", "hood": "Roscoe Village", "site": "https://www.beatkitchen.com/"},
    "Martyrs'": {"short": "Martyrs'", "hood": "North Center", "site": "https://www.martyrslive.com/"},
    "Constellation": {"short": "Constellation", "hood": "Roscoe Village", "site": "https://www.constellation-chicago.com/"},
    "Old Town School of Folk Music": {"short": "Old Town School", "hood": "Lincoln Square", "site": "https://www.oldtownschool.org/concerts/"},
    "Kingston Mines": {"short": "Kingston Mines", "hood": "Lincoln Park", "site": "https://kingstonmines.com/"},
    "Bookclub": {"short": "Bookclub", "hood": "Lakeview", "site": "https://bookclubchi.com/events/"},
    "Wrigley Field": {"short": "Wrigley Field", "hood": "Wrigleyville", "site": "https://www.mlb.com/cubs/tickets/concerts"},
    # Uptown
    "Green Mill": {"short": "Green Mill", "hood": "Uptown", "site": "https://greenmilljazz.com/"},
    "Riviera Theatre": {"short": "Riviera", "hood": "Uptown", "site": "https://www.jamusa.com/venues/riviera-theatre"},
    "Aragon Ballroom": {"short": "Aragon", "hood": "Uptown", "site": "https://www.aragon.com/"},
    # West Loop, Pilsen & Near West
    "Thalia Hall": {"short": "Thalia Hall", "hood": "Pilsen", "site": "https://www.thaliahallchicago.com/"},
    "Bottom Lounge": {"short": "Bottom Lounge", "hood": "West Loop", "site": "https://bottomlounge.com/"},
    "Cobra Lounge": {"short": "Cobra Lounge", "hood": "Near West Side", "site": "https://www.cobralounge.com/"},
    "Hideout": {"short": "Hideout", "hood": "Goose Island", "site": "https://www.hideoutchicago.com/"},
    "The Salt Shed": {"short": "Salt Shed", "hood": "Goose Island", "site": "https://www.saltshedchicago.com/"},
    "United Center": {"short": "United Center", "hood": "Near West Side", "site": "https://www.unitedcenter.com/events/"},
    # Downtown & South Loop
    "The Chicago Theatre": {"short": "Chicago Theatre", "hood": "The Loop", "site": "https://www.msg.com/the-chicago-theatre"},
    "Auditorium Theatre": {"short": "Auditorium", "hood": "The Loop", "site": "https://www.auditoriumtheatre.org/"},
    "Symphony Center": {"short": "Symphony Center", "hood": "The Loop", "site": "https://cso.org/"},
    "House of Blues Chicago": {"short": "House of Blues", "hood": "River North", "site": "https://www.houseofblues.com/chicago"},
    "Reggies": {"short": "Reggies", "hood": "South Loop", "site": "https://www.reggieslive.com/"},
    "Buddy Guy's Legends": {"short": "Buddy Guy's", "hood": "South Loop", "site": "https://buddyguy.com/events/"},
    "Jazz Showcase": {"short": "Jazz Showcase", "hood": "South Loop", "site": "https://www.jazzshowcase.com/"},
    "Soldier Field": {"short": "Soldier Field", "hood": "South Loop", "site": "https://www.soldierfield.com/events"},
    "Huntington Bank Pavilion": {"short": "Huntington Bank Pavilion", "hood": "Northerly Island", "site": "https://www.huntingtonbankpavilion.com/"},
    "Jay Pritzker Pavilion": {"short": "Pritzker Pavilion", "hood": "The Loop", "site": "https://www.chicago.gov/city/en/depts/dca/supp_info/millennium_park.html"},
    # North suburbs (North Shore + northwest suburbs; Jay, Oct 20, 2026, on a tip from his dad)
    "SPACE": {"short": "SPACE", "hood": "Evanston", "site": "https://www.evanstonspace.com/"},
    "Studio5": {"short": "Studio5", "hood": "Evanston", "site": "https://www.studio5.dance/"},
    "North Shore Center for the Performing Arts": {"short": "North Shore Center", "hood": "Skokie", "site": "https://northshorecenter.org/"},
    "Skokie Theatre": {"short": "Skokie Theatre", "hood": "Skokie", "site": "https://skokietheatre.org/"},
    "Ravinia": {"short": "Ravinia", "hood": "Highland Park", "site": "https://www.ravinia.org/"},
    "Gorton Center": {"short": "Gorton Center", "hood": "Lake Forest", "site": "https://www.gortoncenter.org/"},
    "Genesee Theatre": {"short": "Genesee", "hood": "Waukegan", "site": "https://www.geneseetheatre.com/"},
    "Hey Nonny": {"short": "Hey Nonny", "hood": "Arlington Heights", "site": "https://heynonny.com/"},
    "Metropolis Performing Arts Centre": {"short": "Metropolis", "hood": "Arlington Heights", "site": "https://www.metropolisarts.com/"},
    "Des Plaines Theatre": {"short": "Des Plaines Theatre", "hood": "Des Plaines", "site": "https://www.desplainestheatre.com/"},
    "Rosemont Theatre": {"short": "Rosemont Theatre", "hood": "Rosemont", "site": "https://www.rosemont.com/theatre/"},
    "Allstate Arena": {"short": "Allstate Arena", "hood": "Rosemont", "site": "https://www.rosemont.com/allstate/"},
    "Durty Nellie's": {"short": "Durty Nellie's", "hood": "Palatine", "site": "https://www.durtynellies.com/"},
    "Prairie Center for the Arts": {"short": "Prairie Center", "hood": "Schaumburg", "site": "https://www.prairiecenter.org/"},
    # Out of town
    "FitzGerald's": {"short": "FitzGerald's", "hood": "Berwyn", "site": "https://www.fitzgeraldsnightclub.com/"},
    "Credit Union 1 Amphitheatre": {"short": "Credit Union 1 Amphitheatre", "hood": "Tinley Park", "site": "https://www.livenation.com/venue/KovZpZAE6eeA/credit-union-1-amphitheatre-events"},
}

CHICAGO_AREAS = {
    "Wicker Park & Logan Square": ["Ukrainian Village", "Wicker Park", "Bucktown", "Logan Square", "Avondale"],
    "Lakeview & North Side": ["Lakeview", "Wrigleyville", "Lincoln Park", "Roscoe Village", "North Center", "Lincoln Square"],
    "Uptown": ["Uptown"],
    "West Loop & Pilsen": ["West Loop", "Pilsen", "Goose Island", "Near West Side"],
    "Downtown & South Loop": ["The Loop", "River North", "South Loop", "Northerly Island"],
    "North suburbs": ["Evanston", "Skokie", "Highland Park", "Lake Forest", "Waukegan", "Arlington Heights",
                      "Des Plaines", "Rosemont", "Palatine", "Schaumburg"],
    "Out of town": ["Berwyn", "Tinley Park"],
}

# Street addresses for the calendar feed's LOCATION field.
CHICAGO_ADDR = {
    "Empty Bottle": "Empty Bottle, 1035 N Western Ave, Chicago, IL 60622",
    "Subterranean": "Subterranean, 2011 W North Ave, Chicago, IL 60647",
    "Sleeping Village": "Sleeping Village, 3734 W Belmont Ave, Chicago, IL 60618",
    "Avondale Music Hall": "Avondale Music Hall, 3336 N Milwaukee Ave, Chicago, IL 60641",
    "Color Club": "Color Club, 4146 N Elston Ave, Chicago, IL 60618",
    "Concord Music Hall": "Concord Music Hall, 2047 N Milwaukee Ave, Chicago, IL 60647",
    "Outset": "Outset, 1675 N Elston Ave, Chicago, IL 60642",
    "Metro": "Metro, 3730 N Clark St, Chicago, IL 60613",
    "Schubas": "Schubas Tavern, 3159 N Southport Ave, Chicago, IL 60657",
    "Lincoln Hall": "Lincoln Hall, 2424 N Lincoln Ave, Chicago, IL 60614",
    "The Vic": "The Vic Theatre, 3145 N Sheffield Ave, Chicago, IL 60657",
    "Park West": "Park West, 322 W Armitage Ave, Chicago, IL 60614",
    "Beat Kitchen": "Beat Kitchen, 2100 W Belmont Ave, Chicago, IL 60618",
    "Martyrs'": "Martyrs', 3855 N Lincoln Ave, Chicago, IL 60613",
    "Constellation": "Constellation, 3111 N Western Ave, Chicago, IL 60618",
    "Old Town School of Folk Music": "Old Town School of Folk Music, 4544 N Lincoln Ave, Chicago, IL 60625",
    "Kingston Mines": "Kingston Mines, 2548 N Halsted St, Chicago, IL 60614",
    "Bookclub": "Bookclub, 2871 N Lincoln Ave, Chicago, IL 60657",
    "Wrigley Field": "Wrigley Field, 1060 W Addison St, Chicago, IL 60613",
    "Green Mill": "Green Mill, 4802 N Broadway, Chicago, IL 60640",
    "Riviera Theatre": "Riviera Theatre, 4746 N Racine Ave, Chicago, IL 60640",
    "Aragon Ballroom": "Byline Bank Aragon Ballroom, 1106 W Lawrence Ave, Chicago, IL 60640",
    "Thalia Hall": "Thalia Hall, 1807 S Allport St, Chicago, IL 60608",
    "Bottom Lounge": "Bottom Lounge, 1375 W Lake St, Chicago, IL 60607",
    "Cobra Lounge": "Cobra Lounge, 235 N Ashland Ave, Chicago, IL 60607",
    "Hideout": "Hideout, 1354 W Wabansia Ave, Chicago, IL 60642",
    "The Salt Shed": "The Salt Shed, 1357 N Elston Ave, Chicago, IL 60642",
    "United Center": "United Center, 1901 W Madison St, Chicago, IL 60612",
    "The Chicago Theatre": "The Chicago Theatre, 175 N State St, Chicago, IL 60601",
    "Auditorium Theatre": "Auditorium Theatre, 50 E Ida B. Wells Dr, Chicago, IL 60605",
    "Symphony Center": "Symphony Center, 220 S Michigan Ave, Chicago, IL 60604",
    "House of Blues Chicago": "House of Blues Chicago, 329 N Dearborn St, Chicago, IL 60654",
    "Reggies": "Reggies, 2105 S State St, Chicago, IL 60616",
    "Buddy Guy's Legends": "Buddy Guy's Legends, 700 S Wabash Ave, Chicago, IL 60605",
    "Jazz Showcase": "Jazz Showcase, 806 S Plymouth Ct, Chicago, IL 60605",
    "Soldier Field": "Soldier Field, 1410 Special Olympics Dr, Chicago, IL 60605",
    "Huntington Bank Pavilion": "Huntington Bank Pavilion at Northerly Island, 1300 S Linn White Dr, Chicago, IL 60605",
    "Jay Pritzker Pavilion": "Jay Pritzker Pavilion, Millennium Park, 201 E Randolph St, Chicago, IL 60602",
    "SPACE": "SPACE, 1245 Chicago Ave, Evanston, IL 60202",
    "Studio5": "Studio5 Performing Arts Center, 1934 Dempster St, Evanston, IL 60202",
    "North Shore Center for the Performing Arts": "North Shore Center for the Performing Arts, 9501 Skokie Blvd, Skokie, IL 60077",
    "Skokie Theatre": "Skokie Theatre, 7924 Lincoln Ave, Skokie, IL 60077",
    "Ravinia": "Ravinia, 418 Sheridan Rd, Highland Park, IL 60035",
    "Gorton Center": "Gorton Center, 400 E Illinois Rd, Lake Forest, IL 60045",
    "Genesee Theatre": "Genesee Theatre, 203 N Genesee St, Waukegan, IL 60085",
    "Hey Nonny": "Hey Nonny, 10 S Vail Ave, Arlington Heights, IL 60005",
    "Metropolis Performing Arts Centre": "Metropolis Performing Arts Centre, 111 W Campbell St, Arlington Heights, IL 60005",
    "Des Plaines Theatre": "Des Plaines Theatre, 1476 Miner St, Des Plaines, IL 60016",
    "Rosemont Theatre": "Rosemont Theatre, 5400 N River Rd, Rosemont, IL 60018",
    "Allstate Arena": "Allstate Arena, 6920 Mannheim Rd, Rosemont, IL 60018",
    "Durty Nellie's": "Durty Nellie's, 180 N Smith St, Palatine, IL 60067",
    "Prairie Center for the Arts": "Prairie Center for the Arts, 201 Schaumburg Ct, Schaumburg, IL 60193",
    "FitzGerald's": "FitzGerald's, 6615 W Roosevelt Rd, Berwyn, IL 60402",
    "Credit Union 1 Amphitheatre": "Credit Union 1 Amphitheatre, 19100 S Ridgeland Ave, Tinley Park, IL 60477",
}

CITIES = {
    "chicago": {
        "name": "Chicago",
        "tz": "America/Chicago",
        "dir": "chicago",                    # shows/, playlists.json, ... live here
        "data": "data/chicago.json",
        "calendar_file": "chicago-shows.ics",
        "venues": CHICAGO_VENUES,
        "areas": CHICAGO_AREAS,
        "addr": CHICAGO_ADDR,
        "area_playlists": ["Wicker Park & Logan Square", "West Loop & Pilsen", "North suburbs"],   # Jay, Oct 19 / Oct 20, 2026: headliners + openers
        "live": True,
    },
}

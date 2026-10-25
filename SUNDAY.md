# Sunday run (2 Week Soundcheck · Seattle + Chicago)

Jay starts this in the "Seattle concerts" project on Sundays when he's at his computer
("run my Sunday Soundcheck" or "run my Seattle Shows playlist"). It replaces the old
Monday scheduled task, which is paused because unattended runs can't reach the venue sites.
Needs: the Claude desktop app open and in front (about 45–60 minutes), Spotify signed in
in its built-in browser, and Jay's Chrome (the one signed in to beehiiv and the hello@ webmail) connected.

Identity: commit as `Jayst0ne <jaystone9@users.noreply.github.com>`. Never put Jay's real
name or any personal email address in this public repo, the site, or the newsletter.

## Two cities, one newsletter (Jay, Oct 19, 2026)
Seattle and Chicago share ONE beehiiv publication, "2 Week Soundcheck". Readers are split by
which signup form they used: segment **"Seattle readers"** (the Seattle form, plus everyone who
signed up before Chicago) and segment **"Chicago readers"** (the Chicago form on /chicago/).
Each city gets its own issue, sent ONLY to its segment. Never send to All subscribers.
Segments refresh once a day, so click **Refresh segment** on both before sending.
Chicago follows the same steps as Seattle with `--city chicago` (see `chicago/REFRESH.md`).
Chicago has a citywide playlist, two neighborhood playlists (Wicker Park & Logan Square and West Loop &
Pilsen, headliners + openers, like Frelard) and 8 genre playlists (the usual 7 plus Funk & Blues) named `2 Week Soundcheck · Chicago · <Genre>` (dated copies:
`... · <Genre>: <Mon D>–<D>`), listed in `chicago/genre_playlists.json` / `chicago/genre_archive.json`.
`genres.json` is shared by both cities.

## Steps, in order
1. **Inbox check.** Open the hello@2weeksoundcheck.com webmail and look for FormSubmit
   "Report:" messages. Fix flagged listings in step 2 and tell Jay what changed.
2. **Refresh venues.** Follow `REFRESH.md`: re-collect all 22 venue files (today → +6 months),
   run `build_ics.py` and `build_site.py`, append to `log.md`, commit and push.
   Then Chicago: follow `chicago/REFRESH.md` (43 venue files in `chicago/shows/`; parallel
   subagents work well), run `python3 build_ics.py chicago/shows chicago-shows.ics --city chicago`
   and `python3 build_site.py --city chicago`, append to `chicago/log.md`, commit and push.
3. **Playlists.** Follow `PLAYLIST.md` steps 1–4b: build the Seattle Spotify playlist for
   today → today + 13 days, then the Frelard one (step 4b, headliners + openers), update `playlists.json` and `previews.json`, run
   `build_site.py`, commit and push. The site, calendar feed and Playlists archive update
   from this.
   Then the Chicago playlist: `python3 lineup.py --city chicago`, named
   `2 Week Soundcheck · Chicago: <Mon D>–<Mon D>`, added to the top of `chicago/playlists.json`;
   then the Wicker Park & Logan Square and West Loop & Pilsen ones (`lineup.py --city chicago --area "<name>"`;
   headliners + openers, `area` field set, as Frelard);
rewrite `chicago/previews.json`; `python3 build_site.py --city chicago`.
   Then the 7 genre playlists (`PLAYLIST.md` step 4c): look up new headliners on Last.fm,
   seed the Genre Review page, and once Jay has confirmed their genres there, refresh each
   genre playlist and update `genres.json` and `genre_playlists.json`, then save the week's
   dated copies to `genre_archive.json` (the Playlists page archive). Start the lookups early
   so Jay can review while the venue refresh runs. Do Seattle and Chicago genres as separate
   Genre Review weeks (`meta/current` = `seattle-<start>` then `chicago-<start>`; set `meta/current.genres` to the city's genre
   list so Seattle shows 7 chips and Chicago 8 with Funk & Blues); only
   research artists Jay leaves undecided, from the artist's own site or Spotify bio.
4. **Build the issue.** Run `python3 build_issue.py --check-links` (Seattle) and
   `python3 build_issue.py --city chicago --check-links` (Chicago; writes `chicago/issues/`).
   Build each as its own beehiiv post: subject `<dates>: Seattle 2 Week Playlist` /
   `<dates>: Chicago 2 Week Playlist`. The Chicago issue's neighborhood section is Wicker Park & Logan Square
   instead of Frelard. Seattle steps below; Chicago is the same. It writes
   `issues/<start>.html` (the issue), `.txt`, and `issues/<start>-check.txt` (the check email),
   and prints any warnings. Every issue has BOTH playlists; if it warns the Frelard one is
   missing, build it first. In beehiiv, create a blank post:
   - Title (subject): `<Mon D>–<D>: Seattle 2 Week Playlist`
   - Subtitle (preview): the preview text build_issue.py prints.
   - Content, in order, from `issues/<start>.html`:
     1. Intro line ("Two playlists for <dates>: the top three songs from every artist playing. When something grabs you, the show and its ticket link are on the site.")
     2. Heading "All of Seattle", its line, then a pink (#D6336C, bold) Button block
        "▶ Listen to the Seattle playlist on Spotify"
     3. Heading "Frelard", the "I live in Ballard..." line, then a Button
        "▶ Listen to the Frelard playlist on Spotify". Use Button blocks, never the generic
        link embed (it renders as a broken card).
     4. Heading "Just want one genre?", its line, then the 7 genres as Button blocks stacked in
        ONE column (never side-by-side columns: they squish on phones). Each button: size small,
        full width, pink #D6336C, white text, padding 10/12, label = genre name, linked to that
        genre's standing playlist in `genre_playlists.json` (Jay, Oct 18, 2026).
     5. The "Not on Spotify? Copy either playlist..." line, linked to `newsletter.json` `transfer_url`
     6. A divider, then: "All <N> shows are on the site →" (filter by date, neighborhood, venue
        or artist), the neighborhood ask ("Reply and tell us where"), the forward ask, and the
        sponsor line ("Sponsor an issue. Just reply to this email").
   - Post style (Style > Post > Link): links bold, not italic, not underlined, color #D6336C.
   - Author: the "2 Week Soundcheck" guest author only; byline hidden. No lyrics. Never Jay's name.
     Replacing the editor content can reset the title and authors, so re-check the header after edits.
5. **Check newsletter (Jay only).** Two things reach Jay before anything goes out:
   - The beehiiv **Send test** of the real issue, to hello@ (it lands in the webmail's Promotions tab).
     beehiiv tests can only go to hello@, so forward it to Jay from the webmail: open the message,
     click Forward, pick "Compose email with external images", click into the To field and confirm
     it has focus before typing (stray keystrokes trigger webmail shortcuts).
   - The **check email** from `issues/<start>-check.txt`, sent to Jay only (address in the private
     project notes and Claude's memory, never in this repo) via the Gmail connector. Before sending,
     open every link in the beehiiv test in the browser (both playlists, the copy tool, the site)
     and mark each ✓ or ✗ in the LINKS section; add any skipped artists, venues that failed to
     refresh, and reader reports under FLAGS.
6. **Send only with Jay's OK.** Send or schedule only after Jay says OK, in the chat or by
   replying to the check email. Never send without his explicit go-ahead. In beehiiv's send
   settings choose the segment, never All subscribers: the Seattle issue to "Seattle readers",
   the Chicago issue to "Chicago readers" (refresh both segments first). One check email per city.
   There is no separate playlist email any more; everyone else gets the newsletter as a subscriber.

## Already automatic
Playlist archive page, "updated" date on the site, iPhone calendar feed (from step 2),
signup form, and the beehiiv welcome email for new subscribers.

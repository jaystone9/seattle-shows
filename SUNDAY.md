# Sunday run (2 Week Soundcheck · Seattle)

Jay starts this in the "Seattle concerts" project on Sundays when he's at his computer
("run my Sunday Soundcheck" or "run my Seattle Shows playlist"). It replaces the old
Monday scheduled task, which is paused because unattended runs can't reach the venue sites.
Needs: the Claude desktop app open and in front (about 45–60 minutes), Spotify signed in
in its built-in browser, and Jay's Chrome (the one signed in to beehiiv and the hello@ webmail) connected.

Identity: commit as `Jayst0ne <jaystone9@users.noreply.github.com>`. Never put Jay's real
name or any personal email address in this public repo, the site, or the newsletter.

## Steps, in order
1. **Inbox check.** Open the hello@2weeksoundcheck.com webmail and look for FormSubmit
   "Report:" messages. Fix flagged listings in step 2 and tell Jay what changed.
2. **Refresh venues.** Follow `REFRESH.md`: re-collect all 22 venue files (today → +6 months),
   run `build_ics.py` and `build_site.py`, append to `log.md`, commit and push.
3. **Playlists.** Follow `PLAYLIST.md` steps 1–4b: build the Seattle Spotify playlist for
   today → today + 13 days, then the Frelard one (step 4b, headliners + openers), update `playlists.json` and `previews.json`, run
   `build_site.py`, commit and push. The site, calendar feed and Playlists archive update
   from this.
4. **Build the issue.** Run `python3 build_issue.py --check-links`. It writes
   `issues/<start>.html` (the issue), `.txt`, and `issues/<start>-check.txt` (the check email),
   and prints any warnings. Every issue has BOTH playlists; if it warns the Frelard one is
   missing, build it first. In beehiiv, create a blank post:
   - Title (subject): `<Mon D>–<D>: Seattle 2 Week Playlist`
   - Subtitle (preview): the preview text build_issue.py prints.
   - Content, in order, from `issues/<start>.html`:
     1. Intro line ("Two playlists for <dates>: the top three songs from each artist, in show order...")
     2. Heading "All of Seattle", its line, then a pink (#D6336C, bold) Button block
        "▶ Listen to the Seattle playlist on Spotify"
     3. Heading "Frelard", the "I live in Ballard..." line, then a Button
        "▶ Listen to the Frelard playlist on Spotify". Use Button blocks, never the generic
        link embed (it renders as a broken card).
     4. The "Not on Spotify? Copy either playlist..." line, linked to `newsletter.json` `transfer_url`
     5. A divider, then: "All <N> shows are on the site →" (filter by date, neighborhood, venue
        or artist), the neighborhood ask ("Reply and tell us where"), the forward ask, and the
        sponsor line ("Sponsor an issue. Just reply to this email").
   - Author: the "2 Week Soundcheck" guest author only; byline hidden. No lyrics. Never Jay's name.
5. **Check newsletter (Jay only).** Two things reach Jay before anything goes out:
   - The beehiiv **Send test** of the real issue, to hello@ (it lands in the webmail's Promotions tab).
   - The **check email** from `issues/<start>-check.txt`, sent to Jay only (address in the private
     project notes and Claude's memory, never in this repo) via the Gmail connector. Before sending,
     open every link in the beehiiv test in the browser (both playlists, the copy tool, the site)
     and mark each ✓ or ✗ in the LINKS section; add any skipped artists, venues that failed to
     refresh, and reader reports under FLAGS.
6. **Send only with Jay's OK.** Send or schedule to subscribers only after Jay says OK, in the
   chat or by replying to the check email. Never send to the list without his explicit go-ahead.
   There is no separate playlist email any more; everyone else gets the newsletter as a subscriber.

## Already automatic
Playlist archive page, "updated" date on the site, iPhone calendar feed (from step 2),
signup form, and the beehiiv welcome email for new subscribers.

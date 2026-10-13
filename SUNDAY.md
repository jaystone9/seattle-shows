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
2. **Refresh venues.** Follow `REFRESH.md`: re-collect all 21 venue files (today → +6 months),
   run `build_ics.py` and `build_site.py`, append to `log.md`, commit and push.
3. **Playlists.** Follow `PLAYLIST.md` steps 1–4b: build the Seattle Spotify playlist for
   today → today + 13 days, then the Frelard one (step 4b, headliners + openers), update `playlists.json` and `previews.json`, run
   `build_site.py`, commit and push. The site, calendar feed and Playlists archive update
   from this.
4. **Newsletter draft.** Run `python3 build_issue.py` for the subject, preview text and
   show count. In beehiiv, create a blank post:
   - Title (subject): `<Mon D>–<D>: Seattle 2 Week Playlist`
   - Subtitle (preview): `<songs> songs from the <artists> headliners playing Seattle over the next two weeks.`
   - Intro line, then a pink (#D6336C, bold) Button block "▶ Listen to the playlist on Spotify"
     linking to the playlist (don't use the generic link embed; it renders as a broken card),
     then the Frelard line and a second pink Button "▶ Listen to the Frelard playlist"
     (build_issue.py drafts both), then the closing link "All <N> shows are on the site →" with
     "Searchable by venue and artist, with tickets and a preview for every headliner."
   - Author: the "2 Week Soundcheck" guest author only; byline hidden. No lyrics.
   - Send a test to hello@ (it lands in the webmail's Promotions tab) and check it.
5. **Send only with Jay's OK.** Show Jay the test, then send or schedule to subscribers only
   after he says to. Never send to the list without his explicit go-ahead.
6. **Email Jay and Eric** the playlist per `PLAYLIST.md` step 6.

## Already automatic
Playlist archive page, "updated" date on the site, iPhone calendar feed (from step 2),
signup form, and the beehiiv welcome email for new subscribers.

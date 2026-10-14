# Sunday playlist procedure (run when Jay asks)

Part of the Sunday run: see SUNDAY.md for the full order (inbox check, venue refresh, this playlist, newsletter).

Jay prompts this manually each Sunday ("run my Seattle Shows playlist"). Do not email until the playlist is fully built. This needs the desktop app's built-in browser: a cloud-only session (e.g. one started by the weekly scheduled task) can't do it, and the Spotify connector can't build multi-artist playlists.

1. Window: today through today + 13 days.
2. Headliners: from `shows/*.json` in this repo, take each event in the window that isn't cancelled/postponed, and use the headliner only (title text before " (with", " w/", " with", or a ":" tour suffix). Skip themed nights, DJ parties, tribute acts, open mics, showcases, jams, dance nights. Deduplicate and keep show-date order.
3. Build the playlist in the Spotify web player (open.spotify.com) in the Claude desktop app's built-in browser, where Jay is signed in:
   - Create a new playlist named `2 Week Soundcheck · Seattle: <Mon D>–<Mon D>` (brand is city-neutral; Seattle is the first edition).
   - For each headliner: open their artist page, take the first 3 songs under "Popular" (Jay, Oct 13, 2026: 3 per artist now that there are 21 venues; it was 5 before), add them to the playlist. If the artist isn't on Spotify or the match is ambiguous, skip and note it.
   - The Spotify connector's generate_playlist can't do exact track lists — don't use it.
   - What worked (Oct 7, 2026 run): in page JS, navigate with history.pushState + popstate (no reloads) to `/search/<name>/artists`, take the artist link whose normalized text matches the name exactly, then read the first 3 `[data-testid="tracklist-row"]` track links on the artist page. Then on the playlist page, for each track, set the "Search for songs or episodes" input (native value setter + input event) to "<title> <artist>" and click `[data-testid="add-to-playlist-button"]` in the result row whose artist link matches. Run loops in the background (javascript_tool calls cap at 45s) and poll `window.__log`. Pasting links and URL search do not work in the web player.
   - Keep the Claude desktop window in front: when the pane is hidden, timers throttle to ~1/min. ~426 tracks took ~15 minutes visible.
4. Add the new playlist to the TOP of `playlists.json` (name, id, url, start, end, songs, artists, per_artist: 3); older entries stay, so the site's Playlists page keeps the archive.
   Also rewrite `previews.json`: for every show in the window, `{"<show title as in data/seattle.json>": {"artist": id, "track": id of the artist's #1 Popular song, "song": name, "name": search name}}`. You already open each artist page while building the playlist, so take the first track there. This powers the Preview buttons in "The next two weeks".
   Run `python3 build_site.py`, commit and push.
4b. **Frelard playlist** (Ballard + Fremont small rooms: Sunset, Tractor, Conor Byrne, Hidden Hall, Nectar, Add-a-Ball). Build it right after the Seattle one, same window:
   - Run `python3 lineup.py --area Frelard` (add `--json` for a machine-readable list; `--start YYYY-MM-DD` for a window that began earlier, e.g. building Sunday's playlist mid-week). It lists every headliner AND opener at the Frelard venues, with names already cleaned for search. The openers are the point: small rooms are where the discovery is.
   - Create a second playlist named `2 Week Soundcheck · Frelard: <Mon D>–<Mon D>`. Same web-player method as step 3: every act gets its first 3 Popular songs (reuse the headliners' songs you just collected for the Seattle playlist). Never more than 3 per artist in either playlist. Skip anyone not on Spotify or ambiguous (common for local openers, and for very common names) and note them. A bill like "A x B" is two artists; search each.
   - Add it to the TOP of `playlists.json` with `"area": "Frelard"` (name, id, url, start, end, songs, artists, per_artist: 3, area). The site picks the newest entry per area: the Shows page's "Frelard" tab and `?area=frelard` link, the Playlists archive tag, and the newsletter's Frelard button all come from it. The citywide entry stays the one without `area`.
   - Run `python3 build_site.py`, commit and push.
5. Run `python3 build_issue.py` to draft the newsletter issue (issues/<start>.html to paste into beehiiv; subject and preview text are printed). Keep it short. Never quote lyrics.
6. No separate playlist email (Jay, Oct 14, 2026). The links, counts and skipped artists go into the Jay-only check email (`SUNDAY.md` step 5); everyone else gets the newsletter as a subscriber.

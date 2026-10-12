# Sunday playlist procedure (run when Jay asks)

Jay prompts this manually each Sunday ("run my Seattle Shows playlist"). Do not email until the playlist is fully built. This needs the desktop app's built-in browser: a cloud-only session (e.g. one started by the weekly scheduled task) can't do it, and the Spotify connector can't build multi-artist playlists.

1. Window: today through today + 13 days.
2. Headliners: from `shows/*.json` in this repo, take each event in the window that isn't cancelled/postponed, and use the headliner only (title text before " (with", " w/", " with", or a ":" tour suffix). Skip themed nights, DJ parties, tribute acts, open mics, showcases, jams, dance nights. Deduplicate and keep show-date order.
3. Build the playlist in the Spotify web player (open.spotify.com) in the Claude desktop app's built-in browser, where Jay is signed in:
   - Create a new playlist named `Seattle Shows: <Mon D>–<Mon D>`.
   - For each headliner: open their artist page, take the first 5 songs under "Popular", add them to the playlist. If the artist isn't on Spotify or the match is ambiguous, skip and note it.
   - The Spotify connector's generate_playlist can't do exact track lists — don't use it.
   - What worked (Oct 7, 2026 run): in page JS, navigate with history.pushState + popstate (no reloads) to `/search/<name>/artists`, take the artist link whose normalized text matches the name exactly, then read the first 5 `[data-testid="tracklist-row"]` track links on the artist page. Then on the playlist page, for each track, set the "Search for songs or episodes" input (native value setter + input event) to "<title> <artist>" and click `[data-testid="add-to-playlist-button"]` in the result row whose artist link matches. Run loops in the background (javascript_tool calls cap at 45s) and poll `window.__log`. Pasting links and URL search do not work in the web player.
   - Keep the Claude desktop window in front: when the pane is hidden, timers throttle to ~1/min. ~426 tracks took ~15 minutes visible.
4. When the playlist is complete, email Jay at [address removed] and Eric Rue at [address removed] (both in To) via the Gmail connector:
   - Subject: `Seattle Shows playlist: <date range>`
   - Body: playlist link, then the day-by-day lineup (date, headliner, venue), then any skipped artists.

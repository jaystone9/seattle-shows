# Sunday playlist procedure (run when Jay asks)

Jay prompts this manually each Sunday ("run my Seattle Shows playlist"). Do not email until the playlist is fully built.

1. Window: today through today + 13 days.
2. Headliners: from `shows/*.json` in this repo, take each event in the window that isn't cancelled/postponed, and use the headliner only (title text before " (with", " w/", " with", or a ":" tour suffix). Skip themed nights, DJ parties, tribute acts, open mics, showcases, jams, dance nights. Deduplicate and keep show-date order.
3. Build the playlist in the Spotify web player (open.spotify.com) in the Claude desktop app's built-in browser, where Jay is signed in:
   - Create a new playlist named `Seattle Shows: <Mon D>–<Mon D>`.
   - For each headliner: open their artist page, take the first 5 songs under "Popular", add them to the playlist. If the artist isn't on Spotify or the match is ambiguous, skip and note it.
   - The Spotify connector's generate_playlist can't do exact track lists — don't use it.
4. When the playlist is complete, email Jay at [address removed] via the Gmail connector:
   - Subject: `Seattle Shows playlist: <date range>`
   - Body: playlist link, then the day-by-day lineup (date, headliner, venue), then any skipped artists.

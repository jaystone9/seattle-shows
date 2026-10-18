# Sunday playlist procedure (run when Jay asks)

Part of the Sunday run: see SUNDAY.md for the full order (inbox check, venue refresh, this playlist, newsletter).

Jay prompts this manually each Sunday ("run my Seattle Shows playlist"). Do not email until the playlist is fully built. This needs the desktop app's built-in browser: a cloud-only session (e.g. one started by the weekly scheduled task) can't do it, and the Spotify connector can't build multi-artist playlists.

1. Window: today through today + 13 days.
2. Headliners: from `shows/*.json` in this repo, take each event in the window that isn't cancelled/postponed, and use the headliner only (title text before " (with", " w/", " with", or a ":" tour suffix). Skip themed nights, DJ parties, tribute acts, open mics, showcases, jams, dance nights. Deduplicate and keep show-date order.
3. Build the playlist with the **playlist builder** (set up Oct 14, 2026), in the Claude desktop app's built-in browser, where Jay is signed in to Spotify as Jayst0ne:
   - Playlist name: `2 Week Soundcheck · Seattle: <Mon D>–<Mon D>` (brand is city-neutral; Seattle is the first edition).
   - Each headliner gets the first 3 songs under "Popular" on their artist page (Jay, Oct 13, 2026: 3 per artist; it was 5 before). If the artist isn't on Spotify or the match is ambiguous, skip and note it.
   - **How it works.** Spotify app "2 Week Soundcheck playlist builder" (developer.spotify.com, owned by Jayst0ne, development mode, client id `263893bd4f2d4e5080cb0c67f18bdb92`, redirect https://2weeksoundcheck.com/tools/playlist.html). The page `tools/playlist.html` (noindex, not linked) does Spotify sign-in (PKCE; token kept in that browser) and exposes `window.SCB`. If it says "Not connected", click Connect Spotify and have Jay click Agree. Spotify removed the top-tracks API and popularity in Feb 2026, and the connector's song order doesn't match the Popular list, so songs are read from the web player.
     a. Tab A = `https://2weeksoundcheck.com/tools/playlist.html`. `await SCB.findArtists([...names])` → `{status: ok|ambiguous|none, id, candidates}` per name (exact normalized-name match). For "ambiguous", pick the right one by opening the candidates (e.g. local/Seattle, recent releases), or skip. Batches of ~40 names per call keep under the 45s javascript_tool cap.
     b. Tab B = open.spotify.com (any page). Define `harvest` (below) and run `await harvest([...artistIds])` in batches of ~40 → `{artistId: [{id, song}, …3]}` straight from each artist page's Popular list (~0.5s per artist).
     c. Tab A: `await SCB.buildPlaylist({name, description, public: true, tracks: [...track ids in show order]})` → `{id, url, added}`. Adds 100 per request; a whole playlist takes seconds.
     ```js
     window.harvest = async function (ids, n = 3) {
       const out = {}; let prev = null;
       for (const id of ids) {
         history.pushState({}, "", "/artist/" + id); dispatchEvent(new PopStateEvent("popstate", { state: {} }));
         let rows = [], t0 = Date.now();
         while (Date.now() - t0 < 12000) {
           await new Promise(r => setTimeout(r, 250));
           rows = [...document.querySelectorAll('[data-testid="tracklist-row"]')].map(r => { const a = r.querySelector('a[href*="/track/"]');
             return a && { id: a.getAttribute("href").split("/track/")[1].split("?")[0], song: a.innerText }; }).filter(Boolean);
           if (location.pathname.endsWith(id) && rows.length && rows[0].id !== prev) break;
         }
         out[id] = rows.slice(0, n); prev = rows[0] && rows[0].id;
       }
       return out;
     };
     ```
   - Keep the Claude desktop window in front (hidden panes throttle timers).
   - Fallback if the builder breaks (e.g. token or app problem): the old web-player method: on the playlist page set the "Search for songs or episodes" input (native value setter + input event) to "<title> <artist>" and click `[data-testid="add-to-playlist-button"]` in the matching row; ~426 tracks took ~15 minutes. The Spotify connector's generate_playlist can't do exact track lists — don't use it.
4. Add the new playlist to the TOP of `playlists.json` (name, id, url, start, end, songs, artists, per_artist: 3); older entries stay, so the site's Playlists page keeps the archive.
   Also rewrite `previews.json`: for every show in the window, `{"<show title as in data/seattle.json>": {"artist": id, "track": id of the artist's #1 Popular song, "song": name, "name": search name}}`. You already open each artist page while building the playlist, so take the first track there. This powers the Preview buttons in "The next two weeks".
   Run `python3 build_site.py`, commit and push.
4b. **Frelard playlist** (Ballard + Fremont small rooms: Sunset, Tractor, Conor Byrne, Hidden Hall, Nectar, Add-a-Ball). Build it right after the Seattle one, same window:
   - Run `python3 lineup.py --area Frelard` (add `--json` for a machine-readable list; `--start YYYY-MM-DD` for a window that began earlier, e.g. building Sunday's playlist mid-week). It lists every headliner AND opener at the Frelard venues, with names already cleaned for search. The openers are the point: small rooms are where the discovery is.
   - Create a second playlist named `2 Week Soundcheck · Frelard: <Mon D>–<Mon D>`. Same playlist-builder method as step 3: every act gets its first 3 Popular songs (reuse the headliners' songs you just collected for the Seattle playlist). Never more than 3 per artist in either playlist. Skip anyone not on Spotify or ambiguous (common for local openers, and for very common names) and note them. A bill like "A x B" is two artists; search each.
   - Add it to the TOP of `playlists.json` with `"area": "Frelard"` (name, id, url, start, end, songs, artists, per_artist: 3, area). The site picks the newest entry per area: the Shows page's "Frelard" tab and `?area=frelard` link, the Playlists archive tag, and the newsletter's Frelard button all come from it. The citywide entry stays the one without `area`.
   - Run `python3 build_site.py`, commit and push.
4c. **Genre playlists** (added Oct 14, 2026). Seven standing Spotify playlists, one per genre, listed in `genre_playlists.json` (same ids every week; the site's genre chips and `?playlist=<slug>` links come from it). Headliners only, top 3 Popular songs each, in show order; an artist can be in up to two genres. Genres must be verified by a third party, never guessed (Jay, Oct 14, 2026).
   - `genres.json` holds every confirmed artist → genres (`[]` = left out). Only artists not in it need a decision.
   - New artists: look them up on Last.fm in Jay's Chrome (the workspace can't reach Last.fm; the API key is on last.fm/api/accounts, never in this repo): `artist.getinfo` + `artist.gettoptags` with autocorrect=1, written as `show|name|lastfm name|listeners|tag:count,...` lines, then `python3 genre_tags.py lookups.txt` sorts them into ok / check / flag.
   - Jay decides the check and flag artists (and can override any) on the Genre Review artifact page: seed its `weeks/<start>` document and `meta/current`, then read his choices from `weeks/<start>/decisions`. Add every decision to `genres.json`.
   - Refresh each playlist in Tab A: `await SCB.refreshPlaylist({id, tracks, description})` (replaces all songs, keeps the link and followers). Update `songs`, `artists`, `start`, `end` in `genre_playlists.json`, run `python3 build_site.py`, commit and push.
   - **Dated archive copy** (Jay, Oct 18, 2026). Also save each genre's songs as a new dated playlist so past weeks stay listenable: `await SCB.buildPlaylist({name: "2 Week Soundcheck · <Genre>: <Mon D>–<D>", description, tracks})`. Add each to the TOP of `genre_archive.json` (genre, name, id, url, start, end, songs, artists, per_artist: 3). The site's Playlists page lists them under that week, with a filter tab per genre. The standing playlists in `genre_playlists.json` stay the ones the newsletter and site link to.
5. Run `python3 build_issue.py` to draft the newsletter issue (issues/<start>.html to paste into beehiiv; subject and preview text are printed). Keep it short. Never quote lyrics.
6. No separate playlist email (Jay, Oct 14, 2026). The links, counts and skipped artists go into the Jay-only check email (`SUNDAY.md` step 5); everyone else gets the newsletter as a subscriber.

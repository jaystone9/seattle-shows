// Shared helpers for 2 Week Soundcheck pages.
window.SC = (function () {
  const TZ = "America/Los_Angeles";
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const todayISO = () => new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(new Date());
  const addDays = (iso, n) => { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const D = iso => new Date(iso + "T12:00:00Z");
  const fmt = (iso, o) => D(iso).toLocaleDateString("en-US", Object.assign({ timeZone: "UTC" }, o));
  const range = (a, b) => fmt(a, { month: "short" }) === fmt(b, { month: "short" })
    ? `${fmt(a, { month: "short", day: "numeric" })}–${fmt(b, { day: "numeric" })}`
    : `${fmt(a, { month: "short", day: "numeric" })}–${fmt(b, { month: "short", day: "numeric" })}`;
  const time = t => { if (!t) return ""; let [h, m] = t.split(":").map(Number); const ap = h >= 12 ? "pm" : "am"; h = h % 12 || 12; return m ? `${h}:${String(m).padStart(2, "0")}${ap}` : `${h}${ap}`; };
  const load = () => fetch("data/seattle.json", { cache: "no-cache" }).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); });

  function showRow(e, venues, compact) {
    const v = venues[e.venue] || { short: e.venue };
    const cancelled = e.status === "cancelled";
    const flag = e.status ? `<span class="flag">${esc(e.status[0].toUpperCase() + e.status.slice(1))}</span>` : "";
    const t = e.time ? `<span class="t">${time(e.time)}</span> at ` : "";
    const btn = e.url && !cancelled ? `<a class="${e.link}" href="${esc(e.url)}" target="_blank" rel="noopener">${e.link === "tickets" ? "Tickets" : "Details"}<span class="visually-hidden"> for ${esc(e.title)}</span></a>` : "";
    const pv = !compact && e.preview && !cancelled ? `<button class="pv" type="button" data-track="${esc(e.preview.track)}" aria-expanded="false" aria-label="Preview ${esc(e.title)}: ${esc(e.preview.song || "top song")}"><svg viewBox="0 0 16 16" aria-hidden="true"><path class="i-play" d="M4 2.5v11l9-5.5z"/><rect class="i-stop" x="3.5" y="3.5" width="9" height="9" rx="1.5"/></svg><span>Preview</span></button>` : "";
    const d = compact ? `<div class="d">${fmt(e.date, { month: "short", day: "numeric" })}<span>${fmt(e.date, { weekday: "short" })}</span></div>` : "";
    return `<div class="show${cancelled ? " cancelled" : ""}">${d}
      <div><div class="who">${esc(e.title)}${flag}</div>${e.support.length ? `<div class="with">with ${esc(e.support.join(", "))}</div>` : ""}</div>
      <div class="where">${t}${esc(v.short)}<span style="color:var(--muted)">, ${esc(v.hood || "")}</span></div>
      <div class="go">${pv}${btn}</div></div>`;
  }

  // One inline Spotify player at a time, opened under the show that asked for it.
  function previews(root) {
    root.addEventListener("click", ev => {
      const b = ev.target.closest(".pv"); if (!b) return;
      const row = b.closest(".show"), open = root.querySelector(".pv-player");
      const wasThis = open && open.previousElementSibling === row;
      if (open) { open.remove(); root.querySelectorAll('.pv[aria-expanded="true"]').forEach(x => { x.setAttribute("aria-expanded", "false"); x.querySelector("span").textContent = "Preview"; }); }
      if (wasThis) return;
      const box = document.createElement("div");
      box.className = "pv-player";
      box.innerHTML = `<iframe title="Spotify preview" src="https://open.spotify.com/embed/track/${esc(b.dataset.track)}?utm_source=generator&theme=0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>`;
      row.after(box);
      b.setAttribute("aria-expanded", "true"); b.querySelector("span").textContent = "Close";
    });
  }

  // Newsletter signup. newsletter.json can hold:
  //   form_id       beehiiv subscribe form id (loads beehiiv's form script)  <- in use
  //   embed_url     an iframe embed URL (older beehiiv embeds)
  //   subscribe_url a link to the beehiiv signup page
  // With none set, the slot says "opens soon".
  function signupHTML(nl) {
    nl = nl || {};
    if (nl.embed_url) return `<iframe class="nl-embed" title="Sign up for the Sunday email" src="${esc(nl.embed_url)}" loading="lazy" frameborder="0" scrolling="no"></iframe>`;
    if (nl.subscribe_url) return `<a class="btn" href="${esc(nl.subscribe_url)}" target="_blank" rel="noopener">Sign up for the Sunday email</a>`;
    return `<p class="nl-soon">Email signups open soon.</p>`;
  }

  // beehiiv hides its forms for visitors who already subscribed (it sets a
  // bhv_<publication>_subscribed cookie on this site), so show a note instead of an empty box.
  function alreadySubscribed(nl) {
    if (!nl.publication_id) return false;
    try { return document.cookie.split(";").some(c => c.trim().startsWith("bhv_" + nl.publication_id + "_subscribed=")); }
    catch (e) { return false; }
  }

  function fillSignup(slot, nl) {
    if (nl.form_id && alreadySubscribed(nl)) {
      slot.innerHTML = `<p class="nl-done">✓ You're subscribed. The next playlist lands in your inbox Sunday.</p>`;
      return;
    }
    if (nl.form_id) {
      slot.innerHTML = "";
      const sc = document.createElement("script");
      sc.async = true;
      sc.src = "https://subscribe-forms.beehiiv.com/v3/loader.js";
      sc.setAttribute("data-beehiiv-form", nl.form_id);
      slot.appendChild(sc);
    } else slot.innerHTML = signupHTML(nl);
  }

  // A signup band just above the footer on every page, plus any [data-signup] slot.
  function newsletter(data) {
    const nl = data.newsletter || {};
    const foot = document.querySelector("footer");
    // One signup per page: pages that already have a [data-signup] slot (Shows) skip the band.
    if (foot && !document.querySelector("[data-signup]") && !document.getElementById("newsletter")) {
      const band = document.createElement("section");
      band.className = "nl-band";
      band.id = "newsletter";
      band.setAttribute("aria-labelledby", "nl-h");
      band.innerHTML = `<div class="nl-copy"><h2 id="nl-h">The Sunday email</h2>
        <p>Get this week's playlist sent straight to your inbox every Sunday. Free, one email a week.</p></div>
        <div class="nl-form"><div data-signup></div><p class="nl-note">Using Gmail? Your first email may land in Promotions. Drag it to Primary so the playlist shows up in your inbox every Sunday.</p></div>`;
      foot.before(band);
    }
    // The signup is filled in after data loads, so honor a #newsletter link once it exists.
    const target = document.getElementById("newsletter");
    if (target && location.hash === "#newsletter") setTimeout(() => target.scrollIntoView(), 0);
    document.querySelectorAll("[data-signup]").forEach(s => fillSignup(s, nl));
  }

  function footer(data) {
    newsletter(data);
    const el = document.getElementById("venues");
    if (el) el.innerHTML = Object.entries(data.venues).map(([k, v]) => `<li><a href="${esc(v.site)}" target="_blank" rel="noopener">${esc(v.short)}</a>, ${esc(v.hood)}</li>`).join("");
    document.querySelectorAll("[data-cal]").forEach(a => a.href = data.calendar);
    // Google Calendar can't open webcal:// links directly; its "add by URL" screen takes the feed as cid.
    const gcal = "https://calendar.google.com/calendar/render?cid=" + encodeURIComponent(data.calendar);
    document.querySelectorAll("[data-gcal]").forEach(a => { a.href = gcal; a.target = "_blank"; a.rel = "noopener"; });
    const pl = data.playlist;
    document.querySelectorAll("[data-pl]").forEach(a => { if (pl) a.href = pl.url; else a.closest("li")?.remove(); });
    const g = new Date(data.generated), fine = document.getElementById("fine");
    if (fine) fine.textContent = `Show listings updated ${g.toLocaleDateString("en-US", { month: "long", day: "numeric" })}. Times and lineups come from each venue and can change, so check the ticket page before you go.`;
  }

  return { esc, todayISO, addDays, D, fmt, range, time, load, showRow, footer, previews };
})();

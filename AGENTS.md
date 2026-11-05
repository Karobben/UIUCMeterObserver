# Agent guide — UIUC Meter Observer

This guide is for coding agents, including Cursor and Codex. Follow the user's current instructions first. Run commands from the repository root.

## Fast start

This is a static, browser-local dashboard. There is no application server, database, login, npm build, or API key requirement. Python 3's standard library is sufficient to rebuild the HTML. The committed HTML also works without rebuilding.

```sh
git clone https://github.com/Karobben/UIUCMeterObserver.git
cd UIUCMeterObserver
python3 outputs/parking_enforcement/build_dashboard.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/outputs/parking_enforcement/parking_dashboard.html`. Stop the preview server when finished. Alternatively, open that HTML file directly in a browser.

## Source map and update workflow

| Path | Responsibility |
| --- | --- |
| `outputs/parking_enforcement/parking_enforcement_unified.csv` | Current dataset used by the dashboard |
| `outputs/parking_enforcement/dashboard_template.html` | Editable HTML/CSS/JavaScript; `__DATA__` is replaced during build |
| `outputs/parking_enforcement/build_dashboard.py` | Embeds the CSV into `parking_dashboard.html` |
| `outputs/parking_enforcement/parking_dashboard.html` | Generated, self-contained deliverable; commit after source changes |
| `outputs/parking_enforcement/parking_enforcement_unified.xlsx` | Excel snapshot; not changed by the dashboard builder |
| `build_parking.mjs` | Original embedded records and CSV/Excel generator |

For UI changes, edit the template and rebuild. Do not make changes only to generated HTML. Preserve offline operation, accessible controls, responsive layout, and the weekday hover/focus interaction. The hourly and weekday charts share aligned plotting rows through CSS subgrid.

For data changes, edit the CSV without changing its 13 column names, then rebuild the dashboard. If retaining reproducibility through `build_parking.mjs`, update its embedded records, count checks, worksheet ranges, and summary labels too. Keep the dashboard's static record badge and fallback totals synchronized with the data. Document whether Excel was refreshed; never imply it was updated merely because the CSV changed.

**Do not run `build_parking.mjs` casually:** it overwrites the CSV and Excel from its embedded records and can discard CSV-only edits. It requires Node.js and `@oai/artifact-tool` from the Codex spreadsheet runtime, which may be unavailable in Cursor or a clean clone. Do not install an unverified substitute package. A missing spreadsheet runtime does not prevent dashboard development or static deployment.

## Data rules

- Dates: `YYYY-MM-DD`; typed start/end times in CSV: local `HH:MM`. Preserve the original time description, bounds, uncertainty, and notes.
- Resolve “today” using the user's local date, normally America/Chicago here, and record the resolved date in notes.
- Deduplicate repeated nonempty ticket IDs. Preserve distinct IDs even when their timestamps match. Do not deduplicate unrelated sightings solely because they share an hour.
- Ticket `26PE101880` on October 22, 2026 at 12:14 PM appears once; its recent observation is merged into that record.
- Tickets `26PE400158` and `26PE400159` share January 16, 2026 at 1:37 PM on Mathews Avenue but are distinct ticket IDs. Do not merge without further evidence.
- Two reported tickets concern other drivers, have no IDs, and are separate from the user's ticket count. Potential historical overlap remains unverified.
- October 15 afternoon observations retain the conflict between the reported date and “Friday.” Do not silently move them to October 16.
- Unknown meter-payment status stays unknown. A sighting does not establish a ticket or a no-ticket parking session.
- Approximate windows and “before” bounds may overlap a time filter, but must not be assigned fabricated exact hours in hourly charts.
- This selected log measures recorded frequency, not ticket probability. Do not present a ticket percentage as a reliable unpaid-session risk without representative session exposure data.

Baseline as of November 5, 2026: **44 rows**, **36 historical tickets with unique IDs**, **2 additional reported tickets**, **4 officer sightings**, **2 no-ticket observations**. Update this baseline when adding records; it is not a permanent row-count limit.

## Validation before committing

1. Rebuild HTML and confirm the builder's embedded count matches CSV rows.
2. Check nonempty ticket IDs are unique and known uncertainty notes remain present.
3. Confirm no `__DATA__` placeholder remains in generated HTML.
4. In a browser, check street/week/date/weekday/workday/time filters, each hourly fill category and legend, reset, and filtered CSV download.
5. Hover/focus Monday and confirm only the hourly chart changes. Moving away or blurring restores it. Confirm the records table stays unchanged.
6. Check a zero-record selection, desktop axis alignment, and a narrow screen layout. Inspect the browser console for errors.
7. Review `git diff`; keep ticket data intact and exclude local dependencies, caches, preview images, credentials, and machine-specific absolute paths.

Useful baseline checks, run from the root:

```sh
python3 -c 'import csv; from pathlib import Path; p=Path("outputs/parking_enforcement"); rows=list(csv.DictReader((p/"parking_enforcement_unified.csv").open(encoding="utf-8-sig"))); ids=[r["Ticket ID"] for r in rows if r["Ticket ID"]]; assert len(ids)==len(set(ids)), "Duplicate ticket IDs"; assert "__DATA__" not in (p/"parking_dashboard.html").read_text(); print(f"{len(rows)} records; {len(ids)} distinct ticket IDs")'
```

Do not claim browser checks or live deployment passed unless actually verified.

## Prepare a static deployment

When the user requests deployment, first inspect existing hosting settings and preserve them. The repository is public and the generated HTML embeds the dataset. No runtime secrets are needed. This guide alone is not an instruction to deploy during unrelated edits.

For a static host, rebuild and copy the generated HTML to `index.html` in a dedicated publish directory. Do not publish the repository root unintentionally.

### GitHub Pages: simple branch deployment

If no existing hosting configuration must be preserved, use the default branch's `/docs` folder. The branch was `master` when this guide was written; verify it before configuring Pages.

```sh
python3 outputs/parking_enforcement/build_dashboard.py
mkdir -p docs
cp outputs/parking_enforcement/parking_dashboard.html docs/index.html
touch docs/.nojekyll
git add docs/index.html docs/.nojekyll
git commit -m "Prepare dashboard for GitHub Pages"
git push
```

Then configure the repository's **Settings → Pages → Build and deployment → Source: Deploy from a branch**, select the actual default branch and `/docs`, and save. Use authenticated repository tools if available; otherwise explain the precise setting the owner must change. Do not overwrite existing `docs/index.html` content without checking it first.

The expected project URL is `https://karobben.github.io/UIUCMeterObserver/`, but it is not a verified live deployment until Pages succeeds and that URL loads the dashboard. Wait for the deployment result, check the displayed dataset count and filters, then report the verified URL. On later updates, regenerate and copy `docs/index.html` again before pushing.

Official reference: [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

### Other static hosts

Use the same generated HTML as the publish directory's `index.html`. There is no server-side start command. Any host-specific build must have Python 3 if rebuilding from CSV; alternatively deploy the committed, verified HTML. Preserve project-relative URLs if adding assets later.

## Handoff

Report files changed, record counts when relevant, checks actually run, any stale Excel snapshot or unavailable runtime, and the verified deployed URL if deployment was requested. Keep docs and generated outputs synchronized. If an agent does not discover this file automatically, ask it to read root `AGENTS.md` before working.

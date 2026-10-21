# VIX Dashboard

A static dashboard for VIX and cross-asset indicators. A scheduled GitHub Action pulls
data from Yahoo Finance and commits `series.json`; GitHub Pages serves `index.html`.

## Files

- `index.html`: the dashboard. Reads `series.json`; no keys or uploads.
- `fetch_series.py`: downloads the data with yfinance and writes `series.json`.
- `requirements.txt`: Python dependencies.
- `.github/workflows/update.yml`: runs the script on weekdays after the US close.

## Setup

1. Create a new repository on GitHub and upload these files, keeping the `.github/workflows` folder path.
2. Run the first update: go to **Actions → Update market data → Run workflow**.
   This creates `series.json`. Until it exists, the dashboard shows a "not found yet" message.
3. Turn on the site: **Settings → Pages → Build and deployment → Deploy from a branch**,
   choose `main` and `/ (root)`, then save.
4. Open the Pages URL shown on that screen. It looks like `https://<your-user>.github.io/<repo>/`.

Keep the repository private if you don't want the dashboard public. On a private repo,
GitHub Pages needs a paid plan.

## Notes

- Yahoo data is delayed about 15 minutes and comes from an unofficial library, so it can break if Yahoo changes its site.
- The put/call ratio has no free Yahoo source and is shown as unavailable.
- HYG is an ETF price used as a rough high yield proxy. It moves opposite to credit spreads.
- The schedule runs at 22:30 UTC. Adjust the cron line in `update.yml` if you prefer another time.

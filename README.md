# Economic dashboard

A single web page that shows key economic indicators and refreshes itself every day.

**How it works:** a GitHub Action runs `scripts/update_data.py` each morning. The script pulls fresh numbers from FRED (St. Louis Fed) and multpl.com, saves them to `data/indicators.json`, and commits the file. GitHub Pages then republishes `index.html`, which reads that file when someone opens the page.

## What updates automatically

| Indicator | Source | How often it actually changes |
|---|---|---|
| S&P 500 level, YTD, drawdown from high | FRED | Daily (prior day's close) |
| 10-year Treasury, 3-month T-bill | FRED | Daily |
| Fed funds target range and effective rate | FRED | Daily (target moves at FOMC meetings) |
| 30-year mortgage rate | FRED (Freddie Mac) | Weekly |
| CPI inflation, headline and core | FRED | Monthly |
| Unemployment rate | FRED | Monthly |
| Shiller P/E | multpl.com | Daily |
| Federal debt and deficit as % of GDP | FRED | Quarterly / yearly |

## What you update by hand

- **`static-data.js`**: federal brackets, standard deduction, 401(k)/IRA/HSA limits and state tax rates. Update it once a year, when the IRS publishes the next year's numbers (usually October or November), and again in January for state changes.
- **`data/manual.json`**: optional high-yield savings and money market rates. No reliable free feed exists for "best available" rates, so type in what you want to show. Rows left as `null` are hidden.

## One-time setup (about 15 minutes)

1. **Get a free FRED API key.** Create an account at fred.stlouisfed.org, then go to My Account > API Keys > Request API Key.
2. **Create a GitHub repository.** Make it public (GitHub Pages is free only for public repos on a free account). Nothing in this project is private. Everything on it is public data.
3. **Upload these files** to the repository, keeping the folder structure:
   - `index.html`, `static-data.js`, `manifest.webmanifest`, `README.md`
   - `icons/` (three PNG files)
   - `data/indicators.json`, `data/manual.json`
   - `scripts/update_data.py`
   - `.github/workflows/update-data.yml`

   Tip: hidden folders like `.github` are often skipped when dragging folders into the browser. If it's missing, use **Add file > Create new file**, type `.github/workflows/update-data.yml` as the name, and paste in the contents.
4. **Add your API key as a secret.** In the repo: Settings > Secrets and variables > Actions > New repository secret. Name it `FRED_API_KEY` and paste the key.
5. **Turn on Pages.** Settings > Pages > Source: "Deploy from a branch" > Branch: `main`, folder `/ (root)` > Save.
6. **Run the first update.** Actions tab > "Update economic data" > Run workflow. When it turns green (about 30 seconds), your page is live at `https://YOUR-USERNAME.github.io/YOUR-REPO/`.

After that it runs on its own every day at 13:00 UTC (about 7 a.m. Mountain time in summer). To change the time, edit the `cron` line in `.github/workflows/update-data.yml`.

## Save it to your phone's home screen

The page includes an app icon, so the shortcut looks like a real app.

- **iPhone:** open the page in Safari, tap the Share button, then Add to Home Screen.
- **Android:** open the page in Chrome, tap the three-dot menu, then Add to Home screen (or Install app).

Upload the `icons` folder and `manifest.webmanifest` along with the other files so the icon appears.

## Previewing on your computer

The page loads its data with `fetch`, so opening `index.html` by double-click won't work. From the project folder run:

```
python3 -m http.server 8000
```

Then open http://localhost:8000. To test the updater locally: `FRED_API_KEY=your_key python3 scripts/update_data.py`.

## If something looks off

- **Page says "No data yet":** the workflow hasn't run successfully. Check the Actions tab for errors. The most common cause is a missing or mistyped `FRED_API_KEY` secret.
- **"These items could not refresh":** one source failed that day. The page keeps the last good value and marks it "not refreshed". The next run usually fixes it.
- **Shiller P/E shows as not refreshed:** it comes from scraping multpl.com, which could change its layout. Everything else uses the FRED API and is unaffected.
- **Site didn't change after a successful run:** check Actions > "pages build and deployment". Pages can take a minute or two to publish.
- **Data is more than 4 days old:** the page shows a red warning. GitHub pauses scheduled workflows on repos with no activity for 60 days, so re-enable it in the Actions tab if that happens.

## Notes

- S&P 500 drawdown is measured from the highest close in the roughly 10 years of history FRED provides.
- CPI inflation uses the not-seasonally-adjusted index, the same basis as the headline figure BLS publishes.
- The Shiller P/E "long-run average" comes from the multpl.com page when available.

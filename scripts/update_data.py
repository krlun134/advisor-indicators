#!/usr/bin/env python3
"""Pull the latest economic indicators and write data/indicators.json.

Sources
  FRED (St. Louis Fed) API : S&P 500, Nasdaq Composite, Treasury yields, Fed
                             funds, CPI, unemployment, mortgage rates, federal
                             debt/deficit
  Yahoo Finance chart feed : Russell 2000, EEM, Euro Stoxx 50 (unofficial feed,
                             one request per symbol per run)
  multpl.com               : Shiller P/E ratio (page scrape)

Needs one environment variable: FRED_API_KEY (free at fred.stlouisfed.org).
Uses only the Python standard library.

If one indicator fails, the previous good value is kept and flagged as stale
so the dashboard never goes blank because of a single bad request.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "indicators.json"
FRED_KEY = os.environ.get("FRED_API_KEY", "").strip()
UA = "Mozilla/5.0 (economic-dashboard updater)"


# ---------------------------------------------------------------- helpers
def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def fred(series_id, start=None, limit=None, newest_first=False):
    """Return [(date, value), ...] with missing values dropped."""
    params = {
        "series_id": series_id,
        "api_key": FRED_KEY,
        "file_type": "json",
        "sort_order": "desc" if newest_first else "asc",
    }
    if start:
        params["observation_start"] = start
    if limit:
        params["limit"] = limit
    url = "https://api.stlouisfed.org/fred/series/observations?" + urllib.parse.urlencode(params)
    payload = json.loads(http_get(url))
    rows = []
    for obs in payload.get("observations", []):
        try:
            rows.append((obs["date"], float(obs["value"])))
        except (ValueError, KeyError):
            continue  # FRED uses "." for missing values
    if not rows:
        raise ValueError(f"FRED returned no usable data for {series_id}")
    return rows


def latest_two(series_id, freq):
    rows = fred(series_id, limit=12, newest_first=True)
    value_date, value = rows[0]
    prev = rows[1][1] if len(rows) > 1 else None
    return {"value": value, "date": value_date, "prev": prev, "freq": freq}


def year_ago(date_str):
    y, m, d = date_str.split("-")
    return f"{int(y) - 1}-{m}-{d}"


# ------------------------------------------------------------- indicators
def series_summary(rows):
    """Build the hero-panel numbers for any daily price series.

    rows is [(YYYY-MM-DD, close), ...] oldest -> newest. Returns the latest
    close, day change, year to date, drawdown from the high in the window and
    the last 252 closes for the chart."""
    date, value = rows[-1]
    prev_value = rows[-2][1] if len(rows) > 1 else None
    year = date[:4]
    prior_year_closes = [v for d, v in rows if d < f"{year}-01-01"]
    ytd = (value / prior_year_closes[-1] - 1) * 100 if prior_year_closes else None
    high_date, high_value = max(rows, key=lambda r: r[1])
    drawdown = (value / high_value - 1) * 100
    return {
        "value": value,
        "date": date,
        "freq": "d",
        "day_pct": (value / prev_value - 1) * 100 if prev_value else None,
        "ytd_pct": ytd,
        "drawdown_pct": drawdown,
        "high": {"value": high_value, "date": high_date},
        "history": [[d, round(v, 2)] for d, v in rows[-252:]],
    }


def sp500():
    return series_summary(fred("SP500", start="2015-01-01"))  # oldest -> newest


def yahoo_rows(symbol, start="2015-01-01"):
    """Daily closes from Yahoo Finance's unofficial chart feed (price only, not
    dividend adjusted). Returns [(YYYY-MM-DD, close), ...] oldest -> newest."""
    p1 = int(datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    p2 = int(time.time()) + 86400
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(symbol, safe="")
           + f"?period1={p1}&period2={p2}&interval=1d&events=history")
    payload = json.loads(http_get(url))
    chart = payload.get("chart") or {}
    if chart.get("error"):
        raise ValueError(f"Yahoo error for {symbol}: {str(chart['error'])[:120]}")
    result = (chart.get("result") or [None])[0]
    if not result or not result.get("timestamp"):
        raise ValueError(f"Yahoo returned no data for {symbol}")
    offset = (result.get("meta") or {}).get("gmtoffset", 0) or 0
    closes = result["indicators"]["quote"][0]["close"]
    by_date = {}
    for ts, close in zip(result["timestamp"], closes):
        if close is None:
            continue
        day = datetime.fromtimestamp(ts + offset, tz=timezone.utc).strftime("%Y-%m-%d")
        by_date[day] = float(close)  # keep the last bar if a day repeats
    rows = sorted(by_date.items())
    # The bar for today is still forming (the daily run is mid-session for
    # Europe and pre-open for the US), so drop it unless the day has ended.
    now = datetime.now(timezone.utc)
    if rows and rows[-1][0] == now.strftime("%Y-%m-%d") and now.hour < 22:
        rows = rows[:-1]
    if len(rows) < 200:
        raise ValueError(f"Yahoo returned only {len(rows)} usable closes for {symbol}")
    age = (now.date() - datetime.strptime(rows[-1][0], "%Y-%m-%d").date()).days
    if age > 10:
        raise ValueError(f"Latest Yahoo close for {symbol} is {rows[-1][0]} ({age} days old)")
    return rows


# Stock indexes shown in the swipeable charts, in display order. "measure" and
# "prefix" only affect labels on the page. The S&P 500 reuses the sp500 job so
# it is not fetched twice.
INDEXES = [
    {"id": "sp500", "name": "S&P 500", "source": "fred", "symbol": "SP500",
     "note": "Price index, not total return", "prefix": "", "measure": "level"},
    {"id": "nasdaq", "name": "Nasdaq Composite", "source": "fred", "symbol": "NASDAQCOM",
     "note": "Price index, not total return", "prefix": "", "measure": "level"},
    {"id": "russell2000", "name": "Russell 2000", "source": "yahoo", "symbol": "^RUT",
     "note": "Price index, not total return", "prefix": "", "measure": "level"},
    {"id": "eem", "name": "iShares MSCI Emerging Markets ETF (EEM)", "source": "yahoo", "symbol": "EEM",
     "note": "ETF share price in US dollars, not an index; price only", "prefix": "$", "measure": "price"},
    {"id": "eurostoxx50", "name": "Euro Stoxx 50", "source": "yahoo", "symbol": "^STOXX50E",
     "note": "Price index, not total return; priced in euros", "prefix": "", "measure": "level"},
]


def index_summary(spec):
    if spec["source"] == "fred":
        rows = fred(spec["symbol"], start="2015-01-01")
    else:
        rows = yahoo_rows(spec["symbol"])
    return series_summary(rows)


def cpi_yoy(series_id):
    """Year-over-year % change using the not-seasonally-adjusted index (the
    basis BLS uses for headline CPI). Returns None for a month if the year-ago
    month is missing from FRED."""
    rows = fred(series_id, limit=30, newest_first=True)
    lookup = dict(rows)

    def yoy(date):
        base = lookup.get(year_ago(date))
        return (lookup[date] / base - 1) * 100 if base else None

    dates = [d for d, _ in rows]
    latest = yoy(dates[0])
    prev = yoy(dates[1]) if len(dates) > 1 else None
    if latest is None:
        raise ValueError(f"No year-ago value to compute {series_id} inflation")
    return {"value": round(latest, 1), "date": dates[0],
            "prev": round(prev, 1) if prev is not None else None, "freq": "m"}


def fed_funds():
    upper = fred("DFEDTARU", limit=5, newest_first=True)[0]
    lower = fred("DFEDTARL", limit=5, newest_first=True)[0]
    effective = fred("DFF", limit=5, newest_first=True)[0]
    return {"lower": lower[1], "upper": upper[1], "effective": effective[1],
            "date": upper[0], "freq": "d"}


def debt_total():
    info = latest_two("GFDEBTN", "q")  # millions of dollars
    info["value"] = info["value"] / 1_000_000  # -> trillions
    if info["prev"] is not None:
        info["prev"] = info["prev"] / 1_000_000
    return info


def _why(exc):
    """Short reason for a failed request, so the workflow log shows what went wrong."""
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code}"
    if isinstance(exc, urllib.error.URLError):
        return f"network error ({exc.reason})"
    return str(exc)[:80]


def _shiller_main_page():
    html = http_get("https://www.multpl.com/shiller-pe")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-z#0-9]+;", " ", text)
    m = re.search(r"Current Shiller PE Ratio[^0-9]{0,80}?(\d{1,2}\.\d{1,2})", text)
    if not m:
        raise ValueError("value not found on page")
    out = {"value": float(m.group(1)),
           "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "freq": "d"}
    mean = re.search(r"Mean:?\s*(\d{1,2}\.\d{1,2})", text)
    if mean:
        out["mean"] = float(mean.group(1))
    return out


def _shiller_table_page():
    """Backup: the by-year table's first row is the current value and its date."""
    html = http_get("https://www.multpl.com/shiller-pe/table/by-year")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-z#0-9]+;", " ", text)
    m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})\s+(\d{1,2}\.\d{1,2})", text)
    if not m:
        raise ValueError("value not found in table")
    day = datetime.strptime(m.group(1), "%b %d, %Y").strftime("%Y-%m-%d")
    return {"value": float(m.group(2)), "date": day, "freq": "d"}


def shiller_pe():
    """Shiller P/E from multpl.com: main page first, then the table page. If both
    fail, the error names each step and its HTTP status."""
    problems = []
    for label, fetch in (("main page", _shiller_main_page), ("table page", _shiller_table_page)):
        try:
            return fetch()
        except Exception as exc:
            problems.append(f"{label}: {_why(exc)}")
    raise ValueError("multpl.com failed (" + "; ".join(problems) + ")")


JOBS = {
    "sp500": sp500,
    "treasury10": lambda: latest_two("DGS10", "d"),
    "fed_funds": fed_funds,
    "cpi_headline": lambda: cpi_yoy("CPIAUCNS"),
    "cpi_core": lambda: cpi_yoy("CPILFENS"),
    "unemployment": lambda: latest_two("UNRATE", "m"),
    "mortgage30": lambda: latest_two("MORTGAGE30US", "w"),
    "tbill3m": lambda: latest_two("DTB3", "d"),
    "debt_pct_gdp": lambda: latest_two("GFDEGDQ188S", "q"),
    "debt_total_tn": debt_total,
    "deficit_pct_gdp": lambda: latest_two("FYFSGDA188S", "a"),
    "shiller_pe": shiller_pe,
}


def build_indices(result, errors, previous):
    """Assemble the indices list for the swipeable charts. Each index runs in its
    own try/except; a failed one keeps its last good values, flagged stale."""
    old_by_id = {i.get("id"): i for i in previous.get("indices", []) if isinstance(i, dict)}
    out = []
    for spec in INDEXES:
        meta = {k: spec[k] for k in ("id", "name", "symbol", "note", "prefix", "measure")}
        try:
            if spec["id"] == "sp500":
                if "sp500" not in result:  # its own job failed and had no old value
                    continue
                summary = dict(result["sp500"])  # carries stale flag if it was reused
            else:
                summary = index_summary(spec)
                print(f"ok    index_{spec['id']}")
            out.append({**meta, **summary})
        except Exception as exc:
            errors["index_" + spec["id"]] = str(exc)[:200]
            print(f"FAIL  index_{spec['id']}: {exc}", file=sys.stderr)
            old = old_by_id.get(spec["id"])
            if old:
                old.update(meta)
                old["stale"] = True
                out.append(old)
    return out


def main():
    if not FRED_KEY:
        print("FRED_API_KEY is not set.", file=sys.stderr)
        return 1

    try:
        previous = json.loads(OUT.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        previous = {}

    result = {}
    errors = {}
    for name, job in JOBS.items():
        try:
            result[name] = job()
            print(f"ok    {name}")
        except Exception as exc:  # keep going; one bad source shouldn't block the rest
            errors[name] = str(exc)[:200]
            old = previous.get(name)
            if isinstance(old, dict):
                old["stale"] = True
                result[name] = old
            print(f"FAIL  {name}: {exc}", file=sys.stderr)

    result["indices"] = build_indices(result, errors, previous)

    total = len(JOBS) + len(INDEXES) - 1  # the S&P 500 index reuses the sp500 job
    if len(errors) >= total:
        print("Every indicator failed; leaving the existing file untouched.", file=sys.stderr)
        return 1

    result["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    result["errors"] = errors
    OUT.write_text(json.dumps(result, indent=1) + "\n")
    print(f"Wrote {OUT} ({total - len(errors)}/{total} indicators fresh)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

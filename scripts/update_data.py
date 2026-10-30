#!/usr/bin/env python3
"""Pull the latest economic indicators and write data/indicators.json.

Sources
  FRED (St. Louis Fed) API : S&P 500, Treasury yields, Fed funds, CPI,
                             unemployment, mortgage rates, federal debt/deficit
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
def sp500():
    rows = fred("SP500", start="2015-01-01")  # oldest -> newest
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


def shiller_pe():
    html = http_get("https://www.multpl.com/shiller-pe")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-z#0-9]+;", " ", text)
    m = re.search(r"Current Shiller PE Ratio[^0-9]{0,80}?(\d{1,2}\.\d{1,2})", text)
    if not m:
        raise ValueError("Could not find Shiller P/E on multpl.com")
    out = {"value": float(m.group(1)),
           "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "freq": "d"}
    mean = re.search(r"Mean:?\s*(\d{1,2}\.\d{1,2})", text)
    if mean:
        out["mean"] = float(mean.group(1))
    return out


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

    if len(errors) == len(JOBS):
        print("Every indicator failed; leaving the existing file untouched.", file=sys.stderr)
        return 1

    result["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    result["errors"] = errors
    OUT.write_text(json.dumps(result, indent=1) + "\n")
    print(f"Wrote {OUT} ({len(JOBS) - len(errors)}/{len(JOBS)} indicators fresh)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

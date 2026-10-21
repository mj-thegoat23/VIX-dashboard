#!/usr/bin/env python3
"""
Downloads market data from Yahoo Finance (via yfinance) and writes series.json.
Run by GitHub Actions on a schedule; index.html reads the result.

Install:  pip install -r requirements.txt
Run:      python fetch_series.py
Output:   series.json (in the current folder)
"""
import json
from datetime import datetime, timedelta, timezone

import pandas as pd
import yfinance as yf

START = (datetime.now() - timedelta(days=3 * 365)).strftime("%Y-%m-%d")

# key -> Yahoo symbol. ^TNX is the 10-year yield quoted x10, so it is divided by 10.
SYMBOLS = {
    "vix": "^VIX", "vvix": "^VVIX", "vix9d": "^VIX9D", "vix3m": "^VIX3M",
    "vix6m": "^VIX6M", "skew": "^SKEW", "move": "^MOVE", "spx": "^GSPC",
    "gold": "GC=F", "wti": "CL=F", "copper": "HG=F", "ust10y": "^TNX",
    "hy": "HYG",
}
SCALE = {"ust10y": 0.1}


def main():
    df = yf.download(list(SYMBOLS.values()), start=START, auto_adjust=False,
                     progress=False, group_by="column")["Close"]

    series = {}
    for key, sym in SYMBOLS.items():
        if sym not in df.columns:
            print(f"{key} ({sym}): not returned by Yahoo")
            continue
        s = df[sym].dropna()
        if key == "ust10y" and s.median() > 20:
            s = s / 10.0  # ^TNX is sometimes quoted x10 (e.g. 45.2 = 4.52%)
        if len(s) <= 10:
            print(f"{key} ({sym}): too few rows ({len(s)})")
            continue
        series[key] = {
            "source": "Yahoo Finance",
            "symbol": sym,
            "data": [{"d": pd.Timestamp(i).strftime("%Y-%m-%d"), "v": round(float(v), 4)}
                     for i, v in s.items()],
        }

    out = {
        "updated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "series": series,
    }
    with open("series.json", "w") as f:
        json.dump(out, f)
    print("Wrote series.json with:", ", ".join(sorted(series)) or "nothing")


if __name__ == "__main__":
    main()

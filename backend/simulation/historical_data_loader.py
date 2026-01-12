"""
PROJECT PREDATOR - HistoricalDataLoader
Loads OHLCV candles from CSV (simple, no pandas).
"""
import csv
from typing import List
from backend.market.candle import Candle


class HistoricalDataLoader:
    """
    Loads historical candles from CSV.
    CSV columns: timestamp,open,high,low,close,volume
    Timestamp expected as ISO8601 or epoch seconds.
    """
    def load_csv(self, path: str) -> List[Candle]:
        candles: List[Candle] = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_raw = row.get("timestamp") or row.get("time")
                candle = Candle.from_row(
                    ts_raw,
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row.get("volume", 0.0)),
                )
                candles.append(candle)
        return candles

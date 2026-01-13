"""
PROJECT PREDATOR - HistoricalDataLoader
Loads OHLCV candles from CSV or Parquet (UTC-aware timestamps).
"""
import csv
from typing import List, Optional
from datetime import datetime, timezone
from backend.market.candle import Candle


class HistoricalDataLoader:
    """
    Loads historical candles from CSV.
    CSV columns: timestamp,open,high,low,close,volume
    Timestamp expected as ISO8601 or epoch seconds.
    """
    def _parse_timestamp(self, ts_raw: str) -> float:
        """
        Parse timestamp to UTC epoch seconds.
        Supports: ISO8601, epoch seconds (int/float string).
        """
        try:
            # Try ISO8601
            dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except (ValueError, AttributeError):
            try:
                # Try epoch seconds
                return float(ts_raw)
            except ValueError:
                raise ValueError(f"Cannot parse timestamp: {ts_raw}")
    
    def load_csv(self, path: str) -> List[Candle]:
        """
        Load candles from CSV.
        Columns: timestamp,open,high,low,close,volume
        Timestamps are parsed as UTC-aware.
        """
        candles: List[Candle] = []
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_raw = row.get("timestamp") or row.get("time") or row.get("t")
                ts = self._parse_timestamp(ts_raw)
                candle = Candle.from_row(
                    ts,
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row.get("volume", 0.0)),
                )
                candles.append(candle)
        return candles
    
    def load_parquet(self, path: str) -> Optional[List[Candle]]:
        """
        Load candles from Parquet (optional - requires pyarrow or fastparquet).
        Returns None if library not available.
        """
        try:
            import pyarrow.parquet as pq
            table = pq.read_table(path)
            df = table.to_pandas()
            candles: List[Candle] = []
            for _, row in df.iterrows():
                # Parse timestamp (assume UTC if timezone-naive)
                ts = row.get("timestamp") or row.get("time")
                if isinstance(ts, str):
                    ts = self._parse_timestamp(ts)
                elif hasattr(ts, "timestamp"):
                    ts = ts.timestamp()
                else:
                    ts = float(ts)
                candle = Candle.from_row(
                    ts,
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row.get("volume", 0.0)),
                )
                candles.append(candle)
            return candles
        except ImportError:
            return None  # Parquet library not available

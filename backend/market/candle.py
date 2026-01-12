"""
PROJECT PREDATOR - Candle
Simple OHLCV structure.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Union


def _parse_timestamp(value: Union[str, float, int]) -> float:
    if isinstance(value, (float, int)):
        return float(value)
    try:
        # ISO8601
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        # Fallback: float string
        return float(value)


@dataclass
class Candle:
    timestamp: float
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    @staticmethod
    def from_row(ts_value: Union[str, float, int], o: float, h: float, l: float, c: float, v: float) -> "Candle":
        return Candle(_parse_timestamp(ts_value), o, h, l, c, v)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }

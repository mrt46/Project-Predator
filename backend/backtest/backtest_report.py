"""
PROJECT PREDATOR - BacktestReport
Generates simple metrics from trades/equity.
"""
from typing import List, Dict


class BacktestReport:
    @staticmethod
    def summarize(trades: List[Dict], equity: List[Dict]) -> Dict:
        win = 0
        pnl_sum = 0.0
        for t in trades:
            qty = t.get("quantity", 0.0)
            price = t.get("price", 0.0)
            side = t.get("side")
            pnl = qty * price * (1 if side == "SELL" else -1)
            if pnl > 0:
                win += 1
            pnl_sum += pnl
        winrate = (win / len(trades)) if trades else 0.0
        max_dd = BacktestReport._max_drawdown(equity)
        return {
            "total_return": pnl_sum,
            "num_trades": len(trades),
            "winrate": winrate,
            "max_drawdown": max_dd,
        }

    @staticmethod
    def _max_drawdown(equity: List[Dict]) -> float:
        peak = 0.0
        max_dd = 0.0
        for point in equity:
            val = point.get("price", 0.0)
            if val > peak:
                peak = val
            dd = (peak - val)
            if dd > max_dd:
                max_dd = dd
        return max_dd

    @staticmethod
    def to_csv(equity: List[Dict], path: str) -> None:
        with open(path, "w") as f:
            f.write("price\n")
            for p in equity:
                f.write(f"{p.get('price',0.0)}\n")

"""
PROJECT PREDATOR - BacktestReport
Generates simple metrics from trades/equity.
"""
from typing import List, Dict


class BacktestReport:
    @staticmethod
    def summarize(trades: List[Dict], equity: List[Dict]) -> Dict:
        # Calculate winrate from trades (simplified - assumes round trips)
        win = 0
        total = len(trades)
        if total > 0:
            # Simple heuristic: if we have more SELL than BUY, we're winning
            buys = sum(1 for t in trades if t.get("side") == "BUY")
            sells = sum(1 for t in trades if t.get("side") == "SELL")
            if sells > buys:
                win = sells - buys
        
        winrate = (win / total) if total > 0 else 0.0
        
        # Max drawdown from equity curve
        max_dd = BacktestReport._max_drawdown(equity)
        
        # Total return from final equity (if available) or sum of trades
        total_return = 0.0
        if equity:
            final_equity = equity[-1].get("equity", 0.0)
            initial_equity = equity[0].get("equity", 0.0) if equity else 0.0
            total_return = final_equity - initial_equity
        
        return {
            "total_return": total_return,
            "num_trades": total,
            "winrate": winrate,
            "max_drawdown": max_dd,
        }

    @staticmethod
    def _max_drawdown(equity: List[Dict]) -> float:
        if not equity:
            return 0.0
        peak = equity[0].get("equity", 0.0)
        max_dd = 0.0
        for point in equity:
            val = point.get("equity", 0.0)
            if val > peak:
                peak = val
            dd = peak - val
            if dd > max_dd:
                max_dd = dd
        return max_dd

    @staticmethod
    def to_csv(equity: List[Dict], path: str) -> None:
        """Export equity curve to CSV"""
        import csv
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "price", "equity", "realized_pnl", "unrealized_pnl"])
            writer.writeheader()
            for p in equity:
                writer.writerow({
                    "timestamp": p.get("timestamp", ""),
                    "price": p.get("price", 0.0),
                    "equity": p.get("equity", 0.0),
                    "realized_pnl": p.get("realized_pnl", 0.0),
                    "unrealized_pnl": p.get("unrealized_pnl", 0.0),
                })

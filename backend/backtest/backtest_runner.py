"""
PROJECT PREDATOR - BacktestRunner
CLI entry (simple argparse).
"""
import argparse
from backend.simulation.historical_data_loader import HistoricalDataLoader
from backend.backtest.backtest_engine import BacktestEngine


def main():
    parser = argparse.ArgumentParser(description="PROJECT PREDATOR Backtest Runner (FAZ 3, stub)")
    parser.add_argument("--data", required=True, help="Path to CSV with OHLCV")
    parser.add_argument("--strategy", default="fake_trend", choices=["fake_trend", "fake_random"])
    parser.add_argument("--speed", type=float, default=100.0, help="Time speed multiplier")
    args = parser.parse_args()

    loader = HistoricalDataLoader()
    candles = loader.load_csv(args.data)
    engine = BacktestEngine(candles, strategy_name=args.strategy, speed=args.speed)
    report = engine.run()
    print("Backtest complete")
    print(f"Trades: {len(report['trades'])}")
    print(f"Total return (stub): {report['total_return']}")


if __name__ == "__main__":
    main()

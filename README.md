# Project-Predator

Trading Operating System (FAZ 1-2 complete). Current tag: `FAZ-2-STABLE`.

## Status
- Phase 0: ✅ Constitution
- Phase 1: ✅ Core Platform Skeleton
- Phase 2: ✅ Agent Skeletons (Blueprint compliant)
- Phase 3: ✅ Fake Data Flow (Simulation & Backtesting)
- Phase 4+: ⏳ Not started

## Quick Start
```bash
pip install -r requirements.txt
python demo.py               # 10s smoke demo (starts/stops everything)
python -m backend.main       # run system
# in another shell
curl http://localhost:8000/health
```

## Tests
```bash
python -m pytest tests/ -v
```

## Architecture (Phase 1)
- CoreEngine (state machine)
- EventBus (pub/sub)
- Scheduler (tick/heartbeat)
- Registry (component lookup)
- PolicyGuard (CRO gate)
- FakeExecutor (simulated fills)
- Monitoring: logging + /health

## Agents (Phase 2, all STUB/SKELETON)
- MarketScannerAgent: TICK → log "scanning market"
- DataEngineeringAgent: TICK → log "processing data"
- ExecutionAgent: ORDER_REQUEST → log "would execute"
- PortfolioManagerAgent: TICK → log "checking portfolio"
- CRORiskAgent: RISK_CHECK → log "risk check"
- PerformanceKPIAgent: ORDER_FILLED → log "recording KPI"
- ASPAAgent: HEARTBEAT (placeholder) → log "analyzing strategy"
- RRSAgent: HEARTBEAT → log "infra OK"

## Simulation & Backtesting (Phase 3)
- **TimeSource**: Realtime/Accelerated/Backtest time modes
- **HistoricalDataLoader**: CSV/Parquet OHLCV data loading
- **HistoricalReplayer**: Replay historical candles with speed control
- **FakeMarket**: Simulated market with orderbook stub
- **FakePriceFeed**: Converts candles to PRICE_UPDATE events
- **FakeStrategy**: Random and trend-following strategies (stub)
- **BacktestEngine**: End-to-end backtest orchestration
- **BacktestReport**: Performance metrics (return, drawdown, winrate)

### Running Backtests
```bash
# Run backtest via CLI
python -m backend.backtest.backtest_runner --data data.csv --strategy fake_trend --speed 100

# Or programmatically
from backend.backtest.backtest_engine import BacktestEngine
from backend.simulation.historical_data_loader import HistoricalDataLoader

loader = HistoricalDataLoader()
candles = loader.load_csv("data.csv")
engine = BacktestEngine(candles, strategy_name="fake_random", speed=100.0, seed=42)
result = engine.run()
print(f"Total Return: {result['total_return']}, Trades: {result['num_trades']}")
```

## Governance
- No real trading, no real exchanges, no strategies
- Event-driven only (via EventBus)
- PolicyGuard must gate critical actions
- Logging and observability required
- Compliant with `AI_RULES.md` and `docs/constitution/MASTER.md`

## Tests (Phase 3)
```bash
# Run Phase 3 simulation tests (T1-T5)
python -m pytest tests/test_phase3_simulation.py -v

# T1: Replay 1 day of BTC data
# T2: Backtest 1 year of data
# T3: Switch strategies (fake_random vs fake_trend)
# T4: Accelerated time (1 year in minutes)
# T5: Deterministic replay (same seed → same results)
```

## Next
- Phase 4: Paper Trading (real data, fake money)
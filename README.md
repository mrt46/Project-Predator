# Project-Predator

Trading Operating System (FAZ 1-2 complete). Current tag: `FAZ-2-STABLE`.

## Status
- Phase 0: ✅ Constitution
- Phase 1: ✅ Core Platform Skeleton
- Phase 2: ✅ Agent Skeletons (Blueprint compliant)
- Phase 3+: ⏳ Not started

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

## Governance
- No real trading, no real exchanges, no strategies
- Event-driven only (via EventBus)
- PolicyGuard must gate critical actions
- Logging and observability required
- Compliant with `AI_RULES.md` and `docs/constitution/MASTER.md`

## Next
- Phase 3: Fake Data Flow (simulation: fake market → fake strategy → fake orders → fake fills)
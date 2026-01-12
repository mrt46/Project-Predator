================================================================================
PROJECT PREDATOR
PHASE 1–2–3 ENGINEERING BLUEPRINT
================================================================================

This document defines in extreme detail:
- FAZ 1: Core Platform Skeleton
- FAZ 2: Agent Skeletons
- FAZ 3: Fake Data Flow

Each phase includes:
- Goal
- Architecture
- Folder structure
- Responsibilities
- Test scenarios
- Exit criteria

================================================================================
FAZ 1 – CORE PLATFORM SKELETON
================================================================================

GOAL:
Build a living but non-trading Trading OS core.

- No real exchanges
- No real strategies
- No real money
- Only platform skeleton

WHAT MUST EXIST:
- CoreEngine (state machine)
- EventBus (pub/sub)
- Scheduler (tick generator)
- Registry (components)
- PolicyGuard (CRO gate)
- FakeExecution adapter
- Logging
- Health & metrics endpoints
- Dockerized runtime

--------------------------------
FOLDER STRUCTURE
--------------------------------

backend/
  core/
    engine.py
    event_bus.py
    registry.py
    scheduler.py
    policy_guard.py
    config.py

  platform/
    selector.py
    scoring.py
    capital.py

  execution/
    base.py
    fake_executor.py

  monitor/
    health.py
    metrics.py
    logging.py

  interfaces/
    engine.py
    strategy.py
    agent.py

  main.py

docker/
  Dockerfile
  docker-compose.yml

--------------------------------
RESPONSIBILITIES
--------------------------------

CoreEngine:
- State machine: INIT → BOOTING → IDLE → RUNNING → HALTED
- Boots system
- Starts scheduler
- Publishes Tick events
- Owns EventBus, Registry, PolicyGuard

EventBus:
- publish(event)
- subscribe(event, handler)

Scheduler:
- Emits Tick every N seconds

Registry:
- Keeps list of engines, strategies, agents

PolicyGuard:
- Every action must pass here
- Currently stub (allow/deny switch)

Execution:
- FakeExecutor returns fake FILLED

Monitor:
- /health endpoint
- Basic metrics counters

--------------------------------
TEST SCENARIOS (FAZ 1)
--------------------------------

T1: System Boot Test
- Start container
- Expect state transitions: INIT → BOOTING → IDLE → RUNNING

T2: Tick Flow Test
- Wait 3 seconds
- Expect at least 3 Tick events published

T3: PolicyGuard Gate Test
- Set guard.block_all = True
- Attempt any action
- Verify action is rejected

T4: Fake Execution Test
- Send fake order
- Expect fake FILLED result

T5: Health Endpoint Test
- Call /health
- Expect:
  {
    status: "ok",
    state: "RUNNING"
  }

--------------------------------
EXIT CRITERIA (FAZ 1)
--------------------------------

[ ] System boots in Docker
[ ] /health works
[ ] Tick events flow
[ ] PolicyGuard is in the call chain
[ ] FakeExecutor works
[ ] NO real exchange code exists
[ ] NO strategies exist

If all true → FAZ 1 COMPLETE.

================================================================================
FAZ 2 – AGENT SKELETONS
================================================================================

GOAL:
Implement EMPTY but RUNNING agent shells.

- No intelligence
- No trading logic
- Only:
  - Event subscriptions
  - Heartbeats
  - Logging
  - Message passing

AGENTS TO IMPLEMENT:

- MarketScannerAgent
- DataEngineeringAgent
- ExecutionAgent
- PortfolioManagerAgent
- CRORiskAgent
- PerformanceKPIAgent
- ASPAAgent
- RRSAgent (Infra Sentinel)

--------------------------------
FOLDER STRUCTURE
--------------------------------

backend/
  agents/
    market_scanner/
      agent.py
    data_engineering/
      agent.py
    execution/
      agent.py
    portfolio/
      agent.py
    cro/
      agent.py
    performance/
      agent.py
    aspa/
      agent.py
    rrs/
      agent.py

  core/
  platform/
  execution/
  monitor/
  interfaces/

--------------------------------
AGENT BASE INTERFACE

All agents MUST:
- Implement on_event(event)
- Subscribe to EventBus
- Emit logs
- Emit heartbeats

--------------------------------
RESPONSIBILITIES (FAZ 2 LEVEL)

MarketScanner:
- On Tick → log "scanning market"

DataEngineering:
- On Tick → log "processing data"

ExecutionAgent:
- On OrderRequest → log "would execute"

PortfolioManager:
- On Tick → log "checking portfolio"

CRO:
- On RiskEvent → log "risk check"

Performance:
- On ExecutionResult → log "recording KPI"

ASPA:
- On StrategyReviewEvent → log "analyzing strategy"

RRS:
- Every N seconds → log "infra OK"

--------------------------------
TEST SCENARIOS (FAZ 2)

T1: Agent Registration Test
- On startup, all agents appear in Registry

T2: Event Subscription Test
- Publish Tick
- Verify:
  - MarketScanner reacts
  - DataEngineering reacts
  - Portfolio reacts

T3: Execution Flow Test
- Publish fake OrderRequest
- ExecutionAgent logs reception
- FakeExecutor returns FILLED
- PerformanceAgent logs KPI event

T4: CRO Hook Test
- Publish RiskEvent
- CRO agent logs response

T5: Infra Heartbeat Test
- RRS logs periodic heartbeat

--------------------------------
EXIT CRITERIA (FAZ 2)

[ ] All agents exist as modules
[ ] All agents register to EventBus
[ ] All agents receive events
[ ] All agents log activity
[ ] Still NO real trading logic
[ ] Still NO real exchange code

If all true → FAZ 2 COMPLETE.

================================================================================
FAZ 3 – FAKE DATA FLOW (END-TO-END SIMULATION)
================================================================================

GOAL:
Simulate the ENTIRE SYSTEM with FAKE DATA.

- Fake market data
- Fake signals
- Fake orders
- Fake fills
- Real internal flow

--------------------------------
NEW MODULES

backend/
  simulation/
    fake_market.py
    fake_price_feed.py
    fake_strategy.py

--------------------------------
FLOW

FakeMarket:
- Emits FakeCandle events

MarketScanner:
- Receives FakeCandle
- Emits MarketRegimeEvent

FakeStrategy:
- Listens to MarketRegimeEvent
- Emits OrderRequest

ExecutionAgent:
- Receives OrderRequest
- Sends to FakeExecutor

FakeExecutor:
- Emits ExecutionResult

PerformanceAgent:
- Records KPI

PortfolioManager:
- Updates fake portfolio state

--------------------------------
TEST SCENARIOS (FAZ 3)

T1: Fake Market Data Flow
- FakeMarket emits candles
- MarketScanner receives them

T2: Strategy Reaction Test
- FakeStrategy receives regime
- Emits OrderRequest

T3: Full Trade Cycle Test
- OrderRequest →
- ExecutionAgent →
- FakeExecutor →
- ExecutionResult →
- PerformanceAgent →
- PortfolioManager

T4: End-to-End Loop Test
- Run system for 60 seconds
- Expect:
  - Multiple fake trades
  - No crashes
  - Continuous logs

T5: Kill-Switch Simulation Test
- Simulate RiskEvent
- CRO blocks execution
- Verify no more orders pass

--------------------------------
EXIT CRITERIA (FAZ 3)

[ ] Fake market produces data
[ ] Full signal → order → fill → KPI loop works
[ ] CRO can block flow
[ ] System runs 1+ hour without crash
[ ] Still NO real exchange
[ ] Still NO real money

If all true → FAZ 3 COMPLETE.

================================================================================
FINAL NOTE
================================================================================

Only after FAZ 3 is complete:

→ FAZ 4 (Paper Trading) may begin.

Any attempt to skip phases:
→ Is a SYSTEM VIOLATION.

================================================================================
END OF DOCUMENT
================================================================================
# PROJECT PREDATOR - Phase 4 Task Breakdown

## Phase 4: Paper Trading + Chaos Engineering

**Goal**: Prove system survivability under chaos, not profitability.

---

## PHASE 4.1: Paper Trading Infrastructure

### 4.1.1: Paper Exchange
- [ ] `backend/paper/paper_exchange.py`
  - Order book simulation
  - Slippage model
  - Partial fills
  - Order rejections
  - Latency simulation
- [ ] `backend/paper/paper_orderbook.py`
  - Bid/ask levels
  - Depth simulation
  - Spread calculation
- [ ] `backend/paper/paper_latency.py`
  - Network latency simulation
  - Exchange response delays

### 4.1.2: Paper Broker
- [ ] `backend/paper/paper_broker.py`
  - Interface between ExecutionAgent and PaperExchange
  - Order routing
  - Fill reporting
  - Error handling

### 4.1.3: Paper Portfolio
- [ ] `backend/paper/paper_portfolio.py`
  - Position tracking
  - PnL calculation
  - Margin management
  - Exposure limits
- [ ] `backend/paper/paper_margin.py`
  - Margin requirements
  - Margin calls
  - Leverage limits

### 4.1.4: Integration
- [ ] Wire PaperExchange to ExecutionAgent
- [ ] Wire PaperPortfolio to PortfolioManagerAgent
- [ ] Replace FakeMarket with PaperExchange
- [ ] Test end-to-end paper trading flow

---

## PHASE 4.2: Time Acceleration (TimeWarp)

### 4.2.1: TimeWarp Core
- [ ] `backend/simulation/time_warp.py`
  - Speed multiplier control
  - Simulated time tracking
  - Pause/resume functionality
  - Deterministic time progression

### 4.2.2: Scenario Clock
- [ ] `backend/simulation/scenario_clock.py`
  - Schedule events in simulated time
  - Priority queue for chaos events
  - Integration with TimeWarp

### 4.2.3: Integration
- [ ] Replace TimeSource with TimeWarp
- [ ] Update all components to use TimeWarp
- [ ] Test accelerated time (1 second = 1 minute simulated)

---

## PHASE 4.3: Chaos Engine Foundation

### 4.3.1: Chaos Bus
- [ ] `backend/chaos/chaos_bus.py`
  - Event bus for chaos events
  - Separate from main EventBus
  - Chaos event types

### 4.3.2: Chaos Events
- [ ] `backend/chaos/chaos_events.py`
  - Define chaos event types
  - Event data structures
  - Event priorities

### 4.3.3: Chaos Config
- [ ] `backend/chaos/chaos_config.py`
  - Chaos intensity levels
  - Scenario schedules
  - Fault injection rates

---

## PHASE 4.4: Fault Injection System

### 4.4.1: Fault Injector
- [ ] `backend/chaos/fault_injector.py`
  - Kill processes
  - Delay messages
  - Corrupt responses
  - Drop events
  - Freeze components
  - Network partitions

### 4.4.2: Integration Points
- [ ] EventBus fault injection
- [ ] Agent fault injection
- [ ] Exchange fault injection
- [ ] Strategy fault injection

---

## PHASE 4.5: Scenario System

### 4.5.1: Scenario Library
- [ ] `backend/chaos/scenario_library.py`
  - Market chaos scenarios (flash crash, bear market, mania)
  - Infra chaos scenarios (process crash, memory leak, event lag)
  - Exchange chaos scenarios (timeout, ghost fill, partial fills)
  - Strategy chaos scenarios (silent death, tail loss)
  - AI chaos scenarios (overfitting, over-aggression)
  - Governance chaos scenarios (scoring corruption, CRO loss)

### 4.5.2: Scenario Runner
- [ ] `backend/chaos/scenario_runner.py`
  - Load scenarios from library
  - Execute scenario steps
  - Monitor scenario progress
  - Report scenario results

### 4.5.3: Chaos Engine
- [ ] `backend/chaos/chaos_engine.py`
  - Orchestrate chaos scenarios
  - Decide when to inject faults
  - Select target subsystems
  - Work independently from trading logic

---

## PHASE 4.6: State Validation

### 4.6.1: State Invariants
- [ ] `backend/validation/state_invariants.py`
  - Define system invariants
  - Check consistency rules
  - Detect state corruption

### 4.6.2: Consistency Checker
- [ ] `backend/validation/consistency_checker.py`
  - Periodic consistency checks
  - Execution/Portfolio reconciliation
  - Position validation
  - PnL validation

### 4.6.3: Reconciliation
- [ ] `backend/validation/reconciliation.py`
  - Compare ExecutionAgent vs PortfolioManagerAgent
  - Detect desync
  - Auto-correct or halt

### 4.6.4: Post-Mortem
- [ ] `backend/validation/post_mortem.py`
  - Generate post-mortem reports
  - Analyze failures
  - Log state snapshots

---

## PHASE 4.7: Real Market Data Integration

### 4.7.1: Market Data Source
- [ ] Integrate real market data feed (paper mode)
  - Historical data replay
  - Real-time data simulation
  - Multiple symbols support

### 4.7.2: Data Pipeline
- [ ] Connect market data to PaperExchange
- [ ] Update price feeds
- [ ] Handle data gaps

---

## PHASE 4.8: Test Campaigns

### 4.8.1: Campaign 1 (30 days, light chaos)
- [ ] Setup 30-day simulation
- [ ] Light chaos scenarios
- [ ] Monitor system behavior
- [ ] Generate report

### 4.8.2: Campaign 2 (90 days, medium chaos)
- [ ] Setup 90-day simulation
- [ ] Medium chaos scenarios
- [ ] Monitor system behavior
- [ ] Generate report

### 4.8.3: Campaign 3 (180 days, heavy chaos)
- [ ] Setup 180-day simulation
- [ ] Heavy chaos scenarios
- [ ] Monitor system behavior
- [ ] Generate report

### 4.8.4: Campaign 4 (365 days, extreme chaos)
- [ ] Setup 365-day simulation
- [ ] Extreme chaos scenarios
- [ ] Monitor system behavior
- [ ] Generate report

---

## PHASE 4.9: Observability & Metrics

### 4.9.1: Core Metrics
- [ ] System uptime %
- [ ] Kill-switch trigger count
- [ ] Recovery time after halt
- [ ] Max drawdown per pool
- [ ] State corruption incidents (target: 0)
- [ ] Execution/Portfolio mismatches
- [ ] Event loss count

### 4.9.2: Chaos Metrics
- [ ] Number of scenarios injected
- [ ] % survived without human intervention
- [ ] Mean time to recovery (MTTR)

### 4.9.3: Reporting
- [ ] Real-time dashboard
- [ ] Daily reports
- [ ] Campaign summaries
- [ ] Post-mortem reports

---

## PHASE 4.10: Integration & Testing

### 4.10.1: End-to-End Integration
- [ ] Wire all Phase 4 components
- [ ] Test paper trading flow
- [ ] Test chaos injection
- [ ] Test state validation

### 4.10.2: Unit Tests
- [ ] PaperExchange tests
- [ ] ChaosEngine tests
- [ ] FaultInjector tests
- [ ] ScenarioRunner tests
- [ ] State validation tests

### 4.10.3: Integration Tests
- [ ] Paper trading integration tests
- [ ] Chaos scenario integration tests
- [ ] Recovery tests
- [ ] Kill-switch tests

---

## PASS/FAIL CRITERIA

### FAIL if:
- [ ] System trades while blind
- [ ] Kill-switch fails
- [ ] Portfolio state becomes inconsistent
- [ ] A single strategy kills the system
- [ ] Logs cannot explain what happened

### PASS if:
- [ ] System halts itself many times
- [ ] System recovers many times
- [ ] Strategies die, system lives
- [ ] No state corruption
- [ ] No uncontrolled trading

---

## EXIT CRITERIA (FAZ 4)

- [ ] Paper trading stable for long runs
- [ ] Chaos scenarios executed successfully
- [ ] Kill-switch proven in many situations
- [ ] CRO authority proven
- [ ] No state corruption incidents
- [ ] Full logs + post-mortem reports exist
- [ ] Team trusts the system more than before

**Only if ALL true → FAZ 5 (Small real capital) may begin.**

---

## ESTIMATED TIMELINE

- Phase 4.1-4.2: Paper Trading + TimeWarp (Week 1-2)
- Phase 4.3-4.4: Chaos Engine + Fault Injection (Week 3-4)
- Phase 4.5-4.6: Scenarios + State Validation (Week 5-6)
- Phase 4.7-4.8: Real Data + Test Campaigns (Week 7-10)
- Phase 4.9-4.10: Observability + Integration (Week 11-12)

**Total: ~12 weeks for full Phase 4 implementation**

---

Last Updated: 2026-01-14

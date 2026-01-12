================================================================================
PROJECT PREDATOR
PHASE 4 – CHAOS ENGINE & SCENARIO SYSTEM
TECHNICAL ARCHITECTURE SKELETON
================================================================================

PURPOSE
--------------------------------------------------------------------------------
This document defines the FULL technical architecture for:

- ChaosEngine
- Scenario System
- Fault Injection Framework
- Paper Exchange Simulation
- Time Acceleration / TimeWarp
- 1-Year Accelerated Torture Testing

This phase exists to PROVE:
- The system never loses control
- Kill-switch works
- CRO authority is absolute
- State consistency is preserved
- The platform survives hell

================================================================================
HIGH LEVEL ARCHITECTURE
================================================================================

                        +----------------------+
                        |   ScenarioLibrary    |
                        +----------+-----------+
                                   |
                                   v
+------------------+      +----------------------+      +---------------------+
|   TimeWarp       | ---> |   ScenarioClock      | ---> |   ScenarioRunner    |
+------------------+      +----------+-----------+      +----------+----------+
                                                              |
                                                              v
                                                      +------------------+
                                                      |   ChaosEngine    |
                                                      +---------+--------+
                                                                |
                                                                v
+------------------+     +-------------------+     +---------------------+
| FaultInjector    | <-- |   ChaosBus        | --> |   System Components |
+------------------+     +-------------------+     | (Agents, Exchange,  |
                                                     |  EventBus, Infra)  |
                                                     +---------------------+

================================================================================
FOLDER STRUCTURE
================================================================================

backend/
  chaos/
    chaos_engine.py
    scenario_runner.py
    scenario_clock.py
    scenario_library.py
    fault_injector.py
    chaos_bus.py
    chaos_events.py
    chaos_config.py

  paper/
    paper_exchange.py
    paper_orderbook.py
    paper_broker.py
    paper_portfolio.py
    paper_margin.py
    paper_latency.py

  simulation/
    time_warp.py
    simulated_clock.py
    historical_data_replayer.py

  validation/
    state_invariants.py
    consistency_checker.py
    reconciliation.py
    post_mortem.py

================================================================================
CORE COMPONENTS – DETAILED RESPONSIBILITIES
================================================================================

--------------------------------------------------------------------------------
1) TimeWarp (simulation/time_warp.py)
--------------------------------------------------------------------------------

Purpose:
- Control simulated time speed.
- Allow:
  - 1 second real = N minutes simulated
  - Pause / resume
  - Fast-forward
  - Deterministic replay

API:
- set_speed(multiplier)
- now() -> simulated_timestamp
- sleep(simulated_duration)
- freeze()
- resume()

Rules:
- ALL time in FAZ 4 must come from TimeWarp, not system clock.

--------------------------------------------------------------------------------
2) ScenarioClock (chaos/scenario_clock.py)
--------------------------------------------------------------------------------

Purpose:
- Schedule chaos events in simulated time.

Responsibilities:
- Maintain priority queue:
  (timestamp, scenario_event)
- On each tick:
  - Ask TimeWarp for current time
  - Emit due events to ScenarioRunner

API:
- schedule(event, at_time)
- tick()

--------------------------------------------------------------------------------
3) ScenarioLibrary (chaos/scenario_library.py)
--------------------------------------------------------------------------------

Purpose:
- Store reusable scenario definitions.

Scenario Types:

- MarketChaosScenario
- InfraChaosScenario
- ExchangeChaosScenario
- StrategyChaosScenario
- AIGovernanceChaosScenario
- DataCorruptionScenario

Each scenario defines:
- name
- duration
- intensity
- target_components
- steps[] (timeline of injections)

Example:
- FlashCrashScenario:
  t+0s: price shock
  t+10s: spread explosion
  t+30s: liquidity drop

--------------------------------------------------------------------------------
4) ScenarioRunner (chaos/scenario_runner.py)
--------------------------------------------------------------------------------

Purpose:
- Execute scenarios.

Responsibilities:
- Load scenario from library
- Translate steps into:
  ChaosEvents
- Send to ChaosEngine

API:
- start_scenario(scenario)
- stop_scenario(id)
- tick()

--------------------------------------------------------------------------------
5) ChaosEngine (chaos/chaos_engine.py)
--------------------------------------------------------------------------------

Purpose:
- Orchestrator of all chaos.

Responsibilities:
- Receive ChaosEvents
- Decide:
  - Which FaultInjector to call
  - Which subsystem to attack
- Enforce:
  - No chaos may bypass PolicyGuard or CRO logic

API:
- on_chaos_event(event)
- enable()
- disable()

Rules:
- ChaosEngine is OUTSIDE trading logic.
- It attacks the system like nature.

--------------------------------------------------------------------------------
6) ChaosBus (chaos/chaos_bus.py)
--------------------------------------------------------------------------------

Purpose:
- Separate event bus for chaos events.

Why:
- So chaos system cannot be confused with trading events.

Events:
- KillProcess
- DelayEventBus
- CorruptExchangeResponse
- FreezeAgent
- DropMessages
- MemoryPressure
- CPUThrottle

--------------------------------------------------------------------------------
7) FaultInjector (chaos/fault_injector.py)
--------------------------------------------------------------------------------

Purpose:
- Actually perform the attack.

Capabilities:

- kill_process(component)
- freeze_component(component, duration)
- delay_messages(component, ms)
- drop_messages(component, percentage)
- corrupt_payload(component, probability)
- inject_latency(component, distribution)
- simulate_memory_pressure(component)
- simulate_disk_full()
- simulate_network_partition()

Rules:
- Every injection MUST be logged.
- Every injection MUST be reversible.

--------------------------------------------------------------------------------
8) PaperExchange Stack
--------------------------------------------------------------------------------

paper_exchange.py:
- Simulates:
  - Order placement
  - Cancel
  - Modify
  - Partial fills
  - Rejections
  - Slippage
  - Spread dynamics

paper_orderbook.py:
- Level 2 book simulation

paper_latency.py:
- Random / scenario-driven latency

paper_broker.py:
- Interface between ExecutionAgent and PaperExchange

paper_portfolio.py:
- Tracks:
  - Positions
  - PnL
  - Exposure
  - Margin usage

paper_margin.py:
- Simulates:
  - Liquidation
  - Margin calls

--------------------------------------------------------------------------------
9) Validation & Consistency Layer
--------------------------------------------------------------------------------

validation/state_invariants.py:
- Defines invariants:
  - No negative balances
  - Positions match executions
  - Cash + positions = equity
  - No phantom orders

validation/consistency_checker.py:
- Periodically checks invariants

validation/reconciliation.py:
- Reconciles:
  - Execution history
  - Portfolio state
  - Exchange state

validation/post_mortem.py:
- After any crash:
  - Generates report
  - Explains:
    - What happened
    - Why
    - Which invariant broke

================================================================================
SIMULATION FLOW (END TO END)
================================================================================

HistoricalDataReplayer
        ↓
PaperExchange price feed
        ↓
MarketScannerAgent
        ↓
Strategies (paper)
        ↓
OrderRequest
        ↓
ExecutionAgent
        ↓
PaperBroker
        ↓
PaperExchange
        ↓
ExecutionResult
        ↓
PortfolioManager + Performance

In parallel:

TimeWarp → ScenarioClock → ScenarioRunner → ChaosEngine → FaultInjector
                                     ↓
                               System gets attacked

================================================================================
CHAOS CAMPAIGNS
================================================================================

Campaign 1: 30 simulated days – light chaos
Campaign 2: 90 simulated days – medium chaos
Campaign 3: 180 simulated days – heavy chaos
Campaign 4: 365 simulated days – extreme chaos

================================================================================
MANDATORY TEST SCENARIOS
================================================================================

T1: 48h Flash Crash
- Expect:
  - Global kill-switch
  - Trading halted
  - System alive

T2: 3 months bear market
- Expect:
  - Strategy decay detection
  - Rotation / disable

T3: Exchange API chaos
- Expect:
  - No duplicate orders
  - Reconciliation fixes state

T4: Memory leak simulation
- Expect:
  - RRS detects
  - CRO halts trading

T5: Process kill storm
- Expect:
  - Auto-restart
  - No state corruption

T6: AI insanity
- Expect:
  - CRO blocks
  - AutonomyPolicy holds

T7: Data corruption
- Expect:
  - Invariant violation detected
  - System halts

================================================================================
OBSERVABILITY
================================================================================

Everything must be logged:

- Every chaos injection
- Every kill-switch
- Every state transition
- Every invariant violation

Metrics:

- Uptime %
- MTTR (mean time to recovery)
- Number of chaos events survived
- Number of invariants broken (target = 0)

================================================================================
EXIT CRITERIA (FAZ 4)
================================================================================

[ ] 365 simulated days completed
[ ] Dozens of chaos scenarios survived
[ ] Kill-switch proven many times
[ ] No unrecovered state corruption
[ ] Reconciliation always succeeds
[ ] Post-mortems explain every failure
[ ] Team trusts the system more than before

Only if ALL true:
→ FAZ 5 (Small real capital) may begin.

================================================================================
FINAL PHILOSOPHICAL RULE
================================================================================

This phase does not ask:
"Did we make money?"

It asks:
"Did we deserve to survive?"

================================================================================
END OF DOCUMENT
================================================================================
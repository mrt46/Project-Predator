================================================================================
PROJECT PREDATOR
PHASE 4 – PAPER TRADING + CHAOS ENGINEERING MASTER PLAN
================================================================================

Purpose:
This phase is NOT about making money.
This phase is about proving that the system:
- Does not lose control
- Does not lie about its state
- Does not trade blindly
- Does not die under chaos

This phase simulates ~1 YEAR of operation using:
- Real market data (paper)
- Fake money
- Chaos injections
- Infrastructure failures
- Exchange failures
- Strategy failures
- AI failures

================================================================================
HIGH LEVEL GOALS
================================================================================

1. Validate survivability, not profitability.
2. Prove that:
   - Kill-switch works
   - CRO authority is absolute
   - System can stop itself
   - System can recover
3. Detect:
   - State corruption
   - Desync between execution and portfolio
   - Runaway trading
   - Silent failures
4. Stress test:
   - Platform
   - Engines
   - Strategies
   - Agents
   - Infrastructure
   - Decision loops

================================================================================
TIME MODEL
================================================================================

- Simulation time target: 365 days
- Real time execution:
  - Accelerated mode
  - Example:
    - 1 real second = 1 simulated minute
    - 1 real hour ≈ 60 simulated hours
- Total run:
  - Several continuous runs
  - Each run = weeks/months of simulated time

================================================================================
ARCHITECTURE ADDITIONS (FAZ 4)
================================================================================

New modules:

backend/
  chaos/
    chaos_engine.py
    scenario_runner.py
    scenario_library.py
    fault_injector.py

  paper/
    paper_exchange.py
    paper_broker.py
    paper_portfolio.py

  simulation/
    time_warp.py
    scenario_clock.py

--------------------------------------------------------------------------------
COMPONENT RESPONSIBILITIES
--------------------------------------------------------------------------------

ChaosEngine:
- Orchestrates chaos scenarios
- Decides:
  - When to inject faults
  - Which subsystem to attack
- Works independently from trading logic

ScenarioRunner:
- Loads scenarios from ScenarioLibrary
- Schedules them on SimulationClock

ScenarioLibrary:
- Contains:
  - Market chaos scenarios
  - Infra chaos scenarios
  - Exchange chaos scenarios
  - Strategy chaos scenarios
  - AI chaos scenarios

FaultInjector:
- Can:
  - Kill processes
  - Delay messages
  - Corrupt responses
  - Drop events
  - Freeze components

PaperExchange:
- Mimics exchange behavior:
  - Order book
  - Slippage
  - Partial fills
  - Rejections
  - Latency

PaperBroker:
- Interface between ExecutionAgent and PaperExchange

PaperPortfolio:
- Tracks positions, PnL, margin, exposure

TimeWarp:
- Controls accelerated time

ScenarioClock:
- Allows scheduling events in simulated time

================================================================================
CHAOS SCENARIO CATEGORIES
================================================================================

--------------------------------
A) MARKET CHAOS
--------------------------------

A1: Flash Crash
- One asset: -30% in minutes
- Others: -10% to -20%
Test:
- Global kill-switch?
- Positions closed?
- Trading halted?

A2: Prolonged Bear Market
- 3 simulated months of drawdown
Test:
- Strategy scores decay?
- Strategies disabled?
- Capital preserved?

A3: Parabolic Mania
- Volatility 5x
- Fake breakouts
Test:
- Overtrading?
- Risk limits respected?

--------------------------------
B) STRATEGY CHAOS
--------------------------------

B1: Silent Strategy Death
- Strategy slowly loses edge for 2 months
Test:
- FreshnessScore detects decay?
- Strategy demoted/killed?

B2: Explosive Tail Loss
- One strategy: -15% in one day
Test:
- Only that strategy dies?
- System survives?

--------------------------------
C) INFRA CHAOS
--------------------------------

C1: Process Crash
- Kill random agent
Test:
- Auto-restart?
- System state consistent?

C2: Memory Leak Simulation
- RAM usage grows
Test:
- RRS detects?
- CRO halts trading?

C3: Event Bus Lag
- Delay all events by 5–10 seconds
Test:
- Execution safety?
- Double orders?

--------------------------------
D) EXCHANGE CHAOS
--------------------------------

D1: API Timeout
- Order sent, no response
Test:
- Duplicate protection?
- Idempotency?

D2: Ghost Fill
- Exchange says FILLED but actually not
Test:
- Reconciliation catches it?
- Portfolio corrected?

D3: Partial Fill Storm
- Only 30–40% fills
Test:
- Position sizing correct?
- Risk limits respected?

--------------------------------
E) AI / DECISION CHAOS
--------------------------------

E1: AI Overfitting Loop
- AI keeps proposing same broken idea
Test:
- Family killed?
- Blacklist applied?

E2: AI Over-Aggression
- AI proposes 10x more trades
Test:
- CRO blocks?
- AutonomyPolicy enforced?

--------------------------------
F) GOVERNANCE CHAOS
--------------------------------

F1: Scoring Corruption
- Feed wrong scores
Test:
- Sanity checks?
- Fallback to safe mode?

F2: CRO Communication Loss
- CRO agent temporarily unavailable
Test:
- System freezes trading?

================================================================================
OBSERVABILITY & METRICS
================================================================================

Core Metrics:
- System uptime %
- Number of global kill-switch triggers
- Number of local kills
- Recovery time after halt
- Max DD per pool
- State corruption incidents (target: 0)
- Execution/Portfolio mismatches
- Event loss count

Chaos Metrics:
- Number of scenarios injected
- % survived without human intervention
- Mean time to recovery (MTTR)

================================================================================
TEST CAMPAIGNS
================================================================================

Campaign 1:
- 30 simulated days
- Light chaos

Campaign 2:
- 90 simulated days
- Medium chaos

Campaign 3:
- 180 simulated days
- Heavy chaos

Campaign 4:
- 365 simulated days
- Extreme chaos

================================================================================
PASS / FAIL CRITERIA
================================================================================

FAIL if:
- System trades while blind
- Kill-switch fails
- Portfolio state becomes inconsistent
- A single strategy kills the system
- Logs cannot explain what happened

PASS if:
- System halts itself many times
- System recovers many times
- Strategies die, system lives
- No state corruption
- No uncontrolled trading

================================================================================
EXIT CRITERIA (FAZ 4)
================================================================================

[ ] Paper trading stable for long runs
[ ] Chaos scenarios executed successfully
[ ] Kill-switch proven in many situations
[ ] CRO authority proven
[ ] No state corruption incidents
[ ] Full logs + post-mortem reports exist
[ ] Team trusts the system more than before

Only if ALL true:
→ FAZ 5 (Small real capital) may begin.

================================================================================
PHILOSOPHICAL FINAL RULE
================================================================================

This phase exists to answer one question:

> "Does this system deserve real money?"

If the answer is not a confident YES:
→ Go back and fix the system.

================================================================================
END OF DOCUMENT
================================================================================
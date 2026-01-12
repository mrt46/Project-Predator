================================================================================
PROJECT PREDATOR
MASTER BLUEPRINT & SYSTEM CONSTITUTION v2
================================================================================

Status: LOCKED MASTER DOCUMENT  
This document is the single source of truth for the entire system.  
All code, agents, AI, and future development MUST obey this document.

================================================================================
1. PROJECT PURPOSE
================================================================================

PROJECT PREDATOR is an autonomous, multi-engine, multi-strategy, risk-first
trading platform.

Goal:
- Grow capital aggressively but controllably
- Target: 10,000€ → 1,000,000€
- Horizon: 3–5 years

This is:
- NOT a toy bot
- NOT a signal system
- NOT a single-strategy system

This is:
- A professional, hedge-fund-grade autonomous trading platform (Trading OS).

================================================================================
2. CORE PRINCIPLES (NON-NEGOTIABLE)
================================================================================

1. Multi-strategy and multi-engine is mandatory.
2. Risk discipline ALWAYS overrides profit.
3. The system must be able to stop itself.
4. No strategy and no engine is trusted forever.
5. AI is an operator, not a ruler.
6. All decisions must be explainable via logs.
7. The system must survive before it thrives.
8. Autonomy is gradual and gated.
9. Profit NEVER justifies loss of control.

================================================================================
3. PHASED DEVELOPMENT MODEL
================================================================================

FAZ 0: Documentation & Constitution  
FAZ 1: Core Engine Skeleton  
FAZ 2: Agent Skeletons  
FAZ 3: Fake Data Flow  
FAZ 4: Paper Trading Engine  
FAZ 5: Real Data + Fake Money  
FAZ 6: Stability Gate (1–2 months)  
FAZ 7: Small Capital Live Trading  
FAZ 8: Scale & Optimization  

- A phase CANNOT be skipped.
- A phase must be CLOSED before moving on.

================================================================================
4. HIGH LEVEL ARCHITECTURE
================================================================================

Market Data
    ↓
Engines (CARTER, SWARM, others...)
    ↓
Strategy Pool
    ↓
Strategy Scoring Engine
    ↓
Strategy / Engine Selector
    ↓
CRO (Risk Governor, absolute veto)
    ↓
Execution Engine
    ↓
Portfolio & PnL
    ↓
Analytics, Logs, Surveillance, Learning
    ↺ feeds back to Scoring, CRO, AI

================================================================================
5. PLATFORM vs ENGINE CONCEPT
================================================================================

- PROJECT PREDATOR is NOT a trading engine.
- It is a META-PLATFORM / Trading Operating System.
- Engines produce strategies and signals.
- The platform decides:
  - Which engine is allowed to operate
  - Which strategy is active
  - How much capital is allocated
  - When everything must stop

================================================================================
6. ENGINE CONCEPT
================================================================================

An Engine = a full trading philosophy.

Examples:
- CARTER: Regime-aware trend/momentum/rotation core engine
- SWARM: Aggressive scalp / microstructure engine
- SENTINEL: Tail-risk / hedge engine (future)
- ATLAS: Macro / long-term engine (future)

Rules:
- Normally only ONE engine is active.
- Two engines may run only in special low-risk mode with CRO approval.
- Engines are also scored, monitored, demoted, quarantined, or killed.

================================================================================
7. MULTI-STRATEGY CONCEPT
================================================================================

- System SHALL NEVER run a single strategy.
- Each engine contains multiple strategies.
- Strategies compete via scoring.
- Bad strategies are demoted, disabled, quarantined, or killed.

Strategy Classes:
- CORE
- AGGRESSIVE
- TAIL_RISK

================================================================================
8. STRATEGY & ENGINE LIFECYCLE
================================================================================

Statuses:
- CANDIDATE
- ACTIVE
- QUARANTINED
- UNDER_REVIEW
- DISABLED
- KILLED

Rules:
- Score < 40 → DISABLED
- Score < 30 → UNDER_REVIEW
- Catastrophic violation → KILLED
- QUARANTINED = removed from real money, only shadow/paper

================================================================================
9. SHADOW MODE
================================================================================

- Any new engine or strategy must run in SHADOW MODE first.
- Shadow mode:
  - Uses real market data
  - Generates signals
  - Does NOT send orders
  - Produces virtual PnL for comparison

================================================================================
10. STRATEGY SCORING MODEL
================================================================================

StrategyScore ∈ [0,100]

Formula:

StrategyScore =
  0.30 * PerformanceScore
+ 0.15 * StabilityScore
+ 0.15 * RegimeFitScore
+ 0.15 * RiskDisciplineScore
+ 0.10 * ExecutionQualityScore
+ 0.10 * OperationalStabilityScore
+ 0.05 * FreshnessScore

================================================================================
11. EXECUTION & OPERATIONAL GOVERNANCE
================================================================================

ExecutionQualityScore measures:
- Slippage
- Fill ratio
- Rejects
- Latency
- Partial fills

OperationalStabilityScore measures:
- CPU, RAM, Disk
- Network
- API rate limits
- Process restarts

Bad execution or bad infra performance MUST:
- Reduce scores
- Potentially trigger CRO intervention

================================================================================
12. RISK MANAGEMENT (CRO)
================================================================================

CRO = absolute authority.

12.1 GLOBAL KILL-SWITCH
Triggers:
- Portfolio daily drawdown > 5%
- Systemic execution failure
- Infrastructure instability

Effect:
- ALL trading stops
- Cooldown period enforced

12.2 STRATEGY / ENGINE LOCAL KILL
Triggers:
- Risk rule violation
- Abnormal losses

Effect:
- Only that strategy/engine is stopped

================================================================================
13. LEVERAGE POLICY
================================================================================

- Leverage is NOT default.
- Per-strategy permissioned.
- CORE: low leverage allowed
- AGGRESSIVE: very limited
- TAIL_RISK: NEVER

CRO has absolute veto.

================================================================================
14. CAPITAL PARTITIONING
================================================================================

Capital is split into:
- CORE Capital
- AGGRESSIVE Capital
- VAULT Capital

Rules:
- No engine or strategy can access other pools.
- Loss in one pool must NOT endanger others.
- Vault is long-term reserve and profit skim target.

================================================================================
15. FEE TREASURY & BNB POLICY
================================================================================

- Each account (Spot, Futures, etc.) has its OWN Fee Treasury.
- Fee Treasury holds BNB (or equivalent) for fee discounts.
- BNB is:
  - Operational fuel
  - NOT investment capital
  - NOT speculative asset

Rules:
- System auto-monitors and replenishes BNB.
- If fee efficiency degrades:
  - CRO may scale down or halt trading.

================================================================================
16. AI (STRATEGIST MCP) ROLE
================================================================================

AI CAN:
- Propose new strategies
- Optimize parameters
- Create variants
- Analyze failures

AI CANNOT:
- Bypass scoring
- Bypass CRO
- Force activation
- Override kill rules
- Skip autonomy levels

================================================================================
17. AUTONOMY LEVELS
================================================================================

L1: Signal only  
L2: Paper trading  
L3: Strategy ranking & switching  
L4: Parameter optimization  
L5: Strategy generation & retirement  

- System starts at L2–L3.
- Advancement requires proven stability.

================================================================================
18. DATA & LEARNING LOOP
================================================================================

System stores:
- All trades
- All decisions
- All performance
- All execution metrics
- All infra metrics

Loop:
Observe → Score → Quarantine/Disable/Kill → Improve → Replace

No strategy and no engine is permanent.

================================================================================
19. INFRASTRUCTURE POLICY
================================================================================

- Runs 24/7 on server (VPS).
- Docker is mandatory.
- Auto-restart is mandatory.
- Logging is mandatory and first-class.

Infra Sentinel monitors:
- CPU, RAM, Disk
- Network
- API limits

Infrastructure instability = Trading risk.

================================================================================
20. EXCHANGE POLICY
================================================================================

- System is exchange-agnostic by design.
- Start with ONE exchange (Binance).
- Multi-exchange only after stability is proven.
- Multi-exchange = risk multiplier.

================================================================================
21. PRODUCTIZATION VISION
================================================================================

- System is a PLATFORM, not a bot.
- Non-custodial.
- Users control their own API keys.
- Revenue model: SaaS or hybrid.
- System is a tool, not an asset manager.

================================================================================
22. FINAL NON-NEGOTIABLE RULE
================================================================================

> PROFIT NEVER JUSTIFIES LOSS OF CONTROL.

Any component violating this principle is considered a system failure.

================================================================================
END OF MASTER BLUEPRINT v2
================================================================================
================================================================================
PROJECT PREDATOR
MASTER BLUEPRINT & SYSTEM CONSTITUTION v3
================================================================================

Status: LOCKED MASTER DOCUMENT
This document is the single source of truth for the entire system.
All code, agents, AI, engines, and future development MUST obey this document.

================================================================================
0. PHILOSOPHY
================================================================================

PROJECT PREDATOR is not a bot.
It is not a strategy.
It is not an indicator.

PROJECT PREDATOR is a:
- Trading Operating System
- Capital Management Machine
- Risk-First Autonomous Platform

Primary belief:
> PROFIT NEVER JUSTIFIES LOSS OF CONTROL.

================================================================================
1. PROJECT PURPOSE
================================================================================

Goal:
- Grow capital aggressively but controllably
- Target: 10,000€ → 1,000,000€
- Horizon: 3–5 years

This is:
- NOT a toy
- NOT a signal system
- NOT a single-strategy system
- NOT a single-engine system

This is:
- A professional, hedge-fund-grade autonomous trading platform.

================================================================================
2. CORE PRINCIPLES (NON-NEGOTIABLE)
================================================================================

1. Multi-engine and multi-strategy is mandatory.
2. Risk discipline ALWAYS overrides profit.
3. The system must be able to stop itself.
4. No strategy and no engine is trusted forever.
5. AI is an operator, not a ruler.
6. All decisions must be explainable via logs.
7. The system must survive before it thrives.
8. Autonomy is gradual and gated.
9. Operational stability is trading risk.
10. Profit NEVER justifies loss of control.

================================================================================
3. PHASED DEVELOPMENT MODEL
================================================================================

FAZ 0: Constitution & Documentation
FAZ 1: Core Platform Skeleton
FAZ 2: Agent Skeletons
FAZ 3: Fake Data Flow
FAZ 4: Paper Trading
FAZ 5: Real Data + Fake Money
FAZ 6: Stability Gate (1–2 months)
FAZ 7: Small Capital Live Trading
FAZ 8: Scale & Optimization

Rules:
- A phase CANNOT be skipped.
- A phase must be CLOSED before moving on.

================================================================================
4. PLATFORM vs ENGINE CONCEPT
================================================================================

PROJECT PREDATOR is NOT a trading engine.
It is a META-PLATFORM / Trading OS.

Engines:
- Produce strategies and signals.
- Represent complete trading philosophies.

The Platform:
- Decides which engine is allowed to operate.
- Decides which strategy is active.
- Decides capital allocation.
- Decides when everything must stop.

================================================================================
5. ENGINE CONCEPT
================================================================================

An Engine = a full trading philosophy.

Examples:
- CARTER: Regime-aware trend/momentum/rotation core engine.
- SWARM: Aggressive scalp / microstructure engine.
- SENTINEL: Tail-risk / hedge engine (future).
- ATLAS: Macro / long-term engine (future).

Rules:
- Normally only ONE engine is active.
- Two engines may run only in special low-risk mode with CRO approval.
- Engines are scored, quarantined, disabled, or killed.

================================================================================
6. MULTI-STRATEGY CONCEPT
================================================================================

- System SHALL NEVER run a single strategy.
- Each engine contains multiple strategies.
- Strategies compete via scoring.

Strategy Classes:
- CORE
- AGGRESSIVE
- TAIL_RISK

================================================================================
7. STRATEGY & ENGINE LIFECYCLE
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
8. SHADOW MODE
================================================================================

- Any new engine or strategy must run in SHADOW MODE first.
- Shadow mode:
  - Uses real market data
  - Generates signals
  - Does NOT send orders
  - Produces virtual PnL

================================================================================
9. HIGH LEVEL ARCHITECTURE
================================================================================

Market Data
    ↓
Engines
    ↓
Strategy Pool
    ↓
Scoring
    ↓
Selector
    ↓
CRO
    ↓
Execution
    ↓
Portfolio & Logs
    ↺ Feedback loop

================================================================================
10. SCORING MODEL
================================================================================

Score =
  0.30 * Performance
+ 0.15 * Stability
+ 0.15 * RegimeFit
+ 0.15 * RiskDiscipline
+ 0.10 * ExecutionQuality
+ 0.10 * OperationalStability
+ 0.05 * Freshness

================================================================================
11. RISK, CAPITAL, EXECUTION, INFRA, AI, PRODUCT
================================================================================

All detailed rules are defined in their respective policy documents.

================================================================================
12. FINAL RULE
================================================================================

> PROFIT NEVER JUSTIFIES LOSS OF CONTROL.

================================================================================
END
================================================================================
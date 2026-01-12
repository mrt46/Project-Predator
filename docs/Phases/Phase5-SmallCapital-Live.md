================================================================================
PROJECT PREDATOR
PHASE 5 – SMALL REAL CAPITAL LIVE TRADING
CONTROLLED REAL MONEY DEPLOYMENT PHASE
================================================================================

STATUS:
This is the most dangerous phase so far.
The system touches REAL MONEY for the first time.

Purpose:
- Validate the entire platform with REAL exchange APIs
- Validate execution, reconciliation, and safety systems in reality
- NOT to make money
- To prove:
  - The system does not lie
  - The system does not lose control
  - The system can stop itself
  - The system behaves under real-world friction

================================================================================
CAPITAL POLICY FOR PHASE 5
================================================================================

- Total capital used in this phase:
  - 0.5% – 2% of intended production capital
  - Example:
    If target capital = 10,000€
    Phase 5 capital = 50€ – 200€

- This money MUST be considered:
  - Already lost
  - Disposable
  - Test budget

- Capital pools:
  - Only CORE pool is allowed
  - AGGRESSIVE and TAIL_RISK pools are DISABLED

================================================================================
ALLOWED STRATEGY & ENGINE SCOPE
================================================================================

- Only:
  - ONE engine
  - ONE or TWO CORE-class strategies

- Forbidden:
  - AGGRESSIVE strategies
  - TAIL_RISK strategies
  - Any leverage
  - Any cross-asset complex behavior

================================================================================
ARCHITECTURE ADDITIONS FOR PHASE 5
================================================================================

New / Activated modules:

backend/
  live/
    exchange_adapter.py
    live_broker.py
    live_reconciliation.py
    balance_guard.py
    withdrawal_guard.py

  ops/
    runbooks.py
    alerting.py
    circuit_breaker.py

--------------------------------------------------------------------------------
COMPONENT RESPONSIBILITIES
--------------------------------------------------------------------------------

LiveExchangeAdapter:
- Talks to real exchange API (Binance initially)
- ONLY via abstract interface
- Must support:
  - Place order
  - Cancel order
  - Query order
  - Query balances
  - Query positions

LiveBroker:
- Sits between ExecutionAgent and LiveExchangeAdapter
- Enforces:
  - Idempotency
  - Rate limiting
  - Retry discipline
  - No duplicate orders

LiveReconciliation:
- Continuously reconciles:
  - Internal portfolio
  - Exchange balances
  - Exchange positions
  - Exchange open orders

BalanceGuard:
- Verifies:
  - No unexpected balance changes
  - No withdrawals
  - No asset disappearances

WithdrawalGuard:
- Ensures:
  - System NEVER withdraws funds
  - Any withdrawal event triggers GLOBAL HALT

CircuitBreaker:
- Hard safety rules:
  - Too many API errors
  - Too many rejects
  - Too much slippage
  - Too much desync
→ Immediate trading halt

================================================================================
OPERATIONAL RULES
================================================================================

1) SHADOW MODE FIRST

- Even in Phase 5:
  - System MUST run:
    - Shadow mode
    - And Live mode
  - In parallel
- Decisions are compared:
  - If divergence is too high:
    → Trading halts

2) DAILY HUMAN REVIEW

- Every day:
  - Logs reviewed
  - Trades reviewed
  - Reconciliation reviewed
  - Any anomaly = stop

3) NO UNATTENDED WEEKENDS (INITIALLY)

- First weeks:
  - System is supervised
  - No “set and forget”

================================================================================
RISK & KILL-SWITCH RULES (PHASE 5 OVERRIDES)
================================================================================

- Global daily drawdown limit:
  - 1% (stricter than normal)

- Any of the following triggers IMMEDIATE GLOBAL HALT:
  - Reconciliation mismatch
  - Unexpected balance change
  - Order state confusion
  - Exchange API instability
  - Infrastructure instability
  - CircuitBreaker event

- After any GLOBAL HALT:
  - Manual inspection required
  - No automatic resume

================================================================================
MANDATORY TEST SCENARIOS (LIVE)
================================================================================

T1: Small order lifecycle
- Place tiny order
- Verify:
  - Exchange state
  - Internal state
  - Reconciliation

T2: Cancel / Replace test
- Place order
- Cancel it
- Ensure:
  - No ghost orders

T3: Partial fill test
- Force partial fill
- Verify:
  - Position sizing correct
  - No double count

T4: API failure test
- Simulate network block
- Verify:
  - Circuit breaker halts trading

T5: Manual Kill-Switch test
- Trigger manual global halt
- Verify:
  - No more orders go out

T6: Reconciliation drift test
- Artificially corrupt internal state
- Verify:
  - Reconciliation detects
  - System halts

================================================================================
OBSERVABILITY & REPORTING
================================================================================

Daily report MUST include:
- Trades
- Slippage
- Fills
- Rejects
- API errors
- Reconciliation status
- Balance changes
- PnL (but NOT primary focus)

Alerts:
- Telegram / Email / etc.

================================================================================
DURATION OF PHASE 5
================================================================================

- Minimum:
  - 30 real calendar days
- Preferred:
  - 60–90 days

================================================================================
PASS / FAIL CRITERIA
================================================================================

FAIL if:
- System loses track of funds
- System trades while blind
- System ignores reconciliation
- Kill-switch fails
- Any unexplained balance change occurs

PASS if:
- System runs for weeks
- With multiple halts and recoveries
- Without losing state integrity
- Without unexplained money movement
- With full audit trail

================================================================================
EXIT CRITERIA (PHASE 5)
================================================================================

[ ] 30–90 days of live trading completed
[ ] No unexplained balance changes
[ ] No unrecovered reconciliation incidents
[ ] Kill-switch tested in real life
[ ] Circuit breakers proven
[ ] Team confidence achieved
[ ] Post-mortem reports exist

Only if ALL true:
→ FAZ 6 (Scaling & Optimization) may begin.

================================================================================
FINAL PHILOSOPHICAL RULE
================================================================================

This phase does not prove:
"Can we make money?"

It proves:
"Can we touch real money without losing control?"

================================================================================
END OF DOCUMENT
================================================================================
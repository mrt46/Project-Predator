================================================================================
PROJECT PREDATOR
LIVE TRADING SAFETY ARCHITECTURE
BINANCE ADAPTER + RECONCILIATION + CIRCUIT BREAKER
================================================================================

Scope:
This document defines the FULL production-grade safety architecture for:

- Real exchange integration
- Real money state tracking
- Reconciliation & consistency enforcement
- Automatic trading halts (Circuit Breakers)

This layer is what prevents:
- Silent money loss
- Ghost positions
- Duplicate orders
- Desynchronized portfolios
- Runaway trading

================================================================================
PART 1 — EXCHANGE ADAPTER CONTRACT (BINANCE)
================================================================================

PHILOSOPHY:
The system must NEVER depend on Binance directly.
It must depend on an ABSTRACT EXCHANGE CONTRACT.

Binance is just ONE implementation.

--------------------------------------------------------------------------------
INTERFACE: IExchangeAdapter
--------------------------------------------------------------------------------

Methods:

- place_order(order: OrderRequest) -> OrderAck
- cancel_order(order_id: str) -> CancelAck
- get_order(order_id: str) -> OrderStatus
- get_open_orders(symbol: str) -> List[OrderStatus]
- get_balances() -> Dict[Asset, Balance]
- get_positions() -> Dict[Symbol, Position]
- get_trades(since_time) -> List[Trade]
- ping() -> HealthStatus

--------------------------------------------------------------------------------
HARD REQUIREMENTS
--------------------------------------------------------------------------------

1) IDEMPOTENCY

- Every order MUST have:
  - client_order_id (UUID)
- Re-sending same request MUST NOT duplicate orders.

2) RATE LIMITING

- Adapter enforces:
  - Max requests / second
  - Backoff on 429 errors

3) RETRY DISCIPLINE

- Retries allowed ONLY for:
  - Network timeouts
- NEVER blindly retry order placement without checking state.

4) FULL LOGGING

- Every request
- Every response
- Every error

5) NO BUSINESS LOGIC

- Adapter does NOT:
  - Decide size
  - Decide risk
  - Decide strategy
- It only:
  - Translates
  - Sends
  - Receives

--------------------------------------------------------------------------------
BINANCE-SPECIFIC IMPLEMENTATION RULES
--------------------------------------------------------------------------------

- Use:
  - REST for orders & balances
  - WebSocket for:
    - Execution reports
    - Balance updates
- But:
  - System MUST survive WebSocket death.
  - REST polling is mandatory backup.

- NEVER trust WebSocket alone.

--------------------------------------------------------------------------------
FAILURE MODES TO HANDLE
--------------------------------------------------------------------------------

- Timeout after sending order
- Order accepted but response lost
- Duplicate response
- Exchange returns inconsistent state
- Exchange API partial outage

For ANY of these:
→ Trading MUST slow down or halt.

================================================================================
PART 2 — LIVE RECONCILIATION ENGINE
================================================================================

PHILOSOPHY:
> The system MUST NEVER TRUST ITSELF.

Internal state and exchange state MUST be continuously reconciled.

--------------------------------------------------------------------------------
COMPONENT: LiveReconciliation
--------------------------------------------------------------------------------

Runs:
- Every N seconds (e.g., 5–30s)

Fetches:
- Exchange balances
- Exchange positions
- Exchange open orders
- Exchange recent trades

Compares with:
- Internal portfolio state
- Internal order registry
- Internal execution log

--------------------------------------------------------------------------------
CHECKS (INVARIANTS)
--------------------------------------------------------------------------------

1) BALANCE INVARIANTS

- For each asset:
  exchange_balance ≈ internal_balance ± tiny_epsilon

If not:
→ CRITICAL ERROR

2) POSITION INVARIANTS

- For each symbol:
  exchange_position == internal_position

If not:
→ CRITICAL ERROR

3) ORDER INVARIANTS

- No internal open order missing on exchange
- No exchange open order missing internally

If found:
→ CRITICAL ERROR

4) TRADE HISTORY INVARIANT

- Every exchange trade MUST exist in internal execution log

If not:
→ CRITICAL ERROR

--------------------------------------------------------------------------------
ON ANY CRITICAL ERROR
--------------------------------------------------------------------------------

1) Trigger:
   - GLOBAL KILL-SWITCH
2) Freeze trading
3) Dump:
   - Full state snapshot
4) Generate:
   - Incident report
5) Require:
   - Manual intervention

--------------------------------------------------------------------------------
RECONCILIATION STATES
--------------------------------------------------------------------------------

- HEALTHY
- WARNING
- CRITICAL

Only HEALTHY allows trading.

--------------------------------------------------------------------------------
SELF-HEALING (LIMITED)

Allowed:
- Re-sync internal state from exchange
- Only AFTER:
  - Trading is halted
  - Snapshot is taken
  - Operator confirms

================================================================================
PART 3 — CIRCUIT BREAKER SYSTEM
================================================================================

PHILOSOPHY:
> If something feels wrong, STOP.

--------------------------------------------------------------------------------
COMPONENT: CircuitBreakerEngine
--------------------------------------------------------------------------------

Monitors:

- ExchangeAdapter health
- Reconciliation status
- Execution quality
- Infra stability
- Risk metrics

--------------------------------------------------------------------------------
TRIGGERS (ANY = IMMEDIATE GLOBAL HALT)
--------------------------------------------------------------------------------

A) EXCHANGE TRIGGERS
- API error rate > threshold
- Ping fails
- Order reject spike
- Timeout storm

B) RECONCILIATION TRIGGERS
- Any CRITICAL mismatch
- Reconciliation cannot complete

C) EXECUTION TRIGGERS
- Slippage > allowed
- Too many partial fills
- Too many unknown order states

D) INFRA TRIGGERS
- High memory
- High CPU
- Process restarts
- Disk full
- Network instability

E) RISK TRIGGERS
- Daily DD limit exceeded
- Position size invariant violated

--------------------------------------------------------------------------------
CIRCUIT BREAKER STATES
--------------------------------------------------------------------------------

- GREEN: trading allowed
- YELLOW: trading limited / slowed
- RED: trading HALTED

--------------------------------------------------------------------------------
WHEN RED STATE
--------------------------------------------------------------------------------

- No new orders
- Cancel open orders (if safe)
- Keep monitoring
- Wait for:
  - Manual inspection
  - Manual reset

--------------------------------------------------------------------------------
NO AUTO-RESUME POLICY
--------------------------------------------------------------------------------

- After RED:
  - System NEVER resumes automatically.
  - Requires:
    - Human review
    - Explicit command

================================================================================
PART 4 — FULL SAFETY FLOW
================================================================================

OrderRequest
   ↓
PolicyGuard (CRO)
   ↓
CircuitBreaker (must be GREEN)
   ↓
LiveBroker
   ↓
ExchangeAdapter
   ↓
Exchange

In parallel:

LiveReconciliation running every N seconds
CircuitBreaker listening to all subsystems

================================================================================
PART 5 — MANDATORY LIVE TESTS
================================================================================

T1: Order timeout test
- Simulate timeout after send
- Verify:
  - No duplicate order
  - Reconciliation fixes state or halts

T2: Ghost order test
- Inject fake exchange order
- Verify:
  - Reconciliation detects
  - Trading halts

T3: Balance drift test
- Manually change balance
- Verify:
  - Detected
  - Trading halts

T4: API outage test
- Block network
- Verify:
  - Circuit breaker RED

T5: High slippage test
- Simulate huge slippage
- Verify:
  - Trading slowed or halted

================================================================================
PART 6 — EXIT CRITERIA FOR PHASE 5
================================================================================

[ ] Exchange adapter stable for weeks
[ ] Reconciliation never misses a drift
[ ] Circuit breaker triggered correctly many times
[ ] No unexplained balance change ever
[ ] No ghost orders ever
[ ] No silent desync ever
[ ] Full audit trail exists

Only if ALL true:
→ System is allowed to scale capital.

================================================================================
FINAL RULE
================================================================================

> If you are not 100% sure where the money is, YOU MUST NOT TRADE.

================================================================================
END OF DOCUMENT
================================================================================
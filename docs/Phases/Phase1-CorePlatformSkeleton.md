================================================================================
PROJECT PREDATOR – PHASE 1
CORE PLATFORM SKELETON – OFFICIAL SPECIFICATION
================================================================================

Status: LOCKED  
Phase: 1  
Purpose: Build the Trading OS core WITHOUT any trading, strategy, or market logic.

> Phase 1 builds the OPERATING SYSTEM of the platform, not the business logic.

================================================================================
1. PURPOSE OF PHASE 1
================================================================================

Phase 1 exists to:

- Create a stable, observable, governable platform core
- Prove that the system:
  - Boots
  - Runs
  - Schedules
  - Communicates
  - Logs
  - Can stop itself
- Create the foundation on which ALL future phases will run
- Separate:
  - Infrastructure
  - Governance
  - Execution control
  from:
  - Trading logic
  - Strategies
  - Market data

> Phase 1 is the KERNEL of the Trading OS.

================================================================================
2. ABSOLUTE SCOPE BOUNDARIES
================================================================================

Phase 1 MUST NOT contain:

- ❌ Any trading logic
- ❌ Any strategies
- ❌ Any market data handling
- ❌ Any exchange connections
- ❌ Any real or fake money logic
- ❌ Any profit or performance logic
- ❌ Any optimization logic

Phase 1 MUST contain ONLY:

- Core platform infrastructure
- Governance and safety gates
- Observability and control
- Stubs and interfaces

================================================================================
3. CORE COMPONENTS TO BE BUILT
================================================================================

The following components MUST exist:

------------------------------------------------
3.1 CoreEngine
------------------------------------------------
- Central state machine of the system
- States:
  - INIT
  - BOOTING
  - IDLE
  - RUNNING
  - HALTED
- Responsibilities:
  - Boot sequence
  - Start scheduler
  - Register components
  - Graceful shutdown
  - Enforce lifecycle

------------------------------------------------
3.2 EventBus
------------------------------------------------
- Pub/Sub event system
- Used by ALL components
- No direct calls between major components
- Must support:
  - Subscribe
  - Publish
  - Unsubscribe
- All important events must be logged

------------------------------------------------
3.3 Scheduler
------------------------------------------------
- Generates:
  - Heartbeat
  - Tick events
- Drives the system clock
- Can be started and stopped
- Must be controllable by CoreEngine

------------------------------------------------
3.4 Registry
------------------------------------------------
- Central component registry
- Keeps references to:
  - Agents
  - Engines
  - Services
- Allows controlled lookup
- No global variables

------------------------------------------------
3.5 PolicyGuard (CRO Gate)
------------------------------------------------
- Central policy enforcement point
- Every critical action must pass through it
- Must support:
  - Allow
  - Deny
  - Global halt
- Must be able to:
  - Block engine start
  - Block execution
  - Trigger global kill switch

------------------------------------------------
3.6 Execution Layer (FAKE ONLY)
------------------------------------------------
- BaseExecutor interface
- FakeExecutor implementation
- Must:
  - Accept orders
  - Simulate fills
  - Emit events
- Must NOT:
  - Talk to any exchange
  - Touch real markets

------------------------------------------------
3.7 Platform Stubs
------------------------------------------------
The following must exist as STUBS:

- ScoringEngine
- StrategySelector
- CapitalManager

Each must:
- Have interfaces
- Have placeholder implementations
- Log calls
- Return dummy values

------------------------------------------------
3.8 Interfaces Layer
------------------------------------------------
Interfaces must exist for:

- Engine
- Strategy
- Agent
- Executor

Purpose:
- Enforce architecture boundaries
- Prevent tight coupling

------------------------------------------------
3.9 Monitoring & Observability
------------------------------------------------
Must include:

- Structured logging
- Health check endpoint (/health)
- Basic metrics hooks
- State transition logs
- Policy decision logs

------------------------------------------------
3.10 Configuration
------------------------------------------------
- .env.example
- Central config loader
- No secrets in repo

------------------------------------------------
3.11 Dockerization
------------------------------------------------
- Dockerfile
- docker-compose.yml
- System must be runnable via Docker

================================================================================
4. REQUIRED REPOSITORY STRUCTURE (MINIMUM)
================================================================================

Project-Predator/
  .env.example
  requirements.txt

  backend/
    main.py

    core/
      engine.py
      event_bus.py
      scheduler.py
      registry.py
      policy_guard.py
      config.py

    platform/
      selector.py
      scoring.py
      capital.py

    execution/
      base.py
      fake_executor.py

    interfaces/
      engine.py
      strategy.py
      agent.py

    monitor/
      health.py
      metrics.py
      logging.py

  docker/
    Dockerfile
    docker-compose.yml

================================================================================
5. ARCHITECTURE RULES
================================================================================

- No component may:
  - Talk directly to an exchange
  - Bypass PolicyGuard
  - Bypass EventBus
- No strategy logic may exist
- No market data logic may exist
- All actions must be:
  - Logged
  - Observable
  - Explainable

================================================================================
6. WHAT PHASE 1 PRODUCES
================================================================================

Phase 1 produces:

- A bootable platform
- A running event loop
- A ticking scheduler
- A controllable lifecycle
- A working /health endpoint
- A fake execution path
- A fully governed core

> But ZERO business logic.

================================================================================
7. COMPLETION CRITERIA
================================================================================

Phase 1 is COMPLETE when:

- The system:
  - Boots
  - Runs without crashing
  - Exposes /health
  - Produces logs
  - Can be started and stopped
- Smoke test passes
- No forbidden features exist
- Code is committed
- Git tag is created:

> FAZ-1-STABLE

================================================================================
8. WHAT PHASE 1 FORBIDS
================================================================================

- ❌ Any real trading
- ❌ Any strategies
- ❌ Any market data
- ❌ Any exchange integration
- ❌ Any PnL logic
- ❌ Any performance optimization

================================================================================
9. UPGRADE RULE
================================================================================

> Phase 2 may NOT start unless Phase 1 is:
- Tested
- Stable
- Tagged

================================================================================
10. FINAL NON-NEGOTIABLE RULE
================================================================================

> PROFIT NEVER JUSTIFIES LOSS OF CONTROL.

Any code violating this principle is INVALID.

================================================================================
END OF PHASE 1
================================================================================
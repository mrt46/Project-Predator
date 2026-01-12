# PROJECT PREDATOR - Quick Start Guide

## Overview

**PROJECT PREDATOR** is a Trading Operating System (not a trading bot) built with strict governance and risk-first principles.

**Current Phase**: FAZ 2 - Agent Skeletons  
**Status**: Ready to run (STUB mode - no real trading)

---

## Prerequisites

- Python 3.11+
- Docker (optional)

---

## Installation

### Option 1: Local Python

```bash
# Clone the repository
cd Project-Predator

# Install dependencies
pip install -r requirements.txt

# Run the platform
python -m backend.main
```

### Option 2: Docker

```bash
# Build and run
docker-compose -f docker/docker-compose.yml up --build

# Run in background
docker-compose -f docker/docker-compose.yml up -d
```

---

## Verification

### Check Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "state": "RUNNING",
  "components": {
    "event_bus": {...},
    "registry": {...},
    "policy_guard": {...},
    "scheduler": {...}
  },
  "agents": [
    "MarketScannerAgent",
    "DataEngineeringAgent",
    "ExecutionAgent",
    "PortfolioManagerAgent",
    "CRORiskAgent",
    "PerformanceKPIAgent",
    "ASPAAgent",
    "RRSAgent"
  ],
  "phase": 2
}
```

### Check Root Endpoint

```bash
curl http://localhost:8000/
```

---

## What You'll See

When running, the system will:

1. **Boot** - CoreEngine initializes all components
2. **Start Agents** - All 6 agents start and subscribe to events
3. **Generate Events** - Scheduler produces TICK and HEARTBEAT events
4. **Publish Data** - Agents publish fake market data, positions, performance
5. **Log Activity** - All activity is logged to stdout

### Sample Log Output

```
================================================================================
PROJECT PREDATOR - Trading Operating System
Phase: 2 (FAZ 2 - Agent Skeletons)
Environment: development
================================================================================
=== CoreEngine Boot Sequence Started ===
[1/5] Validating configuration...
[2/5] Checking PolicyGuard...
[3/5] Publishing boot event...
[4/5] Starting 8 agents...
  ✓ MarketScannerAgent started
  ✓ DataEngineeringAgent started
  ✓ ExecutionAgent started
  ✓ PortfolioManagerAgent started
  ✓ CRORiskAgent started
  ✓ PerformanceKPIAgent started
  ✓ ASPAAgent started
  ✓ RRSAgent started
[5/5] Starting scheduler...
=== CoreEngine Boot Sequence Complete ===
================================================================================
✓ PROJECT PREDATOR is RUNNING
✓ Health check: http://localhost:8000/health
================================================================================
```

---

## Architecture

### Core Components (FAZ 1)

- **CoreEngine** - Central state machine
- **EventBus** - Pub/sub event system
- **Registry** - Component registry
- **Scheduler** - System clock (TICK/HEARTBEAT)
- **PolicyGuard** - CRO gate (risk enforcement)

### Agents (FAZ 2 - Blueprint)

All agents are **SKELETONS** with no real business logic (per Blueprint):

| Agent | Blueprint Responsibility |
|-------|--------------------------|
| MarketScannerAgent | On Tick → log "scanning market" |
| DataEngineeringAgent | On Tick → log "processing data" |
| ExecutionAgent | On OrderRequest → log "would execute" |
| PortfolioManagerAgent | On Tick → log "checking portfolio" |
| CRORiskAgent | On RiskEvent → log "risk check" |
| PerformanceKPIAgent | On ExecutionResult → log "recording KPI" |
| ASPAAgent | On StrategyReviewEvent → log "analyzing strategy" |
| RRSAgent | Every N seconds → log "infra OK" |

---

## Configuration

Configuration is done via environment variables (`.env` file):

```bash
# System
ENVIRONMENT=development
LOG_LEVEL=INFO

# Core Engine
SCHEDULER_TICK_INTERVAL=1.0
HEARTBEAT_INTERVAL=5.0

# Policy Guard
GLOBAL_KILL_SWITCH=false

# Phase Control
CURRENT_PHASE=2
ALLOW_REAL_EXCHANGE=false    # MUST be false in Phase 2
ALLOW_REAL_TRADING=false     # MUST be false in Phase 2
```

---

## Shutdown

### Graceful Shutdown

Press `Ctrl+C` to trigger graceful shutdown.

The system will:
1. Stop scheduler
2. Stop all agents
3. Publish shutdown event
4. Exit cleanly

### Docker Shutdown

```bash
docker-compose -f docker/docker-compose.yml down
```

---

## Important Notes

### What This Is NOT

- ❌ This is NOT a trading bot
- ❌ This does NOT connect to real exchanges
- ❌ This does NOT handle real money
- ❌ This does NOT execute real trades
- ❌ This does NOT use real market data

### What This IS

- ✅ A Trading Operating System platform
- ✅ An agent-based architecture
- ✅ A governance framework
- ✅ A foundation for future phases
- ✅ A fully observable, controllable system

### Governance

This implementation strictly follows:
- `/AI_RULES.md`
- `/docs/constitution/MASTER.md`
- Phase boundaries
- Risk-first principles

> **PROFIT NEVER JUSTIFIES LOSS OF CONTROL**

---

## Next Steps

1. **Explore the code** - All code is documented
2. **Read the docs** - See `/docs/Phases/`
3. **Check health endpoint** - Monitor system state
4. **Review logs** - Understand event flow

---

## Troubleshooting

### Port Already in Use

```bash
# Change the port in .env or docker-compose.yml
HEALTH_CHECK_PORT=8001
```

### Import Errors

```bash
# Make sure you're in the Project-Predator directory
export PYTHONPATH=$(pwd)
```

### Docker Build Fails

```bash
# Clean and rebuild
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up
```

---

## Project Structure

```
Project-Predator/
  backend/
    agents/                      # FAZ 2: Agent skeletons (Blueprint structure)
      market_scanner/            # MarketScannerAgent
      data_engineering/          # DataEngineeringAgent
      execution/                 # ExecutionAgent
      portfolio/                 # PortfolioManagerAgent
      cro/                       # CRORiskAgent
      performance/               # PerformanceKPIAgent
      aspa/                      # ASPAAgent
      rrs/                       # RRSAgent
    core/                        # FAZ 1: Core platform
    execution/                   # FAZ 1: Execution layer
    interfaces/                  # FAZ 1: Interface definitions
    monitor/                     # FAZ 1: Monitoring
    platform/                    # FAZ 1: Platform stubs
    main.py                      # Entry point
  
  docker/                        # Docker configuration
  docs/                          # Documentation
  tests/                         # Blueprint tests
  
  requirements.txt               # Python dependencies
  BLUEPRINT_COMPLIANCE.md        # Blueprint uyumluluk dokümanı
  QUICKSTART.md                  # This file
```

---

## Support

For issues or questions, refer to:
- `/docs/Phases/Phase2-AgentSkeletons.md` - Phase 2 details
- `/docs/constitution/MASTER.md` - System constitution
- `/AI_RULES.md` - Development rules

---

**Version**: 0.2.0-faz2  
**Phase**: FAZ 2 - Agent Skeletons  
**Status**: ✓ COMPLETE

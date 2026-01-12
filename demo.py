#!/usr/bin/env python3
"""
PROJECT PREDATOR - Demo Script
Demonstrates the FAZ 2 Agent Skeletons in action
"""
import time
import sys
from backend.monitor.logging import setup_logging

# Setup logging
logger = setup_logging()

from backend.core.engine import CoreEngine
from backend.agents.market_scanner.agent import MarketScannerAgent
from backend.agents.data_engineering.agent import DataEngineeringAgent
from backend.agents.execution.agent import ExecutionAgent
from backend.agents.portfolio.agent import PortfolioManagerAgent
from backend.agents.cro.agent import CRORiskAgent
from backend.agents.performance.agent import PerformanceKPIAgent
from backend.agents.aspa.agent import ASPAAgent
from backend.agents.rrs.agent import RRSAgent


def main():
    """Run a short demo of the system"""
    
    print()
    print("=" * 80)
    print("PROJECT PREDATOR - FAZ 2 Demo")
    print("=" * 80)
    print()
    print("This demo will:")
    print("  1. Initialize the CoreEngine")
    print("  2. Create and register all 8 agents (Blueprint)")
    print("  3. Start the system")
    print("  4. Run for 10 seconds")
    print("  5. Show statistics")
    print("  6. Shutdown cleanly")
    print()
    print("=" * 80)
    print()
    
    # Initialize CoreEngine
    print("[*] Initializing CoreEngine...")
    engine = CoreEngine()
    print("[OK] CoreEngine initialized")
    print()
    
    # Create agents (Blueprint structure)
    print("[*] Creating agents (Blueprint)...")
    agents = [
        MarketScannerAgent(engine.event_bus, engine.registry),
        DataEngineeringAgent(engine.event_bus, engine.registry),
        ExecutionAgent(engine.event_bus, engine.registry),
        PortfolioManagerAgent(engine.event_bus, engine.registry),
        CRORiskAgent(engine.event_bus, engine.registry),
        PerformanceKPIAgent(engine.event_bus, engine.registry),
        ASPAAgent(engine.event_bus, engine.registry),
        RRSAgent(engine.event_bus, engine.registry)
    ]
    
    for agent in agents:
        engine.register_agent(agent)
        print(f"  [OK] {agent.get_name()}")
    print()
    
    # Start system
    print("[*] Starting system...")
    if not engine.start():
        print("❌ Failed to start system")
        sys.exit(1)
    print()
    
    print("=" * 80)
    print("[OK] SYSTEM RUNNING - Watch the events flow!")
    print("=" * 80)
    print()
    
    # Run for 10 seconds
    try:
        for i in range(10, 0, -1):
            print(f"Running... {i} seconds remaining", end='\r')
            time.sleep(1)
        print()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    
    print()
    print("=" * 80)
    print("[*] System Statistics")
    print("=" * 80)
    print()
    
    # Show statistics
    health = engine.health_check()
    
    print("Core Components:")
    print(f"  State: {health['state']}")
    print(f"  Phase: {health['phase']}")
    print()
    
    print("EventBus:")
    eb_stats = health['components']['event_bus']
    print(f"  Events Published: {eb_stats['total_events_published']}")
    print(f"  Subscribers: {eb_stats['subscriber_count']}")
    print()
    
    print("Scheduler:")
    sched_stats = health['components']['scheduler']
    print(f"  Ticks Generated: {sched_stats['ticks_generated']}")
    print(f"  Heartbeats Generated: {sched_stats['heartbeats_generated']}")
    print()
    
    print("PolicyGuard:")
    pg_stats = health['components']['policy_guard']
    print(f"  Decisions Made: {pg_stats['decisions_made']}")
    print(f"  Denials: {pg_stats['denials']}")
    print(f"  Kill Switch: {'ACTIVE' if pg_stats['global_kill_switch'] else 'INACTIVE'}")
    print()
    
    print("Agents:")
    for agent_name in health['agents']:
        agent = engine.registry.get(agent_name)
        if agent:
            agent_health = agent.health_check()
            print(f"  {agent_name}:")
            print(f"    Running: {agent_health['running']}")
            print(f"    Events Processed: {agent_health['events_processed']}")
    print()
    
    # Shutdown
    print("=" * 80)
    print("[*] Shutting down...")
    print("=" * 80)
    print()
    
    engine.stop()
    
    print()
    print("=" * 80)
    print("[OK] Demo Complete!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  - Read QUICKSTART.md for full documentation")
    print("  - Run: python -m backend.main (for full system)")
    print("  - Run: pytest tests/test_basic.py (for tests)")
    print("  - Check: http://localhost:8000/health (when running)")
    print()
    print("Remember: This is STUB mode - no real trading!")
    print()


if __name__ == "__main__":
    main()

"""
PROJECT PREDATOR - Basic Smoke Tests
Verifies that the core system boots and runs correctly
"""
import pytest
import time
from backend.core.engine import CoreEngine
from backend.agents.market_scanner.agent import MarketScannerAgent
from backend.agents.data_engineering.agent import DataEngineeringAgent
from backend.agents.execution.agent import ExecutionAgent
from backend.agents.portfolio.agent import PortfolioManagerAgent
from backend.agents.cro.agent import CRORiskAgent
from backend.agents.performance.agent import PerformanceKPIAgent
from backend.agents.aspa.agent import ASPAAgent
from backend.agents.rrs.agent import RRSAgent


def test_core_engine_initialization():
    """Test that CoreEngine initializes correctly"""
    engine = CoreEngine()
    assert engine is not None
    assert engine.event_bus is not None
    assert engine.registry is not None
    assert engine.policy_guard is not None
    assert engine.scheduler is not None


def test_agent_initialization():
    """Test that all agents can be initialized (Blueprint)"""
    engine = CoreEngine()
    
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
    
    assert len(agents) == 8
    for agent in agents:
        assert agent is not None
        assert agent.get_name() is not None


def test_engine_boot_and_shutdown():
    """Test that CoreEngine can boot and shutdown cleanly (Blueprint)"""
    engine = CoreEngine()
    
    # Register agents (Blueprint)
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
    
    # Start engine
    assert engine.start() is True
    
    # Let it run briefly
    time.sleep(2)
    
    # Check health
    health = engine.health_check()
    assert health["status"] == "healthy"
    assert len(health["agents"]) == 8
    
    # Stop engine
    assert engine.stop() is True


def test_event_bus():
    """Test that EventBus works"""
    engine = CoreEngine()
    
    event_received = []
    
    def handler(event):
        event_received.append(event)
    
    from backend.core.event_bus import EventType
    
    engine.event_bus.subscribe(EventType.TICK, handler)
    engine.event_bus.publish(EventType.TICK, {"test": True}, source="test")
    
    assert len(event_received) == 1
    assert event_received[0].data["test"] is True


def test_policy_guard():
    """Test that PolicyGuard works"""
    engine = CoreEngine()
    
    # System start should be allowed
    decision = engine.policy_guard.check_system_start()
    assert decision.allowed is True
    
    # Activate kill switch
    engine.policy_guard.activate_kill_switch("test")
    
    # System start should now be denied
    decision = engine.policy_guard.check_system_start()
    assert decision.allowed is False
    
    # Deactivate kill switch
    engine.policy_guard.deactivate_kill_switch()
    
    # System start should be allowed again
    decision = engine.policy_guard.check_system_start()
    assert decision.allowed is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
PROJECT PREDATOR - CoreEngine
Central state machine and orchestrator
"""
import logging
from typing import List, Optional
from backend.interfaces.engine import IEngine, EngineState
from backend.core.event_bus import EventBus, EventType
from backend.core.registry import Registry
from backend.core.scheduler import Scheduler
from backend.core.policy_guard import PolicyGuard
from backend.core.config import config


class CoreEngine(IEngine):
    """
    Central state machine of the Trading OS
    
    Responsibilities:
    - Boot sequence
    - Component lifecycle management
    - State transitions
    - Graceful shutdown
    - Enforce platform governance
    
    States: INIT -> BOOTING -> IDLE -> RUNNING -> HALTED
    """
    
    def __init__(self):
        """Initialize CoreEngine"""
        self.logger = logging.getLogger(__name__)
        self._state = EngineState.INIT
        
        # Core components
        self.event_bus = EventBus()
        self.registry = Registry()
        self.policy_guard = PolicyGuard(self.event_bus)
        self.scheduler = Scheduler(
            self.event_bus,
            tick_interval=config.SCHEDULER_TICK_INTERVAL,
            heartbeat_interval=config.HEARTBEAT_INTERVAL
        )
        
        # Agent registry (FAZ 2)
        self._agents: List = []
        
        # Register core components
        self.registry.register("EventBus", self.event_bus)
        self.registry.register("Registry", self.registry)
        self.registry.register("PolicyGuard", self.policy_guard)
        self.registry.register("Scheduler", self.scheduler)
        self.registry.register("CoreEngine", self)
        
        self.logger.info("CoreEngine initialized")
    
    def start(self) -> bool:
        """
        Start the CoreEngine
        
        Boot sequence:
        1. Validate configuration
        2. Check PolicyGuard
        3. Boot components
        4. Start agents
        5. Start scheduler
        6. Transition to RUNNING
        
        Returns:
            True if started successfully
        """
        if self._state == EngineState.RUNNING:
            self.logger.warning("CoreEngine already running")
            return False
        
        self.logger.info("=== CoreEngine Boot Sequence Started ===")
        self._state = EngineState.BOOTING
        
        try:
            # Step 1: Validate configuration
            self.logger.info("[1/5] Validating configuration...")
            if not config.validate():
                raise Exception("Configuration validation failed")
            
            # Step 2: Check PolicyGuard
            self.logger.info("[2/5] Checking PolicyGuard...")
            decision = self.policy_guard.check_system_start()
            if not decision.allowed:
                raise Exception(f"PolicyGuard denied system start: {decision.reason}")
            
            # Step 3: Publish boot event
            self.logger.info("[3/5] Publishing boot event...")
            self.event_bus.publish(
                EventType.SYSTEM_BOOT,
                {"phase": config.CURRENT_PHASE, "environment": config.ENVIRONMENT},
                source="CoreEngine"
            )
            
            # Step 4: Start agents (FAZ 2)
            self.logger.info(f"[4/5] Starting {len(self._agents)} agents...")
            for agent in self._agents:
                agent.start()
                self.logger.info(f"  [OK] {agent.get_name()} started")
            
            # Step 5: Start scheduler
            self.logger.info("[5/5] Starting scheduler...")
            self.scheduler.start()
            
            # Transition to RUNNING
            self._state = EngineState.RUNNING
            self.logger.info("=== CoreEngine Boot Sequence Complete ===")
            self.logger.info(f"State: {self._state.value}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Boot sequence failed: {e}")
            self._state = EngineState.ERROR
            self.event_bus.publish(
                EventType.SYSTEM_ERROR,
                {"error": str(e), "state": "BOOT_FAILED"},
                source="CoreEngine"
            )
            return False
    
    def stop(self) -> bool:
        """
        Stop the CoreEngine
        
        Shutdown sequence:
        1. Stop scheduler
        2. Stop agents
        3. Publish shutdown event
        4. Transition to HALTED
        
        Returns:
            True if stopped successfully
        """
        if self._state == EngineState.HALTED:
            self.logger.warning("CoreEngine already halted")
            return False
        
        self.logger.info("=== CoreEngine Shutdown Sequence Started ===")
        
        try:
            # Step 1: Stop scheduler
            self.logger.info("[1/3] Stopping scheduler...")
            self.scheduler.stop()
            
            # Step 2: Stop agents
            self.logger.info(f"[2/3] Stopping {len(self._agents)} agents...")
            for agent in self._agents:
                agent.stop()
                self.logger.info(f"  [OK] {agent.get_name()} stopped")
            
            # Step 3: Publish shutdown event
            self.logger.info("[3/3] Publishing shutdown event...")
            self.event_bus.publish(
                EventType.SYSTEM_SHUTDOWN,
                {"reason": "Normal shutdown"},
                source="CoreEngine"
            )
            
            # Transition to HALTED
            self._state = EngineState.HALTED
            self.logger.info("=== CoreEngine Shutdown Complete ===")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Shutdown sequence failed: {e}")
            self._state = EngineState.ERROR
            return False
    
    def register_agent(self, agent) -> None:
        """
        Register an agent (FAZ 2)
        
        Args:
            agent: Agent instance implementing IAgent
        """
        self._agents.append(agent)
        self.registry.register(agent.get_name(), agent)
        self.logger.info(f"Registered agent: {agent.get_name()}")
    
    def get_state(self) -> EngineState:
        """Get current engine state"""
        return self._state
    
    def health_check(self) -> dict:
        """
        Perform comprehensive health check
        
        Returns:
            Dictionary with health status
        """
        return {
            "status": "healthy" if self._state == EngineState.RUNNING else "unhealthy",
            "state": self._state.value,
            "components": {
                "event_bus": self.event_bus.get_stats(),
                "registry": self.registry.get_stats(),
                "policy_guard": self.policy_guard.get_stats(),
                "scheduler": self.scheduler.get_stats()
            },
            "agents": [agent.get_name() for agent in self._agents],
            "phase": config.CURRENT_PHASE
        }

"""
PROJECT PREDATOR - PolicyGuard
Central Risk Officer (CRO) gate - enforces all policies
"""
import logging
from typing import Any, Optional
from backend.core.event_bus import EventBus, EventType


class PolicyDecision:
    """Policy decision result"""
    
    def __init__(self, allowed: bool, reason: str = ""):
        self.allowed = allowed
        self.reason = reason


class PolicyGuard:
    """
    Central policy enforcement point (CRO Gate)
    
    EVERY critical action must pass through PolicyGuard.
    
    Responsibilities:
    - Enforce risk limits
    - Global kill switch
    - Block unauthorized actions
    - Trigger system halts
    
    Phase 2 Note: This is a STUB implementation.
    Real policy logic will be added in future phases.
    """
    
    def __init__(self, event_bus: EventBus):
        """
        Initialize PolicyGuard
        
        Args:
            event_bus: EventBus instance
        """
        self.logger = logging.getLogger(__name__)
        self.event_bus = event_bus
        
        # Policy state
        self._global_kill_switch = False
        self._system_halted = False
        
        # Stats
        self._decisions_made = 0
        self._denials = 0
        
        self.logger.info("PolicyGuard initialized (CRO Gate active)")
    
    def check_system_start(self) -> PolicyDecision:
        """
        Check if system is allowed to start
        
        Returns:
            PolicyDecision
        """
        self._decisions_made += 1
        
        if self._global_kill_switch:
            self._denials += 1
            self.logger.warning("DENIED: System start blocked by global kill switch")
            return PolicyDecision(False, "Global kill switch active")
        
        self.logger.info("ALLOWED: System start")
        return PolicyDecision(True, "System start permitted")
    
    def check_order_submission(self, order: Any) -> PolicyDecision:
        """
        Check if order is allowed to be submitted
        
        Args:
            order: Order object
        
        Returns:
            PolicyDecision
        """
        self._decisions_made += 1
        
        if self._global_kill_switch:
            self._denials += 1
            self.logger.warning("DENIED: Order blocked by global kill switch")
            return PolicyDecision(False, "Global kill switch active")
        
        if self._system_halted:
            self._denials += 1
            self.logger.warning("DENIED: Order blocked - system halted")
            return PolicyDecision(False, "System halted")
        
        # Phase 2: All orders are allowed (stub logic)
        self.logger.info(f"ALLOWED: Order submission (STUB - no real checks)")
        return PolicyDecision(True, "Order permitted (stub)")
    
    def activate_kill_switch(self, reason: str = "Manual activation") -> None:
        """
        Activate global kill switch
        
        Args:
            reason: Reason for activation
        """
        self.logger.critical(f"KILL SWITCH ACTIVATED: {reason}")
        self._global_kill_switch = True
        self._system_halted = True
        
        # Publish critical event
        self.event_bus.publish(
            EventType.KILL_SWITCH_ACTIVATED,
            {"reason": reason},
            source="PolicyGuard"
        )
    
    def deactivate_kill_switch(self) -> None:
        """Deactivate global kill switch (requires manual intervention)"""
        self.logger.warning("Kill switch deactivated - manual intervention")
        self._global_kill_switch = False
        self._system_halted = False
    
    def halt_system(self, reason: str = "Policy violation") -> None:
        """
        Halt the system
        
        Args:
            reason: Reason for halt
        """
        self.logger.critical(f"SYSTEM HALTED: {reason}")
        self._system_halted = True
        
        self.event_bus.publish(
            EventType.SYSTEM_ERROR,
            {"reason": reason, "action": "HALT"},
            source="PolicyGuard"
        )
    
    def is_system_halted(self) -> bool:
        """Check if system is halted"""
        return self._system_halted
    
    def get_stats(self) -> dict:
        """Get PolicyGuard statistics"""
        return {
            "global_kill_switch": self._global_kill_switch,
            "system_halted": self._system_halted,
            "decisions_made": self._decisions_made,
            "denials": self._denials,
            "denial_rate": self._denials / max(1, self._decisions_made)
        }

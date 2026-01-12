"""
PROJECT PREDATOR - Main Entry Point
Bootstraps and runs the Trading OS
"""
import signal
import sys
import time
import uvicorn
from threading import Thread

# Setup logging first
from backend.monitor.logging import setup_logging
logger = setup_logging()

# Import core components
from backend.core.engine import CoreEngine
from backend.core.config import config
from backend.monitor.health import HealthMonitor

# Import all agents (FAZ 2 - Blueprint structure)
from backend.agents.market_scanner.agent import MarketScannerAgent
from backend.agents.data_engineering.agent import DataEngineeringAgent
from backend.agents.execution.agent import ExecutionAgent
from backend.agents.portfolio.agent import PortfolioManagerAgent
from backend.agents.cro.agent import CRORiskAgent
from backend.agents.performance.agent import PerformanceKPIAgent
from backend.agents.aspa.agent import ASPAAgent
from backend.agents.rrs.agent import RRSAgent
from backend.agents.rrs.agent import RRSAgent


class PredatorPlatform:
    """
    Main platform orchestrator
    
    Integrates FAZ 1 (Core Platform) and FAZ 2 (Agent Skeletons).
    """
    
    def __init__(self):
        """Initialize the platform"""
        logger.info("=" * 80)
        logger.info("PROJECT PREDATOR - Trading Operating System")
        logger.info(f"Phase: {config.CURRENT_PHASE} (FAZ 2 - Agent Skeletons)")
        logger.info(f"Environment: {config.ENVIRONMENT}")
        logger.info("=" * 80)
        
        # Initialize core engine (FAZ 1)
        self.core_engine = CoreEngine()
        
        # Initialize health monitor
        self.health_monitor = HealthMonitor(self.core_engine)
        
        # Initialize agents (FAZ 2)
        self._initialize_agents()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self._health_server = None
    
    def _initialize_agents(self) -> None:
        """
        Initialize and register all agents (FAZ 2 - Blueprint)
        
        Agents (per Blueprint):
        - MarketScannerAgent: On Tick → log "scanning market"
        - DataEngineeringAgent: On Tick → log "processing data"
        - ExecutionAgent: On OrderRequest → log "would execute"
        - PortfolioManagerAgent: On Tick → log "checking portfolio"
        - CRORiskAgent: On RiskEvent → log "risk check"
        - PerformanceKPIAgent: On ExecutionResult → log "recording KPI"
        - ASPAAgent: On StrategyReviewEvent → log "analyzing strategy"
        - RRSAgent: Every N seconds → log "infra OK"
        """
        logger.info("Initializing agents (FAZ 2 - Blueprint)...")
        
        event_bus = self.core_engine.event_bus
        registry = self.core_engine.registry
        
        # Create agents (exact Blueprint order)
        agents = [
            MarketScannerAgent(event_bus, registry),
            DataEngineeringAgent(event_bus, registry),
            ExecutionAgent(event_bus, registry),
            PortfolioManagerAgent(event_bus, registry),
            CRORiskAgent(event_bus, registry),
            PerformanceKPIAgent(event_bus, registry),
            ASPAAgent(event_bus, registry),
            RRSAgent(event_bus, registry)
        ]
        
        # Register agents with CoreEngine
        for agent in agents:
            self.core_engine.register_agent(agent)
        
        logger.info(f"[OK] {len(agents)} agents initialized and registered")
    
    def start(self) -> bool:
        """
        Start the platform
        
        Returns:
            True if started successfully
        """
        logger.info("Starting PROJECT PREDATOR...")
        
        # Start core engine (which starts all agents)
        if not self.core_engine.start():
            logger.error("Failed to start CoreEngine")
            return False
        
        # Start health check server
        self._start_health_server()
        
        logger.info("=" * 80)
        logger.info("[OK] PROJECT PREDATOR is RUNNING")
        logger.info(f"[OK] Health check: http://localhost:{config.HEALTH_CHECK_PORT}/health")
        logger.info("=" * 80)
        
        return True
    
    def stop(self) -> bool:
        """
        Stop the platform
        
        Returns:
            True if stopped successfully
        """
        logger.info("Stopping PROJECT PREDATOR...")
        
        # Stop health server
        if self._health_server:
            self._health_server.should_exit = True
        
        # Stop core engine (which stops all agents)
        result = self.core_engine.stop()
        
        logger.info("=" * 80)
        logger.info("[OK] PROJECT PREDATOR stopped")
        logger.info("=" * 80)
        
        return result
    
    def run(self) -> None:
        """
        Run the platform
        
        Starts the platform and keeps it running until interrupted.
        """
        if not self.start():
            logger.error("Failed to start platform")
            sys.exit(1)
        
        try:
            # Keep running
            while True:
                time.sleep(1.0)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            self.stop()
    
    def _start_health_server(self) -> None:
        """Start the health check HTTP server"""
        def run_server():
            uvicorn.run(
                self.health_monitor.get_app(),
                host="0.0.0.0",
                port=config.HEALTH_CHECK_PORT,
                log_level="warning"
            )
        
        self._health_server = Thread(target=run_server, daemon=True)
        self._health_server.start()
        logger.info(f"Health check server started on port {config.HEALTH_CHECK_PORT}")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        logger.info(f"Received signal {signum}")
        self.stop()
        sys.exit(0)


def main():
    """Main entry point"""
    platform = PredatorPlatform()
    platform.run()


if __name__ == "__main__":
    main()

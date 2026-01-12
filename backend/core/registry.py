"""
PROJECT PREDATOR - Registry
Central component registry for controlled lookup
"""
import logging
from typing import Any, Optional, Dict


class Registry:
    """
    Central registry for all system components
    
    Allows controlled component lookup without global variables.
    Enforces architecture boundaries.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._components: Dict[str, Any] = {}
        self.logger.info("Registry initialized")
    
    def register(self, name: str, component: Any) -> None:
        """
        Register a component
        
        Args:
            name: Component name
            component: Component instance
        """
        if name in self._components:
            self.logger.warning(f"Component {name} already registered, overwriting")
        
        self._components[name] = component
        self.logger.info(f"Registered component: {name}")
    
    def get(self, name: str) -> Optional[Any]:
        """
        Get a component by name
        
        Args:
            name: Component name
        
        Returns:
            Component instance or None
        """
        component = self._components.get(name)
        if component is None:
            self.logger.warning(f"Component {name} not found in registry")
        return component
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a component
        
        Args:
            name: Component name
        
        Returns:
            True if unregistered, False if not found
        """
        if name in self._components:
            del self._components[name]
            self.logger.info(f"Unregistered component: {name}")
            return True
        else:
            self.logger.warning(f"Cannot unregister {name}: not found")
            return False
    
    def list_components(self) -> list:
        """Get list of registered component names"""
        return list(self._components.keys())
    
    def get_stats(self) -> dict:
        """Get registry statistics"""
        return {
            "component_count": len(self._components),
            "components": self.list_components()
        }

"""
Logging utility for LAEV-Agents.
Provides consistent logging configuration across the project.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    handler: Optional[logging.Handler] = None
) -> logging.Logger:
    """
    Set up a logger with consistent configuration.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        format_string: Custom format string
        handler: Custom handler (default: StreamHandler to stdout)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Application started")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Default format
    if format_string is None:
        format_string = (
            "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
        )
    
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Default handler
    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    return logger


class AgentLogger:
    """
    Logger wrapper for agents with structured logging support.
    
    Provides methods for logging agent actions with consistent formatting.
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize agent logger.
        
        Args:
            agent_name: Name of the agent (e.g., "PlannerAgent")
        """
        self.logger = setup_logger(f"agents.{agent_name}")
        self.agent_name = agent_name
    
    def action(self, action: str, details: Optional[dict] = None):
        """
        Log an agent action.
        
        Args:
            action: Description of the action
            details: Optional dictionary of additional details
        """
        message = f"[{self.agent_name}] {action}"
        if details:
            message += f" | {details}"
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(f"[{self.agent_name}] {message}")
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(f"[{self.agent_name}] {message}")
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(f"[{self.agent_name}] {message}")
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(f"[{self.agent_name}] {message}")
    
    def exception(self, message: str):
        """Log exception with traceback."""
        self.logger.exception(f"[{self.agent_name}] {message}")


# Global logger for the module
logger = setup_logger("laev_agents")

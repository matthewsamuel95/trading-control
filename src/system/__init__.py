"""
System package for trading system orchestration and production
"""

from .professional_trading_orchestrator import (
    SupervisorOrchestrator, TradingState, TradingPhase,
    SafetyProtocol, create_professional_orchestrator
)

from .production_trading_system import (
    ProductionTradingAPI, ProductionTradingSystem
)

from .claude_code_template import (
    TradingSystemClaudeTemplate, create_trading_template
)

__all__ = [
    # Professional orchestration
    'SupervisorOrchestrator', 'TradingState', 'TradingPhase',
    'SafetyProtocol', 'create_professional_orchestrator',
    
    # Production system
    'ProductionTradingAPI', 'ProductionTradingSystem',
    
    # Claude integration
    'TradingSystemClaudeTemplate', 'create_trading_template'
]

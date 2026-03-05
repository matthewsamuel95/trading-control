"""
Agent Factory Registration - Clean Agent System
Registers all concrete agent implementations with the factory
"""

from agent.agent_contract import AgentFactory
from agent.business_analyst import BusinessAnalystAgent
from agent.sentiment_analyst import SentimentAnalystAgent
from agent.technical_analyst import TechnicalAnalystAgent

# Register all agent types with the factory
AgentFactory.register_agent_type("technical_analyst", TechnicalAnalystAgent)
AgentFactory.register_agent_type("business_analyst", BusinessAnalystAgent)
AgentFactory.register_agent_type("sentiment_analyst", SentimentAnalystAgent)

# Export key components for easy access
__all__ = [
    "AgentFactory",
    "TechnicalAnalystAgent",
    "BusinessAnalystAgent",
    "SentimentAnalystAgent",
]

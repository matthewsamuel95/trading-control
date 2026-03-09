---
name: trading-agent-orchestration
description: Multi-agent orchestration and communication for collaborative trading decisions. Use when you need to coordinate multiple trading agents, run collaborative analysis, or manage agent workflows like "coordinate the trading agents" or "run the analysis team".
---

# Trading Agent Orchestration

Manages multi-agent workflows and collaborative decision-making for trading strategies.

## Quick Start
```python
from trading_agent_orchestration.scripts.orchestrator import OpenClawOrchestrator

orchestrator = OpenClawOrchestrator()
await orchestrator.start()

# Execute analysis cycle
result = await orchestrator.execute_cycle()
print(f"Cycle success: {result.success}")

status = orchestrator.get_status()
print(f"Success rate: {status['success_rate']:.2%}")
```

## Features
- **Multi-agent coordination** with lifecycle management
- **Cycle-based execution** with comprehensive tracking
- **Status monitoring** and health checks
- **Error handling** with graceful recovery

## Orchestrator States
- **IDLE**: Ready to start execution
- **RUNNING**: Actively processing cycles
- **STOPPED**: Shutdown and inactive
- **ERROR**: Error state requiring intervention

## Cycle Workflow
1. **Data Collection**: Gather market data and inputs
2. **Agent Analysis**: Process through multiple agents
3. **Signal Generation**: Produce trading signals
4. **Consensus Building**: Reach collaborative decisions

## Output Format
```python
{
    "cycle_id": "uuid",
    "success": True,
    "signals_generated": 3,
    "tasks_executed": 5,
    "steps_completed": ["data_collection", "analysis", "signal_generation"],
    "errors": []
}
```

## Performance Metrics
- **Cycle Time**: Typically less than 100ms per cycle
- **Success Rate**: Tracks execution success over time
- **Error Tracking**: Detailed error logging and analysis

---
*See [references/agent-architecture.md](references/agent-architecture.md) for detailed agent workflow specifications.*

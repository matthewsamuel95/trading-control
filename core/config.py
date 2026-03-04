"""
Configuration management for Trading Control Platform
"""

import os
from typing import Optional

try:
    import structlog

    logger = structlog.get_logger()
except ImportError:
    logger = None


class Settings:
    """Application settings"""

    def __init__(self) -> None:
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.environment = os.getenv("ENVIRONMENT", "development")

        # Trading Configuration
        self.max_concurrent_tasks = int(os.getenv("MAX_CONCURRENT_TASKS", "50"))
        self.task_queue_size = int(os.getenv("TASK_QUEUE_SIZE", "1000"))
        self.agent_pool_size = int(os.getenv("AGENT_POOL_SIZE", "10"))
        self.auto_scaling_enabled = (
            os.getenv("AUTO_SCALING_ENABLED", "true").lower() == "true"
        )

        # Performance Thresholds
        self.min_accuracy_threshold = float(os.getenv("MIN_ACCURACY_THRESHOLD", "0.6"))
        self.min_sharpe_ratio_threshold = float(
            os.getenv("MIN_SHARPE_RATIO_THRESHOLD", "0.5")
        )
        self.max_error_rate_threshold = float(
            os.getenv("MAX_ERROR_RATE_THRESHOLD", "0.1")
        )

        # Data Configuration
        self.data_update_frequency_ms = int(
            os.getenv("DATA_UPDATE_FREQUENCY_MS", "5000")
        )
        self.consensus_timeout_ms = int(os.getenv("CONSENSUS_TIMEOUT_MS", "30000"))

        # External API Keys
        self.langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        self.langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        self.langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        self.langfuse_enabled = os.getenv("LANGFUSE_ENABLED", "true").lower() == "true"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> None:
    """Reload settings from environment"""
    global _settings
    _settings = Settings()

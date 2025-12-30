# Common configuration utilities
import os
from typing import Optional

def get_env_variable(key: str, default: Optional[str] = None) -> str:
    """Get environment variable with optional default."""
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return value

def is_development() -> bool:
    """Check if running in development mode."""
    return get_env_variable("ENVIRONMENT", "development") == "development"
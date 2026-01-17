from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Database Helper"
    API_V1_STR: str = "/api/v1"
    METADATA_DB_URL: str = "sqlite:///./metadata.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # LLM
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: str = "openai"
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
    OLLAMA_MODEL: str = "llama3"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

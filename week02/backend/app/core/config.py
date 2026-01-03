from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Database Helper"
    API_V1_STR: str = "/api/v1"
    METADATA_DB_URL: str = "sqlite:///./metadata.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

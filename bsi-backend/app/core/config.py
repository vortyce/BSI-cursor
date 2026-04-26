from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/bsi_db"
    APP_NAME: str = "BTC Signal Intelligence"
    DEBUG: bool = True
    ENVIRONMENT_MODE: str = "DEVELOPMENT"
    
    # LLM Settings
    DEFAULT_LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o"
    PROMPT_VERSION: str = "v1.0"

    class Config:
        env_file = ".env"

settings = Settings()

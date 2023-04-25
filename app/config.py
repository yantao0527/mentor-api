# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DEFAULT_VAR="some default string value"  # default value if env variable does not exist
    API_KEY: str
    APP_MAX: int=100 # default value if env variable does not exist
    OPENAI_API_KEY: str

    # specify .env file location as Config attribute
    class Config:
        env_file = ".env"
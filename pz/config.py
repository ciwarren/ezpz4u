from pydantic import BaseSettings
class Settings(BaseSettings):
    username: str
    password: str
    collection_id: str
    host: str = "0.0.0.0"
    port: int = 1337
    server_config_path: str = "/home/steam/Zomboid/Server/servertest.ini"

    class Config:
        env_file = "/opt/pz/.env"

settings = Settings()
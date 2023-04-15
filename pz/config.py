from pydantic import BaseSettings
class Settings(BaseSettings):
    username: str
    password: str
    collection_id: str
    server_management_path: str = "/home/steam/pz/server.sh"
    server_config_path: str = "/home/steam/pz/projectzomboid/Zomboid/Server/servertest.ini"

    class Config:
        env_file = "/opt/pz/.env"

settings = Settings()
from .pz import PZServer
from .config import Settings
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import secrets, json
import uvicorn

app_config = Settings()
pz = PZServer(app_config)
app = FastAPI()
security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = app_config.username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = app_config.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}

@app.get("/server/stop_server")
def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.stop_server()

@app.get("/server/start_server")
def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.start_server()

@app.get("/server/restart_server")
def restart_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.restart_server()

@app.get("/server/update_mods")
def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.update_server_mods()

@app.get("/server/update_server")
def update_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.update_server()

@app.get("/server/stats")
def update_server():
    return pz.get_stats_server()

def start_server():
    uvicorn.run(
        app,
        host=app_config.host,
        port=app_config.port,
        log_level="debug",
    )

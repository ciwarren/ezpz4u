from pz import PZServer
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets, json

pz = PZServer(config_path="pz_config.json")
app_config = json.load("api_config.json")
app = FastAPI()
security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = app_config.get("username").encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = app_config.get("password").encode("utf8")
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
async def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.stop_server()

@app.get("/server/start_server")
async def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.start_server()

@app.get("/server/restart_server")
async def restart_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.restart_server()

@app.get("/server/update_mods")
async def stop_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.update_server_mods()

@app.get("/server/update_server")
async def update_server(username: Annotated[str, Depends(get_current_username)]):
    if username == "admin":
        return pz.update_server()

@app.get("/server/stats")
async def get_stats():
    return pz.get_stats_server()    
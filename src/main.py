from fastapi import FastAPI
from fastapi.security import HTTPBearer
import uvicorn

from middleware.load_env import load_env

# Load .env before any import that builds agents (agent_service needs OPENAI_API_KEY)
load_env()

from middleware.register_middleware import register_middlewares

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app.title = 'Uranus_server'
auth_scheme = HTTPBearer()

# Adding middleares
register_middlewares(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=4300, log_level="info", reload=True)

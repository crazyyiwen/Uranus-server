from fastapi import FastAPI
from fastapi.security import HTTPBearer
import uvicorn
from middleware.register_middleware import register_middlewares
import routing.modules_injection as modules_injection

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app.title = 'Uranus_server'
auth_scheme = HTTPBearer()

# Adding middleares
register_middlewares(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=4300, log_level="info", reload=True)

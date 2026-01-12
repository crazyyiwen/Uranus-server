from fastapi import FastAPI
from fastapi.security import HTTPBearer
import uvicorn
from middleware.register_middleware import register_middlewares
import routing.modules_injection as modules_injection

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app.title = 'leo-p2p-common-ai'
auth_scheme = HTTPBearer()

# Adding middleares
register_middlewares(app)

# Include the API routes
for router in modules_injection.routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=4300, log_level="info")

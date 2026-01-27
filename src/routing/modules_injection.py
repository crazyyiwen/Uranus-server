from api import agent_api
from api import health_check_api

# adding routers
routers = [
    agent_api.router,
    health_check_api.router
]
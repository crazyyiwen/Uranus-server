from api import common_agent_api
from api import health_check_api

# adding routers
routers = [
    common_agent_api.router,
    health_check_api.router
]
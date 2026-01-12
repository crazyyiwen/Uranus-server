from api import duplication_check_api, recommendation_api, buyer_agent_api, deep_agent_mcp_api

# adding routers
routers = [
    recommendation_api.router,
    duplication_check_api.router,
    buyer_agent_api.router,
    deep_agent_mcp_api.router
]
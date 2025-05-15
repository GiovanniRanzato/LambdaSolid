from api.api_gateway.routes.default.v1.router import router as default_v1_router

routers = [
    {
        "router": default_v1_router,
        "prefix": "/api/v1",
        "tags": ["default"]
    }
]
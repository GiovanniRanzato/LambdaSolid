from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from inputs.api_gateway.exceptions.ExceptionsRegistry import ExceptionRegistry
from inputs.api_gateway.routes.routes import routers
from inputs.api_gateway.interfaces.APIGatewayRequestI import APIGatewayRequestI

from infrastructure.containers import Container
from infrastructure.interfaces.ConfigI import ConfigI
from infrastructure.interfaces.HandlerI import HandlerI


class APIGatewayHandler(HandlerI):
    @inject
    def __init__(self, config: ConfigI = Provide[Container.config], standalone=False):
        self.standalone = standalone
        self.app_name = config.get("APP_NAME")
        self.doc_url = config.get("FASTAPI_DOCS_URL")
        self.redoc_url = config.get("FASTAPI_REDOC_URL")
        self.cors_allow_origins = config.get("CORS_ALLOW_ORIGINS")
        self.cors_allow_methods = config.get("CORS_ALLOW_METHODS")
        self.cors_allow_headers = config.get("CORS_ALLOW_HEADERS")

    def handle(self, event: APIGatewayRequestI):
        print(f"Handling API Gateway event: {event}")
        fast_api = FastAPI(
            title=self.app_name,
            version=event.get_version(),
            root_path="/{}/".format(event.get_stage()),
            docs_url=self.doc_url,
            openapi_url="/openapi.json",
            redoc_url=self.redoc_url,
        )
        self._set_exceptions_handlers(fast_api)
        self._set_middlewares(fast_api)
        self._set_routes(fast_api)

        if self.standalone:
            return fast_api

        asgi_handler = Mangum(app=fast_api, lifespan="off")

        return asgi_handler(event.get_body(), event.get_context())

    @staticmethod
    def _set_routes(fast_api):
        for router in routers:
            fast_api.include_router(router.get("router"), prefix=router.get("prefix"))

    @staticmethod
    def _set_exceptions_handlers(fast_api):
        for class_handler in ExceptionRegistry.exceptions_handlers():
            fast_api.add_exception_handler(class_handler.handled_exception(), class_handler.handle)

    def _set_middlewares(self, fast_api):
        fast_api.add_middleware(
            CORSMiddleware,
            allow_origins=self.cors_allow_origins.split(","),
            allow_credentials=True,
            allow_methods=self.cors_allow_methods,
            allow_headers=self.cors_allow_headers,
        )


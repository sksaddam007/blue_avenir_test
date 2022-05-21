from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# import py_eureka_client.eureka_client as eureka_client
from app.api.api_v1.api import api_router
from app.core.config import settings

# rest_port = 8000
# eureka_client.init(eureka_server="http://localhost:8761/eureka",
#                    eureka_protocol="https",
#                    eureka_basic_auth_user="admin",
#                    eureka_basic_auth_password="admin",
#                    eureka_context="/eureka/v2",
#                    app_name="python_module_1",
#                    instance_port=rest_port)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

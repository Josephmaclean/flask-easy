# """OpenAPI v3 Specification"""
#
# # apispec via OpenAPI
# from apispec import APISpec
# from apispec.ext.marshmallow import MarshmallowPlugin
# from apispec_webframeworks.flask import FlaskPlugin
#
# spec = APISpec(
#     title="Flask Easy",
#     version="1.0.0",
#     openapi_version="3.0.2",
#     plugins=[FlaskPlugin(), MarshmallowPlugin()],
# )
# # Security
# api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
# bearer_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
# spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
# spec.components.security_scheme("bearerAuth", bearer_scheme)

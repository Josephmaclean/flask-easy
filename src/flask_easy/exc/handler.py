from flask import Response, json
from .app_exceptions import HTTPException


def app_exception_handler(exc):
    if isinstance(exc, HTTPException):
        return Response(
            json.dumps(
                {"app_exception": "HTTP Error", "errorMessage": exc.description}
            ),
            status=exc.code,
        )
    return Response(
        json.dumps({"app_exception": exc.exception_case, "errorMessage": exc.context}),
        status=exc.status_code,
        mimetype="application/json",
    )

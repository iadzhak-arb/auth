from authx import TokenExpiredError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

from .auth import auth


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    formatted_errors = [
        {
            'field': ".".join(map(str, err["loc"][1:])),
            'message': err["msg"],
        }
        for err in exc.errors()
    ]
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=formatted_errors
    )


async def token_expired_handler(request: Request, exc: TokenExpiredError):
    raise HTTPException(
        status_code=401,
        detail={"type": "Unauthorized", "error": "Token has expired"},
    )


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )
    auth.handle_errors(app)
    app.add_exception_handler(TokenExpiredError, token_expired_handler)

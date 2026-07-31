from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError

from .main import app


@app.exception_handler(RequestValidationError)
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
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=formatted_errors)


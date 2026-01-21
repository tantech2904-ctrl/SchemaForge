from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.exceptions import AppException


def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code
        }
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )


def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )

from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Step 1 — let DRF handle it first the default way
    response = exception_handler(exc, context)

    if response is not None:
        # Step 2 — reshape it into our consistent format
        response.data = {
            "success": False,
            "error": {
                "code": get_error_code(response.status_code),
                "message": get_error_message(response.status_code),
                "details": response.data
            }
        }

    return response


def get_error_code(status_code):
    codes = {
        400: "validation_error",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        429: "too_many_requests",
    }
    return codes.get(status_code, "server_error")


def get_error_message(status_code):
    messages = {
        400: "Invalid input.",
        401: "Authentication required.",
        403: "You do not have permission to perform this action.",
        404: "The requested resource was not found.",
        429: "Too many requests. Please slow down.",
    }
    return messages.get(status_code, "An unexpected error occurred.")

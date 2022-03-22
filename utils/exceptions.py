from sanic.exceptions import SanicException
from tortoise.exceptions import IntegrityError


class BadRequest(SanicException):
    status_code = 400
    message = 'Bad Request'
    quiet = True


class ValidationError(BadRequest):
    message = 'Validation Error'


async def integrity_error_handler(request, exception: IntegrityError):
    raise BadRequest(str(exception))

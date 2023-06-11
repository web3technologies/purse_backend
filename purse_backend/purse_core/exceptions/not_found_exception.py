from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 400
    default_detail = "Object not found"
    default_code = "object_not_found"
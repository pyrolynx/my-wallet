class APIError(Exception):
    http_code = 500
    message: str


class InvalidContent(APIError):
    http_code = 400
    message = "json body expected"


class InvalidArgument(APIError):
    def __init__(self, arg_name):
        self.message = self.message.format(arg_name)

    http_code = 400
    message = "argument `{}` have invalid value"


class MissingArgument(APIError):
    def __init__(self, arg_name):
        self.message = self.message.format(arg_name)

    http_code = 400
    message = "argument `{}` is missing"


class InvalidTransactionType(APIError):
    http_code = 400
    message = "invalid transaction type"

class ProjectControllerError(Exception):
    code_error = None
    message = None

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AppSecurityControllerError(Exception):
    message = None

    def __init__(self, message):
        self.message = message
        super().__init__(message)

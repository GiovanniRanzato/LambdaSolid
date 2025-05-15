class UnauthorizedException(Exception):
    def __str__(self):
        return "Unauthorized Exception"

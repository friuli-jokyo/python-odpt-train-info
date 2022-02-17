from urllib.error import HTTPError


class OdptException(Exception):
    """Base exception class of odpttraininfo."""

    pass

class HTTPException(OdptException):
    """HTTP status error"""

    code: int
    """Response HTTP status code."""

    reason: str
    """Response HTTP status message."""

    def __init__(self, e: HTTPError) -> None:
        self.code = e.code
        self.reason = str(e.reason)

    def __str__(self) -> str:
        if self.reason:
            return "StatusCode:%s (%s)" % (self.code,self.reason)
        else:
            return "StatusCode:%s" % (self.code)

    pass

class InvalidParameterError(HTTPException):
    """HTTP status code was 400."""
    pass

class InvalidConsumerKeyError(HTTPException):
    """HTTP status code was 401."""
    pass

class Forbidden(HTTPException):
    """HTTP status code was 403."""

    def __str__(self) -> str:
        return "%s Maybe acl:consumerKey is not correct." % (super().__str__())

class NotFound(HTTPException):
    """HTTP status code was 404."""

    url: str
    """URL which is not found."""

    def __init__(self, e: HTTPError, url: str) -> None:
        super().__init__(e)
        self.url = url

    def __str__(self) -> str:
        return "%s URL: %s" % (super().__str__(), self.url)

class UnknownHTTPError(HTTPException):
    """HTTP status code was unexpected."""
    pass

class OdptServerError(HTTPException):
    """HTTP status code was 500 through 599."""
    pass

class TooOldCacheError(OdptException):
    pass
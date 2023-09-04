from fastapi import HTTPException, status


class NoDatabaseConnection(HTTPException):
    def __init__(self):
        super(HTTPException, self).__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No database connection"
        )


class GetErrorFromBlackbox(Exception):
    pass

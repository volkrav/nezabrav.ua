from fastapi import HTTPException, status


NoDatabaseConnection = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="No database connection"
)


ClientNotFoundInBlackbox = HTTPException(
    status_code=status.HTTP_410_GONE,
    detail="Client not found"
)

GetErrorFromApiBlackbox = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
)

BlackboxRequestTimeoutExpired = HTTPException(
    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    detail="blackbox request timed out"
)

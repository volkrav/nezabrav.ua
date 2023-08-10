from fastapi import HTTPException, status


NoDatabaseConnection = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='No database connection'
)

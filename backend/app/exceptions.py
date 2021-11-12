from fastapi import status, HTTPException

EXCEPTION_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
from typing import Generator
from app.database import SessionLocal
from fastapi import HTTPException,Header
from app.security import verify_access_token


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#Will work as depedency/middleware for api key validity
def token_verification(type: str = "User"):
    def _token_verification(token: str = Header(..., description="Bearer JWT Authentication")):
        # Check if the API key is present
        if not token:
            raise HTTPException(status_code=403, detail="JWT is missing")
        # Verify the token
        valid=verify_access_token(token=token)
        if not valid:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return valid
    return _token_verification


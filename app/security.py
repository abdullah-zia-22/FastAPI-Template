from typing import Union,Any
from jose import jwt
from app.constants import TOKEN_ALGORITHM,SECRET_KEY,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime,timedelta
from passlib.context import CryptContext

def create_access_token(
    subject: Union[int, Any], is_admin=0, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "is_admin": is_admin}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, check_admin=False) -> Any:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=TOKEN_ALGORITHM)
        if not check_admin:
            return int(decoded_token["sub"])
        else:
            return int(decoded_token["sub"]), decoded_token.get("is_admin")
    except jwt.JWTError as exx:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
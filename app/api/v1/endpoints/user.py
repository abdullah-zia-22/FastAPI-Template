from typing import Any
from fastapi import APIRouter, Depends,HTTPException,Body
from sqlalchemy.orm import Session
import app.crud as crud
from app.dependencies import get_db,token_verification
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.security import create_access_token,verify_password

router = APIRouter()


@router.get("/list_all/",dependencies=[Depends(token_verification())])
async def list_all(
    *,
    db: Session = Depends(get_db),
    search: str = None
) -> Any:
    """
    Get Users in Database
    """
    results = await crud.user.get_all(db=db,search=search)
    if not results:
        raise HTTPException(status_code=404, detail="No Data Found")
    return jsonable_encoder({"status":"success", "data":results})

@router.post("/login/")
async def login(
    *,
    db: Session = Depends(get_db),
    email: str = Body(...),
    password: str = Body(...),
) -> Any:
    """
    Login API
    """
    email = email.lower()
    user = await crud.user.authenticate(
        db, email=email
    )
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Email or Password")
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jsonable_encoder({
        "access_token":create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    })



# book_service/app/auth.py


from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from .database import SettingsDep
from .security import hash_password, create_access_token, verify_password

router = APIRouter(prefix="/token", tags=["auth"])

USERS = {
    "teacher": {
        "username": "teacher",
        "hashed_password": hash_password("classroom"),
        "roles": ["editor"],
    }
}

def authenticate(username: str, password: str):
    record = USERS.get(username)
    if not record or not verify_password(password, record["hashed_password"]):
        return None
    return record

# A simple Pydantic model for the login request
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("", response_model=Token)        # ← POST /token
@router.post("/login", response_model=Token) # ← POST /token/login

def login(
    form: LoginRequest,
    settings: SettingsDep,
):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        subject=user["username"],
        roles=user["roles"],
        settings=settings,
        expires_delta=timedelta(minutes=settings.jwt_expiry_minutes),
    )
    return {"access_token": access_token, "token_type": "bearer"}
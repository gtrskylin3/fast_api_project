from fastapi import APIRouter, Depends, Form, HTTPException, status, Header
from users.schemas import UserSchema
from pydantic import BaseModel
from auth import utils as auth_utils
from jwt import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])


john = UserSchema(
    username="John",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

danya = UserSchema(
    username="ZXCdanchik",
    password=auth_utils.hash_password("qwerty"),
    email="danya@example.com",
)


users_db: dict[str, UserSchema] = {john.username: john, danya.username: danya}


# pip install python-multipart
def validate_auth_user(username: str = Form(), password: str = Form()):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password"
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user inactive"
        )

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserSchema:
    try:
        token = credentials.credentials
        payload = auth_utils.decode_jwt(
            token=token,
        )
        print(payload)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")


@router.post("/login", response_model=TokenInfo)
def auth_user_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject - то к чему принадлежит тоесть id или username
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=access_token, token_type="Bearer")


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get('iat')
    return {
        "username": user.username,
        "email": user.email,
        "logged_at": iat,
    }

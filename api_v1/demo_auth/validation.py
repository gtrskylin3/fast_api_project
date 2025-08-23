from typing import Any
from fastapi import APIRouter, Depends, Form, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from api_v1.demo_auth.helpers import create_access_token, create_refresh_token
from users.schemas import UserSchema
from auth import utils as auth_utils
from jwt import InvalidTokenError
from .crud import users_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/jwt/login/")


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    try:
        # token = credentials.credentials
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


from .helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=401,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_user_by_token_sub(payload) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return get_user_by_token_sub(payload)


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")


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


# def get_current_auth_user(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:
#     return get_user_by_token_sub(payload)


# def get_current_auth_user_for_refresh(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserSchema:

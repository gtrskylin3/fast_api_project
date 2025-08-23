from api_v1.demo_auth.validation import (
    Depends,
    HTTPException,
    UserSchema,
    get_current_auth_user,
    status,
)
from users.schemas import UserSchema


from fastapi import Depends, HTTPException, status


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")

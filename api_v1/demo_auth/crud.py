from auth import utils as auth_utils
from users.schemas import UserSchema


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

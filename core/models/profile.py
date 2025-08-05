from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from .base import Base
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_back_populates = "profile"
    _user_id_unique = True

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    bio: Mapped[str | None]

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True) то же самое уже есть в posts
    # чтобы не повторять код воспульзуемся mixins
    # user: Mapped["User"] = relationship(back_populates="profile")

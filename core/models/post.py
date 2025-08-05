from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .user import User

    # если идет проверка типов а не выполнение кода и избегаем цикл импорт

class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default=''
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        # nullable=False
    )
    # user: Mapped[User] # неможем будет цикл импорт 
    user: Mapped["User"] = relationship(back_populates="posts")
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from .base import Base
from .mixins import UserRelationMixin

    # если идет проверка типов а не выполнение кода и избегаем цикл импорт

# class Post(Base):
#     title: Mapped[str] = mapped_column(String(100), unique=False)
#     body: Mapped[str] = mapped_column(
#         Text,
#         default='',
#         server_default=''
#     )

#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         # nullable=False
#     )
#     # user: Mapped[User] # неможем будет цикл импорт 
#     user: Mapped["User"] = relationship(back_populates="posts")

class Post(Base, UserRelationMixin):
    # _user_id_nullable = False
    # _user_id_unique = False
    _user_back_populates = 'posts'

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default=''
    )
     
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user_id={self.user_id})"
    
    def __repr__(self):
        return str(self)
   
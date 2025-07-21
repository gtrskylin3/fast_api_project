from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    # __tablename__ = "products"

    name: Mapped[str]
    discription: Mapped[str]
    price: Mapped[int]
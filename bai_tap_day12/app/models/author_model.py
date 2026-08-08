from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(String(200), nullable=True)

    books: Mapped[list["BookModel"]] = relationship(
        "BookModel", back_populates="author", cascade="all, delete-orphan"
    )

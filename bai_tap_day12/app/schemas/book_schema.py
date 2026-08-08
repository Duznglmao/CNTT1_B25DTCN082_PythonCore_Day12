from pydantic import BaseModel, ConfigDict

from .author_schema import AuthorResponse


class BookBase(BaseModel):
    title: str
    category: str
    price: float
    borrow_count: int = 0
    available_quantity: int = 0
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author_id: int | None = None
    category: str | None = None
    price: float | None = None
    borrow_count: int | None = None
    available_quantity: int | None = None


class BookResponse(BookBase):
    id: int
    author: AuthorResponse | None = None

    model_config = ConfigDict(from_attributes=True)

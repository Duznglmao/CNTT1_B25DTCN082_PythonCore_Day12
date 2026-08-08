from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import BookModel, AuthorModel
from app.schemas import BookUpdate, BookCreate


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self) -> list[BookModel]:
        return self.db.query(BookModel).all()

    def get_book(self, book_id: int) -> BookModel | None:
        return self.db.query(BookModel).filter(BookModel.id == book_id).first()

    def create_book(self, data: BookCreate) -> BookModel | None:
        try:
            author = (
                self.db.query(AuthorModel)
                .filter(AuthorModel.id == data.author_id)
                .first()
            )
            if author is None:
                return None

            db_book = BookModel(**data.model_dump())
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)
            return db_book
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_book(self, data: BookUpdate, book_id: int) -> BookModel | None:
        try:
            db_book = self.get_book(book_id)
            if not db_book:
                return None

            data_dict = data.model_dump(exclude_unset=True)
            for k, v in data_dict.items():
                setattr(db_book, k, v)

            self.db.commit()
            self.db.refresh(db_book)
            return db_book
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_book(self, book_id: int) -> bool:
        try:
            db_book = self.get_book(book_id)
            if not db_book:
                return False

            self.db.delete(db_book)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def search_books(self, query_str: str) -> list[BookModel]:
        return (
            self.db.query(BookModel)
            .join(AuthorModel)
            .filter(
                BookModel.title.ilike(f"%{query_str}%")
                | AuthorModel.name.ilike(f"%{query_str}%")
                | BookModel.category.ilike(f"%{query_str}%")
            )
            .all()
        )

    def get_book_warning(self, threshold: int) -> list[BookModel]:
        return (
            self.db.query(BookModel)
            .filter(BookModel.available_quantity <= threshold)
            .all()
        )

    def get_top_books(self, limit: int) -> list[BookModel]:
        return (
            self.db.query(BookModel)
            .order_by(BookModel.borrow_count.desc())
            .limit(limit)
            .all()
        )

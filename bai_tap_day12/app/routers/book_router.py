from fastapi import APIRouter, status, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated

from app.schemas import BookResponse, BookUpdate, BookCreate
from app.core import get_db
from app.services import BookService

db_dependency = Annotated[Session, Depends(get_db)]
IdParam = Annotated[int, Path(..., gt=0, description="ID của sách")]

get_book_service = lambda db: BookService(db)

router = APIRouter(prefix="/api/v1/books", tags=["Book Controller"])


@router.get(
    "",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Lấy danh sách sách",
)
def get_books_endpoint(db: db_dependency) -> list[BookResponse]:
    return get_book_service(db).get_books()


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(db: db_dependency, data: BookCreate) -> BookResponse:
    db_book = get_book_service(db).create_book(data)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã tác giả author_id = {data.author_id} không tồn tại trong hệ thống CSDL!",
        )
    return db_book


@router.get(
    "/search",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Tìm kiếm sách",
)
def search_books_endpoint(db: db_dependency, query_str: str) -> list[BookResponse]:
    return get_book_service(db).search_books(query_str)


@router.get(
    "/book_warning",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Cảnh báo số lượng sách sắp hết",
)
def get_book_warning_endpoint(
    db: db_dependency, threshold: int = 5
) -> list[BookResponse]:
    return get_book_service(db).get_book_warning(threshold)


@router.get(
    "/top-borrowed",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Top sách được mượn nhiều nhất",
)
def top_books_endpoint(db: db_dependency, limit: int = 5) -> list[BookResponse]:
    return get_book_service(db).get_top_books(limit)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy chi tiết sách theo ID",
)
def get_book_by_id_endpoint(db: db_dependency, book_id: IdParam) -> BookResponse:
    if (book := get_book_service(db).get_book(book_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} does not exist",
        )
    return book


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật thông tin sách",
)
def update_book_endpoint(
    db: db_dependency, data: BookUpdate, book_id: IdParam
) -> BookResponse:
    if (book := get_book_service(db).update_book(data, book_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} does not exist",
        )
    return book


@router.delete(
    "/{book_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Xóa sách theo ID",
)
def delete_book_endpoint(db: db_dependency, book_id: IdParam) -> dict:
    if not get_book_service(db).delete_book(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} does not exist",
        )
    return {"message": f"Đã xóa thành công sách có id {book_id}"}

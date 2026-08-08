from fastapi import FastAPI, status

from app.routers import book_router
from app.core import Base, engine
from app.models import AuthorModel, BookModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health", status_code=status.HTTP_200_OK, summary="...")
def health_check() -> dict[str, str]:
    return {"message": "FastAPI is running!"}


app.include_router(book_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

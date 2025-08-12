from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


# ----------- Data Model (not Pydantic) -----------
class Book:
    # Basic Book class to simulate a DB model
    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date


# ----------- Pydantic Model for Validation -----------
class BooksRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    publish_date: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A New Book",
                "author": "RJR - First",
                "description": "A Brand new Description",
                "rating": 3,
                "publication date": 2025,
            }
        }
    }


# ----------- In-Memory Storage -----------
BOOKS = [
    Book(1, "Computer Science Pro", "RJR", "Good", 4, 2024),
    Book(2, "Computer Science Pro - 2", "RJR", "Better ", 5, 2024),
    Book(3, "Master End Points", "RJR", "Better", 5, 2023),
    Book(4, "HP - 1", "RJR - 1", "Worse", 1, 2024),
    Book(5, "HP - 2", "RJR - 1", "Bad ", 2, 2023),
    Book(6, "HP - 1", "RJR - 1", "Good", 3, 2023),
]


# ----------- Endpoints -----------


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """Get all books"""
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    """Get a book by its ID"""
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not Found')


@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    """Get books by rating"""
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(publish_date: int):
    """Get books by publish year"""
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BooksRequest):
    """Create a new book entry"""
    converted_value = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(converted_value))  # Assign ID before appending


def find_book_id(book: Book):
    """Assigns a new ID based on the last book's ID"""
    book.id = 1 if len(BOOKS) < 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BooksRequest):
    """Update an existing book (must include ID)"""
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book  # type: ignore
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not Found')


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    """Delete a book by its ID"""
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not Found')


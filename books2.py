from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()


# automatic data validation
class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(max_length=100, min_length=1)
    description: Optional[str] = Field(title="Description of the book", min_length=1, max_length=100)
    rating: int = Field(lt=101, gt=-1)

    # to override default example post body
    class Config:
        schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title": "New Title",
                "author": "New Author",
                "description": "New Description",
                "rating": 8.2
            }
        }


BOOKS = []


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(max_length=100, min_length=1)
    description: Optional[str] = Field(title="Description of the book", min_length=1, max_length=100)


@app.exception_handler(NegativeNumberException)
async def raise_negative_number_exception(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message": f'Hey! Why do you want {exception.books_to_return} books'
                                                             f'. You need to read more!'})


@app.post("/books/login")
async def login_books(username: str = Form(...), password: str = Form(...)):
    return {
        "username": username,
        "password": password
    }


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {
        "Random-Header": random_header
    }


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)

    if len(BOOKS) < 1:
        create_book_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 0
        new_books = []
        while i < books_to_return:
            new_books.append(BOOKS[i])
            i += 1
        return new_books
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_book_no_api():
    book_1 = Book(id="db373127-4796-4087-a084-cb18c5b81696", title="Title 1",
                  author="Author 1", description="Description 1", rating=4)
    book_2 = Book(id="db373127-4796-4087-a084-cb18c5b81697", title="Title 2",
                  author="Author 2", description="Description 1", rating=6)
    book_3 = Book(id="db373127-4796-4087-a084-cb18c5b81698", title="Title 3",
                  author="Author 3", description="Description 1", rating=7)
    book_4 = Book(id="db373127-4796-4087-a084-cb18c5b81699", title="Title 4.0",
                  author="Author 4", description="Description 1", rating=8)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


@app.get("/books/{book_id}")
async def get_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x

    raise raise_item_cannot_be_found_exception()


@app.get("/books/rating/{book_id}", response_model=BookNoRating)
async def get_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x

    raise raise_item_cannot_be_found_exception()


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        if x.id == book_id:
            BOOKS[counter] = book
            return book
        counter += 1

    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        if x.id == book_id:
            del BOOKS[counter]
            return f'Book {book_id} deleted.'
        counter += 1

    raise raise_item_cannot_be_found_exception()


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found",
                        headers={"X-Header-Error": "Nothing to be seen at the UUID"})
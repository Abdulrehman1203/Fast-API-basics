from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory list to store books
books_db = []


class Book(BaseModel):
    title: str
    author: str
    published_year: int
    price: int


""" Method to delete a book from the list"""


@app.get("/books", response_model=List[Book])
async def get_books():
    return books_db


""" Method to get book details by providing the id """


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    if book_id >= len(books_db) or book_id < 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]


""" Method to add a book in the list"""


@app.post("/books", response_model=Book)
async def add_book(book: Book):
    books_db.append(book)
    return book


""" Method to delete a book from the list"""


@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int):
    if book_id >= len(books_db) or book_id < 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db.pop(book_id)

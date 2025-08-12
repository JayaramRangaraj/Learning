from fastapi import FastAPI

app = FastAPI()

# Simple book dataset: each book has a title, author, and category
BOOKS = [
    {"title": "The Pragmatic Programmer","author": "Andrew Hunt","category": "Programming"},
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Programming"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "History"},
    {"title": "Deep Work", "author": "Cal Newport", "category": "Productivity"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"title": "Intro to Algorithms","author": "Thomas H. Cormen","category": "Computer Science"},
]

# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS


# Get a book by its title (case-insensitive match)
@app.get("/books/{book_title}")
async def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book


# Get books by category using a query parameter
# Example: /books/?category=Programming
@app.get("/books/")
async def get_books_by_category(category: str):
    return [
        book for book in BOOKS if book["category"].casefold() == category.casefold()
    ]


# Get books by author (path) and category (query)
# Example: /books/James Clear/?category=Self-Help
@app.get("/books/{author}/")
async def get_books_by_author_and_category(author: str, category: str):
    return [
        book
        for book in BOOKS
        if book["author"].casefold() == author.casefold()
        and book["category"].casefold() == category.casefold()
    ]

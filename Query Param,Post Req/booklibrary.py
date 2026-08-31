from fastapi import FastAPI,HTTPException,Body,Query,Path
import json

app=FastAPI()

def load_books():
    with open('books.json','r') as f:
        books=json.load(f)
    
    return books

def save_books(books):
    with open('books.json','w') as f:
        json.dump(books,f)


@app.get('/books')
def view_books():
    books=load_books()
    return books

@app.get("/books/sort")
def sorted_books(sorted_by:str=Query(...,description="Sort on the basis of book_id,pages & rating"),order:str=Query('asc',description="Choose order ascending(asc) or descending(des)")):
    books=load_books()
    valid_fields=['pages','book_id','rating']
    if sorted_by not in valid_fields:
        return HTTPException(status_code=404,detail=f"Invalid field,select from {valid_fields}")
    if order not in ['asc','des']:
        return HTTPException(status_code=404,detail=f"Invalid order,select from {valid_fields}")

    sort_order=True if order=='des' else False
    sorted_books=list(books)
    sorted_books.sort(key=lambda x:x[sorted_by],reverse=sort_order)

    return sorted_books

@app.get("/books/{book_id}")
def view_books_by_id(book_id:int=Path(...,description="Give the Book Id",examples="1-...")):
    books=load_books()

    for book in books:
        if book_id==book['book_id']:
            return book
    return HTTPException(status_code=404,detail="Book Id not found.")

@app.post("/create_books")
def create_books(book:dict=Body(...,description="Book information")):
    books=load_books()
    books.append(book)
    save_books(books)

    return "Book saved successfully."


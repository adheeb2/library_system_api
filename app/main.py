from fastapi import FastAPI
from app.database import Base, engine
from app.routers import books
from .routers import users
from fastapi.middleware.cors import CORSMiddleware
# from app.routes import auth_routes, book_routes, borrow_routes

app = FastAPI()
app.router.redirect_slashes=False

app.add_middleware(
    
    CORSMiddleware,
    
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Create tables
Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(books.router)
# app.include_router(book_routes.router, prefix="/books", tags=["Books"])
# app.include_router(borrow_routes.router, prefix="/borrows", tags=["Borrows"])


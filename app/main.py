from fastapi import FastAPI
from app.database import Base, engine
# from app.routes import auth_routes, book_routes, borrow_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# # Include routes
# app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
# app.include_router(book_routes.router, prefix="/books", tags=["Books"])
# app.include_router(borrow_routes.router, prefix="/borrows", tags=["Borrows"])

def run():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

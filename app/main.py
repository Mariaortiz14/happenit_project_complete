from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, events,pqr  # los routers que usás
from app.database import engine, Base
from app.routers import comment


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(events.router)
app.include_router(pqr.router)
app.include_router(comment.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a Happenit!"}

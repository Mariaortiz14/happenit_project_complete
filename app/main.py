from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, events, pqr, comment
from database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://proyecto.up.railway.app",
    "https://proyecto-production-fbe9.up.railway.app"],
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

print("Routers cargados: /users, /events, /pqr, /comment")

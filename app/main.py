from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth_router

ROUTERS = [auth_router.router]

app = FastAPI()

for router in ROUTERS:
    app.include_router(router)

Base.metadata.create_all(bind=engine)



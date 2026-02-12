from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_routers, user_routers, product_routers, seller_router
from app.routers import order_router

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://buyandofront.share.zrok.io",
]

ROUTERS = [
    auth_routers.router, 
    user_routers.router,
    product_routers.router,
    seller_router.router,
    order_router.router,

    #Router Public
    product_routers.router_public   
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in ROUTERS:
    app.include_router(route)

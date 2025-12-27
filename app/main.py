from fastapi import FastAPI
from app.routers import auth_routers, user_routers, product_routers, seller_router

ROUTERS = [
    auth_routers.router, 
    user_routers.router,
    product_routers.router,
    seller_router.router
]

app = FastAPI()

for route in ROUTERS:
    app.include_router(route)
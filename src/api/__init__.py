from fastapi import APIRouter
from api.endpoints.url_shortener import router as url_shortener_router

main_router = APIRouter()

main_router.include_router(url_shortener_router)
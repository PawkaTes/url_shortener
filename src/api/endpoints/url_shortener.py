from fastapi import APIRouter, HTTPException, Request, status

from core.database import engine, Base
from schemas.url_shoretener import UrlCreateSchema, UrlResponseSchema
from api.dependencies.depends import SessionDepends, PaginationDepends
from api.services.url_service import create_short_url, redirect_link

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post("/", response_model=UrlCreateSchema)
async def shorten_url(
    data: UrlCreateSchema,
    session: SessionDepends
):
    try:
        url = await create_short_url(data.original_url, session)
        return url
    except Exception as e:
        logger.error(f"Ошибка при создании короткой ссылки: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/r/{short_code}")
async def redirect_to_origin_link(
    short_code: str,
    request: Request,
    session: SessionDepends
):
    result = await redirect_link(short_code, session, request)
    return result
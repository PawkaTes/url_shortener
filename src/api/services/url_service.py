import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import Request, HTTPException, Response

from models.url_shortener import Urls, Clicks


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


async def create_short_url(original_url: str, session: AsyncSession) -> Urls:
    result = await session.execute(
        select(Urls).where(Urls.original_url == original_url)
    )
    exesting = result.scalar_one_or_none()
    if exesting:
        return exesting
    
    while True:
        short_code = generate_short_code()
        result = await session.execute(
            select(Urls).where(Urls.short_code == short_code)
        )
        if not result.scalar_one_or_none():
            break

    new_url = Urls(
        original_url=original_url,
        short_code=short_code
    )
    session.add(new_url)
    await session.commit()
    await session.refresh(new_url)

    result = await session.execute(
        select(Urls)
        .where(Urls.id == new_url.id)
        .options(selectinload(Urls.clicks))
    )
    loaded_url = result.scalar_one()

    return loaded_url


async def redirect_link(short_code: str, session: AsyncSession, request: Request):
    result = await session.execute(
        select(Urls).where(Urls.short_code == short_code)
    )
    url = result.scalar_one_or_none()

    if not url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    new_click = Clicks(
        url_id=url.id,
        ip_address=client_ip,
        user_agent=user_agent
    )
    session.add(new_click)
    await session.commit()

    return Response(
        status_code=307,
        headers={"Location": url.original_url}
    )

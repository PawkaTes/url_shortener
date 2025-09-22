from typing import Annotated
from fastapi import Depends
from core.database import get_session
from schemas.url_shoretener import PaginationParams
from sqlalchemy.ext.asyncio import AsyncSession

SessionDepends = Annotated[AsyncSession, Depends(get_session)]
PaginationDepends = Annotated[PaginationParams, Depends(PaginationParams)]

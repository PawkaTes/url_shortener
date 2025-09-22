from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class PaginationParams(BaseModel):
    limit: int = Field(10, ge=0, le=100, description="Кол-вол элементов на странице")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")


class UrlCreateSchema(BaseModel):
    original_url: str


class ClickStatsSchema(BaseModel):
    clicked_at: datetime.datetime
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

    class Config:
        from_attributer = True


class UrlResponseSchema(BaseModel):
    id: int
    original_url: str
    created_at: datetime.datetime
    clicks: List[ClickStatsSchema]

    class Config:
        from_attributes = True
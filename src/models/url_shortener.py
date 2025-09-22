from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.postgresql import INET
import datetime

class Urls(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str]
    short_code: Mapped[str]

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now()
    )

    clicks: Mapped[list["Clicks"]] = relationship("Clicks", back_populates="url")


class Clicks(Base):
    __tablename__ = "clicks"

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id", ondelete="CASCADE")
    )
    clicked_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now()
    )
    user_agent: Mapped[str] = mapped_column()
    ip_address: Mapped[str] = mapped_column(INET)

    url: Mapped["Urls"] = relationship("Urls", back_populates="clicks")
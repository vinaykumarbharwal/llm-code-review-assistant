from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, JSON
import datetime

class Base(AsyncAttrs, DeclarativeBase):
	pass

class Review(Base):
	__tablename__ = "reviews"
	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	review_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
	pr_reference: Mapped[str] = mapped_column(String(128), nullable=True)
	created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
	summary: Mapped[str] = mapped_column(String(512))
	stats: Mapped[dict] = mapped_column(JSON)
	comments: Mapped[list] = mapped_column(JSON)

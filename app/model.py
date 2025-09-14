from sqlmodel import Field, SQLModel, DateTime, Relationship
from sqlalchemy import text
from datetime import datetime, UTC


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(
        default=True, sa_column_kwargs={"server_default": text("TRUE")}, nullable=False
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")},
        nullable=False,
    )
    ownerid: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)

    owner: "User" = Relationship()


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")},
        nullable=False,
    )


class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(
        primary_key=True, foreign_key="users.id", ondelete="CASCADE", nullable=False
    )
    post_id: int = Field(
        primary_key=True, foreign_key="posts.id", ondelete="CASCADE", nullable=False
    )

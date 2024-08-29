from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class LivroState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    livro: Mapped[list['Livro']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livro'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    ano: Mapped[str]
    autor: Mapped[str]
    state: Mapped[LivroState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(init=False, back_populates='livro')

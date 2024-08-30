from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from mada.database import get_session
from mada.models import Livro, User
from mada.schemas import (
    LivroList,
    LivroPublic,
    LivroSchema,
    LivroUpdate,
    Message,
)
from mada.security import get_current_user

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/livro', tags=['livro'])


@router.post('/', response_model=LivroPublic)
def create_livro(
    livro: LivroSchema,
    user: CurrentUser,
    session: Session,
):
    db_livro: Livro = Livro(
        title=livro.title,
        description=livro.description,
        ano=livro.ano,
        autor=livro.autor,
        state=livro.state,
        user_id=user.id,
    )
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.get('/', response_model=LivroList)
def list_livros(  # noqa
    session: Session,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Livro).where(Livro.user_id == user.id)

    if title:
        query = query.filter(Livro.title.contains(title))

    if description:
        query = query.filter(Livro.description.contains(description))

    if state:
        query = query.filter(Livro.state == state)

    livros = session.scalars(query.offset(offset).limit(limit)).all()

    return {'livros': livros}


@router.patch('/{livro_id}', response_model=LivroPublic)
def patch_livro(
    livro_id: int, session: Session, user: CurrentUser, livro: LivroUpdate
):
    db_livro = session.scalar(
        select(Livro).where(Livro.user_id == user.id, Livro.id == livro_id)
    )

    if not db_livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)

    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    return db_livro


@router.delete('/{livro_id}', response_model=Message)
def delete_livro(livro_id: int, session: Session, user: CurrentUser):
    livro = session.scalar(
        select(Livro).where(Livro.user_id == user.id, Livro.id == livro_id)
    )

    if not livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(livro)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}

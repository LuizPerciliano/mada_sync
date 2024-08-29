from http import HTTPStatus

from fastapi import FastAPI

from mada.routers import autor, livro, users
from mada.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(autor.router)
app.include_router(livro.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}

from pathlib import Path
import environ
from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import create_engine

import infra.repository.model as model

router = APIRouter(tags=['DB'])

@router.post(
        '/',
        status_code=status.HTTP_201_CREATED,
        description='Эндпоинт создаёт новую комнату, если комната с таким именем уже существует, то возвращается 400 ошибка',
)
async def create_database():
    '''Создать новую музыкальную комнату'''

    BASE_DIR = Path(__file__).resolve().parent.parent
    # print(BASE_DIR)
    env = environ.Env()
    environ.Env.read_env(BASE_DIR / '.env')
    DATABASE_URL = f"postgresql://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"
    engine = create_engine(DATABASE_URL, echo=True)
    model.Base.metadata.create_all(engine)
    
    return True
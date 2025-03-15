from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASE_URL = None

def _init_db(is_test=False):
    global DATABASE_URL
    if is_test:
        DATABASE_URL = f"postgresql://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_TEST_DB')}"
    else:
        DATABASE_URL = f"postgresql://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"

# DATABASE_URL = f"postgresql://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}/{env('POSTGRES_TEST_DB')}"
# engine.connect()


def get_engine() -> Engine:
    if DATABASE_URL is None:
        raise ValueError("Database is not configuration")
    return create_engine(DATABASE_URL, echo=True)
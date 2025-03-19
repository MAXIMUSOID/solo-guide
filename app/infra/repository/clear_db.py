from sqlalchemy.orm import Session

from infra.repository.model import City, Favorite, ShowPlace, User, Visit
from infra.repository.connect import get_engine


def clear_all():
    engine = get_engine()

    with Session(bind=engine) as session:
        session.query(Visit).delete()
        session.query(Favorite).delete()
        session.query(ShowPlace).delete()
        session.query(City).delete()
        session.query(User).delete()
        session.commit()
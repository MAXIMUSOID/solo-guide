from sqlalchemy.orm import Session

from infra.repository.exceptions.user import IncorrectUserPassword, UserAlreadyExistException, UserNotFoundException, UserCreateException
from infra.repository.converter import convert_city_to_model, convert_show_place_to_model, convert_user_to_model, convert_visit_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CitiesNotFoundException, CityAlreadyExistException, CityNotFoundException, ShowPlaceAddingException, ShowPlaceAlreadyExistException, ShowPlaceNotFoundException, ShowPlacesCityNotFoundException, VisitAlreadyExistException, VisitCreateException
import domain.entities.model as model
from infra.repository.connect import get_engine
from infra.repository.model import City, ShowPlace, User, Visit


def add_city(city:model.City) -> City:
    '''Adding city to database'''
    engine = get_engine()

    if check_city(city):
        raise CityAlreadyExistException(city.name)
    
    with Session(engine) as session:
        city_db:City = City(name=city.name, country=city.country)
        session.add(city_db)
        session.commit()

        city_db = session.query(City).filter(City.name == city.name).first()
    return convert_city_to_model(city_db)

def check_city(city:City) -> bool:
    with Session(get_engine()) as session:
        return bool(session.query(City).filter(City.name == city.name).first())

def get_city(name:str) -> City | None:
    '''Get city by citi name'''
    engine = get_engine()
    with Session(engine) as session:
        city:City = session.query(City).filter(City.name == name).first()
    
    if not city:
        return None
    
    return city

def get_cities() -> list[model.City]:
    engine = get_engine()

    with Session(engine) as session:
        query = session.query(City).all()

    if len(query) == 0:
        raise CitiesNotFoundException()
    
    return list(map(convert_city_to_model, query))


def add_show_place(show_place:model.ShowPlace)->model.ShowPlace:
    '''Add show place'''
    city_db = get_city(show_place.city.name)
    if not city_db:
        raise CityNotFoundException(city_name=show_place.city.name)
    
    try:
        get_show_place(name=show_place.name, city_name=show_place.city.name)
    except ShowPlaceNotFoundException:
        pass
    else:
        raise ShowPlaceAlreadyExistException(show_place_name=show_place.name, city_name=show_place.city.name)
    
    engine = get_engine()
    with Session(engine) as session:
        
        sp = ShowPlace(
            name=show_place.name,
            place_type=show_place.place_type,
            description=show_place.description, 
            latitude=show_place.latitude, 
            longitude=show_place.longitude,
            city_id=city_db.id,
            addres=show_place.addres
            )
        session.add(sp)
        session.commit()
        
    sp = get_show_place(name=show_place.name, city_name=show_place.city.name)
    if not sp:
        raise ShowPlaceAddingException(show_place.name)
    
    return sp


def _get_show_place(name:str, city_name:str) -> ShowPlace:
    engine = get_engine()
    if get_city(city_name) is None:
        raise CityNotFoundException(city_name)
    
    with Session(engine) as session:
        query = session.query(ShowPlace, City).join(City, ShowPlace.city_id == City.id).filter(ShowPlace.name == name, City.name == city_name).first()
    
    return query[0]


def get_show_place(name:str, city_name:str) -> model.ShowPlace:
    engine = get_engine()
    if get_city(city_name) is None:
        raise CityNotFoundException(city_name)
    
    with Session(engine) as session:
        query = session.query(ShowPlace, City).join(City, ShowPlace.city_id == City.id).filter(ShowPlace.name == name, City.name == city_name).first()
    
    if query is None:
        raise ShowPlaceNotFoundException(show_place_name=name, city_name=city_name)

    return convert_show_place_to_model(query[0], query[1])


def get_show_places_by_city(city_name:str) -> list[model.ShowPlace]:
    engine = get_engine()
    if get_city(city_name) is None:
        raise CityNotFoundException(city_name)
    
    with Session(engine) as session:
        query = session.query(ShowPlace, City).join(City, ShowPlace.city_id == City.id).filter(City.name == city_name).all()
    
    if not query:
        raise ShowPlacesCityNotFoundException(city_name)
    
    result = [convert_show_place_to_model(show_place, city) for show_place, city in query]

    return result
    
    

def check_user(login:str) -> bool:
    engine = get_engine()

    with Session(engine) as session:
        return bool(session.query(User).filter(User.login == login).first())
    

def check_user_password(user:User, password:str) -> bool:
    if not check_user(user.login):
        raise UserNotFoundException(user.login)

    engine = get_engine()
    with Session(engine) as session:
        result = session.query(User).filter(User.login == user.login,
                                            User.nickname == user.nickname, 
                                            User.password == model.User.get_password_hash(password)).first()
        return bool(result)

def _change_user_password(user:User, new_password:str):
    if not check_user(user.login):
        raise UserNotFoundException(user.login)
    
    engine = get_engine()
    with Session(engine) as session:
        update_user = session.query(User).filter(User.login == user.login).first()
        update_user.password = model.User.get_password_hash(new_password)

        session.commit()


def change_user_password(user_login:str, new_password:str) -> model.User:
    user:User = get_user(user_login)

    _change_user_password(user=user, new_password=new_password)
    return convert_user_to_model(user)

def get_user(login:str) -> User:
    engine = get_engine()

    with Session(engine) as session:
        user:User = session.query(User).filter(User.login == login).first()
    if not user:
        raise UserNotFoundException(login)

    return user

def get_user_to_model(login:str):
    return convert_user_to_model(get_user(login=login))


def add_user(user:model.User, password:str) -> model.User:
    if check_user(user.login):
        raise UserAlreadyExistException(user.login)
    
    engine = get_engine()
    with Session(engine) as session:
        new_user:User = User(
            nickname=user.nickname,
            login=user.login,
            password=model.User.get_password_hash(password)
        )
        session.add(new_user)
        session.commit()

        user_db:User = session.query(User).filter(User.login == user.login).first()
        
        if not user_db:
            raise UserCreateException(user.login)

        return convert_user_to_model(user_db)
    
def get_visit(visit:model.Visit) -> Visit:
    with Session(get_engine()) as session:
        query = session.query(Visit, User, ShowPlace, City).join(
            User, Visit.user_id == User.id).join(
            ShowPlace, Visit.show_place_id == ShowPlace.id).join(
                City, ShowPlace.city_id == City.id).filter(
                Visit.user_id == visit.user.oid, Visit.show_place_id == visit.show_place.oid).first()
    return query


def check_unique_visit(visit:model.Visit) -> bool:
    query = get_visit(visit=visit)    
    return bool(query)

def add_visit(user_login:str, show_place_name:str, show_place_city:str, grade:int, review:str):
    user_model:model.User = get_user_to_model(user_login)
    show_place_model:model.ShowPlace = get_show_place(show_place_name, show_place_city)
    visit:model.Visit = model.Visit(
        user=user_model,
        show_place=show_place_model,
        grade=grade,
        review=review)
    if check_unique_visit(visit=visit):
        raise VisitAlreadyExistException(visit.show_place.name, visit.user.login)
    
    engine = get_engine()
    with Session(engine) as session:
        new_visit = Visit(
            user_id = visit.user.oid,
            show_place_id = visit.show_place.oid,
            grade = visit.grade,
            review = visit.review,
            datetime=visit.create_at
        )
        session.add(new_visit)
        session.commit()        
        
    query = get_visit(visit)
    test_visit:model.Visit = convert_visit_to_model(*query)
    if test_visit is None:
        raise VisitCreateException(visit.show_place.name, visit.user.login)
    
    return test_visit

def get_user_history(user_login:str) -> list[model.Visit]:
    user = get_user(user_login)
    
    with Session(get_engine()) as session:
        query = session.query(Visit, User, ShowPlace, City).join(
            User, Visit.user_id == User.id).join(
            ShowPlace, Visit.show_place_id == ShowPlace.id).join(
                City, ShowPlace.city_id == City.id).filter(Visit.user_id == user.id).all()
    
    result = [convert_visit_to_model(*visit) for visit in query]
    return result


def login_user(user_login:str, password:str) -> model.User:
    user:User = get_user(login=user_login)
    if not check_user_password(user, password):
        raise IncorrectUserPassword()
    
    return convert_user_to_model(user)
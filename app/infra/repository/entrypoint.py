from sqlalchemy.orm import Session

from infra.repository.exceptions.user import UserAlreadyExistException, UserNotFoundException, UserCreateException
from infra.repository.converter import convert_city_to_model, convert_show_place_to_model, convert_user_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAddingException, ShowPlaceAlreadyExistException, ShowPlaceNotFoundException
import domain.entities.model as model
from infra.repository.connect import get_engine
from infra.repository.model import City, ShowPlace, User


def add_city(city:model.City) -> City:
    '''Adding city to database'''
    engine = get_engine()

    _city = get_city(city.name)
    if _city:
        raise CityAlreadyExistException(city.name)
    
    with Session(engine) as session:
        city_db:City = City(name=city.name, country=city.country)
        session.add(city_db)
        session.commit()

        city_db = session.query(City).filter(City.name == city.name).first()
    return convert_city_to_model(city_db)


def get_city(name:str) -> City | None:
    '''Get city by citi name'''
    engine = get_engine()
    with Session(engine) as session:
        city:City = session.query(City).filter(City.name == name).first()
    
    if not city:
        return None
    
    return city


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


def get_show_place(name:str, city_name:str) -> model.ShowPlace:
    engine = get_engine()
    if get_city(city_name) is None:
        raise CityNotFoundException(city_name)
    
    with Session(engine) as session:
        query = session.query(ShowPlace, City).join(City, ShowPlace.city_id == City.id).filter(ShowPlace.name == name, City.name == city_name).first()
    
    if query is None:
        raise ShowPlaceNotFoundException(show_place_name=name, city_name=city_name)

    return convert_show_place_to_model(query[0], convert_city_to_model(query[1]))


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

def get_user(login:str) -> User:
    engine = get_engine()

    with Session(engine) as session:
        user = session.query(User).filter(User.login == login).first()

    if not user:
        raise UserNotFoundException(user.login)


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
        
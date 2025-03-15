from sqlalchemy.orm import Session

from infra.repository.converter import convert_city_to_model, convert_show_place_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAddingException, ShowPlaceAlreadyExistException, ShowPlaceNotFoundException
import domain.entities.model as model
from infra.repository.connect import get_engine
from infra.repository.model import City, ShowPlace


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


def get_city_by_id(id:int) -> model.City | None:
    '''Get city by city id'''
    engine = get_engine()
    with Session(engine) as session:
        city = session.query(City).filter(City.id == id).first()
    
    if not city:
        return None
    
    return convert_city_to_model(city)


def add_show_place(show_place:model.ShowPlace)->model.ShowPlace:
    '''Add show place'''
    city_db = get_city(show_place.city.name)
    if not city_db:
        raise CityNotFoundException(city_name=show_place.city.name)
    
    # raise ValueError(ShowPlace(show_place.place_type))
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
    
    showplace:ShowPlace = query[0]
    city:City = convert_city_to_model(query[1])

    return convert_show_place_to_model(showplace, city)

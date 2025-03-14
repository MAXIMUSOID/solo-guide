from sqlalchemy.orm import Session

from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAddingException
import domain.entities.model as model
from infra.repository.connect import get_engine
from infra.repository.model import City, ShowPlace


def add_city(name:str, country:str) -> model.City:
    '''Adding city to database'''
    engine = get_engine()

    city = get_city(name)
    if city:
        raise CityAlreadyExistException(name)
    
    
    with Session(engine) as session:
        city = City(name=name, country=country)
        session.add(city)
        session.commit()

        city_db = session.query(City).filter(City.name == name).first()
    return model.City(oid=city_db.id, name=city_db.name, country=city_db.country)


def get_city(name:str) -> model.City | None:
    '''Get city by citi name'''
    engine = get_engine()
    with Session(engine) as session:
        city = session.query(City).filter(City.name == name).first()
    
    return city

def get_city_by_id(id:int) -> model.City | None:
    '''Get city by city id'''
    engine = get_engine()
    with Session(engine) as session:
        city = session.query(City).filter(City.id == id).first()
    
    return city

def add_show_place(name:str, place_type:PlaceType, description:str, latitude:float, longitude:float, city_name:str, addres:str):
    city:City = get_city(city_name)
    if not city:
        raise CityNotFoundException(name)
    
    engine = get_engine()
    with Session(engine) as session:
        show_place = ShowPlace(
            name=name,
            place_type=place_type,
            description=description, 
            latitude=latitude, 
            longitude=longitude,
            city_id=city.id,
            addres=addres
            )
        session.add(show_place)
        session.commit()
    sp = get_show_place(name=name)
    if not sp:
        raise ShowPlaceAddingException(name)
    
    return sp

def get_show_place(name:str) -> model.ShowPlace:
    engine = get_engine()
    with Session(engine) as session:
        sp = session.query(ShowPlace).filter(ShowPlace.name == name).first()
    
    city:City = get_city_by_id(id=sp.city_id)
    if sp is None:
        return None
    
    return model.ShowPlace(
        oid=sp.id, 
        name=sp.name,
        _place_type=sp.place_type, 
        description=sp.description, 
        latitude=sp.latitude, 
        longitude=sp.longitude,
        city=model.City(oid=city.id, name=city.name, country=city.country),
        addres=sp.addres
        )
    
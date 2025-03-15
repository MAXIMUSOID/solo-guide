from sqlalchemy.orm import Session

from infra.repository.converter import convert_city_to_model, convert_show_place_to_model
from domain.entities.place_types import PlaceType
from infra.repository.exceptions.route_to_db import CityAlreadyExistException, CityNotFoundException, ShowPlaceAddingException, ShowPlaceAlreadyExistException, ShowPlaceNotFoundException
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
        city:City = session.query(City).filter(City.name == name).first()
    
    if not city:
        return None
    
    return convert_city_to_model(city)


def get_city_by_id(id:int) -> model.City | None:
    '''Get city by city id'''
    engine = get_engine()
    with Session(engine) as session:
        city = session.query(City).filter(City.id == id).first()
    
    if not city:
        return None
    
    return convert_city_to_model(city)


def add_show_place(name:str, place_type:PlaceType, description:str, latitude:float, longitude:float, city_name:str, addres:str):
    '''Add show place'''
    city:model.City = get_city(city_name)
    if not city:
        raise CityNotFoundException(city_name=city_name)
    
    try:
        get_show_place(name=name, city_name=city_name)
    except ShowPlaceNotFoundException:
        pass
    else:
        raise ShowPlaceAlreadyExistException(show_place_name=name, city_name=city_name)

    engine = get_engine()
    with Session(engine) as session:
        show_place = ShowPlace(
            name=name,
            place_type=place_type,
            description=description, 
            latitude=latitude, 
            longitude=longitude,
            city_id=city.oid,
            addres=addres
            )
        session.add(show_place)
        session.commit()
    sp = get_show_place(name=name, city_name=city.name)
    if not sp:
        raise ShowPlaceAddingException(name)
    
    return sp


def get_show_place(name:str, city_name:str) -> model.ShowPlace:
    engine = get_engine()
    
    city:model.City = get_city(city_name)
    if city is None:
        raise CityNotFoundException(city_name)
    
    with Session(engine) as session:
        query = session.query(ShowPlace, City).join(City, ShowPlace.city_id == City.id).filter(ShowPlace.name == name, City.name == city_name).first()
    
    if query is None:
        raise ShowPlaceNotFoundException(show_place_name=name, city_name=city_name)
    

    showplace:ShowPlace = query[0]
    city:City = convert_city_to_model(query[1])

    return convert_show_place_to_model(showplace, city)

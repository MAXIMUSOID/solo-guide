from abc import ABC
from dataclasses import dataclass
from datetime import date

from domain.entities.place_types import PlaceType

@dataclass
class Base(ABC):
    oid:int

@dataclass
class User(Base):
    nickname:str
    login:str

@dataclass
class City(Base):
    name:str
    country:str

@dataclass
class ShowPlace(Base):
    _place_type:PlaceType
    name:str
    description:str
    latitude:float
    longitude:float
    city:City
    addres:str

    @property
    def place_type(self):
        return PlaceType(self._place_type).value

@dataclass
class Visit(Base):
    user_id:int
    show_place_id:int
    grade:int
    review:int
    datetime:date

@dataclass
class Favorite(Base):
    user_id:int
    show_place_id:int
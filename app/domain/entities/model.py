from abc import ABC
from dataclasses import dataclass
from datetime import date

from domain.entities.base import BaseValueObject
from domain.entities.place_types import PlaceType

@dataclass
class Base(ABC):
    oid:int

@dataclass
class User(BaseValueObject):
    nickname:str
    login:str

    def validate(self):
        ...

    def is_generic_type(self):
        return self.nickname

@dataclass
class City(BaseValueObject):
    name:str
    country:str

    def validate(self):
        ...
        
    def is_generic_type(self):
        return f"{self.name}, {self.country}"

@dataclass
class ShowPlace(BaseValueObject):
    name:str
    _place_type:str
    description:str
    latitude:float
    longitude:float
    city:City
    addres:str

    @property
    def place_type(self) -> PlaceType:
        return PlaceType(self._place_type)
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        ...
        
    def is_generic_type(self):
        return self.name

@dataclass
class Visit(BaseValueObject):
    user_id:int
    show_place_id:int
    grade:int
    review:int
    datetime:date

    def validate(self):
        ...
        
    def is_generic_type(self):
        return f"{self.user_id}"

@dataclass
class Favorite(BaseValueObject):
    user_id:int
    show_place_id:int

    def validate(self):
        ...
        
    def is_generic_type(self):
        return f"{self.user_id}"
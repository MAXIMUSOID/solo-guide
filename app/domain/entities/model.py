from abc import ABC
from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256

from domain.exceptions.model import (CityCountryToLongException, 
                                     CityEmptyCountryException, 
                                     CityEmptyNameException, 
                                     CityNameToLongException, 
                                     PlaceTypeNotFoundException, 
                                     ShowPlaceEmptyNameException, 
                                     ShowPlaceNameToLongException, 
                                     UserLoginEmptyException, 
                                     UserLoginToLongException, 
                                     UserNicknameEmptyException, 
                                     UserNicknameToLongException,
                                     )
from domain.entities.base import BaseValueObject
from domain.entities.place_types import PlaceType

@dataclass
class Base(ABC):
    oid:int

@dataclass
class User(BaseValueObject):
    nickname:str
    login:str
    password:str = field(default=None)

    def validate(self):
        if self.nickname == "":
            raise UserNicknameEmptyException()
        
        if len(self.nickname) > 255:
            raise UserNicknameToLongException(self.nickname)
        
        if self.login == "":
            raise UserLoginEmptyException()
        
        if len(self.login) > 255:
            raise UserLoginToLongException(self.login)


    def check_password(self, password) -> bool:
        return self.password == User.get_password_hash(password)
    
    def is_generic_type(self) -> str:
        return self.nickname
    
    @classmethod
    def get_password_hash(cls, password:str) -> str:
        return sha256(password.encode()).hexdigest()

@dataclass
class City(BaseValueObject):
    name:str
    country:str

    def validate(self):
        if self.name == "":
            raise CityEmptyNameException()
        
        if len(self.name) > 255:
            raise CityNameToLongException(self.name)
        
        if self.country == "":
            raise CityEmptyCountryException()
        
        if len(self.country) > 255:
            raise CityCountryToLongException(self.name)
        
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
        try:
            self.place_type
        except:
            raise PlaceTypeNotFoundException(self._place_type)
        
        if self.name == "":
            raise ShowPlaceEmptyNameException()
        
        if len(self.name) > 255:
            raise ShowPlaceNameToLongException(self.name)
        
        
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
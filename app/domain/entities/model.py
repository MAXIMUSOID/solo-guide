from abc import ABC
from dataclasses import dataclass, field
from datetime import date, datetime
from hashlib import sha256

from domain.exceptions.model import (CityCountryToLongException, 
                                     CityEmptyCountryException, 
                                     CityEmptyNameException, 
                                     CityNameToLongException, 
                                     FavoriteEmptyShowPlaceException, 
                                     FavoriteEmptyUserException, 
                                     PlaceTypeNotFoundException, 
                                     ShowPlaceEmptyNameException, 
                                     ShowPlaceNameToLongException, 
                                     UserLoginEmptyException, 
                                     UserLoginToLongException, 
                                     UserNicknameEmptyException, 
                                     UserNicknameToLongException, 
                                     VisitEmptyShowPlaceException, 
                                     VisitEmptyUserException, 
                                     VisitGradeIncorrectException, 
                                     VisitReviewToLongException,
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
    oid:int = field(default=None)

    def validate(self):
        if self.nickname == "":
            raise UserNicknameEmptyException()
        
        if len(self.nickname) > 255:
            raise UserNicknameToLongException(self.nickname)
        
        if self.login == "":
            raise UserLoginEmptyException()
        
        if len(self.login) > 255:
            raise UserLoginToLongException(self.login)

    
    def is_generic_type(self) -> str:
        return self.login
    
    @classmethod
    def get_password_hash(cls, password:str) -> str:
        return sha256(password.encode()).hexdigest()

@dataclass
class City(BaseValueObject):
    name:str
    country:str
    oid:int = field(default=None)
    
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
    oid:int = field(default=None)

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
        return f"{self.name}, {self.city.name}"

@dataclass
class Visit(BaseValueObject):
    user:User
    show_place:ShowPlace
    grade:int
    review:str
    create_at:datetime = field(default_factory=datetime.now)

    def validate(self):
        if self.user is None:
            raise VisitEmptyUserException()
        if self.show_place is None:
            raise VisitEmptyShowPlaceException()
        if not -1 < self.grade < 6:
            raise VisitGradeIncorrectException(self.grade)
        if len(self.review) > 255:
            raise VisitReviewToLongException(self.review)
        
    def is_generic_type(self):
        return f"{self.user.login}"

@dataclass 
class Visits(BaseValueObject):
    visits_list:list[Visit] = field(default_factory=list)

@dataclass
class Favorite(BaseValueObject):
    user:User
    show_place:ShowPlace

    def validate(self):
        if self.user is None:
            raise FavoriteEmptyUserException()
        if self.show_place is None:
            raise FavoriteEmptyShowPlaceException()
        
    def is_generic_type(self):
        return f"{self.user.login}"
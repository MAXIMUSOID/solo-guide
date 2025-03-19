from dataclasses import dataclass

from domain.entities.place_types import PlaceType
from domain.exceptions.base import BaseEntityException


@dataclass
class CityEmptyNameException(BaseEntityException):
    @property
    def message(self):
        return f"Отсутствует название у города"
    

@dataclass    
class CityNameToLongException(BaseEntityException):
    name:str

    @property
    def message(self):
        return f"Слишком длинное название города {self.name[:255]}"
    
    
@dataclass
class CityEmptyCountryException(BaseEntityException):
    @property
    def message(self):
        return f"Отсутствует название у страны"
    

@dataclass    
class CityCountryToLongException(BaseEntityException):
    name:str

    @property
    def message(self):
        return f"Слишком длинное название страны {self.name[:255]}"
    

@dataclass
class PlaceTypeNotFoundException(BaseEntityException):
    place_type:str

    @property
    def message(self):
        return f"Некорректный тип достопримечательности {self.place_type} используйте один из этих типов {[i.value for i in PlaceType]}"


@dataclass
class ShowPlaceEmptyNameException(BaseEntityException):
    @property
    def message(self):
        return f"Отсутствует название достопримечательности"
    

@dataclass    
class ShowPlaceNameToLongException(BaseEntityException):
    name:str

    @property
    def message(self):
        return f"Слишком длинное название достопримечательности {self.name[:255]}"
    

@dataclass
class UserNicknameEmptyException(BaseEntityException):
    @property
    def message(self):
        return f"Отсутствует имя пользователя"
    

@dataclass
class UserNicknameToLongException(BaseEntityException):
    nickname:str

    @property
    def message(self):
        return f"Слишком длинное имя пользователя {self.nickname[:255]}"
    

@dataclass
class UserLoginEmptyException(BaseEntityException):
    @property
    def message(self):
        return f"Отсутствует логин"
    

@dataclass
class UserLoginToLongException(BaseEntityException):
    login:str

    @property
    def message(self):
        return f"Слишком длинный логин {self.login[:255]}"
    

@dataclass
class VisitEmptyUserException(BaseEntityException):
    @property
    def message(self):
        return f"Для регистрации визита следует указать пользователя"
    

@dataclass
class VisitEmptyShowPlaceException(BaseEntityException):
    @property
    def message(self):
        return f"Для регистрации визита следует указать достопримечательность"


@dataclass
class VisitGradeIncorrectException(BaseEntityException):
    grade:int
    
    @property
    def message(self):
        return f"Оценка {self.grade} выходит за рамки 0-5"
    

@dataclass
class VisitReviewToLongException(BaseEntityException):
    review:str
    
    @property
    def message(self):
        return f"Слишком длинный обзор {self.review}"
    
    
@dataclass
class FavoriteEmptyUserException(BaseEntityException):
    @property
    def message(self):
        return f"Для добавления в избранное следует указать пользователя"
    

@dataclass
class FavoriteEmptyShowPlaceException(BaseEntityException):
    @property
    def message(self):
        return f"Для добавления в избранное следует указать достопримечательность"

    
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
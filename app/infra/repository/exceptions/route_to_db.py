from dataclasses import dataclass
from infra.repository.exceptions.base import RepositoryException

@dataclass
class CityAlreadyExistException(RepositoryException):
    city_name:str

    @property
    def message(self):
        return f'Город с именем {self.city_name} уже существует'
    

@dataclass
class CityNotFoundException(RepositoryException):
    city_name:str

    @property
    def message(self):
        return f'Город с именем {self.city_name} не найден'
    

@dataclass
class ShowPlaceAddingException(RepositoryException):
    show_place_name:str

    @property
    def message(self):
        return f'При добавлении достопримечательности {self.show_place_name} произошла ошибка'
    
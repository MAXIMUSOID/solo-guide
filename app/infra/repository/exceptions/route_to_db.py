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
class CitiesNotFoundException(RepositoryException):
    @property
    def message(self):
        return f'Нет ни одного города'


@dataclass
class ShowPlaceAddingException(RepositoryException):
    show_place_name:str

    @property
    def message(self):
        return f'При добавлении достопримечательности {self.show_place_name} произошла ошибка'

@dataclass
class ShowPlaceNotFoundException(RepositoryException):
    show_place_name:str
    city_name:str

    @property
    def message(self):
        return f'Достопримечательность {self.show_place_name} не найдена в городе {self.city_name}'
    
@dataclass
class ShowPlacesCityNotFoundException(RepositoryException):
    city_name:str

    @property
    def message(self):
        return f'Достопримечательности не найдены в городе {self.city_name}'
    
    
@dataclass
class ShowPlaceAlreadyExistException(RepositoryException):
    show_place_name:str
    city_name:str

    @property
    def message(self):
        return f'Достопримечательность {self.show_place_name} уже есть в городе {self.city_name}'
    

@dataclass
class VisitAlreadyExistException(RepositoryException):
    show_place_name:str
    user_login:str

    @property
    def message(self):
        return f'Пользователь {self.user_login} уже посещал достопримечательность {self.show_place_name}'
    

@dataclass
class VisitCreateException(RepositoryException):
    show_place_name:str
    user_login:str

    @property
    def message(self):
        return f'Для пользователя {self.user_login} не удалось зарегестрировать посещение достопримечательности {self.show_place_name}'
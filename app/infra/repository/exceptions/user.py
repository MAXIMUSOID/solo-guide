from dataclasses import dataclass

from infra.repository.exceptions.base import RepositoryException


@dataclass
class UserNotFoundException(RepositoryException):
    login:str

    @property
    def message(self):
        return f'Пользователь с таким логином {self.login} не найден'
    
@dataclass
class IncorrectUserPassword(RepositoryException):

    @property
    def message(self):
        return f'Неверный пароль пользователя'

@dataclass
class UserAlreadyExistException(RepositoryException):
    login:str

    @property
    def message(self):
        return f'Пользователь с таким логином {self.login} уже существует'
    

@dataclass
class UserCreateException(RepositoryException):
    login:str

    @property
    def message(self):
        return f'Не удалось создать пользователя {self.login}'
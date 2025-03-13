from dataclasses import dataclass

@dataclass
class RepositoryException(Exception):
    @property
    def message(self):
        return "Произошла ошибка хранилища"
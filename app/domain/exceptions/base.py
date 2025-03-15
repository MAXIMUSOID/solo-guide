from dataclasses import dataclass

@dataclass
class BaseEntityException(Exception):
    
    @property
    def message(self):
        ...
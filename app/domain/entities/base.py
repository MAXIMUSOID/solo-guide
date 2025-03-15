from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar

VT = TypeVar("VT", bound=Any)

@dataclass()
class BaseValueObject(ABC):
    
    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def is_generic_type(self) -> VT:
        ...
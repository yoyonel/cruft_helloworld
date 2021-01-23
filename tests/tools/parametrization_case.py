"""
https://www.python.org/dev/peps/pep-0557/#inheritance
"""
from abc import ABC
from dataclasses import InitVar, asdict, dataclass, field
from typing import Optional

from parametrization import Parametrization


@dataclass
class IParametrizationCase(ABC):
    # https://stackoverflow.com/a/55796971
    name: Optional[str] = field(init=False)  # pytest case name
    name_init: InitVar[Optional[str]]

    def __post_init__(self, name_init: Optional[str]):
        if self.__class__ == IParametrizationCase:
            raise TypeError("Cannot instantiate abstract class.")
        self.name = name_init
        if self.name == "":
            self.name = None

    def __iter__(self):
        return iter(asdict(self).items())

    @classmethod
    def create(cls, name_init=None, **kwargs):
        return cls(name_init=name_init, **kwargs)

    @classmethod
    def case(cls, parametrization_case):
        if not isinstance(parametrization_case, IParametrizationCase):
            raise TypeError(
                f"{parametrization_case} not an instance of abstract class: {IParametrizationCase}"
            )
        return Parametrization.case(**dict(parametrization_case))

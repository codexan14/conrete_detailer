from dataclasses import dataclass, field
from typing import Literal 
from abc import ABC, abstractmethod

@dataclass
class Support(ABC): 
    restrained_dofs: tuple[bool, bool, bool, bool, bool, bool]

@dataclass
class FixedSupport(Support):
    restrained_dofs: tuple[bool, bool, bool, bool, bool, bool] = (True, True, True, True, True, True)

@dataclass

@dataclass
class Force: 
    force_type: Literal['punctual']


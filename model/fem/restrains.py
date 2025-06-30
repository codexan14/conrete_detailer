from dataclasses import dataclass, field
from typing import Literal 
from abc import ABC, abstractmethod
from core.fem.elements import Node

@dataclass
class Support(ABC): 
    node: Node
    restrained_dofs: tuple[bool, bool, bool, bool, bool, bool]

@dataclass
class FixedSupport(Support):
    restrained_dofs: tuple[bool, bool, bool, bool, bool, bool] = (True, True, True, True, True, True)

@dataclass
class PinnedSupport(Support): 
    restrained_dofs: tuple[bool, bool, bool, bool, bool, bool] = (True, True, True, False, False, False)



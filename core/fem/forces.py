from dataclasses import dataclass
from core.fem.elements import Node, B2D2
from abc import ABC, abstractmethod
from typing import Literal
from numpy.typing import NDArray
import numpy as np 

@dataclass
class Load(ABC):
    load_case: str

    @property
    @abstractmethod 
    def equivalent_FEM_force(self) -> dict[Node, list[NDArray[np.float64]]]:
        # for each element provided (first list), it returns a list (second list) of 
        # vecotr forces [NDArray] for each node of the element
        # list of elements
        #   element 1
        #       node 1
        #           force_vector
        #       node 2 
        #       node 3
        #   element 2
        #   element 3
        pass 

@dataclass
class PunctualForceOnBeams(Load): 
    magnitud: float 
    axis: tuple[Literal[1,2,3], Literal['global', 'local']]
    position: float
    elements: list[B2D2]

    @property
    def equivalent_FEM_force(self) -> dict[Node, list[NDArray[np.float64]]]:
        dict_of_forces: dict[Node, list[NDArray[np.float64]]] = {}
        P = self.magnitud 
        ar = self.position
        br = (1-self.position)

        if self.axis == (1, 'global'): 
            F1 = np.array([
                        P/2,0,0,0,0,0,P/2,0,0,0,0,0]
                        , dtype=np.float64)
            
            F2 = np.array([
                        P/2,0,0,0,0,0,P/2,0,0,0,0,0]
                        , dtype=np.float64)
            
            for element in self.elements:
                if element.nodes[0] in dict_of_forces.keys(): 
                    dict_of_forces[element.nodes[0]] += F1
                else: 
                    dict_of_forces[element.nodes[0]] = F1
                
                if element.nodes[1] in dict_of_forces.keys(): 
                    dict_of_forces[element.nodes[1]] += F2
                else: 
                    dict_of_forces[element.nodes[1]] = F2
        
        if self.axis == (2, 'global'): 
            F1 = np.array([
                        0,P/2,0,0,0,0,0,P/2,0,0,0,0]
                        , dtype=np.float64)
            
            F2 = np.array([
                        P/2,0,0,0,0,0,P/2,0,0,0,0,0]
                        , dtype=np.float64)
            
            for element in self.elements:
                if element.nodes[0] in dict_of_forces.keys(): 
                    dict_of_forces[element.nodes[0]] += F1
                else: 
                    dict_of_forces[element.nodes[0]] = F1
                
                if element.nodes[1] in dict_of_forces.keys(): 
                    dict_of_forces[element.nodes[1]] += F2
                else: 
                    dict_of_forces[element.nodes[1]] = F2

        return dict_of_forces
from dataclasses import dataclass, field

import scipy.linalg 
from core.fem.elements import FEMElement
from core.fem.restrains import Support
from core.fem.forces import Load
from core.fem.elements import Node
from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np
import scipy
import pandas as pd 

@dataclass

class Model(ABC):
    active_dofs: tuple[bool, bool, bool, bool, bool, bool]
    elements: list[FEMElement]
    restrains: list[Support]
    loads: list[Load]
    nodes: list[Node] = field(init=False)

    @property
    @abstractmethod
    def global_stiffness_matrix(self) -> NDArray[np.float64]: 
        pass 

@dataclass
class LinearElastic(Model): 
    
    def __post_init__(self): 
        nodes: list[Node] = []

        for element in self.elements: 
            for ElementNode in element.nodes: 
                if ElementNode in nodes: 
                    pass 
                else: 
                    nodes.append(ElementNode)
        
        self.nodes: list[Node] = nodes

    @property
    def global_stiffness_matrix(self) -> NDArray[np.float64]:
        #depreciated. No need to run this to solve the problem
        return self.elements[0].stiffness_matrix

    def sub_stiffness_matrix(self, force_dof: list[int], displacement_dof: list[int]) -> NDArray[np.float64]:
        #get stiffness matrix of specified dofs
        K: NDArray[np.float64] = np.zeros([len(force_dof), len(displacement_dof)], dtype=np.float64)
        K = self.elements[0].stiffness_matrix[np.ix_(force_dof, displacement_dof)]
        return K
    
    def alt_sub_stiffness_matrix(self, force_dof: list[int], displacement_dof: list[int]) -> NDArray[np.float64]:
        #get stiffness matrix of specified dofs
        K: NDArray[np.float64] = np.zeros([len(force_dof), len(displacement_dof)], dtype=np.float64)
        K = self.elements[0].alt_stiffness_matrix[np.ix_(list(force_dof), list(displacement_dof))]
        return K
    
    def assembly(self) -> NDArray[np.float64]: 
        pass 
        
    
    def solve(self) -> NDArray[np.float64]: 
        active_dof_indeces: set[int] = set()
        local_dof_index_counter = 0
        for condition in self.active_dofs * len(self.nodes): 
            if condition: 
                active_dof_indeces.add(local_dof_index_counter)
        
            local_dof_index_counter +=1 

        inactive_dof_indeces: set[int] = set(range(0, len(self.nodes)*6)) - active_dof_indeces

        print(active_dof_indeces)
        print(inactive_dof_indeces, " inact")

        known_displacement_indeces: set[int]= set()
        for support in self.restrains: 
            node_index = self.nodes.index(support.node)
            local_support_dof_index = 0
            for condition in support.restrained_dofs: 
                if condition: 
                    known_displacement_indeces.add(node_index*6 + local_support_dof_index)
                    local_support_dof_index += 1
        
        known_displacement_indeces = known_displacement_indeces - inactive_dof_indeces
        known_forces_indeces = (set(range(0, len(self.nodes)*6))
                                 - known_displacement_indeces 
                                 - inactive_dof_indeces)
        
        known_forces_indeces = list(known_forces_indeces)
        known_forces_indeces.sort()

        known_displacement_indeces = list(known_displacement_indeces)
        known_displacement_indeces.sort()

        unknown_displacement_indeces = known_forces_indeces 
        unknown_forces_indeces = known_displacement_indeces

        print(known_displacement_indeces, "known")
        print(known_forces_indeces, "yes")

        Kku = self.alt_sub_stiffness_matrix(known_forces_indeces,unknown_displacement_indeces)
        Kkk = self.alt_sub_stiffness_matrix(known_forces_indeces,known_displacement_indeces)

        Kuk = self.alt_sub_stiffness_matrix(unknown_forces_indeces,known_displacement_indeces)
        Kuu = self.alt_sub_stiffness_matrix(unknown_forces_indeces,unknown_displacement_indeces)

        print("Kku")
        print(pd.DataFrame(Kku))
        Kku = self.sub_stiffness_matrix([3,4,5],[3,4,5])
        print(pd.DataFrame(Kku))
        print("theother")
        # # Kkk = self.sub_stiffness_matrix([3,4,5],[0, 1, 2])

        # # Kuk = self.sub_stiffness_matrix([0,1,2],[0,1,2])
        # # Kuu = self.sub_stiffness_matrix([0,1,2],[3,4,5])
        Fk = self.loads[known_forces_indeces]
        # Fk = np.array([0, -2000, 0])
        Uk = np.array([0, 0, 0])

        Uu = scipy.linalg.solve(Kku,Fk - Kkk.dot(Uk))
        Fu = Kuk.dot(Uk) + Kuu.dot(Uu)
        print("solution")
        return Uu, Fu
        
    
    def reduce_stiffness_matrix_dimension(self): 
        pass 
    
    

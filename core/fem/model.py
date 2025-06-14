from dataclasses import dataclass

import scipy.linalg 
from core.fem.elements import FEMElement
from core.fem.restrains import Support
from core.fem.forces import Load
from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np
import scipy

@dataclass
class Model(ABC):
    active_axis: tuple[bool, bool, bool]
    elements: list[FEMElement]
    restrains: list[Support]
    loads: list[Load]

    @property
    @abstractmethod
    def global_stiffness_matrix(self) -> NDArray[np.float64]: 
        pass 


@dataclass
class LinearElastic(Model): 
    

    @property
    def global_stiffness_matrix(self) -> NDArray[np.float64]:
        #depreciated. No need to run this to solve the problem
        return self.elements[0].stiffness_matrix
    
    def sub_stiffness_matrix(self, force_dof: list[int], displacement_dof: list[int]) -> NDArray[np.float64]:
        #get stiffness matrix of specified dofs
        K: NDArray[np.float64] = np.zeros([len(force_dof), len(displacement_dof)], dtype=np.float64)
        K = self.elements[0].stiffness_matrix[np.ix_(force_dof, displacement_dof)]
        return K
        
    
    def solve(self) -> NDArray[np.float64]: 
        Kku = self.sub_stiffness_matrix([3,4,5],[3,4,5])
        Kkk = self.sub_stiffness_matrix([3,4,5],[0, 1, 2])

        Kuk = self.sub_stiffness_matrix([0,1,2],[0,1,2])
        Kuu = self.sub_stiffness_matrix([0,1,2],[3,4,5])

        Fk = np.array([0, -2000, 0])
        Uk = np.array([0, 0, 0])

        Uu = scipy.linalg.solve(Kku,Fk - Kkk.dot(Uk))
        Fu = Kuk.dot(Uk) + Kuu.dot(Uu)
        return Uu, Fu
        
    
    def reduce_stiffness_matrix_dimension(self): 
        pass 
    
    

from numpy.typing import NDArray 
import numpy as np 
from core.fem.truss_2D import get_truss_stiffness
import pandas as pd 

def truss_2D_model(connection: list[tuple[tuple[float,float], tuple[float,float]]]) -> None: 
    

if __name__ == "__main__": 

    nodes: list[tuple[float, float]] = [
        (0, 0), 
        (4000, 0), 
        (4000, 3000), 
        (8000, 3000)
    ]

    force_vector = np.array([0, 0, 0, 0, 0, -9000, 0, 0])
    restrains: list[bool] = [True, True, False, False, False, False, True, True]
    displacements: NDArray[np.float64] = np.array([-4, 0, 0, 0, 0, 0, 0, 0], dtype=np.float64)
    unknown_displacement_dofs: list[bool] = [not restrain for restrain in restrains]
    specified_displacement_dofs: list[bool] = restrains

    areas: list[float] = [100, 200, 100, 200, 100]


    connection = [
        (nodes[0], nodes[1]),
        (nodes[0], nodes[2]),
        (nodes[1], nodes[2]),
        (nodes[1], nodes[3]),
        (nodes[2], nodes[3]),
        ]

    K: NDArray[np.float64] = np.zeros([len(restrains), len(restrains)])
    for pair_nodes, area in zip(connection,areas):
        kl: NDArray[np.float64]
        te: NDArray[np.float64]
        kg: NDArray[np.float64]
        kl, te, kg = get_truss_stiffness(nodes=pair_nodes, area=area, young_modulus=200_000, poison_ratio=0.25)

        node_indeces: list[int] = [nodes.index(node) for node in pair_nodes]
    
        dof: list[int] = [2*nodes.index(node) + i for node in pair_nodes for i in range(2)]

        K[np.ix_(dof, dof)] += kg

    Kuu: NDArray[np.float64] = K[np.ix_(unknown_displacement_dofs, unknown_displacement_dofs)]
    Kus: NDArray[np.float64] = K[np.ix_(unknown_displacement_dofs, specified_displacement_dofs)]
    Ksu: NDArray[np.float64] = K[np.ix_(specified_displacement_dofs, unknown_displacement_dofs)]
    Kss: NDArray[np.float64] = K[np.ix_(specified_displacement_dofs, specified_displacement_dofs)]

    Pu: NDArray[np.float64] = force_vector[unknown_displacement_dofs]
    du: NDArray[np.float64] = displacements[unknown_displacement_dofs]
    ds: NDArray[np.float64] = displacements[specified_displacement_dofs]

    du = np.linalg.inv(Kuu).dot(Pu - Kus.dot(ds))

    displacements[unknown_displacement_dofs] += du 
    
    Rs: NDArray[np.float64] = Ksu.dot(du) + Kss.dot(ds)
    
    force_vector[specified_displacement_dofs] = Rs
    print(pd.DataFrame(force_vector))
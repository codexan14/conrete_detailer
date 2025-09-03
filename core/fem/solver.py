from numpy.typing import NDArray 
import numpy as np 
from core.fem.bar import get_2D_truss_global_stiffness, get_2D_truss_local_to_global_transformation_matrix, get_truss_local_stiffness, get_node_rotation_matrix
import pandas as pd 

def truss_2D_model(
        nodes: list[tuple[float,float]], 
        connection: list[tuple[tuple[float,float], tuple[float,float]]],
        areas: list[float], 
        young_moduli: list[float],
        global_force_matrix: list[tuple[float, float]],
        global_displacement_matrix: list[tuple[float, float]],
        restrained_dof: list[tuple[bool, bool]]
        ) -> tuple[NDArray[np.float64], NDArray[np.float64]]: 
    """Returns the vector of global forces and global displacements"""
    number_of_dof: int = 2 * len(nodes)
    
    specified_displacement_dofs: list[bool] = np.array(restrained_dof).ravel().tolist()
    unknown_displacement_dofs: list[bool] = [not restrain for restrain in specified_displacement_dofs]

    # Transforms the global displacement matrix into a row
    global_displacements: NDArray[np.float64] = np.array(global_displacement_matrix, dtype=np.float64).ravel()
    global_forces: NDArray[np.float64] = np.array(global_force_matrix, dtype=np.float64).ravel()
    
    K: NDArray[np.float64] = np.zeros([number_of_dof, number_of_dof])
    for pair_nodes, area, young_modulus in zip(connection,areas,young_moduli):
        direction_vector = np.array(pair_nodes[1]) - np.array(pair_nodes[0])
        length: float = float(np.linalg.norm(direction_vector))
        kl: NDArray[np.float64] = get_truss_local_stiffness(length=length, area=area, young_modulus=young_modulus)
        rotation_matrix: NDArray[np.float64] = get_node_rotation_matrix(direction_vector=direction_vector)
        te: NDArray[np.float64] = get_2D_truss_local_to_global_transformation_matrix(rotation_matrix=rotation_matrix)
        kg: NDArray[np.float64] = get_2D_truss_global_stiffness(local_stiffness_matrix=kl, transformation_matrix=te)
    
        dof: list[int] = [2*nodes.index(node) + i for node in pair_nodes for i in range(2)]

        K[np.ix_(dof, dof)] += kg
    
    Kuu: NDArray[np.float64] = K[np.ix_(unknown_displacement_dofs, unknown_displacement_dofs)]
    Kus: NDArray[np.float64] = K[np.ix_(unknown_displacement_dofs, specified_displacement_dofs)]
    Ksu: NDArray[np.float64] = K[np.ix_(specified_displacement_dofs, unknown_displacement_dofs)]
    Kss: NDArray[np.float64] = K[np.ix_(specified_displacement_dofs, specified_displacement_dofs)]

    Pu: NDArray[np.float64] = global_forces[unknown_displacement_dofs]
    du: NDArray[np.float64] = global_displacements[unknown_displacement_dofs]
    ds: NDArray[np.float64] = global_displacements[specified_displacement_dofs]

    du = np.linalg.inv(Kuu).dot(Pu - Kus.dot(ds))
    # print(du)
    global_displacements[unknown_displacement_dofs] = du 
    
    Rs: NDArray[np.float64] = Ksu.dot(du) + Kss.dot(ds)
    
    global_forces[specified_displacement_dofs] = Rs

    return global_forces, global_displacements

def beam_2D_model(connection: list[tuple[tuple[float, float], tuple[float,float]]]) -> None: 
    pass 
    
if __name__ == "__main__": 
    nodes: list[tuple[float, float]] = [
        (0, 0), 
        (4000, 0), 
        (4000, 3000), 
        (8000, 3000)
    ]

    force_vector = np.array([0, 0, 0, 0, 0, -9000, 0, 0])
    global_force_matrix: list[tuple[float,float]] = [
        (0,0), (0,0), (0,-9000), (0,0)
    ]

    global_displacement_matrix: list[tuple[float, float]] = [(-4,0), (0,0), (0,0), (0,0)]
    connection = [
        (nodes[0], nodes[1]),
        (nodes[0], nodes[2]),
        (nodes[1], nodes[2]),
        (nodes[1], nodes[3]),
        (nodes[2], nodes[3]),
        ]
    
    restrains: list[bool] = [True, True, False, False, False, False, True, True]
    restrained_dof: list[tuple[bool, bool]] = [(True, True), (False, False), (False, False), (True, True)]

    
    result = truss_2D_model(
        nodes=nodes, 
        connection=connection,
        areas=[100, 200, 100, 200, 100],
        young_moduli=[200_000, 200_000, 200_000, 200_000, 200_000],
        global_force_matrix=global_force_matrix,
        global_displacement_matrix=global_displacement_matrix,
        restrained_dof=restrained_dof
        )
    
    print(result)
    
    displacements: NDArray[np.float64] = np.array([-4, 0, 0, 0, 0, 0, 0, 0], dtype=np.float64)
    unknown_displacement_dofs: list[bool] = [not restrain for restrain in restrains]
    specified_displacement_dofs: list[bool] = restrains

    areas: list[float] = [100, 200, 100, 200, 100]

    

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
    print(pd.DataFrame(force_vector), "\n",pd.DataFrame(displacements))
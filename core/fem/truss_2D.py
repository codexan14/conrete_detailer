import numpy as np 
from numpy.typing import NDArray
from typing import Callable

def get_length(first_node: tuple[float, float], second_node: tuple[float, float]) -> float: 
    return float(np.linalg.norm(np.array(first_node) - np.array(second_node)))

def get_rotation_matrix(direction_vector: NDArray[np.float64]) -> NDArray[np.float64]: 
    return np.array(
        [
            [direction_vector[0],   direction_vector[1],    0,  0],
            [-direction_vector[1],  direction_vector[0],    0,  0],
            [0,                     0,                      direction_vector[0], direction_vector[1]],
            [0,                     0,                      direction_vector[1], direction_vector[0]]
        ], dtype=np.float64
    )

def get_truss_stiffness(
        nodes: tuple[tuple[float, float], tuple[float, float]],
        area: float,
        young_modulus: float,
        poison_ratio: float) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:

    length: float = get_length(first_node=nodes[0], second_node=nodes[1])

    direction_vector: NDArray[np.float64] = (np.array(nodes[1]) - np.array(nodes[0]))/length

    local_stiffness_matrix: NDArray[np.float64] = young_modulus * area / length * np.array([
        [1, -1],
        [-1, 1]
    ])

    rotation_matrix: NDArray[np.float64] = get_rotation_matrix(direction_vector=direction_vector)

    transformation_matrix: NDArray[np.float64] = rotation_matrix[[0,2],:]

    global_stiffness_matrix: NDArray[np.float64] = transformation_matrix.transpose().dot(local_stiffness_matrix).dot(transformation_matrix)

    return local_stiffness_matrix, transformation_matrix, global_stiffness_matrix

if __name__ == "__main__":
    # assert np.allclose(
    #     get_D_matrix(elastic_modulus=1, poison_ration=0.25),
    #     1.6 * np.array([
    #         [0.75,  0.25,   0.25,   0,      0,      0       ],
    #         [0.25,  0.75,   0.25,   0,      0,      0       ],
    #         [0.25,  0.25,   0.75,   0,      0,      0       ],
    #         [0,     0,      0,      0.25,   0,      0       ],
    #         [0,     0,      0,      0,      0.25,   0       ],
    #         [0,     0,      0,      0,      0,      0.25    ]], 
    #         dtype=np.float64
    #     )
    # )
    print(get_truss_stiffness(nodes=((0,3000), (4000,3000)), area=100, young_modulus=200_000, poison_ratio=0.25))
    print(get_truss_stiffness(nodes=((0,0), (4000,3000)), area=100, young_modulus=200_000, poison_ratio=0.25))
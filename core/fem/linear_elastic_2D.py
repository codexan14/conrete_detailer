import numpy as np 
from numpy.typing import NDArray
from typing import Callable

def get_D_matrix(elastic_modulus: float, poison_ration: float) -> NDArray[np.float64]: 
    D: NDArray[np.float64] = np.zeros([6,6], dtype=np.float64)
    D[range(3), range(3)] = 1 - poison_ration       # Just the (0,0), (1,1) and (2,2) entries
    D[range(3,6), range(3,6)] = 0.5 - poison_ration # Just the (3,3), (4,4) and (5,5) entries
    D[[1, 2, 2], [0, 0, 1]] = poison_ration
    D[[0, 0, 1], [1, 2, 2]] = poison_ration
    k: float = elastic_modulus / ((1 + poison_ration) * (1 - 2 * poison_ration))
    return k * D

def get_spatial_dimension_number(points: list[list[float]]) -> int: 
    return len(points[0])

def get_length(first_point: list[float], last_point: list[float]) -> float: 
    return float(np.linalg.norm(np.array(first_point) - np.array(last_point)))

def get_truss_stiffness_matrix(points: list[list[float]], area: float, young_modulus: float, poison_ratio: float) -> NDArray[np.float64]: 
    spatial_dimension: int = get_spatial_dimension_number(points=points)
    
    length: float = get_length(first_point=points[0], last_point=points[1])

    orientation_vector: NDArray[np.float64] = (np.array(points[1]) - np.array(points[0]))/length

    local_stiffness_matrix: NDArray[np.float64] = young_modulus * area / length * np.array([
        [1, -1],
        [-1, 1]
    ])

    rotation_matrix: NDArray[np.float64] = np.array([
        [orientation_vector[0], orientation_vector[1]],
        [-orientation_vector[1], orientation_vector[0]]
    ])

    rotation_matrix: NDArray[np.float64] = np.zeros([2*spatial_dimension, 2*spatial_dimension], dtype=np.float64)
    rotation_matrix[0][]
    return np.zeros(3, dtype=np.float64)

if __name__ == "__main__":
    assert np.allclose(
        get_D_matrix(elastic_modulus=1, poison_ration=0.25),
        1.6 * np.array([
            [0.75,  0.25,   0.25,   0,      0,      0       ],
            [0.25,  0.75,   0.25,   0,      0,      0       ],
            [0.25,  0.25,   0.75,   0,      0,      0       ],
            [0,     0,      0,      0.25,   0,      0       ],
            [0,     0,      0,      0,      0.25,   0       ],
            [0,     0,      0,      0,      0,      0.25    ]], 
            dtype=np.float64
        )
    )
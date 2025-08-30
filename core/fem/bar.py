import numpy as np 
from numpy.typing import NDArray

def get_node_rotation_matrix(direction_vector: NDArray[np.float64]) -> NDArray[np.float64]: 
    if direction_vector.shape == (2,): #2D Problem
        nx: NDArray[np.float64] = np.array([direction_vector[0], direction_vector[1], 0], dtype=np.float64) / np.linalg.norm(direction_vector)
    elif direction_vector.shape == (3,): #3D Problem
        nx: NDArray[np.float64] = direction_vector / np.linalg.norm(direction_vector)
    else:
        raise Exception("Direction vector must be 2D (shape (2,)) or 3D (shape (3,))") 

    if nx[0] == 0 and nx[1] == 0: 
        ny: NDArray[np.float64] = np.array([0, 1, 0], dtype=np.float64)
    else: 
        ny: NDArray[np.float64] = np.array([-nx[1], nx[0], 0], dtype=np.float64) / np.sqrt(nx[1]**2 + nx[0]**2)

    nz: NDArray[np.float64] = np.linalg.cross(nx, ny)
    rotation_matrix: NDArray[np.float64] = np.array([nx, ny, nz], dtype=np.float64)
    
    return rotation_matrix

def get_truss_local_to_global_rotation_matrix(node_rotation_matrix: NDArray[np.float64]) -> NDArray[np.float64]: 
    local_to_global_rotation_matrix: NDArray[np.float64] = np.zeros([6,6])
    local_to_global_rotation_matrix[np.ix_(range(3), range(3))] = node_rotation_matrix
    local_to_global_rotation_matrix[np.ix_(range(3,6), range(3,6))] = node_rotation_matrix
    return local_to_global_rotation_matrix

def get_2D_truss_local_to_global_transformation_matrix(rotation_matrix:NDArray[np.float64]) -> NDArray[np.float64]:
    transformation_matrix: NDArray[np.float64] = rotation_matrix[[0,2],:]
    return transformation_matrix

def _get_truss_unit_stiffness() -> NDArray[np.float64]:
    return np.array([[1, -1], [-1, 1]], dtype = np.float64)

def get_beam_torsion_stiffness(length: float, polar_inertia: float, shear_modulus: float) -> NDArray[np.float64]:
    return shear_modulus * polar_inertia / length * np.array([[1, -1], [-1, 1]], dtype = np.float64)

def get_truss_local_stiffness(
        length: float,
        area: float,
        young_modulus: float) -> NDArray[np.float64]:

    local_stiffness_matrix: NDArray[np.float64] = young_modulus * area / length * _get_truss_unit_stiffness()

    return local_stiffness_matrix

def get_2D_truss_global_stiffness(
        local_stiffness_matrix: NDArray[np.float64],
        transformation_matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    return transformation_matrix.transpose().dot(local_stiffness_matrix).dot(transformation_matrix)

def get_beam_local_stiffness(length: float, inertia: float, young_modulus: float) -> NDArray[np.float64]:
    return young_modulus * inertia / length**3 * np.array([
        [   +12,           +6 *length,     -12,            +6**length      ],
        [   +6**length,    +4**length**2,  -6**length,     +2**length**2   ],
        [   -12,           -6 *length,     +12,            -6**length      ],
        [   +6**length,    +2**length**2,  -6**length,     +4**length**2   ]
    ], dtype=np.float64)

def get_2D_frame_local_stiffness(length: float, area: float, inertia: float, young_modulus: float) -> NDArray[np.float64]: 
    stiffness: NDArray[np.float64] = np.zeros([6, 6])
    stiffness[np.ix_([0, 3], [0, 3])] = get_truss_local_stiffness(length=length, area=area, young_modulus=young_modulus)
    stiffness[np.ix_([1, 2, 4, 5], [1, 2, 4, 5])] = get_beam_local_stiffness(length=length, inertia=inertia, young_modulus=young_modulus)
    return stiffness

def get_3D_frame_local_stiffness(
        length: float, 
        area: float, 
        inertia_z: float,
        inertia_y: float,
        young_modulus: float,
        shear_modulus: float) -> NDArray[np.float64]: 
    stiffness: NDArray[np.float64] = np.zeros([12, 12])
    stiffness[np.ix_([0, 6], [0, 6])] = get_truss_local_stiffness(length=length, area=area, young_modulus=young_modulus)
    stiffness[np.ix_([1, 5, 7, 11], [1, 5, 7, 11])] = get_beam_local_stiffness(length=length, inertia=inertia_z, young_modulus=young_modulus)

    rotation_matrix: NDArray[np.float64] = np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
    stiffness[np.ix_([2, 4, 8, 10], [2, 4, 8, 10])] = ((rotation_matrix.transpose()).dot(get_beam_local_stiffness(length=length, inertia=inertia_y, young_modulus=young_modulus))).dot(rotation_matrix)
    stiffness[np.ix_([3, 9], [3, 9])] = get_beam_torsion_stiffness(length=length, polar_inertia=inertia_z + inertia_y, shear_modulus=shear_modulus)
    return stiffness
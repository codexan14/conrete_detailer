import numpy as np 
import pandas as pd 
from core.fem.bar import get_node_rotation_matrix
from core.fem.bar import get_truss_local_to_global_rotation_matrix
from core.fem.bar import get_2D_frame_local_stiffness
from core.fem.bar import get_3D_frame_local_stiffness

from numpy.typing import NDArray

def test_get_node_rotation_matrix () -> bool: 
    value: NDArray[np.float64] = get_node_rotation_matrix(np.array([1, 2, 0], dtype=np.float64))
    goal: NDArray[np.float64] = np.array([[1/np.sqrt(5), 2/np.sqrt(5), 0], [-2/np.sqrt(5), 1/np.sqrt(5), 0], [0, 0, 1]], dtype=np.float64)

    # To test a matrix, value == test
    # But since it is a rotation, we will do: 
    # value.dot(test.transpose()) and compare the trace to 3
    test = (value.dot(goal.transpose())).trace()

    return abs((test-3)/3) < 1e-10

def test_get_rotation_matrix() -> bool: 
    node_rotation_matrix: NDArray[np.float64] = get_node_rotation_matrix(np.array([1, 2, 0], dtype=np.float64))
    value: NDArray[np.float64] = get_truss_local_to_global_rotation_matrix(node_rotation_matrix=node_rotation_matrix)
    goal: NDArray[np.float64] = np.zeros([6,6])
    goal[np.ix_(range(0,3), range(0,3))] = node_rotation_matrix
    goal[np.ix_(range(3,6), range(3,6))] = node_rotation_matrix
    
    test = (value.dot(goal.transpose())).trace()
    # To test a matrix, value == test
    # But since it is a rotation, we will do: 
    # value.dot(test.transpose()) and compare the trace to 6
    return (test - 6)/6 < 1e-10

if __name__ == "__main__":
    assert test_get_node_rotation_matrix()
    assert test_get_rotation_matrix()
    print(get_2D_frame_local_stiffness(1, 1, 1, 200_000))
    print(pd.DataFrame(get_3D_frame_local_stiffness(length=1, area=2, inertia_z=3, inertia_y=4, young_modulus=10, shear_modulus=20)))
    
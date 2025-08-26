from numpy.typing import NDArray 
import numpy as np 
from core.fem.truss_2D import get_truss_stiffness

if __name__ == "__main__": 
    nodes: list[tuple[float, float]] = [
        (0, 0), 
        (4000, 0), 
        (4000, 3000), 
        (8000, 3000)
    ]

    connection = [nodes[0], nodes[1]]
    get_truss_stiffness(
        nodes=()
    )
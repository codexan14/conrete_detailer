from core.fem.solver import truss_2D_model

def test_truss_2D_model() -> bool: 
    """A structure is composed by 4 frame elements and 4 nodes: """
    nodes: list[tuple[int, int]] = [(0, 0), (4000, 0), (4000, 3000), (8000, 3000)]
    connection: list[tuple[tuple[int, int], tuple[int, int]]] = [
        (nodes[0], nodes[1]), 
        (nodes[1], nodes[2])
    ]
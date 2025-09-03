from core.fem.solver import truss_2D_model

def test_truss_2D_model() -> bool: 
    """A structure is composed by 4 frame elements and 4 nodes: """
    nodes: list[tuple[float, float]] = [(0, 0), (4000, 0), (4000, 3000), (8000, 3000)]
    connection: list[tuple[tuple[float, float], tuple[float, float]]] = [
        (nodes[0], nodes[1]), 
        (nodes[1], nodes[2])
    ]

    truss_2D_model(
        nodes=nodes,
        connection=connection, 
        areas=[10, 10], 
        young_moduli=[200_000, 200_000], 
        global_force_matrix=[(0, 0), (0,2)],
        global_displacement_matrix=[(-4, 0), (0, 0)], 
        restrained_dof=[(True, True), (False, False)])
from core.fem.solver import truss_2D_model

def test_truss_2D_model() -> bool: 
    """A structure is composed by 4 frame elements and 4 nodes: """
    nodes: list[tuple[float, float]] = [(0, 0), (4000, 0), (4000, 3000), (8000, 3000)]
    connection: list[tuple[tuple[float, float], tuple[float, float]]] = [
        (nodes[0], nodes[1]), 
        (nodes[0], nodes[2]),
        (nodes[1], nodes[2]),
        (nodes[1], nodes[3]),
        (nodes[2], nodes[3])
    ]

    areas: list[float] = [100, 100, 100, 100, 100]
    young_moduli: list[float] = [200_000, 200_000, 200_000, 200_000, 200_000]

    global_force_matrix: list[tuple[float, float]] = [
        (0, 0), 
        (0, 0), 
        (0, -9000), 
        (0, 0),
        (0, 0)
    ]

    global_displacement_matrix: list[tuple[float, float]] = [
        (-4, 0), 
        (0, 0), 
        (0, 0), 
        (0, 0),
        (0, 0)
    ]

    restrained_dof: list[tuple[bool, bool]] = [
        (True, True), 
        (False, False),
        (False, False),
        (False, False),
        (True, True), 

    ]

    global_forces, global_displacements = truss_2D_model(
        nodes=nodes, 
        connection=connection, 
        areas=areas, 
        young_moduli=young_moduli, 
        global_force_matrix=global_force_matrix,
        global_displacement_matrix=global_displacement_matrix, 
        restrained_dof=restrained_dof)


if __name__ == "__main__": 
    test_truss_2D_model()
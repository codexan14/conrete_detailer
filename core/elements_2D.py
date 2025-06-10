from dataclasses import dataclass

@dataclass
class Beam: 
     joints: tuple[tuple[float,float], tuple[float, float]]


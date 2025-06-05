# Factors to convert input units to SI (N, kg, mm, density: kg/m3)

INPUT_LENGTH_FACTOR: dict[str, float] = {
     "m": 1000, 
     "in": 2.54*10,
     "ft": 12*2.54*10, 
     "cm": 10, 
     "mm": 1
}

INPUT_MASS_FACTOR: dict[str, float] = {
     "kg": 1.00000, 
     "lb": 0.453592,
}

INPUT_WEIGHT_FACTOR: dict[str, float] = {
     "N": 1.00000, 
     "kN": 0.001,
     "kgf": 9.80,
     "lbf":  INPUT_MASS_FACTOR["lb"]*9.80
}
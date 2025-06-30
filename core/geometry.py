import math 

def bar_area(diameter: float) -> float: 
    return 1/4 * math.pi * diameter**2

def circle_perimeter(center, radius, n=10) -> list[float]: 
    x = [center + radius*math.cos(2*math.pi*(i)/(n-1) for i in range(n))]
    y = [center + radius*math.sin(2*math.pi*(i)/(n-1) for i in range(n))]

    return x, y

import numpy as np 
from typing import Callable, Literal

def numeric_integration(function: Callable[[float],float], x0: float, xf: float, n: int = 10) -> float | Literal[0]: 
    integral = 0 
    for x in np.linspace(start=x0, stop=xf, num = n, endpoint=True): 
        integral += function(x) * (xf-x0)/n

    return integral


def numeric_solver(function: Callable[[float], float], goal: float, x1: float, x2: float, error: float) -> float: 
    y1: float = function(x1) - goal
    y2: float = function(x2) - goal

    # x3 = (x1 + x2)/2  
    x3: float = x1 - y1 * (x2-x1) / (y2-y1)
    y3: float = function(x3) - goal

    iter = 0

    while ((abs(function(x3) - goal) >= error) and (iter < 100)):

        if np.sign(y3) == np.sign(y2): 
            x1, x2, y1, y2 = x1, x3, y1, y3 

        else: 
            x1, x2, y1, y2 = x3, x2, y3, y2 

        # x3 = (x1 + x2)/2 
        x3 = x1 - y1 * (x2-x1) / (y2-y1)
        y3 = function(x3) - goal 

        iter += 1

    return x3
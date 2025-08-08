import csv 
from typing import cast, Iterator, Callable
import numpy as np 

def extract_headers_from_csv(path: str) -> list[str]: 
    with open(file=path, mode='r') as file: 
        data_iterator: Iterator[list[str]] = cast(Iterator[list[str]], csv.reader(file, delimiter=','))
        header: list[str] = [text for text in next(data_iterator)]

    return header 

def extract_column_from_csv(path: str, column_name: str) -> list[str]: 
    with open(file=path, mode='r') as file: 
        data_iterator: Iterator[list[str]] = cast(Iterator[list[str]], csv.reader(file, delimiter=','))
        header: list[str] = [text for text in next(data_iterator)]
        column_index: int = header.index(column_name)
        desired_column: list[str] = [row[column_index].replace(" ","") for row in data_iterator]
    
    return desired_column

def solve(function: Callable[[float], float], target: float, initial_value_1: float, initial_value_2: float, error: float = 0.10) -> float:
    """
    Uses the numerical method called bisection method. Where two initial values x1 and x2 are given
    and the function should return values y1 and y2 with different signs
    """
    x1: float = initial_value_1
    x2: float = initial_value_2

    y1: float = function(x1)
    y2: float = function(x2)

    # Asserts that the two initial values give two outputs with different signs.
    assert int(y2/abs(y2)) != int(y1/abs(y1))

    # First approximation of the solution
    x: float = x1 + (target - y1)*(x2-x1)/(y2-y1)
    

    while abs(function(x) - target) > error: # Iterates until the function is near the target within an error. 
        y: float = function(x)
        if int(y1/abs(y1)) == int(y/abs(y)): # signs are equal
            x1 = x
            y1 = y
        else: 
            x2 = x
            y2 = y

        x: float = x1 + (target - y1)*(x2-x1)/(y2-y1)

    return x

def evaluate(function: Callable[[float], float], eval_value: float, expected_return_value: float, name: str = '', error: float = 0.01) -> None: 
        if name != '': 
            function.__name__ = name
        try: 
            assert abs(function(eval_value) - expected_return_value)/function(eval_value) < error 
            print(f"{function.__name__}: \033[1;32mCORRECT\033[0m, error: {(abs(function(eval_value) - expected_return_value))/function(eval_value)}")
        except AssertionError: 
            print(f"{function.__name__}: \033[1;31mERROR\033[0m, error: {(abs(function(eval_value) - expected_return_value))/function(eval_value)}")


if __name__ == '__main__':
    print(extract_column_from_csv(path = "core/examples/01/beam_sections.csv", column_name="height"))

    a: list[str] = extract_column_from_csv(path = "core/examples/01/beam_sections.csv", column_name="base")
    b = np.array(a, dtype=np.float64) *2 
    print(b)

    evaluate(
        lambda c: solve(lambda x: 0.20*x**3 - x, target=c, initial_value_1=1, initial_value_2=3, error=10e-10), 
        eval_value=0, 
        expected_return_value=2.236068, 
        name="solve",
        error=0.1)
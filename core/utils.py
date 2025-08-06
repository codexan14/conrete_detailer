import csv 
from typing import cast, Iterator
import numpy as np 

def extract_column_from_csv(path: str, column_name: str) -> list[str]: 
    with open(file=path, mode='r') as file: 
        data_iterator: Iterator[list[str]] = cast(Iterator[list[str]], csv.reader(file, delimiter=','))
        header: list[str] = [text.replace(" ","") for text in next(data_iterator)]
        column_index: int = header.index(column_name)
        desired_column: list[str] = [row[column_index].replace(" ","") for row in data_iterator]
    
    return desired_column


if __name__ == '__main__':
    print(extract_column_from_csv(path = "core/examples/01/beam_sections.csv", column_name="height"))

    a = extract_column_from_csv(path = "core/examples/01/beam_sections.csv", column_name="base")
    b = np.array(a, dtype=np.float64) *2 
    print(b)
def write(variable_name: str, variable_value: float, unit: str) -> str: 
    text: str = f"{variable_name} = {variable_value} {unit}"
    return text


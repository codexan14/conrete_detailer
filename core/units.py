FACTORS = {
    "preassure": 1, 
    "force": 1, 
    "mass": 1, 
    "time": 1, 
    "length": 1, 
}

## HAER QUE EL FRONT END CAMBIEN LAS UNIDADES< NO EL BACKEND .


def outter(a = 2):
    def decorator(func): 
        def wrapper(c): 
            print("1") 
            func(c*a)
            print("2")
        
        return wrapper
    return decorator


@outter(a = 2)
def a(c): 
    print(c)


if __name__ == "__main__": 

    a(2)